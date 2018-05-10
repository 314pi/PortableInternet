#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import pickle
import bsddb
from bsddb import db, dbshelve
import logging
import shutil
import os, os.path
import threading
import time

log = logging.getLogger('Juice')

class State(object): 
    def __init__(self, config, checkfirst=True): 
        """Open ourself using config.appdata_dir as the 
        Berkeley DB private environment that'll enable us to 
        be thread-safe."""
        self.__config = config
        self.__shelf = None
        self.__lock = threading.RLock(verbose=None)
        if checkfirst: 
            self.check()
        self.open()

    def _acquire(self): 
        if self.__lock is not None:
            self.__lock.acquire()

    def _release(self): 
        if self.__lock is not None: 
            self.__lock.release()

    def open(self): 
        if self.__shelf is not None:
            return
        log.debug("Opening state database...")
        self.__flags = db.DB_PRIVATE | db.DB_CREATE | db.DB_THREAD \
                  | db.DB_INIT_LOCK | db.DB_INIT_MPOOL
        self.__env = env = db.DBEnv()
        env.open(self.__config.appdata_dir, self.__flags)
        self.__shelf = dbshelve.open(self.__config.state_db_file, 
                                     'c', dbenv=env)
        log.debug("State database opened with %d entries.", 
                  len(self.keys()))

    def call_and_close(self, callable, *a, **kw): 
        """Wrap a call in a try: finally: that'll force state closed."""
        try: 
            callable(*a, **kw)
        finally: 
            self.close()

    def close(self): 
        """Close our shelf carefully."""
        if self.__shelf is not None: 
            log.debug("Closing state database...")
            try: 
                self.__shelf.close()
            finally: 
                self.__shelf = None
                self.__env.close()

    def sync(self): 
        """Synchronise changes to disk."""
        try: 
            self._acquire()
            self.__shelf.sync()
        finally: 
            self._release()

    def check(self): 
        """Perform a self-check."""
        try: 
            self._acquire()
            filename = self.__config.state_db_file
            if not os.path.exists(filename): 
                return
            wasopen = self.__shelf is not None
            should_salvage = False
            if wasopen: 
                self.close()
            log.info("Performing a self-check of the state database...")
            try: 
                corrupt = '%s.corrupt' % filename
                idb = db.DB()
                try: 
                    idb.verify(filename)
                    idb.close()
                except bsddb._db.DBVerifyBadError, ex: 
                    log.exception("Database verification failed.")
                    should_salvage = True
            except: 
                log.exception("That didn't work.")
                try: 
                    idb.close()
                except:
                    pass
            log.info("Self-check complete.")
            if should_salvage:
                self.salvage()
            if wasopen:
                self.open()
        finally:
            self._release()

    def salvage(self): 
        """Salvage what we can recover."""
        try: 
            self._acquire()
            self.close()
            filename = self.__config.state_db_file
            corrupt = '%s.corrupt' % filename
            recovery = '%s.recovery' % filename
            shutil.copyfile(filename, corrupt)
            idb = db.DB()
            try: 
                idb.verify(filename, outfile=recovery, flags=db.DB_SALVAGE)
            except bsddb._db.DBVerifyBadError, ex: 
                pass
            idb.close()
            os.unlink(filename)
            cdb = db.DB()
            cdb.open(corrupt)
            rdb = db.DB()
            rdb.open(filename, dbtype=db.DB_HASH, flags=db.DB_CREATE)
            keys = cdb.keys()
            goodkeys = []
            for key in keys:
                for good in ('cache\0', 'lastfeedid', 'feed#'): 
                    if key[:len(good)] == good:
                        if good == 'cache\0': 
                            break # silently ditch
                        try: 
                            value = cdb.get(key)
                            if key == 'lastfeedid' \
                            and not isinstance(value, int):                             
                                log.warn("Discarding dodgy lastfeedid",
                                         repr(value))
                                continue
                            goodkeys.append(key)
                        except: 
                            log.exception("Can't recover key %s", repr(key))
                        break
                else: 
                    log.error("Discarding dodgy key %s", repr(key))

            for key in goodkeys:
                rdb.put(key, cdb.get(key))

            log.info("Recovered %d of %d keys.", len(goodkeys), len(keys))
            cdb.close()
            rdb.close()
        finally:
            self._release()

    def flush_cache(self, days=30): 
        """Flush all cache entries older than `days`."""
        try: 
            self._acquire()
            shelf = self.__shelf
            threshold = time.time() - 3600*24*days
            bodycount = 0
            try: 
                for victim in [k for k in shelf.keys() if k.startswith('cache\0')]: 
                   try: 
                       lastchecked = state[k]['checked']
                       if time.mktime(lastchecked) >= threshold: 
                           continue
                   except KeyError: 
                       pass # Don't know when we last checked it? Kill it with glee.
                   del shelf[victim]
                   bodycount += 1
            except: 
                log.exception("Couldn't flush all cache entries.")
        finally: 
            self._release()
        log.info("Flushed %d cache entries older than %d days.", bodycount, days)
        return bodycount
        
    # Dictionary magic methods.
            
    def __getitem__(self, key): 
        try:
            self._acquire()
            return self.__shelf[key]
        finally:
            self._release()

    def __delitem__(self, key): 
        try: 
            self._acquire()
            del self.__shelf[key]
        finally:
            self._release()

    def __setitem__(self, key, value): 
        try: 
            self._acquire()
            self.__shelf[key] = value
        finally:
            self._release()

    def keys(self): 
        try: 
            self._acquire()
            return self.__shelf.keys()
        finally:
            self._release()

    def __len__(self): 
        try: 
            self._acquire()
            return len(self.__shelf.keys())
        finally:
            self._release()

    def get(self, key, default): 
        try: 
            self._acquire()
            return self.__shelf.get(key, default)
        finally:
            self._release()

    def has_key(self, key):
        try: 
            self._acquire()
            return self.__shelf.has_key(key)
        finally:
            self._release()

    def iterkeys(self): 
        try: 
            self._acquire()
            return self.__shelf.iterkeys()
        finally:
            self._release()

open = State

def main():
    from ipodder import conlogging, configuration
    SPAM = logging.DEBUG / 2
    
    # Initialise the logging module and configure it for our console logging.
    # I'll factor this out soon so it's less convoluted.
    logging.basicConfig()
    handler = logging.StreamHandler()
    handler.formatter = conlogging.ConsoleFormatter("%(message)s", wrap=False)
    log.addHandler(handler)
    log.propagate = 0
    logging.addLevelName(SPAM, "SPAM")
    
    # Parse our configuration files.
    # I'll factor this out soon so it's less convoluted.
    parser = configuration.makeCommandLineParser()
    options, args = parser.parse_args()
    if args:
        parser.error("only need options; no arguments.")
    if options.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    config = configuration.Configuration(options)
    if options.debug: # just in case config file over-rode it
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # Open our state database.
    return State(config)

if __name__ == '__main__': 
    state = main()
