from bsddb import db, dbshelve
import bsddb
import logging,md5,time,os,threading,time
import shelve
import shutil
import ipodder.core
from ipodder import threads
from ipodder import misc

log = logging.getLogger('Juice')

def mkurlkey(url):
    urlhash = md5.md5(url).hexdigest()
    return "url:%s" % urlhash

def mkguidkey(guid, index):
    guidhash = md5.md5(guid).hexdigest()
    return "guid:%d:%s" % (index,guidhash)

def mkenclosurekey(enclosure_id):
    return 'enclosure:%d' % enclosure_id

def mkfilenamekey(filename):
    filenamehash = md5.md5(misc.encode(filename, encoding='ascii', replace='xmlcharrefreplace')).hexdigest()
    return 'filename:%s' % filenamehash    

def mkfeedkey(feed_id):
    return 'feed:%d' % feed_id

class HistoryDb(threads.SelfLogger): 
    def __init__(self, config, checkfirst=True): 
        """Open ourself using config.appdata_dir as the 
        Berkeley DB private environment that'll enable us to 
        be thread-safe."""
        threads.SelfLogger.__init__(self, tag='History')
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
        history_dir = os.path.join(self.__config.appdata_dir,"history")
        if not os.path.exists(history_dir):
            self.info("Creating history dir %s", history_dir)
            os.mkdir(history_dir)
        self.debug("Opening history database...")
        self.__flags = db.DB_PRIVATE | db.DB_CREATE | db.DB_THREAD \
                  | db.DB_INIT_LOCK | db.DB_INIT_MPOOL
        self.__env = env = db.DBEnv()
        env.open(history_dir, self.__flags)
        self.__shelf = dbshelve.open("history.db", 
                                     'c', dbenv=env)
        self.debug("History database opened with %d entries.", 
                  len(self.keys()))

    def close(self): 
        """Close our shelf carefully."""
        if self.__shelf is not None: 
            self.debug("Closing state database...")
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
            filename = os.path.join(self.__config.appdata_dir,"history","history.db")
            if not os.path.exists(filename): 
                return
            wasopen = self.__shelf is not None
            should_salvage = False
            if wasopen: 
                self.close()
            log.info("Performing a self-check of the history database...")
            try: 
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
            filename = os.path.join(self.__config.appdata_dir,"history","history.db")
            corrupt = '%s.corrupt' % filename
            recovery = '%s.recovery' % filename
            shutil.copyfile(filename, corrupt)
            idb = db.DB()
            try:
                #AG: Saves recoverable data in the file pointed to by 'recovery'.
                #We don't actually do anything with that data yet but
                #it's nice to have a backup.
                idb.verify(filename, outfile=recovery, flags=db.DB_SALVAGE)
            except bsddb._db.DBVerifyBadError, ex: 
                pass
            idb.close()
            os.unlink(filename) #worst case, we lose history and start fresh.
            cdb = db.DB()
            cdb.open(corrupt) #but we'll try to open the old, corrupt db and copy its keys.
            rdb = db.DB()
            rdb.open(filename, dbtype=db.DB_HASH, flags=db.DB_CREATE)
            keys = cdb.keys()
            goodkeys = []
            for key in keys:
                try: 
                    value = cdb.get(key)
                    goodkeys.append(key)
                except: 
                    log.exception("Can't recover key %s", repr(key))

            for key in goodkeys:
                rdb.put(key, cdb.get(key))

            log.info("Recovered %d of %d keys.", len(goodkeys), len(keys))
            cdb.close()
            rdb.close()
        finally:
            self._release()
    
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

    def next_enclosure_id(self):
        try: 
            self._acquire()
            if self.__shelf.has_key('last_enclosure_id'):
                last_enclosure_id = self.__shelf['last_enclosure_id']
            else:
                last_enclosure_id = 0
            enclosure_id = last_enclosure_id + 1
            self.__shelf['last_enclosure_id'] = enclosure_id
            if enclosure_id % 50 == 0:
                # is this the right way to do it?
                tskey = "timestamp:%d" % enclosure_id
                tsval = time.time()
                self.__shelf[tskey] = tsval
            return enclosure_id
        finally:
            self._release()
        
    def new_enclosure(self,urlkey,urlval,guidkey,guidval,enclosurekey,enclosureval):
        """Atomic write of the enclosure record and two indices."""
        try: 
            self._acquire()

            if self.__shelf.has_key(urlkey):
                dict = self.__shelf[urlkey]
                dict[urlval[0]] = urlval[1]
                self.__shelf[urlkey] = dict
            else:
                self.__shelf[urlkey] = { urlval[0] : urlval[1] }

            if guidkey:
                self.__shelf[guidkey] = guidval

            self.__shelf[enclosurekey] = enclosureval
            
        finally:
            self._release()

    def save_encinfo(self,enclosurekey,local,filenamekey):
        try: 
            self._acquire()

            if not self.__shelf.has_key(enclosurekey):
                self.error("Enclosure not found for key: %s", enclosurekey)
                return
            
            enclosureval = self.__shelf[enclosurekey]
            enclosureval['local'] = local
            self.__shelf[enclosurekey] = enclosureval

            if filenamekey is not None:
                self.__shelf[filenamekey] = enclosurekey
                
        finally:
            self._release()

    def update_enclosure_status(self, enclosurekey, status, marked):
        try: 
            self._acquire()
            if self.__shelf.has_key(enclosurekey):
                enclosureval = self.__shelf[enclosurekey]
                local = enclosureval['local']
                local['status'] = status
                local['marked'] = marked
                self.__shelf[enclosurekey] = enclosureval
        finally:
            self._release()

    def log_feedscan(self, feedkey, tsval, live_enc_ids):
        try: 
            self._acquire()

            if not self.__shelf.has_key(feedkey):
                self.__shelf[feedkey] = (tsval,live_enc_ids,live_enc_ids)
            else:
                (old_tsval,old_live_enc_ids,all_enc_ids) = self.__shelf[feedkey]
                for id in live_enc_ids:
                    if all_enc_ids.count(id) == 0:
                        all_enc_ids.append(id)
                self.__shelf[feedkey] = (tsval,live_enc_ids,all_enc_ids)
                self.debug("All enclosures for feedkey %s: %s", feedkey, all_enc_ids)

            if not self.__shelf.has_key('feeds_index'):
                self.__shelf['feeds_index'] = [feedkey]
            else:
                feeds_index = self.__shelf['feeds_index']
                if feeds_index.count(feedkey) == 0:
                    feeds_index.append(feedkey)
                self.__shelf['feeds_index'] = feeds_index
                #self.debug("Feeds index: %s", str(feeds_index))
        finally:
            self._release()
                     
    def clean_history(self,max_age):
        """Clean history items older than max_age days if not still present
        in the feed."""

        def clean_enclosure_history(enc_id):
            """Remove history records for enclosure and associated indexes.
            This procedure MUST be run inside an _acquire()/_release() block."""
            
            self.debug("clean_enclosure_history: id = %d", enc_id)
            enclosurekey = mkenclosurekey(enc_id)
            if not self.__shelf.has_key(enclosurekey):
                return
            
            enclosureval = self.__shelf[enclosurekey]
            entrytitle = enclosureval['entry'].get('title', '(no title)')
            self.debug("clean_enclosure_history: name = %s", entrytitle)
            local = enclosureval['local']
            entry = enclosureval['entry']
            enclosure = enclosureval['enclosure']
            
            filename = local['filename']
            if filename:
                self.debug("clean_enclosure_history: attempting to remove history key for filename = %s", filename)
                filenamekey = mkfilenamekey(filename)
                try:
                    del self.__shelf[filenamekey]
                except KeyError:
                    pass

            url = enclosure['url']
            urlkey = mkurlkey(url)
            urldict = None
            if self.__shelf.has_key(urlkey):
                urldict = self.__shelf[urlkey]

            guid = entry.get('id')
            if guid:
                self.debug("clean_enclosure_history: attempting to remove history key for guid = %s", guid)
                index = local.get('index',0)
                guidkey = mkguidkey(guid,index)
                try:
                    del self.__shelf[guidkey]
                except KeyError:
                    pass
                
                if urldict != None and urldict.has_key(guid):
                    self.debug("clean_enclosure_history: attempting to remove urldict history key for guid = %s", guid)
                    del urldict[guid]
                        
            if urldict != None:
                if len(urldict) == 0:
                    self.debug("clean_enclosure_history: urldict is empty, deleting.")
                    del self.__shelf[urlkey]
                else:
                    self.debug("clean_enclosure_history: saving urldict with %d keys.", len(urldict))
                    self.__shelf[urlkey] = urldict

            self.debug("clean_enclosure_history: attempting to remove history key for enclosure %d.", enc_id)            
            del self.__shelf[enclosurekey]

            self.debug("clean_enclosure_history: finished removing history for enclosure %d.", enc_id)
            
        try: 
            self._acquire()

            #Determine threshold enclosure id from timestamps.
            if not self.__shelf.has_key('last_enclosure_id'):
                #We have no history!
                return

            last_enclosure_id = self.__shelf['last_enclosure_id']
            threshold_id = (last_enclosure_id/50)*50
            while threshold_id > 0:
                tskey = "timestamp:%d" % threshold_id
                if self.__shelf.has_key(tskey):
                    tsval = self.__shelf[tskey]
                    if isinstance(tsval,time.struct_time):
                        tsval = time.mktime(tsval) #support initial tstruct impl
                    if time.time() - tsval > max_age*86400:
                        break
                threshold_id = threshold_id - 50

            self.debug("clean_history: threshold id for %d days = %d", max_age, threshold_id)
        
            #Troll for old enclosures.
            if self.__shelf.has_key('feeds_index'):
                feeds_index = self.__shelf['feeds_index']
                for feedkey in feeds_index:
                    if self.__shelf.has_key(feedkey):
                        (tsval,live_enc_ids,all_enc_ids) = self.__shelf[feedkey]
                        removed_enc_ids = []
                        for enc_id in all_enc_ids:
                            if live_enc_ids.count(enc_id) == 0:
                                self.debug("clean_history: enclosure %d is no longer live.", enc_id)
                                #Not in most recent scan.  Check age.
                                if enc_id < threshold_id:
                                    try:
                                        clean_enclosure_history(enc_id)
                                        removed_enc_ids.append(enc_id)
                                    except:
                                        self.exception("clean_history: there was an error cleaning history for enclosure %d.", enc_id)
                                else:
                                    self.debug("clean_history: enclosure %d is less than %d days old so we'll keep it around.", enc_id, max_age)
                        #Prune the removed ids from all_enc_ids and save.
                        for enc_id in removed_enc_ids:
                            all_enc_ids.remove(enc_id)
                        self.__shelf[feedkey] = (tsval,live_enc_ids,all_enc_ids)

        finally:
            self._release()
        
class History(object):
    def __init__(self,config,feeds):
        self.db = HistoryDb(config)
        self.config = config
        self.feeds = feeds
        self.m_downloadlog = []

    def sync(self):
        self.db.sync()
    
    def save_encinfo(self,encinfo):
        local = {'enclosure_id' : encinfo.id }
    
        local = { \
            'enclosure_id' : encinfo.id, \
            'feed_id' : encinfo.feed.id \
            }

        for attr in ['marked','creation_time','download_started', \
                     'download_completed','status','filename']:
            local[attr] = getattr(encinfo,attr)

        enclosurekey = mkenclosurekey(encinfo.id)
        filenamekey = None
        if local['filename'] is not None:
            filenamekey = mkfilenamekey(local['filename'])
            
        self.db.save_encinfo(enclosurekey,local,filenamekey)

    def new_enclosure(self,enclosure,index,entry,feedinfo,status):
        enclosure_id = self.db.next_enclosure_id()
        enclosurekey = mkenclosurekey(enclosure_id)
        guid = entry.get('id')
        urlkey = mkurlkey(enclosure.get('url'))
        urlval = (guid,enclosurekey)
        if guid is None:
            guidkey = None
            guidval = None
        else:
            guidkey = mkguidkey(guid,index)
            guidval = enclosurekey

        local = { \
            'enclosure_id' : enclosure_id, \
            'feed_id' : feedinfo.id, \
            'marked' : False, \
            'creation_time' : time.localtime(), \
            'download_started' : None, \
            'download_completed' : None, \
            'status' : status, \
            'filename' : None, \
            'index' : index
            }

        thin_entry = {}
        for key in ['title','link','description','id','modified_parsed']:
            if entry.has_key(key):
                thin_entry[key] = entry[key]
                
        #Compare disk usage with more compact data.
        enclosureval = { \
            'enclosure' : enclosure.copy(), \
            'entry' : thin_entry, \
            'local' : local }

        self.db.new_enclosure(urlkey,urlval,guidkey,guidval,enclosurekey,enclosureval)

        return enclosureval
    
    def close(self):
        self.db.close()

    def _get_target_status(self,url,feedinfo):
        """Support for legacy history system."""
        return self.feeds.get_target_status(url,feedinfo)
    
    def _urlishistoric(self,url):
        """Support for legacy history system."""
        urlsplit = url.split('/')
        filename = urlsplit[-1]
        return self._filenameishistoric(filename)

    def _filenameishistoric(self,filename):
        """Support for legacy history system."""
        if len(self.m_downloadlog) == 0:
            self._absorbhistory()
        return self.m_downloadlog.__contains__(filename)
    
    def _absorbhistory(self):
        """Support for legacy history file."""

        try:
            historyfile = open(self.config.history_file, 'r')
        except IOError, ex:
            errno, args = ex.args
            if errno != 2:
                log.exception("Unexpected exception opening history file.")
            return
        try:
            entries = [entry.rstrip() for entry in historyfile]
            historyfile.close()
        except IOError, ex:
            log.exception("Unexpected exception reading history file.")
            return
        log.debug("Absorbing %d entries from the history file.", len(entries))
        for item in entries:
            self.m_downloadlog.append(item)
    
    def get_encinfo(self, enclosure, index, entry, feedinfo, default_status):
        """
        Build an 'encinfo' dict from information obtained by feedparser. 

        enclosure -- feedparser's enclosure dict
        index -- which enclosure we're looking at, from...
        entry -- the entry we're looking at, which in turn we found in
        feedinfo -- probably, an instance of ipodder.feeds.Feed. 
        defaut_status -- which status (e.g. 'to_download') to assign by 
                default.
        """

        # Get enclosure attributes
        url = enclosure.get('url')

        if url is None:
            raise BadEnclosureException("Enclosure has no 'url' attribute.")

        if not url:
            raise BadEnclosureException("Enclosure has empty 'url' attribute.")

        guid = entry.get('id')

        enclosurekey = None
        
        # Compute a "URL key", which will change whenever the podcaster 
        # re-hosts their content or otherwise renames it. 
        urlkey = mkurlkey(url) 

        # If we find the URL key, use it to retrieve the "URL record". 
        if self.db.has_key(urlkey): 
            # If we have an enclosure guid, we use it to look for the 
            # "enclosure key", either one that matches the guid or, if 
            # none does, the "topmost" one (which, for a dict, is un-
            # predictable). 
            log.debug("Found key for url: %s" % url)
            urlrec = self.db[urlkey]
            if guid:
                if urlrec.has_key(guid):
                    log.debug("Found enclosure matching guid: %s" % guid)
                    enclosurekey = urlrec[guid]
                else:
                    log.debug("No enclosure found for guid: %s" % guid)
                    # Note that if we don't have a guid, we're left without
                    # an enclosure key. 
            else:
                log.debug("No guid available for this url.")
                enclosurekey = urlrec.values()[0]
        # If not, but at least we have a guid...
        elif guid:
            # Make a guid key given the guid and enclosure index, and... 
            guidkey = mkguidkey(guid,index)
            # Look for it in the database. I THINK this means that if someone 
            # changes how many enclosures are in each entry, we could miss 
            # spotting a match. 
            if self.db.has_key(guidkey):
                log.debug("""Warning: new enclosure url at %s matches guid %s.
                Assuming the podcaster moved hosts or changed the URL. 
                If this is not the case, please contact the podcaster and ask
                them to review their guid usage.""" % (url,guid))
                enclosurekey = self.db[guidkey]

        if enclosurekey and self.db.has_key(enclosurekey):
            log.debug("Matched enclosure key: %s" % enclosurekey)
            enclosureval = self.db[enclosurekey]
        else:
            log.debug("Looks like a new enclosure to us!")
            enclosureval = self.new_enclosure(enclosure,index,entry,feedinfo,default_status)

            #Try to do the right thing if history got wiped for some reason.
            log.debug("Checking for file on disk, in the default location.")
            (is_present,filename,feedwherepresent) = \
                self._get_target_status(url,feedinfo)
            local = enclosureval['local']
            if is_present:
                log.debug("Found file, marking downloaded.")
                local['status'] = 'downloaded'
                local['marked'] = False
                local['filename'] = filename   
                enclosurekey = mkenclosurekey(local['enclosure_id'])
                self.db[enclosurekey] = enclosureval
            elif feedinfo.consider_legacy_history:
                log.debug("Considering legacy history.txt")
                if self._urlishistoric(url):
                    log.debug("Found url in legacy history, but can't find file on disk, marking skipped.")
                    local['status'] = 'skipped'
                    local['marked'] = False
                    enclosurekey = mkenclosurekey(local['enclosure_id'])
                    self.db[enclosurekey] = enclosureval
                else:
                    log.debug("Didn't find url in legacy history and didn't find file on disk, so as far as we know it's new.")
            else:
                #Warning: files in unexpected locations, that would require HTTP
                #actions to resolve, such as filenames set by content-disposition or
                #30x redirects, will not be found by this algorithm.
                log.debug("Didn't find file on disk in the default location, so as far as we know it's new.")
                
        return self.mkencinfo(enclosureval)

    def mkencinfo(self,rec):
        enclosure = rec['enclosure']
        entry = rec['entry']
        local = rec['local']

        url = enclosure.get('url')
        
        try: 
            length = int(enclosure.get('length', -1))
        except ValueError, ex: 
            length = -1

        #Get the enclosing item's title for displaying in the UI
        item_title = url
        if entry.has_key('title'):
            #Unicode issues?
            item_title = entry['title']

        item_description = ""
        if entry.has_key('description'):
            item_description = entry['description']

        item_link = ""
        if entry.has_key('link'):
            item_link = entry['link']

        status = local['status']

        if status in ['downloaded','skipped','cancelled','clearing','removed']:
            mark_for_download = False
        else:
            mark_for_download = True

        feed_id = local['feed_id']
        feedinfo = self.feeds[feed_id]

        filename = local['filename']
        if status == 'downloaded' and (not filename or not os.path.exists(filename)):
            #uh oh, the file's gone missing.
            status = 'removed'
            mark_for_download = False
            
        enclosure_id = local['enclosure_id']
        
        return ipodder.core.Enclosure(enclosure_id, url, feedinfo, length, mark_for_download, item_title, item_description, item_link, status=status, filename=filename)

    def remove_files(self,files):
        for file in files:
            filenamekey = mkfilenamekey(file)
            if self.db.has_key(filenamekey):
                enclosurekey = self.db[filenamekey]
                self.db.update_enclosure_status(enclosurekey,'removed',False)

    def log_feedscan(self, feedinfo, enclosures):
        feedkey = mkfeedkey(feedinfo.id)
        enclist = [enclosure.id for enclosure in enclosures]
        self.db.log_feedscan(feedkey,time.time(),enclist)

    def clean_history(self, max_age):
        if max_age >= 0:
            log.info("Compacting the history file with a threshold of %d days." % max_age)
            self.db.clean_history(max_age)

    def pretty_name_from_path(self,path):
        """Get the RSS entry title associated with the enclosure for this
        filename.  Alternatively we could introspect the file for metadata.
        That's code for another module :-)"""
        filenamekey = mkfilenamekey(path)
        try:
            enclosurekey = self.db[filenamekey]
            enclosureval = self.db[enclosurekey]
            return enclosureval['entry']['title']
        except:
            pass
        
        #No match in history.  Return the filename.
        return os.path.split(path)[-1]
    
    def history_for_feed(self, feed, rescan=True): 
        """
        Figure out the history for a given feed. 

        feed -- the Feed, or its feed_id
        rescan -- whether to rescan the history database (default: True)
        """
        if not isinstance(feed, int): 
            feed = feed.id
        if rescan or not hasattr(self, '_history_scanned_enc_map'): 
            enc_keys = [k for k in self.db.keys() if k.startswith('enclosure:')]
            enc_map = {}
            for key in enc_keys: 
                val = self.db[key]
                enc_map.setdefault(val['local']['feed_id'], []).append(val)
            for enc_list in enc_map.values(): 
                enc_list.sort(lambda x, y: cmp(x['local']['creation_time'], y['local']['creation_time']))
            self._history_scanned_enc_map = enc_map
        else: 
            enc_map = self._history_scanned_enc_map
        return enc_map.get(feed, [])
    
class BadEnclosureException(Exception):
    """Raised when we're unable to work with the enclosure passed in."""
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
                  


if __name__ == '__main__': 
    import shelve
    import types
    import pickle
    from ipodder import conlogging, configuration, hooks
    from ipodder.core import iPodder
    import ipodder.state
    import dbhash
    import pprint
    
    logging.basicConfig()
    handler = logging.StreamHandler()
    handler.formatter = conlogging.ConsoleFormatter("%(message)s", wrap=False)
    log.addHandler(handler)
    log.propagate = 0
    log.setLevel(logging.DEBUG)
    parser = configuration.makeCommandLineParser()
    options, args = parser.parse_args()
    if args: 
        parser.error("only need options; no arguments.")
    config = configuration.Configuration(options)
    hooks.log.setLevel(logging.INFO)
    state = ipodder.state.open(config)
    ipodder = iPodder(config, state)

    for feed in ipodder.feeds: 
        pprint.pprint(ipodder.history.history_for_feed(feed, rescan=False))

    
    
