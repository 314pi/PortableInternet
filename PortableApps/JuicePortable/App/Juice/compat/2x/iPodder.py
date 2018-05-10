import ipodder

class Enclosure:
    """Support shelved iPodder.Enclosure objects, which were moved to
    ipodder.core after the 2.1 release.  This is a straight copy from
    core.py v1.1."""
    
    def __init__(self, url, feed, length, marked, item_title, item_description, item_link):
        """Initialise the `Enclosure`.
        
        url -- the url of the enclosure
        feed -- the feed it's in
        length -- the length of the enclosure
        marked -- marked for download?
        title -- title of the enclosing item"""
        
        self.url = url
        self.feed = feed
        self.marked = marked # for download
        self.length = length
        self.item_title = item_title
        self.creation_time = time.localtime()
        self.download_started = None
        self.download_completed = None
        self.description = item_description
        self.item_link = item_link
        self.status = "new"
        
    def unmark(self):
        "Unmark this enclosure for download."
        self.marked = False

    def GetStatus(self):
        """Return a displayable version of self.status.
        AG: Superseded by i18n lookups in str_dl_(state)"""
        if self.status == "new":
            return "New"
        if self.status == "queued":
            return "Queued"
        if self.status == "downloading":
            return "Downloading"
        if self.status == "cancelled":
            return "Cancelled"
        if self.status == "downloaded":
            return "Finished"
        if self.status == "partial":
            return "Partially downloaded"
        log.debug("Enclosure has unknown status %s" % self.status)
        return "Unknown"
    
    def GetStatusDownloadSpeed(self):
        """Return a displayable version of self.status.  i18n lookups
        go in here."""
        retval = ""
        if self.status == "downloading" and hasattr(self,"grabber") and self.grabber:
            retval += "%.1f%%; %.1fkB/s" % ((100*self.grabber.fraction_done),self.grabber.download_rate/1024)
        return retval

    def get_target_status(self):
        """Just an alias for a method of the containing feed.
        See ipodder.Feed.get_target_status()."""
        return self.feed.get_target_status(self)
    
    #We have to remove the feed object to make this pickleable.
    def __getstate__(self):
        state = self.__dict__.copy()
        state['feedid'] = self.feed.id
        del state['feed']
        return state
    
    def __setstate__(self,dict):
        self.__dict__.update(dict)
        self.feed = ipodder.get_feeds_instance()[self.feedid]
        del self.feedid
        if not hasattr(self,"creation_time"):
            self.creation_time = time.localtime()
        if not hasattr(self,"download_started"):
            self.download_started = None
        if not hasattr(self,"download_completed"):
            self.download_completed = None
        if not hasattr(self,"status"):
            self.status = "downloaded"
        if not hasattr(self,"description"):
            self.description = None
        if not hasattr(self,"item_link"):
            self.item_link = None
            
    def __str__(self): 
        "Return our filename as a string."
        return basename(self.feed.get_target_filename(self))
