#
# iPodder thread management code
#

import threading
import logging
import hooks
import sys

COM = False
try: 
    import pythoncom
    COM = True
except ImportError: 
    pass

log = logging.getLogger('Juice')

# TODO: add all the COM initialisation stuff

def mklogmethod(level): 
    """Make a log method for `SelfLogger`."""
    def logmethod(self, *a, **kw): 
        self.log(level, *a, **kw)
    logmethod.__doc__ = "Issue tagged level %d log record." % level
    return logmethod

class SelfLogger(object): 
    """Mixin class to give objects the ability to log via their own
    methods. It's useful for threads wanting to identify themselves 
    when they log, for example."""

    def __init__(self, log=None, tag=None):
        """Initialise the generic thread."""

        if log is None: 
            self.__log = logging.getLogger('Juice')
        else: 
            self.__log = log
            
        classname = self.__class__.__name__
        if tag is None: 
            self.__tag = "%s %d" % (classname, id(self))
        else: 
            self.__tag = "%s %d %s" % (classname, id(self), repr(tag))

    def log(self, level, msg, *args, **kwargs): 
        """Issue a tagged log entry via our logger."""
        msg = "%s reports: " + msg
        args = list(args) # take a copy
        args.insert(0, self.__tag)
        self.__log.log(level, msg, *args, **kwargs)

    # Construct logging methods at various levels
    fatal = mklogmethod(logging.CRITICAL)
    critical = mklogmethod(logging.CRITICAL)
    error = mklogmethod(logging.ERROR)
    warning = mklogmethod(logging.WARNING)
    warn = warning
    info = mklogmethod(logging.INFO)
    debug = mklogmethod(logging.DEBUG)
    spam = mklogmethod(int(logging.DEBUG/2)) # heh

    def exception(self, msg, *args, **kwargs): 
        kwargs['exc_info'] = 1
        self.error(msg, *args, **kwargs)

class OurThread(threading.Thread, SelfLogger): 
    """Generic thread."""

    def __init__(self, log=None, target=None, *a, **kw): 
        """Initialise the generic thread."""

        self.hooks = hooks.HookCollection()
        self.exc_info = None
        self.target = target

        # if we have a name, steal it
        self.name = kw.get('name')

        # Initialise our parents
        SelfLogger.__init__(self, log=log, tag=self.name)
        threading.Thread.__init__(self, *a, **kw)

    def run(self): 
        """Run .our_run(), catching exceptions."""
        target = self.target
        if target is None: 
            target = self.our_run
        try: 
            if COM: 
                pythoncom.CoInitialize()
            try: 
                target()
            except: 
                self.exc_info = sys.exc_info() 
                self.exception("Uncaught exception.")
                raise # just in case threading.Thread catches it in some 
                      # standard way in a later version of Python
        finally: 
            if COM: 
                pythoncom.CoUninitialize()

    def catch(self): 
        """Check for exceptions and re-raise them in the calling thread."""
        if self.exc_info is not None: 
            one, two, three = self.exc_info
            raise one, two, three

if __name__ == '__main__': 
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    sl = SelfLogger(log=log, tag="soon to die")
    sl.fatal("I can see the fnords!")

    def boom(): 
        raise AssertionError, "KABOOM!"
    
    ot = OurThread(target=boom)
    ot.fatal("Boo?")
    ot.start()
    ot.join()
    ot.catch()
