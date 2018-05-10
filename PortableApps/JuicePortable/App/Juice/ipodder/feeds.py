# 
# iPodder feeds module
#

import os
import sys
import stat
import logging
import urlparse
import urllib
import re
import time
import misc

from ipodder.contrib import bloglines
from ipodder.contrib import urlnorm
import ipodder
from ipodder.grabbers import BasicGrabber
from ipodder import feedmanager
from gui.skin import DEFAULT_SUBS

log = logging.getLogger('Juice')

SUB_STATES = ('unsubscribed', 'newly-subscribed', 'subscribed', 'preview', 'disabled', 'force')

def mkfeedkey(feedorint): 
    "Make a feedkey out of a feed or an integer."
    assert feedorint is not None
    return 'feed#%d' % int(feedorint)

def urlrstrip(url): 
    "Strip nasty things from the trailing end of a URL."
    while url[-3:] in ['%00', '%20']: 
        url = url[:-3]
    scheme, addr, path, query, fragid = urlparse.urlsplit(url)
    while path and ord(path[-1:]) <= 32:
        path = path[:-1]
    return urlparse.urlunsplit((scheme, addr, path, query, fragid))

class Normalizer(object): 
    """Class to normalize URLs."""
    __cache = {}
    def normalize(cls, url): 
        try: 
            return cls.__cache[url]
        except KeyError: 
            return urlnorm.normalize(url)
    normalize = classmethod(normalize)
        
class Feed(object): 
    "Represent a podcast feed."

    def __init__(self, feeds, url, title='', sub_state='autopreview', manager_url=None, username='', password=''): 
        "Initialise the feed."
        self.feeds = feeds
        self.id = feeds.nextfeedid()
        self.url = urlrstrip(url) # fix 1060842 whilst adding
        assert sub_state in SUB_STATES
        self.sub_state = sub_state
        self.title = title
        self.manager_url = manager_url
        self.username = username
        self.password = password
        self.consider_legacy_history = False
        self.fix_state(noisy=False)
    
    def fix_state(self, noisy=True):
        "On unpickling, we might not have all the attributes we want."

        def info(*a, **kw): 
            """Let the user know what's going on, unless we're being quiet.
            Uses a function attribute to keep track of whether it's the 
            first call or not."""
            if not noisy: 
                return
            if info.first: 
                log.debug("Fixing feed state for feed ID #%d", self.id)
                info.first = False
            log.info(*a, **kw)

        info.first = True

        if not self.sub_state in SUB_STATES: 
            info("Reassigning invalid subscription state %s", 
                 self.sub_state)
            self.sub_state = 'subscribed'
           
        defaults = {
            # maintained exclusively by us
            'checked': None, # when did we last check? (time tuple)
            'grabbed': None, # when did we last grab an enclosure? 
            'error': '', # set to string to give feed error display
            'dirname': None,   # relative to config.download_dir

            # used when we start managing disk consumption: 
            'priority': 1,
            'mblimit': 0,
            
            # set from feedparser/HTTP
            'modified': '', # last-modified according to HTTP (time tuple)
            'etag': '', # etag last time we checked
            'status': -1, # http status
            
            # set from feedparser: 
            'version': 'unknown', 
            'title': '', 
            'tagline': '',
            'generator': '', 
            'copyright_detail': {}, 
            'copyright': '',
            'link': '',

            # auto cleanup options
            'cleanup_enabled': False, # is auto-cleanup enabled?
            'cleanup_max_days': 14, # cleanup files more than this many days old
            'cleanup_last': None, # last time auto cleanup was run for this feed

            # feed manager options
            'manager_url': None,  # are we managed by a central service?

            # authentication options
            'username': '',
            'password': '',

            # history options
            'consider_legacy_history' : True #old feeds should check old history
            
            }
        for att, value in defaults.items(): 
            if not hasattr(self, att): 
                info("Defaulting missing attribute %s to %s.", 
                      repr(att), repr(value))
                setattr(self, att, value)
        if hasattr(self, 'name'): 
            info("Replacing old 'name' attribute with 'title'.")
            self.title = self.name
            del self.name
        if isinstance(self.dirname,basestring) and self.dirname.startswith(' '):
            info("Stripping spaces off self.dirname")
            self.dirname = self.dirname.strip()
        strippedurl = urlrstrip(self.url)
        if not strippedurl and self.sub_state != 'disabled': 
            info("Disabling Garth's empty feed from hell...")
            self.sub_state = 'disabled'
        elif strippedurl != self.url: 
            info("Fixing feed with trailing control characters or whitespace.")
            self.url = strippedurl
        # strip out old normurl attributes
        if self.__dict__.has_key('normurl'): 
            del self.__dict__['normurl']
        # Do NOT helpfully flush changes. It'll lead to massive duplication. 
        
    def _get_normurl(self): 
        "What's our normalized URL?"
        # info("Calculating normalized URL.")
        return Normalizer.normalize(str(self.url))

    normurl = property(_get_normurl)
        
    def __str__(self): 
        "Convert a Feed into a string: use its name."
        return unicode(self).encode('ascii', 'replace')

    def __unicode__(self): 
        "Return a Unicode title for a feed."
        if self.title: 
            return unicode(self.title)
        else: 
            return unicode("Feed ID %d at %s" % (self.id, self.url))
        

    def __int__(self): 
        "Convert a Feed into an int: use its id."
        return self.id

    # TODO: add a feeds arg to __init__, and a flush method. 

    def half_flush(self): 
        """Flush this feed's information back to the state database."""
        self.feeds.write_feed_to_state(self)

    def flush(self): 
        """Flush all feeds everywhere."""
        self.feeds.flush()

    def mb_on_disk(self): 
        """Calculate how much disk space we're using. Doesn't scan the 
        playlist, so won't find anything outside of the feed's current 
        target directory."""
        if self.dirname is None: 
            return 0.0
        try: 
            path = self.target_directory
            if not os.path.isdir(path):
                return 0.0
            files = [os.path.join(path, f) for f in os.listdir(path)]
            files = [f for f in files if os.path.isfile(f)]
            bytes = sum([os.stat(f)[stat.ST_SIZE] for f in files])
            return float(bytes) / (1024.0*1024.0)
        except OSError, ex: 
           errno, message = ex.args
           if errno == 3: # ESRCH, directory not found 
               return 0.0
           log.exception("Caught OSError (errno %d, \"%s\") "\
                         "scanning directory %s", errno, message, path)
           return 0.0
        except: # Oh, no. Another @(*&^! blind exception catcher.
            try:
                log.exception("Can't calculate MB total for %s", self)
            except (NameError, UnboundLocalError):
                log.exception("Can't find path for feed at %s", self.url)
            return 0.0

    def get_target_directory(self): 
        """Calculate the full target directory for this feed.

        Computes self.dirname on the fly if necessary."""
        if not self.dirname:
            if self.title:
                self.dirname = re.sub('[\\\\/?*:<>|;"\'\.]','', self.title).strip()
            else:
                self.dirname = "Feed%d" % self.id
            log.info("Feed \"%s\" now has target directory %s", 
                    self.title, self.dirname)
            self.half_flush()
        return os.path.join(self.feeds.config.download_dir, self.dirname)

    target_directory = property(
            fget = get_target_directory,
            doc = "Target directory for this feed."
            )

    def mkdir(self): 
        """Ensure our directory exits."""
        tg = self.target_directory
        if not os.path.isdir(tg): 
            log.info("Creating target directory %s", tg)
            os.makedirs(tg)

    def _get_target_filename(url): 
        """get_target_filename's complicated guts, presented for ease of 
        testing."""
        scheme, netloc, path, args, fragment = urlparse.urlsplit(url)
        filename = re.split(r'\/|\\', path)[-1] # take the last fragment
        if '%' in filename: # FeedBurner-embedded URL? 
            url2 = urllib.unquote(filename)
            scheme2, netloc2, path2, args2, fragment2 = urlparse.urlsplit(url2)
            if args2 and not args: 
                args = args2
            filename = re.split(r'\/|\\', path2)[-1] 
        if args:  # Merge them back in, in safe form
            args = re.sub("[^A-Za-z0-9]","_",args)
            base, ext = os.path.splitext(filename)
            filename = "%s_%s%s" % (base, args, ext)
        return filename
    _get_target_filename = staticmethod(_get_target_filename)
    
    def get_target_filename(self, enclosure): 
        """Calculate the target filename for an enclosure referred to
        by this feed.
        
        enclosure -- either a URL or something with a .url attribute."""

        if hasattr(enclosure, 'url'): 
            url = enclosure.url
        else: 
            url = enclosure
        
        filename = self._get_target_filename(url)
        result = os.path.join(self.target_directory, filename)
            
        # log.debug("%s -> %s", url, result)
        return result

    def get_target_status(self, enclosure):
        """Return target file status for this URL.
        
        Was: is_url_present"""
        target_file = self.get_target_filename(enclosure)
        return self.get_target_file_status(target_file)

    def get_target_file_status(self, filename):
        """Return (True, foundpath), or (False, None) if the path can't 
        be determined.

        filename -- the base filename of the file (no path information!)

        This method used to be called is_file_present."""
        
        # match without extra resolution
        if os.path.isfile(filename): 
            return (True, filename) 
        
        # match in our target directory
        path = os.path.join(self.target_directory, filename)
        if os.path.isfile(path): 
            return (True, path)

        # match, uh, weirdly
        path2 = os.path.join(self.feeds.config.download_dir, self.dirname, urllib.url2pathname(filename))
        if os.path.isfile(path2):
            return (True, path2)

        # don't match
        return (False, None)

    if 0: 
        # These should be unused by now. 

        def file_path_from_url(self,url):
            return self.is_url_present(url)[1]
        
        def file_path(self,filename):
            return self.is_file_present(filename)[1]

    def getfiles(self, min_age=None):
        """Get files older than days or all files if days is None."""
        files = []
        if not self.dirname:
            return []
        dir = os.path.join(self.feeds.config.download_dir, self.dirname)
        if not os.path.isdir(dir):
            return files
        files.extend(misc.get_fileinfos(
            [os.path.join(dir,f) for f in os.listdir(dir)],
            min_age = min_age))

        return files
        
class DuplicateFeedUrl(ValueError): 
    """Used to reject duplicate feeds."""
    pass
    
class Feeds(feedmanager.ManagedFeeds): 
    "A list to keep track of feeds."
    
    def __init__(self, config, state): 
        "Initialize the feeds from `config` and `state`."
        object.__init__(self)
        self.config = config
        self.state = state
        self.feeds_by_normalized_url = {}
        self._members = []
        self.absorb()
        self.flush()
        self.clean_state_database()
        self.refresh_grabber_passwords()
        
        #We need this for unpickling Enclosure objects.
        ipodder.set_feeds_instance(self)
        
    def nextfeedid(self): 
        "Return the next feed ID. Doesn't sync(); that's expected later."
        state = self.state
        feedid = state.get('lastfeedid', 1) # What's the last feedid we used?
        if not isinstance(feedid, int): 
            feedid = 1
        # Just in case, make sure we avoid collisions. 
        while True: 
            feedkey = mkfeedkey(feedid)
            if state.has_key(feedkey): 
                feedid = feedid + 1
            else: 
                break
        state['lastfeedid'] = feedid
        return feedid

    def has_feed_url(self, url): 
        return self.has_feed_normurl(urlnorm.normalize(url))

    def has_feed_normurl(self, normurl):
        return self.feeds_by_normalized_url.has_key(normurl)

    def __getitem__(self, key): 
        """Retrieve a feed."""
        if isinstance(key, int): 
            for feed in self._members: 
                if feed.id == key: 
                    return feed
            else: 
                raise KeyError, key
        else: 
            normurl = urlnorm.normalize(key)
            return self.feeds_by_normalized_url[normurl]

    def get(self, key, default=None): 
        """Retrieve a feed, returning a default value if it's not found."""
        try: 
            return self[key]
        except KeyError: 
            return default
    
    def addfeed(self, url, quiet=False, *a, **kw): 
        "Create and add a feed, taking care of all state."
        state = self.state
        feed = Feed(self, url, *a, **kw)
        assert feed is not None
        match = self.feeds_by_normalized_url.get(feed.normurl)
        if match is not None:
            if match.sub_state != 'subscribed' and match.sub_state != feed.sub_state:
                #update the old feed with the new feed's state, to
                #handle adding a previously deleted feed.
                match.sub_state = feed.sub_state
                match.manager_url = feed.manager_url
                if hasattr(state, 'sync'): 
                    state.sync()
            if quiet: 
                return None
            else: 
                raise DuplicateFeedUrl, match
        else: 
            self.feeds_by_normalized_url[feed.normurl] = feed
        self.write_feed_to_state(feed)
        self._members.append(feed)
        return feed
        
    def absorb(self): 
        "Absorb feed definitions from everywhere."
        self.absorb_from_state()
        self.absorb_from_favorites_file()
        self.absorb_from_command_line()
        self.absorb_from_bloglines()
        self.absorb_from_named_preloads()
        self.absorb_default_feeds()

    def absorb_default_feeds(self): 
        "Absorb the default feed if necessary."
        if not len(self): 
            log.info("No feeds defined! Adding the default feeds.")
            for (title,url) in DEFAULT_SUBS:
                self.addfeed(url, title=title, sub_state='subscribed')

    def absorb_from_state(self): 
        "Absorb feeds from the state database."
        # First, let's dodge a known pickle problem. 
        try: 
            sys.modules['feeds'] = sys.modules['ipodder.feeds']
        except KeyError: 
            pass # ugh
        state = self.state
        feeds_by_normalized_url = self.feeds_by_normalized_url
        feedcount = 0
        delfeeds = []
        feedkeys = [key for key in state.keys() if key[:5] == 'feed#']
        goodfeeds = []
        for key in feedkeys:
            feed = state[key] # will fail on pickle problem
            if not hasattr(feed, '__class__') \
            or feed.__class__.__name__ not in ['Feed', 'ipodder.feeds.Feed']: 
                log.error("Deleting non-feed object for key %s", key)
                del state[key]
                state.sync()
                continue
            goodfeeds.append(feed)
        feedidmap = dict([(feed.id, feed) for feed in goodfeeds])
        feedids = feedidmap.keys()
        feedids.sort()
        for feedid in feedids: 
            feed = feedidmap[feedid]
            feed.fix_state() # add new attributes, etc
            feed.feeds = self # and this one :)
            # feeds_by_url is used so we can avoid loading duplicate
            # feeds from all these different sources
            collision = feeds_by_normalized_url.get(feed.normurl)
            if collision is not None: 
                log.warn("Feed #%d (\"%s\") has the same URL as feed #%d (\"%s\"): %s", 
                         feed.id, str(feed), collision.id, str(collision), feed.url)
                delfeeds.append(feed)
            else: 
                feeds_by_normalized_url[feed.normurl] = feed
                self._members.append(feed)
                feedcount = feedcount + 1
        log.info("Loaded %d feeds from the state database.", feedcount)
        if delfeeds: 
            log.warn("%d feeds need deleting.", len(delfeeds))
            for delfeed in delfeeds: 
                feedkey = mkfeedkey(delfeed.id)
                del state[feedkey]
            if hasattr(state, 'sync'): 
                state.sync()
            
    def absorb_from_favorites_file(self): 
        "Absorb feeds from the old favorites file."
        filename = self.config.favorites_file
        name, ext = os.path.splitext(filename)
        feedcount = 0
        sub_state = 'newly-subscribed'
        if not len(self): 
            # If we're upgrading from 1.0 or previous, assume everything 
            # is subscribed. 
            sub_state = 'subscribed'
       
        # If it's an OPML file, use the other method. 
        if ext == '.opml': 
            return self.absorb_from_opml_file(filename)

        # Load from a flat file of URLs
        log.debug("Attempting to load favorites file %s", filename)
        try: 
            feeds = file(filename, 'rt')
            for line in feeds: 
                url = line.strip()
                if not url: 
                    continue # it's an empty line!
                if url[:1] == '#': 
                    continue # it's a comment!
                try: 
                    self.addfeed(url, sub_state=sub_state)
                    log.info("Added from favorites file: %s", url)
                    feedcount = feedcount + 1
                except DuplicateFeedUrl, ex: 
                    pass # log.debug("Skipping known feed %s", url)
            feeds.close()
        except (IOError, OSError), ex: 
            errno, message = ex.args
            if errno == 2: # ENOFILE
                log.debug("... but it doesn't exist. Oops.")
            else: 
                log.exception("Ran into some problem loading feeds "\
                              "from favorites file %s", filename)
        log.info("Loaded %d new feeds from %s", feedcount, filename)

    def absorb_from_command_line(self): 
        """Absorb favorites from the command line."""
        pass # not implemented yet, but let's not make it a show-stopper

    def absorb_from_opml(self, opml, default_sub_state='unknown'):
        import ipodder.outlines
        tree = ipodder.outlines.Head.fromopml(opml)
        if not tree:
            return None
        
        def traverse(node,numadded):
          if not isinstance(node, ipodder.outlines.Node):
            return
          if not hasattr(node,"type"):
            return

          url = ''
          if node.type == "link":
              title = node.text
              url = node.url
          if node.type == "rss":
              title = node.title
              url = node.xmlUrl

          if url:
            self.addfeed(url,title=title,quiet=True,sub_state='newly-subscribed')
            numadded += 1

          for child in node:
            numadded = traverse(child,numadded)

          return numadded
 
        numadded = traverse(tree,0)

        return numadded

    def absorb_from_opml_file(self, filename, default_sub_state='unknown'): 
        """Absorb favorites from an OPML file, defaulting their 
        subscription state.  Return the number of subscriptions added,
        or None if parsing failed."""
        fh = open(filename,'r')
        opml = fh.read()
        fh.close()
        return self.absorb_from_opml(opml, default_sub_state)

    def absorb_from_bloglines(self): 
        """Absorb favorites from Bloglines."""
        if not self.config.bl_username:
            log.info("Bloglines not configured.")
            return
        log.info("Attempting to load new feeds from Bloglines...")
        if not self.config.bl_password: 
            log.error("Can't access Bloglines; no password specified.")
            return
        if not self.config.bl_folder: 
            log.error("Can't access Bloglines; no blogroll folder specified.")
            return
        newfeeds = 0
        blfeeds = 0
        try: 
            for url in bloglines.extractsubs(self.config.bl_username, 
                    self.config.bl_password, self.config.bl_folder): 
                blfeeds += 1
                try: 
                    url = str(url) # strip Unicode
                    self.addfeed(url, sub_state='newly-subscribed')
                    log.info("Added from Bloglines: %s", url)
                    newfeeds = newfeeds + 1
                except DuplicateFeedUrl, ex: 
                    log.debug("Skipping known feed %s", url)
            if not blfeeds:
                log.error("Couldn't see anything in Bloglines. Either your "\
                          "folder is wrong, or you haven't subscribed to "\
                          "anything in it.")
        except KeyError: 
            log.error("Couldn't load feeds from Bloglines because blogroll "\
                      "folder %s doesn't exist.", self.config.bl_folder)
        except KeyboardInterrupt: 
            raise
        except bloglines.urllib2.HTTPError, ex: 
            log.debug("%s", repr(ex.__dict__))
            if ex.code == 401:
                log.error("Can't access Bloglines: authentication failure.")
            elif ex.code == 404:
                log.error("Bloglines service appears to no longer be "\
                          "available where we think it is (404).")
            elif ex.code == 503:
                log.error("Bloglines service unavailable (503).")
            else:
                log.error("Can't access Bloglines; HTTP return code %d", 
                        ex.code)
            return
        except: 
            log.exception("Experimental Bloglines support failed. "\
                          "Please report the following information:")
            return
        log.info("Loaded %d new feeds out of %d from Bloglines.", 
                 newfeeds, blfeeds)

    def absorb_from_named_preloads(self):
        """Absorb feeds from named preloads defined in the skin."""

        #locate the preloads directory.
        try:
            from gui.skin import PRELOAD_SUBS
        except ImportError:
            log.debug("No PRELOAD_SUBS variable found in the skin.")
            return

        if PRELOAD_SUBS == None:
            log.debug("PRELOAD_SUBS is None.")
            return
        
        #load history.
        state = self.state
        try: 
            old_preloads = state['old_preloads']
        except KeyError: 
            old_preloads = []
        log.debug("Old preloads: %s" % str(old_preloads))

        #check preloads against history
        preloads_added = 0
        for (name,subs) in PRELOAD_SUBS:
            if old_preloads.count(name) > 0:
                log.debug('Preload %s is in history.  Skipping.' % name)
                continue
            log.debug("Absorbing preload %s" % name)
            try:
                feeds_added = 0
                for (title,url) in subs:
                    self.addfeed(url, title=title, sub_state='newly-subscribed')
                    feeds_added += 1
                if feeds_added:
                    old_preloads.append(name)
                    preloads_added += 1
            except:
                log.exception("Preload failed from name %s" % name)
                
        if preloads_added > 0:
            log.debug("Absorbed %d new preloads." % preloads_added)
            state['old_preloads'] = old_preloads
       
    def flush(self): 
        """Flush feed definitions to our various places."""
        self.write_to_state()
        self.write_to_favorites_file()

    def write_feed_to_state(self, feed, sync=True): 
        """Write one feed's state to the state database."""
        # TODO: fix grotty hack by using pickle protocol properly
        state = self.state
        feedkey = mkfeedkey(feed)
        if hasattr(feed, 'feeds'): 
            del feed.feeds
        state[feedkey] = feed
        if sync: 
            if hasattr(state, 'sync'): 
                state.sync()
        feed.feeds = self
        
    def write_to_state(self): 
        """Flush feed definitions to the state database."""
        state = self.state
        for feed in self._members: 
            self.write_feed_to_state(feed, sync=False)
        if hasattr(state, 'sync'): 
            state.sync()
        
    def write_to_favorites_file(self): 
        """Flush feed definitions to the favorites file."""
        filename = self.config.favorites_file
        name, ext = os.path.splitext(filename)
        
        # If it's a torrent, use the other method. 
        if ext == '.torrent': 
            return self.write_to_opml_file(filename)

        # Otherwise...
        try: 
            favorites = file(filename, 'wt')
            for feed in self._members: 
                if feed.sub_state in ('disabled',): 
                    continue
                try: 
                    print >> favorites, "# %s" % feed
                except UnicodeEncodeError, ex: 
                    pass # simplistic, but it'll work
                print >> favorites, feed.url
            favorites.close()
            log.info("Wrote %d entries to %s", len(self._members), filename)
        except (IOError, OSError): 
            log.exception("Unexpected problem writing favorites file %s", 
                          filename)
        
    def write_to_opml_file(self, filename): 
        """Flush feed definitions to an OPML file."""

        #Step 1: Build the XML document
        from xml.dom.minidom import getDOMImplementation
        import time
        import locale
        
        encoding = locale.getpreferredencoding()
        log.info("Exporting feeds to OPML file: %s", filename)
        log.info("Using system locale's preferred encoding: %s", encoding)
        
        def enc(s): 
            """Encode a string to Unicode using the locale's preferred encoding."""
            try: 
                return unicode(s, encoding)
            except TypeError: 
                log.error("Can't encode %s; trying another approach...", repr(s))
                return misc.encode(s)
        
        impl = getDOMImplementation()
        doc = impl.createDocument(None,"opml",None)
        opml = doc.documentElement
        opml.setAttribute("version","1.1")
        head = doc.createElement("head")
        title = doc.createElement("title")
        title.appendChild(doc.createTextNode("iPodder Exported Subscriptions"))
        head.appendChild(title)
        dc = doc.createElement("dateCreated")
        dc.appendChild(doc.createTextNode(time.strftime('%a, %d %b %Y %T %z',time.localtime())))
        head.appendChild(dc)
        opml.appendChild(head)
        body = doc.createElement("body")
        rootOutline = doc.createElement("outline")
        rootOutline.setAttribute("text","iPodder Exported Subscriptions")
        n = 0
        for feed in self._members: 
            if feed.sub_state in ('disabled',): 
                continue

            outline = doc.createElement("outline")
            outline.setAttribute("type", "rss")
            outline.setAttribute("text", feed.title)
            outline.setAttribute("title", feed.title)
            outline.setAttribute("xmlUrl", feed.url)
            log.info(outline.toxml())
            rootOutline.appendChild(outline)
            n += 1
        body.appendChild(rootOutline)
        opml.appendChild(body)

        #Step 2: Write to file
        try: 
            fh = open(filename, 'wb')
            fh.write(doc.toxml(encoding='utf-8'))
            fh.close()
            log.info("Wrote %d entries to %s", n, filename)
        except (IOError, OSError): 
            log.exception("Unexpected problem writing opml file %s", 
                          filename)

    def __len__(self): 
        "How long are we?"
        return len(self._members)

    def __iter__(self): 
        "Support iteration through our members."
        return iter(self._members)

    def clean_state_database(self): 
        "Delete now-obsolete state keys." 
        state = self.state
        first = True
        for key in state.iterkeys(): 
            if key[:5] == 'feed-': 
                if first: 
                    first = False
                    log.info("Cleaning up state database of stale feed "\
                             "status items.")
                    del state[key]

    def get_target_status(self, url, hint=None, greedy=False):
        """Finds a target and returns information on it. 

        url -- the URL (or something with a .url attribute) to check
        hint -- a particular Feed object to check against
        greedy -- scan through all known feeds if hint isn't set

        Returns: (exists, found_path, first_feed_it_was_found_in)

        Was: is_url_present."""

        if hint:
            (is_present,path) = hint.get_target_status(url)
            if is_present:
                return (is_present, path, hint)

        if not greedy:
            return (False,None,None)

        for feedinfo in self:
            (is_present, path) = feedinfo.get_target_status(url)
            if is_present:
                return (is_present, path, feedinfo)            

        return (False, None, None)

    def refresh_grabber_passwords(self):
        """Set up feed passwords.  NOTE: urllib2 wants to deal with passwords
        at the host level, and things break if we set up the password at
        e.g. http://foo.bar.com/path/to/rss.xml, so we have to strip off
        the path and register the password for http://foo.bar.com/".  The
        upshot is you can only register one username/password per host, at
        least until one of us writes a better password manager."""
        for feed in self._members:
            if feed.username and feed.password:
                import urlparse
                p = urlparse.urlsplit(feed.url)
                url = urlparse.urlunsplit([p[0],p[1],'/','',''])
                BasicGrabber.shared_password_mgr.add_password(None, url, \
                    feed.username, feed.password)

if __name__ == '__main__': 
    import shelve
    import types
    import pickle
    from ipodder import conlogging, configuration
    import ipodder.state
    import dbhash
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
    if 1: 
        log.info("Checking we can unpickle everything...")
        state = dbhash.open(config.state_db_file, 'w')
        keys = state.keys()
        for key in keys:
            if key == "tmp_downloads":
                #don't unpickle me unless Feeds has been instantiated.
                continue
            try: 
                value = state[key]
            except KeyError, ex: 
                log.error("Database corruption on key %s", repr(key))
                state[key] = ''
                del state[key]
                state.sync()
            else: 
                delete = False
                try: 
                    item = pickle.loads(value)
                except (IndexError, KeyError, EOFError), ex: 
                    delete = True
                except TypeError, ex: 
                    if ex.args: 
                        if 'null bytes' in ex.args[0]: 
                            delete = True

                    log.exception("Can't import module for key %s: %s", repr(key), ex.args)
                if delete: 
                    log.error("Record %s damaged beyond repair.", repr(key))
                    del state[key]
                    state.sync()
                    continue
        state.close()
        del state
        log.info("Check complete. Creating Feeds object...")
    
    state = ipodder.state.State(config)
    feeds = Feeds(config, state)

    if 0: 
        for feed in feeds: 
            print str(feed)
            atts = [att for att in dir(feed) 
                    if att[:1] != '_' 
                    and not att in ['feeds']
                    and not isinstance(getattr(feed, att), types.MethodType)]
            atts.sort()
            for att in atts: 
                print "  %s = %s" % (att, repr(getattr(feed, att)))
