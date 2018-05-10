# Removed: we want these things to persist; I only put this code 
# in because of a bug which caused resumable to be set False 
# even if resumability wasn't tested. 
# iPodder file grabbing code
#
# TODO: grab timeoutsocket; put into contrib; make sure feedparser
#       can see it and is happy. 
# 
# TODO: check content type to see if something is a torrent, just 
#       in case the extension isn't '.torrent'
#
# TODO: test passing handler classes to build_opener
# TODO: test proxy handlers (can we avoid the hangs?)
# TODO: test progress reporting for transfers >1s
# TODO: test basic authentication
# TODO: test etag matching (hang on; don't we already?) if etag ~324
# TODO: test modified matching
# TODO: test gzip (hang on, don't we already?) elif feedparser.gzip and use_gzip ~338
# TODO: test _explainDownloadException (not called once!)
# TODO: test unpickling errors in _get_cachestate
# TODO: test passing checked to _cache_hit or pull it out
# TODO: test BasicGrabber of an existing file to an existing un|matching file
# TODO: test resume of cached
# TODO: test grab errors forcing cache hits
# TODO: test 304 responses (hang on; don't we already?)
# TODO: test commas in content-length (should come for free with cache hits)
# TODO: test running out of space on writes
# TODO: test unbencodable and otherwise wrong bittorrent response files
# TODO: test torrents with multiple files
# TODO: test GrabberTestServer.serve_forever (maybe the validator didn't pick up that thread)

import os
import stat
import sys
import time
import stat
import logging
import threading
import socket
import random
import urllib2
import sha
import gzip
import zlib
import StringIO
import pickle, cPickle # so we can catch exceptions
import urlparse, base64, urllib # for _open_resource
import re
import tempfile
import platform

try: 
    import timeoutsocket
except ImportError: 
    timeoutsocket = None

from configuration import __version__
import threads
import hooks

import contrib.feedparser as feedparser
from contrib.BitTorrent.bencode import bencode, bdecode
from contrib.BitTorrent.btformats import check_message
import contrib.BitTorrent.download as download
import contrib.BitTorrent.track as track
import contrib.urlnorm as urlnorm
import itunes

if hasattr(socket, 'setdefaulttimeout'): 
    if __name__ == '__main__': 
        limit = 5
    else: 
        limit = 60
    socket.setdefaulttimeout(limit)

log = logging.getLogger('Juice')

SPAM = logging.DEBUG//2 # even more detailed than logging.DEBUG
AGENT = "Juice/%s (%s) +http://juicereceiver.sf.net/" % (__version__,platform.system())
BLOCKSIZE = 4096*8
CACHEMAX = 128*1024
POLITENESS = 2*60

class GrabError(Exception): 
    """Raised when we fail to grab something."""
    def __init__(self, message, ex=None): 
        """Initialise the GrabError."""
        Exception.__init__(self, message, ex)
        self.message = message
        self.exception = ex

class GzipError(GrabError): 
    """Raised when Gzip fails."""
    pass

class AuthenticationError(GrabError):
    """Raised when authentication fails."""
    pass

class UserAborted(GrabError): 
    """Raised when we realise stop() was called before we were done."""
    pass

class GenericGrabber(threads.SelfLogger):
    """Generic grabber. Over-ride download()."""

    def __init__(self, what, dest, blocksize=BLOCKSIZE): 
        """Initialise the GenericGrabber.
        
        what -- a url, unless specified other
        dest -- either a filename or a file handle like object
        blocksize -- how much data to read at once

        If dest is a file handle, it is the caller's responsibility 
        to close it. This makes sure StringIO.StringIO instances work. 
        """

        self.what = what # probably a URL
        self.blocksize = blocksize

        if isinstance(dest, basestring): 
            self.name = os.path.basename(dest)
            self.destfilename = dest
            self.destfp = None
        else: 
            self.name = what
            self.destfilename = None
            self.destfp = dest
        
        self.stopflag = threading.Event() # set to tell us to stop
        self.doneflag = threading.Event() # set by us when we're done

        threads.SelfLogger.__init__(self, tag=self.name)

        # Public attributes, meant for interrogation from other threads
        self.last_activity = ''
        self.upload_rate = 0.0
        self.upload_mb = 0.0
        self.fraction_done = 0.0
        self.download_rate = 0.0
        self.download_mb = 0.0
        self.eta = 0.0 # units should be seconds
        self.complete = False

    def __call__(self): 
        """download()"""
        self.debug("downloading...")
        try: 
            return self.download()
        finally: 
            if not self.doneflag.isSet(): 
                self.done(complete=False)
        
    def download(self): 
        """Download whatever we're supposed to.
        
        Return filename, headers (if you can)."""
        self.done()
        return None, {}

    def done(self, complete=True):
        """Declare that we're done."""
        if complete:
            self.fraction_done = 1.0
            self.eta = 0.0
            self.hooks.get('complete')()
        self.hooks.get('update')()
        self.hooks.get('done')()
        self.doneflag.set()
        self.complete = True

    def stop(self, wait=True, timeout=None): 
        """Ask the grabber to stop."""
        self.info("Asked to stop. Setting flag...")
        self.stopflag.set()
        #self._stop()
        if wait: 
            self.debug("asked to shut down; waiting...")
            self.doneflag.wait(timeout=timeout)
            if not self.doneflag.isSet(): 
                 self.warn("Stop request timed out after %.1fs.", timeout)
            else:
                self.debug("shut down.")
        else: 
            self.debug("asked to shut down, but not waiting.")
    
        

class NullFile(object): 
    """Pretend to be a writable file, but just throw away data."""
    def write(self, data): 
        pass

# Grabbed from urllib2 in order to try to fix handler ordering problems. 

def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP and FTP.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """

    if not build_opener.warned:
        log.debug("Using custom build_opener.")
        build_opener.warned = True

    opener = urllib2.OpenerDirector()
    default_classes = [
        urllib2.ProxyHandler, urllib2.UnknownHandler, urllib2.HTTPHandler,
        urllib2.HTTPDefaultErrorHandler, urllib2.HTTPRedirectHandler,
        urllib2.FTPHandler, urllib2.FileHandler]
    if hasattr(urllib2.httplib, 'HTTPS'):
        default_classes.append(urllib2.HTTPSHandler)
    skip = []
    for klass in default_classes:
        for check in handlers:
            if urllib2.inspect.isclass(check):
                if issubclass(check, klass):
                    skip.append(klass)
            elif isinstance(check, klass):
                skip.append(klass)
    for klass in skip:
        default_classes.remove(klass)

    for h in handlers:
        if urllib2.inspect.isclass(h):
            h = h()
        if isinstance(h, urllib2.ProxyHandler): 
            opener.add_handler(h)

    for klass in default_classes:
        opener.add_handler(klass())

    for h in handlers:
        if urllib2.inspect.isclass(h):
            h = h()
        if not isinstance(h, urllib2.ProxyHandler): 
            opener.add_handler(h)

    return opener

build_opener.warned = False

class GzipFile(gzip.GzipFile):
    """Adjusted GzipFile object that doesn't need seek or tell."""

    def __init__(self, *a, **kw): 
        gzip.GzipFile.__init__(self, *a, **kw)
        self.unused_reads = ''
        
    def _read_gzip_header(self, buffer):
        """Overloaded _read_gzip_header() method. Returns what's left of your buffer."""
        old_fileobj = self.fileobj
        self.fileobj = StringIO.StringIO(buffer)
        gzip.GzipFile._read_gzip_header(self)
        position = self.fileobj.tell()
        self.fileobj = old_fileobj
        return buffer[position:]

    def _read_eof(self): 
        log.log(SPAM, "len(unused_reads) == %d", len(self.unused_reads))
        assert len(self.unused_reads) >= 8
        old_fileobj = self.fileobj
        self.fileobj = StringIO.StringIO(self.unused_reads)
        self.fileobj.read() # seek to the end
        self.unused_reads = ''
        #self.fileobj.seek(0, 2)
        gzip.GzipFile._read_eof(self)
        position = self.fileobj.tell()
        self.fileobj = old_fileobj

    def _read(self, size=1024):
        """Overloaded _read() method."""

        if self.fileobj is None:
            raise EOFError, "Reached EOF"

        # Read a chunk of data from the file
        buf = self.unused_reads + self.fileobj.read(size)
        self.unused_reads = ''

        if self._new_member:
            # If the _new_member flag is set, we have to
            # jump to the next member, if there is one.
            #
            # First, check if we're at the end of the file;
            # if so, it's time to stop; no more members to read.
            if not buf:
                raise EOFError, "Reached EOF"

            self._init_read()
            buf = self._read_gzip_header(buf)
            
            self.decompress = zlib.decompressobj(-zlib.MAX_WBITS)
            self._new_member = False

        # If the EOF has been reached, flush the decompression object
        # and mark this object as finished.

        if buf == "":
            uncompress = self.decompress.flush()
            self._read_eof()
            self._add_read_data( uncompress )
            raise EOFError, 'Reached EOF'

        uncompress = self.decompress.decompress(buf)
        self._add_read_data(uncompress)

        if self.decompress.unused_data != "":
            # Ending case: we've come to the end of a member in the file,
            # so seek back to the start of the unused data, finish up
            # this member, and read a new gzip header.
            # (The number of bytes to seek back is the length of the unused
            # data, minus 8 because _read_eof() will rewind a further 8 bytes)
            ## Well, we're cheating. _read_eof() now won't. 
            log.log(SPAM, "unused_data")
            grablength = len(self.decompress.unused_data) + 8
            self.unused_reads = buf[-grablength:]

            # Check the CRC and file size, and set the flag so we read
            # a new member on the next call
            self._read_eof()
            self._new_member = True

# Grabbed from feedparser so we can over-ride headers.

def _open_resource(url_file_stream_or_string, etag, modified, agent, 
        referrer, handlers, usegzip=True, user_headers={}):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    If the etag argument is supplied, it will be used as the value of an
    If-None-Match request header.

    If the modified argument is supplied, it must be a tuple of 9 integers
    as returned by gmtime() in the standard Python time module. This MUST
    be in GMT (Greenwich Mean Time). The formatted date/time will be used
    as the value of an If-Modified-Since request header.

    If the agent argument is supplied, it will be used as the value of a
    User-Agent request header.

    If the referrer argument is supplied, it will be used as the value of a
    Referer[sic] request header.

    If handlers is supplied, it is a list of handlers used to build a
    urllib2 opener.
    """
    if not _open_resource.warned:
        log.debug("Using internal _open_resource.")
        _open_resource.warned = True

    if hasattr(url_file_stream_or_string, "read"):
        return url_file_stream_or_string

    if url_file_stream_or_string == "-":
        return sys.stdin

    if urlparse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp','itms'):
        if not agent:
            agent = USER_AGENT
        # test for inline user:password for basic auth
        auth = None
        if base64:
            urltype, rest = urllib.splittype(url_file_stream_or_string)
            realhost, rest = urllib.splithost(rest)
            if realhost:
                user_passwd, realhost = urllib.splituser(realhost)
                if user_passwd:
                    url_file_stream_or_string = "%s://%s%s" % (urltype, realhost, rest)
                    auth = base64.encodestring(user_passwd).strip()
        # try to open with urllib2 (to use optional headers)
        request = urllib2.Request(url_file_stream_or_string)
        request.add_header("User-Agent", agent)
        if etag:
            request.add_header("If-None-Match", etag)
        if modified:
            # format into an RFC 1123-compliant timestamp. We can't use
            # time.strftime() since the %a and %b directives can be affected
            # by the current locale, but RFC 2616 states that dates must be
            # in English.
            short_weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            months = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                ]
            request.add_header(
                "If-Modified-Since", "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
                    short_weekdays[modified[6]], 
                    modified[2], 
                    months[modified[1] - 1], 
                    modified[0], 
                    modified[3], 
                    modified[4], 
                    modified[5]
                    )
                )
        if referrer:
            request.add_header("Referer", referrer)
        if feedparser.gzip and feedparser.zlib and usegzip:
            request.add_header("Accept-encoding", "gzip, deflate")
        elif feedparser.gzip and usegzip:
            request.add_header("Accept-encoding", "gzip")
        elif feedparser.zlib and usegzip:
            request.add_header("Accept-encoding", "deflate")
        else:
            request.add_header("Accept-encoding", "")
        if auth:
            request.add_header("Authorization", "Basic %s" % auth)
        if feedparser.ACCEPT_HEADER:
            request.add_header("Accept", feedparser.ACCEPT_HEADER)
        for key, value in user_headers.items(): 
            request.add_header(key, value)
        opener = apply(urllib2.build_opener, 
                       tuple([feedparser._FeedURLHandler()] + handlers))
        opener.addheaders = [] # RMK - must clear so we only send our custom User-Agent
        direct = True
        try: 
            fp = opener.open(request)
            # Special code for Python 2.4, which breaks the use of 
            # _FeedURLHandler somehow
            if hasattr(fp, 'code') and fp.code in [301, 302, 303, 307]: 
                dest = fp.info().get('location')
                return _open_resource(dest, etag, modified, agent, referrer, 
                                      handlers, usegzip, user_headers)
            else: 
                return fp
        finally:
            opener.close() # JohnD
    
    # try to open with native open function (if url_file_stream_or_string is a filename)
    try:
        return open(url_file_stream_or_string)
    except:
        pass

    # treat url_file_stream_or_string as string
    log.warn("Unexpectedly tried to open a string? %s", 
            repr(url_file_stream_or_string))
    return feedparser._StringIO(str(url_file_stream_or_string))

_open_resource.warned = False

class MyHTTPPasswordMgrWithDefaultRealm(urllib2.HTTPPasswordMgrWithDefaultRealm):
    """This class band-aids over some quirks in urllib2's password managers.
    Specifically, the HTTPPasswordMgr.find_user_password() method sometimes
    receives an authuri that is missing the protocol designator, "http://".
    When this happens, urlparse.urlsplit() gets confused and bad things happen.
    So we're sneaking in and ensuring that the authuri has "http://", which
    fixes the problem."""
    
    def find_user_password(self, realm, authuri):
        if not authuri.startswith('http://'):
            authuri = 'http://%s' % authuri
        return urllib2.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authuri)
    
class BasicGrabber(GenericGrabber): 
    """Basic grabber. Uses feedparser to help."""
    
    http_proxy_server = None
    http_proxy_port = None
    http_proxy_username = None
    http_proxy_password = None

    #Load me up with passwords that should be available all the time.
    shared_password_mgr = MyHTTPPasswordMgrWithDefaultRealm()
    
    def set_proxy(self_or_class, protocol, server, port, username, password): 
        """Set the proxy server. 
        
        If called on BasicGrabber, this is global to all instances.
        If called on an instance, it isn't."""
        assert protocol == 'http'
        assert (server and port) or (server is None and port is None)
        self_or_class.http_proxy_server = server
        self_or_class.http_proxy_port = port
        self_or_class.http_proxy_username = username
        self_or_class.http_proxy_password = password
        
    set_global_proxy = classmethod(set_proxy)
    
    def __init__(self, what, dest, blocksize=BLOCKSIZE, 
                 etag='', modified='', referrer='', 
                 state=None, offline=False,                 
                 politeness=POLITENESS): 
        """Initialise the BasicGrabber.

        what -- the URL to grab
        dest -- the destination filename or file pointer
        blocksize -- the block size for reads
        etag -- the etag to give the server
        modified -- the last-modification timestamp
        offline -- just return the cached copy

        If dest is a file handle, it is the caller's responsibility 
        to close it. This makes sure StringIO.StringIO instances work. 
        """

        GenericGrabber.__init__(self, what, dest, blocksize)
        if etag: 
            self.warn("etag specified but deprecated")
        if modified: 
            self.warn("modified specified but deprecated")
        self.referrer = referrer
        self.state = state
        self.offline = offline
        self.politeness = politeness
        self.hooks = hooks.HookCollection()
        # Private attributes
        self._began = self._last = time.time()
        self._last_bytes = 0
 
    def _explainDownloadException(self, ex, default=None): 
        """Explain an exception caught during download.
        Returns (trace, reason, useclass).
        """

        trace = False
        useclass = GrabError
        
        if default is None: 
            reason = 'unexpected error %s' % repr(ex)
        else: 
            reason = default

        if isinstance(ex, zlib.error): 
            reason = 'decompression error'
            useclass = GzipError

        elif isinstance(ex, socket.timeout): 
            reason = 'timeout'

        elif timeoutsocket and isinstance(ex, timeoutsocket.Timeout): 
            reason = 'timeout'
        
        elif isinstance(ex, socket.gaierror): 
            reason = 'DNS lookup failure'
        
        elif isinstance(ex, socket.error): 
            try: 
                errno, message = ex.args
                if errno == 10054: 
                    reason = 'connection reset by peer'
                elif errno == 10060: 
                    reason = 'timeout'
                else: 
                    trace = True
                    reason = 'socket.error %d: %s' % (errno, message)
            except ValueError: # unpack tuple of wrong size
                if ex.args == ('timed out',): 
                    reason = 'timeout'
                else: 
                    log.warn("socket.error doesn't have two arguments; got %s", 
                            repr(ex.args))
                    trace = True
                    reason = 'socket.error with args %s' % repr(ex.args)

        elif isinstance(ex, urllib2.URLError): 
            uedefault = 'URLError wrapped around unexpected %s' % (
                repr(ex.reason))
            trace, reason, useclass = self._explainDownloadException(ex.reason, uedefault)
            if reason == uedefault: 
                trace = True

        elif isinstance(ex, IOError): 
            if hasattr(ex, 'args') and ex.args[0] == 2: 
                reason = 'no such file or directory'
            elif hasattr(ex, 'args') and ex.args[0] == 'CRC check failed':
                reason = 'gzip CRC check failure'
                useclass = GzipError
            else: 
                reason = 'unexpected IOError %s' % repr(ex)
                trace = True

        elif isinstance(ex, ValueError):
            if hasattr(ex, 'args'):
                #"AbstractDigestAuthHandler doesn't know about Basic"
                reason = "probably a bad username/password."
                useclass = AuthenticationError
        else: 
            self.exception("This traceback is new to us:")

        return trace, reason, useclass
    
    def _translateUsualDownloadErrors(self, callable, *args, **kwargs): 
        """Call the callable, catching socket.error and other likely 
        exceptions and raise instead the appropriate GrabError."""
        try: 
            return callable(*args, **kwargs)
            
        except Exception, ex: 
            # log.exception("_translateUsualDownloadErrors caught:") 
            trace, reason, useclass = self._explainDownloadException(ex)
            if trace:
                self.exception("Caught %s", reason)
            raise useclass, (reason, ex)

    def _log_cachestate(self, message): 
        statecopy = self.whatstate.copy()
        if statecopy.has_key('content'): 
            statecopy['content'] = '...'
        import pprint
        self.spam("%s: %s", message, pprint.pformat(statecopy))

    def _get_cachestate(self): 
        """Get the cache state."""
        state = self.state
        if state is None: 
            return {}
        self.cachekey = "cache\0%s" % str(urlnorm.normalize(self.what))
        try: 
            gotstate = state.get(self.cachekey, {})
        except (EOFError, pickle.UnpicklingError, cPickle.UnpicklingError), ex: 
            self.warn("Discarding cache state for %s", self.what)
            gotstate = {}
            self._set_cachestate(gotstate)
        self.whatstate = gotstate
        if 1: self._log_cachestate("Fetched cache state")
        return gotstate

    def _set_cachestate(self, whatstate): 
        """Set the cache state."""
        state = self.state
        if state is not None: 
            state[self.cachekey] = whatstate
            self._log_cachestate("Set cache state")
            if hasattr(state, 'sync'): 
                state.sync()

    cache_state = property(_get_cachestate, _set_cachestate, 
            doc="The cache state for `self.what`.")

    def _cflush(self): 
        """Flush the cache with whatstate."""
        self._set_cachestate(self.whatstate)

    def _consider_cache(self): 
        """Consider whether or not to cache."""
        self.etag = self.modified = ''
        self.last_hit_complete = False
        self.is_cached = False
        self.is_cache_complete = False
        self.is_cache_hit = False
        self.cache_headers = None
        self.cache_fp = None

        self.whatstate = whatstate = self.cache_state
        self.use_gzip = whatstate.get('usegzip', True)
        
        if self.whatstate.get('content'): 
            # Stock our attributes
            self.is_cache_complete = whatstate.get('complete', False)
            self.last_hit_complete = self.is_cache_complete
            self.is_cached = True
            self.cache_fp = StringIO.StringIO(whatstate['content'])
            self.cache_headers = headers = whatstate['headers']
            etag = whatstate.get('etag', '')
            modified = whatstate.get('modified', '')
            lastchecked = whatstate.get('checked', '')

            # Print some debugging information
            cinfo = '; '.join(
                    ["%s=%s" % (k, repr(locals()[k])) 
                     for k in ('etag', 'modified', 'lastchecked')]
                    )
            self.debug("Found %s copy in cache. %s", 
                       ['partial', 'complete'][self.is_cache_complete],
                       cinfo)

            # Consider whether it would be impolite to check again
            delta = time.time() - time.mktime(lastchecked)
            if delta < 0: 
                delta = self.politeness
            if self.is_cache_complete and delta < self.politeness: 
                self.debug("We checked only %.2fs ago; forcing offline.", 
                          delta)
                self.offline = True
        else: 
            self.last_hit_complete = whatstate.get('complete', False)
        
    def _cache_hit(self, checked=None): 
        """Return fp, headers for a cache hit."""
        self.is_cache_hit = True
        if checked is not None: 
            self.whatstate['checked'] = checked
            self.cache_state = self.whatstate
        clength = self.cache_headers.get('content-length', '0')
        self.content_size = self._parse_length(clength)
        return self.cache_fp, self.cache_headers, 0L
        
    def _parse_range(self, content_range): 
        """Parse a Content-Range header.
        Returns begin, end, total_length"""

        match = re.match(r"^bytes (\d+)\-(\d+)\/(\d+)$", content_range)
        if match is not None: 
            begin, end, total_length = [int(x) for x in match.groups()]
            return begin, end, total_length

        match = re.match(r"^bytes \*\/(\d+)$", content_range)
        if match is not None: 
            total_length = int(match.groups()[0])
            return 0, total_length, total_length

        if content_range == '0': 
            # Seen on EGC and SDR, but not HTTP compliant
            return 0, 0, 0

        raise ValueError, \
              "Malformed Content-Range header %s" % \
              repr(content_range)

    def _parse_length(self, content_length): 
        # Determine the content-length, as it's quite handy.
        if ',' in content_length: 
            self.debug("Comma found in content-length: %s", content_length)
            content_lengths = content_length.split(',')
            assert len(content_lengths) == 2
            cachemessagesize, size = map(int, content_lengths)
            self.debug("Assuming cache message size %d; "
                      "original content-length %d.", 
                      cachemessagesize, size)
            return size
        else: 
            return int(content_length)

    def _open(self): 
        """Open the source -- whatever we decide that is. :)
        Returns fp, headers."""
        
        # If we're copying from a file to a file, open it and return.
        self.nocopy = False
        what = self.what
        what = self.what.strip()
        if what != self.what: 
            self.warn("The requested URL %s has leading or trailing " \
                      "whitespace.", repr(self.what))
        destfilename = self.destfilename

        if os.path.exists(what): 
            # We're copying a file. 
            # Implication: we don't need to worry about proxy servers. :)
            os.chdir(os.path.split(what)[0])
            fp = urllib.urlopen(os.path.splitdrive(what)[1])
            headers = fp.info()
            if destfilename is not None and os.path.exists(destfilename): 
                if os.path.getsize(destfilename) == os.path.getsize(what): 
                    self.info("Target already exists with right length.")
                    self.nocopy = True
                else: 
                    self.warn("Target exists, but is different length. "\
                              "We will copy again from the beginning.")
            return fp, headers, 0L
        
        # If we hit this point, we're probably opening a remote resource. 
        # The other possibility is a file: URL. Let's pretend that won't 
        # happen for the time being. 



        # If we prefer offline (either because the BasicGrabber was 
        # initialised that way or it would be impolite to hit again so 
        # soon) AND the cached copy is complete, return a cache hit. 
        if self.offline and self.is_cache_complete: 
            self.debug("Using offline copy.")
            return self._cache_hit()

        # Consider the destination file. If it exists, we want to construct 
        # a byte-range request to resume it. 
        request_headers = {}
        
        test_resumability = not self.whatstate.has_key('resumable')
        tested_resumability = False
        if test_resumability and False: ### temporarily disabled
            self.debug("Testing for resumability (rules out cache hits)")
            request_headers['Range'] = 'bytes=0-*'
            tested_resumability = True
            
        if self.whatstate.get('resumable', True) and not self.last_hit_complete: 
            origin = 0 # requires we don't save incompletes on no data rcvd
            if destfilename is not None and os.path.exists(destfilename): 
                origin = os.stat(destfilename)[stat.ST_SIZE]
                self.warn("Destination file exists. "\
                          "Requesting resume from %d bytes.", 
                          origin)
                self.warn("Disabling gzip just in case.")
                self.use_gzip = False
                
            elif self.is_cached: 
                origin = len(self.whatstate.get('content'))
                origin = 0 # uh... TODO: cry.
                #raise NotImplementedError, \
                #        "Can't resume from cache to sio yet."
            if origin: 
                request_headers['Range'] = 'bytes=%d-' % origin
                    
        # If we want to use proxy servers or password-proteced downloads
        # we need to prepare a handler to do so.
        handlers = [urllib2.HTTPBasicAuthHandler(self.shared_password_mgr), \
                    urllib2.HTTPDigestAuthHandler(self.shared_password_mgr)]

        if self.http_proxy_server and self.http_proxy_port:
            url = "%s:%s" % (self.http_proxy_server, self.http_proxy_port)
            self.spam("Adding proxy: %s", url)
            handlers.append(urllib2.ProxyHandler({'http' : url}))                        
            if self.http_proxy_username and self.http_proxy_password:
                # AG: urllib2 is a little quirky, at least in Python 2.3/2.4.
                # ProxyBasicAuthHandler matches the password against the proxy
                # uri, while ProxyDigestAuthHandler matches the password
                # against the target uri.
                # ProxyDigestAuthHandler should be tried last, because
                # it blows out with an exception if the auth method doesn't
                # match.  Happily, ProxyBasicAuthHandler fails quietly so
                # we can try it first.
                passman = MyHTTPPasswordMgrWithDefaultRealm()
                passman.add_password(None, url, self.http_proxy_username, self.http_proxy_password)
                passman.add_password(None, self.what, self.http_proxy_username, self.http_proxy_password)
                self.spam("Adding proxy authentication handlers for: basic, digest")
                handlers.append(urllib2.ProxyBasicAuthHandler(passman)) #Try basic first!
                handlers.append(urllib2.ProxyDigestAuthHandler(passman))

        # We install our own opener in a futile attempt to get proxies 
        # working. This should work: 
        #   urllib2.install_opener(build_opener)
        # ... except feedparser bypasses it, so we need to do this:
        #AG: The custom build_opener interferes with password-protected feeds
        #AG: in Python 2.4.  Our custom password manager,
        #AG: MyHTTPPasswordMgrWithDefaultRealm, seems to fix things so we
        #AG: can probably drop the custom build_opener.
        #urllib2.build_opener = build_opener

        if what.startswith('itms://'):
            handlers.append(itunes.ITMSHandler())
            
        # Let's try to open the target. 
        try: 
            self.spam("Calling _open_resource...")
            fp = self._translateUsualDownloadErrors(
                    _open_resource,
                    what,
                    self.etag, # retrieved from cache
                    self.modified,# retrieved from cache
                    AGENT, # module global
                    self.referrer,
                    handlers, 
                    usegzip = self.use_gzip,
                    user_headers = request_headers)
            headers = fp.info() ###
        except GrabError, ex: 
            if isinstance(ex, GzipError): 
                self.error("Gzip decoding error on open.")
                # That'll now be disabled from inside 
                # _translateUsualDownloadErrors
            if self.is_cache_complete: 
                self.warn("Caught %s whilst opening %s; "\
                         "using cached copy.", ex.message, 
                         what)
                return self._cache_hit()
            else:
                raise

        self.whatstate['checked'] = time.localtime()

        # Check for a cache hit. Even if we have something in the cache, 
        # we should only use it if the web server tells us to. 
        seek = 0L

        content_range = headers.get('content-range')
        if tested_resumability: 
            if content_range is not None: 
                self.debug("Got content-range; download is resumable.")
                self.whatstate['resumable'] = True
            else: 
                self.whatstate['resumable'] = False
            self._cflush() #self.cache_state = self.whatstate # updates
        # Removed: we want these things to persist; I only put this code 
        # in because of a bug which caused resumable to be set False 
        # even if resumability wasn't tested. 
        #else: 
        #    try: 
        #        del self.whatstate['resumable']
        #    except KeyError: 
        #        pass

        self.range_begin = 0
        self.range_end = 0
        self.range_size = 0

        clength = headers.get('content-length', '0')
        size = self.content_size = self._parse_length(clength)
            
        if hasattr(fp, 'status'): 
            self.debug('status: %s', repr(fp.status))
            
            # Switch on the status
            if fp.status == 304: 
                self.debug("Got 304; using cached copy.")
                fp.close()
                return self._cache_hit(checked=time.localtime())
            
            elif fp.status == 206: 
                if content_range is None: 
                    raise GrabError, \
                          "Content-Range header missing on 206 response."
                try:
                    begin, end, total_length = self._parse_range(content_range)
                    self.range_begin = begin
                    self.range_end = end
                    self.range_size = end - begin
                    self.content_size = total_length
                except ValueError, ex: 
                    raise GrabError, ex.args
                seek = begin
                if seek > 0: 
                    self.debug("Got partial response!")
                    self.info("Will resume from %d if we can.", seek)
            
            elif fp.status == 301: # remember the new location
                self.debug("Got 301 response; didn't remember new location "\
                         "%s (was %s)", fp.geturl(), what)

            elif fp.status == 416: # can't satisfy range
                self.warn("The server can't satisfy the requested range.")
                self.info("content-length: %s", repr(headers.get('content-length')))
                self.info("content-range: %s", repr(headers.get('content-range')))
                if content_range is None: 
                    self.whatstate['resumable'] = False
                    self._cflush()
                    raise GrabError, "resume failed; disabling it for next time"
                try:
                    begin, end, total_length = self._parse_range(content_range)
                    if begin == end == total_length == 0: 
                        self.whatstate['resumable'] = False
                        self._cflush()
                        raise GrabError, \
                            "resume failed because the return range was 0;" \
                            "disabling it for next time"
                    self.debug("%d, %d, %d", begin, end, total_length)
                    seek = begin
                    self.range_begin = begin
                    self.range_end = end
                    self.range_size = end - begin
                    self.content_size = total_length
                except ValueError, ex: 
                    raise GrabError, ex.args
            elif fp.status == 404:
                raise GrabError, "The requested URL was not found: %s" % fp.geturl()
            elif fp.status == 401:
                raise AuthenticationError, "Unauthorized.  Re-check your username and password on the Authentication tab."           
        else: 
            self.spam('No status. Assuming 200.')

        if not self.range_size: 
            self.range_end = size
            self.range_size = size

        # Kludge for the iPodder directory, which DOESN'T support 
        # get-if-modified-since, etags, or even give a last-modified 
        # date. :|
        #
        # The checks against cache, last-modified and etag disable 
        # the kludge if the directory server starts issuing headers 
        # that suggest it's cacheable. 
        if what == 'http://www.ipodder.org/discuss/reader$4.opml' \
        and not (headers.has_key('last-modified') \
                 or headers.has_key('etag')) \
        and self.whatstate \
        and self.cache_headers is not None \
        and self.cache_headers['content-length'] == headers['content-length']: 
            self.debug("iPodder directory kludge: the lengths match, "\
                      "so we're assuming it hasn't changed.")
            return self._cache_hit(checked=time.localtime())

        # It's a normal fetch! Return the file pointer and the headers. 
        # First, though, let's delete the old content from the cache: 
        try: 
            del self.whatstate['content']
            self._cflush() # self.cache_state = whatstate # flush
        except KeyError: 
            pass
        return fp, headers, seek
        
    def download(self): 
        """Download the file."""
        # TODO: separate out a catcherrors which calls its arguments and 
        # translates socket.* and URLError et al into GrabErrors.
        #
        # TODO: use that to help use the cached copy on timeouts etc.
        nocopy = False
        what = self.what
        destfilename = self.destfilename

        # If it's an ftp:// or http:// URL, normalise `what`. 
        if urlparse.urlsplit(what)[0].lower() in ['http', 'ftp']: 
            if ' ' in what: 
                self.debug("Re-wrote URL to eliminate spaces.")
            self.what = what = urlnorm.normalize(what)

        self._consider_cache() # prepares atts according to cache
        fp, headers, seek = self._open()
        if hasattr(fp,'status') and fp.status in [301, 302, 303, 307]:
            #Ugly way to send back the new URL in case the calling code
            #wants to re-compute the final destination filename.
            headers['__ipodder_redirected_destination_url'] = fp.geturl()
            
        whatstate = self.whatstate
        size = self.content_size

        try: 
            # Stash the headers where they'll be saved to state later, 
            # even if GrabErrors are caught. That makes sure our resume 
            # attempt will have access to the right etag, modified etc. 
            whatstate['headers'] = headers
            if headers.has_key('last-modified'): 
                whatstate['modified'] = feedparser._parse_date(headers['last-modified'])
            if headers.has_key('etag'): 
                whatstate['etag'] = headers['etag']
            self._cflush()

            if self.is_cache_hit: 
                # If we're cached, what we cached was the ungzipped 
                # content, so it doesn't make much sense to try to 
                # decode it again. 
                #
                # if headers.has_key('content-encoding'): 
                #     del headers['content-encoding'] # that might not work
                pass
                
            else: 
                # If the encoding is gzip... 
                encoding = headers.get('content-encoding', '')
                self.debug("content-encoding: %s", encoding)
                if encoding == 'gzip': 
                    # Figure out the file pointer and wrap it with 
                    # a GzipFile decompressor instance. 
                    if isinstance(fp, feedparser.urllib.addbase): 
                        fp = fp.fp
                    self.debug("gzip decoding %s", repr(fp))
                    decompressor = GzipFile(mode='rb', fileobj=fp)
                    fp = decompressor

            # Perform the actual copy. 
            if not self.nocopy: 
                #if seek: 
                #    log.warn("Resumes disabled because seek doesn't seem "\
                #             "to be working on Windows.")
                #    seek = 0
                whatstate['complete'] = False
                whatstate['partial'] = 0
                self._cflush()
                #self.cache_state = whatstate # flush
                bytes = 0 
                if self.destfp is not None: 
                    destfp = self.destfp
                    if seek: 
                        self.debug("Seeking destination file handle to %d...", seek)
                        destfp.seek(seek)
                        bytes = seek ### TODO: if we're getting our length
                                     ### from the headers, and that is giving
                                     ### us the length of the range rather 
                                     ### than the length of the file, that'll 
                                     ### explain the over% problem
                else: 
                    if seek: 
                        self.debug("Opening %s for append...", destfilename)
                        destfp = file(destfilename, 'r+b')
                        self.debug("Seeking to %d...", seek)
                        destfp.seek(seek)
                        bytes = seek ### see above
                    else: 
                        destfp = file(destfilename, 'wb')
                teefp = StringIO.StringIO() # to take a copy
                self.progress(bytes, size)
                lastpartial = time.time()
                try:
                    while 1: 
                        block = self._translateUsualDownloadErrors(fp.read, self.blocksize)
                        if not block: 
                            break
                        if self.stopflag.isSet(): 
                            self.warn("Download aborted: %s", self.what)
                            teefp = None # don't cache it
                            self.doneflag.set()
                            raise UserAborted, "download aborted"
                            # TODO: delete the dest file? what else?
                        bytes += len(block)
                        whatstate['partial'] = bytes
                        if time.time() - lastpartial > 10: 
                            lastpartial = time.time()
                            self._cflush() # self.cache_state = whatstate # flush
                        self.progress(bytes, size)
                        try: 
                            destfp.write(block)
                        except IOError, ex: 
                            if hasattr(ex, 'args') and ex.args[0] == 28: 
                                raise GrabError, \
                                        ("Can't write; out of disk space.", 
                                         ex)
                            else: 
                                self.exception("Unexpected IOError on write.")
                                raise GrabError, ("Unexpected IOError", ex)
                        # If we're still small enough, keep taking a copy
                        if teefp is not None: 
                            if bytes > CACHEMAX: 
                                self.debug("Size exceeds CACHEMAX (%d > %d); "\
                                          "stopping copy.", size, CACHEMAX)
                                teefp = None
                            else: 
                                teefp.write(block)
                except: 
                    if destfp is not None: 
                        self.debug("Forcing destination file handle closed.")
                        destfp.close()
                    raise
            whatstate['complete'] = True
            fp.close()

            # Update the cache content?
            if not (self.is_cache_complete or self.state is None or teefp is None): 
                whatstate['content'] = teefp.getvalue()
            # ... and flush it. 
            self._cflush() # self.cache_state = whatstate
                
            self.done()

            return destfilename, headers
            
        except KeyboardInterrupt: # not likely in a thread, but what the hey.
            raise
        
        except GrabError, ex: # _translateUsualDownloadErrors caught it
            if isinstance(ex, GzipError): 
                self.error("Gzip decoding error on read; "\
                           "disabling gzip for this feed.")
                whatstate['usegzip'] = False
            if whatstate.has_key('content'): 
                del whatstate['content']
            self.cache_state = whatstate
            raise

        except Exception, ex:
            self.exception("Problem downloading %s", what)
            raise GrabError, ("unexpected error %s" % repr(ex), ex)

    def done(self, complete=True): 
        """Declare we're done. Special one-file version."""
        GenericGrabber.done(self, complete) # call our parent
        self.hooks.get('report-finished-file')(self.destfilename, self.info)
     
    def progress(self, bytes, size):
        """Update our status variables."""
        mb = bytes / 1048576.0
        delta_b = self._last_bytes - bytes
        self._last_bytes = bytes

        now = time.time()
        delta_t = now - self._last
        self._last = now

        # After calculating delta_t and delta_b, I'm going to ignore them because 
        # I have no idea how short the durations will be. Instead, I'll go for the 
        # more boring "progress so far over time so far" number. 

        duration = now - self._began
        if duration > 1: 
            if hasattr(self,"range_begin"):
                rate = (bytes-self.range_begin) / float(duration) 
            else:
                rate = bytes / float(duration)
        else: 
            rate = 0.0

        if rate and size: 
            left = size - bytes
            self.eta = left / rate
        else: 
            self.eta = 0 # use as a sentinel: no idea :)

        self.upload_rate = 0.0
        self.upload_mb = 0.0
        self.download_rate = rate
        self.download_mb = mb
        
        ###
        if size > 0: 
            self.fraction_done = bytes / float(size)
        else: 
            self.fraction_done = random.random()

        self.hooks.get('updated')() # tell others to check our state vars

# Terminology changes from 1.1:
# 
# * Instead of a TorrentMetaInfoFile or whatever it was, we're using a 
#   TorrentFile. I suspect it should just be a Torrent now that I think 
#   about it. TODO: stop thinking about it. 
# 
# * The previous version of the code in TorrentFile.__init__ used 
#   'metainfo' a lot. I'm calling it 'response', just like the BitTorrent 
#   internals. 
#
# TODO: take off the read-only bit on finished files so we can change 
# their ID3 information, so that the user can delete them, etc. 

class TorrentFile(threads.SelfLogger):
    """Class to keep track of BitTorrent file information."""

    def __init__(self, responseorfilename): 
        """Initialise the TorrentFile."""

        object.__init__(self)
        threads.SelfLogger.__init__(self)

        # BitTorrent.download.download() can download the torrent file all 
        # by itself. I think the only reason we're doing it ourselves is 
        # so we can figure out the length and the filename. 
        # 
        # TODO: consider whether we could double-check to make sure that 
        # nobody is faking nasty paths. 
        # 
        # TODO: definitely use this information to make sure there's 
        # enough disk space for the maneouvre. 
        # 
        # TODO: intelligently handle multiple-file torrents, with users 
        # being able to choose whether to unpack each torrent's files 
        # into a subdirectory for that torrent, or to unpack each 
        # torrent into the same directory (which might also make sense). 
        # That'd also be a good time to ponder how to handle items with 
        # multiple enclosure tags. 

        try: 
            response = responseorfilename
            tinfo = bdecode(response)
            self.responsefilename = None
        except ValueError: 
            infofd = open(responseorfilename, 'rb')
            response = infofd.read()
            infofd.close() # explicit close seen as better
            try:
                tinfo = bdecode(response) 
            except ValueError: 
                self.error("Couldn't decode BitTorrent response file %s",
                          responseorfilename)
                self.error("Response was: %s", repr(response))
                raise
            self.responsefilename = responseorfilename

        try: 
            check_message(tinfo)
            self.response = response
        except ValueError, ex: 
            self.error("Couldn't decode BitTorrent response file: %s", 
                      str(ex))
            raise # Force whomever is initialising us to deal with it. 

        self.announce = tinfo['announce'] # not used?
        info = tinfo['info']
        # self.info_hash = sha.new(bencode(info)).digest() # also not used?
        self.name = info['name']

        if info.has_key('length'):
            self.length = info['length']
        else:
            raise AssertionError, "can't handle multi-file torrents"
            # TODO: wade through real examples and figure out what this 
            # code is trying to accomplish. Okay, so it's calculating 
            # a length, but what's the path variable for? 
            #
            # TODO: decide how to correctly handle torrents that download 
            # multiple files, such as those whopping huge ones from 
            # LegalTorrents. LegalTorrents also deliver zip files, which 
            # also make our life hard. 
            length = 0
            for file in info['files']:
                path = ''
                for item in file['path']:
                    if (path != ''):
                      path = path + "/"
                    path = path + item
                length += file['length']
            self.length = length

        #piece_length = info['piece length'] # also not used?
        #piece_number, last_piece_length = divmod(self.length, piece_length)

    def __repr__(self): 
        """Issue a string representation of the TorrentFile."""
        hexid = '%08x' % id(self)
        atts = ['length', 
                #'info_hash',
                'announcer',
                'length',
                'name',
                'responsefilename']
        attdict = {}
        for att in atts: 
            try: 
                attdict[att] = getattr(self, att)
            except AttributeError: 
                pass
        attrep = ', '.join(["%s=%s" % (att, val)
                            for att, val in attdict.items()])
        return "<%s.%s instance at 0x%s with attributes %s>" % (
                self.__module__, 
                self.__class__.__name__, 
                hexid.upper,
                attrep)

class TorrentGrabber(GenericGrabber): 
    """BitTorrent downloader thread.
    
    Not interested in multi-threading? Call .run() instead of .start()."""
    
    # TODO: make this match GenericGrabber :)

    def __init__(self, what, destfilename, blocksize=BLOCKSIZE, keepserving=False, generosity=0.2, btoptions=[]): 
        """Initialise the TorrentGrabber.
        
        what -- a TorrentFile object
        destfilename -- obvious
        blocksize -- not so obvious
        keepserving -- caller takes full responsibility for setting .done
        generosity -- stick around for longer to upload; 0.0 - 1.0
        """

        assert isinstance(destfilename, basestring), \
               "Torrent grabbing to file like objects is not supported."
        GenericGrabber.__init__(self, what, destfilename, blocksize)

        self.name = os.path.basename(what.name)
        #threading.Thread.__init__(self, name = self.name)
        self.hooks = hooks.HookCollection()
        self.filefunc_called = False
        self.keepserving = keepserving
        self.generosity = generosity
        self.btoptions = btoptions
        self.seeding = False

        # Declare a status map for both __init__ and statusfunc
        self.statusMap = {
            'activity': ('last_activity', ''),
            'upRate': ('upload_rate', 0.0), 
            'upTotal': ('upload_total', 0.0), 
            'fractionDone': ('fraction_done', 0.0),
            'downRate': ('download_rate', 0.0), 
            'downTotal': ('download_total', 0.0), 
            'timeEst': ('time_remaining', 0), # not sure about this one
            }

        # Set some defaults
        for statuskey, settings in self.statusMap.items(): 
            att, default = settings
            setattr(self, att, default)

    def errorfunc(self, message):
        """Issue an error on behalf of BT.d.d."""
        self.error("%s thread reports: %s", self.name, message)
        raise GrabError, message

    def statusfunc(self, statusdict): 
        """Called by BT.d.d to indicate its status."""
        for key, value in statusdict.items(): 
            self.spam("%s thread reports: %s: %s", 
                      self.name, key, value)
            settings = self.statusMap.get(key)
            if settings is not None: 
                att = settings[0]
                setattr(self, att, value)
        self.hooks.get('updated')() # tell others to check our state vars

        # If we're seeding, see if we need to stop: 
        if self.seeding and self.generosity>0.0: 
            self.spam("Checking to see if we've been generous enough...")
            if time.time() > self.end:
                self.debug("Stopping because we've seeded for long enough.")
                self.stopflag.set()
            elif self.upload_total >= self.upload_target: 
                self.debug("Stopping because we've seeded enough.")
                self.stopflag.set()
        
    def finfunc(self): 
        """Called by BT.d.d when it's done."""
        # TODO: this is an indication of download success! 
        # report back so we can add to playlists, etc!
        # (good use for hooks, that... though we might have 
        #  to notify completion on multiple files)
        self.debug("BitTorrent.download.download says it's done.")
        if self.keepserving or self.generosity>0: ###
            if self.generosity: 
                if self.upload_total > 0: 
                    now = time.time()
                    duration = now - self.begin
                    newduration = duration * self.generosity
                    self.end = now + newduration
                    self.upload_target = self.download_total * (1.0+self.generosity)
                    if self.upload_target < self.download_total: 
                        self.debug("We'll keep running for another %.1f hours " \
                                   "or until we've uploaded %.1fMB total "
                                   "(we've sent %.1fMB so far)", 
                                   newduration/3600.0, 
                                   self.upload_target, 
                                   self.upload_total)
                        self.seeding = True
                    else: 
                        self.debug("We've already uploaded at least %.1fMB, " \
                                   "which satisfies our generosity target " \
                                   "of %.1fMB.", self.upload_total, 
                                   self.upload_target)
                else: 
                    self.debug("There's no point trying to be generous; we " \
                               "didn't manage to upload anything during " \
                               "the download.")
        if not self.seeding: 
            self.stopflag.set()
        # TODO: self.hooks.get('report-finished-file')(filename,fakeheaders) for each
        self.done()
        
    def filefunc(self, name, length, saveas, isdir):
        """Decide where to put the downloaded files. 
        
        Called by BT.d.d with the following arguments:

        name -- response['info']['name']
        length -- file length or total file length
        saveas -- BT's configured saveas target
        isdir -- False for single file, True for multiple files

        BT's behaviour with isdir true is a little unusual: if you hand 
        it an existing directory with none of the torrent's named files 
        in it, it'll create a subdirectory in it to put the files into. 
        If just one of the files exist, it won't create a subdirectory. 
        Your only clue as to what happened is pathfunc getting called.

        The GOOD news is that resumption is pretty much automatic.
        """
        if isdir: 
            self.warn("iPodder's handling of torrents with multiple "\
                      "files is a little primitive. Please let us "\
                      "know of any problems.")
        return saveas

    def pathfunc(self, target): 
        """Called by BT to reveal the newly created directory it'll be 
        downloading files into. Only called for torrents with multiple 
        files. See also the documentation for filefunc."""
        self.info("Multiple files will be put in: %s", target)
        # TODO: something more useful than that

    def paramfunc(self, params): 
        """Called by BT.d.d to let us know how we can change some key 
        controls on the fly."""
        pass
        # TODO: make good use of
        # 'max_upload_rate': change_max_upload_rate(<int bytes/sec>)
        # 'max_uploads': change_max_uploads(<int max uploads>)
        # 'listen_port': int
        # 'peer_id': string
        # 'info_hash': string (why calculate it ourselves?)
        # 'start_connection': start_connection((<string ip>, <int port>), <peer id>)
        
    # This was being called with: 
    #
    #   url = enclosure url, 
    #   file = destination filename
    #   maxUploadRate = 0 (unlimited)
    #   torrentmeta = the torrent meta bit thingy
    #
    # Interestingly, no attempt is made to re-use the downloaded torrent 
    # file; BitTorrent.download.download() was having to do it *again*. 
    # How droll. It's weird because we can pass --responsefile as easily 
    # as we can pass --url... 
    
    def download(self): 
        """Perform the download. Called by run()."""
        # TODO: user-configurable  from keeping seedingtimeouts
        # TODO: user-configurable upload rate limits
        self.begin = time.time()
        responsefilename = self.what.responsefilename
        if responsefilename is None: # only likely during testing, but...
            rawfd, responsefilename = tempfile.mkstemp('.torrent')
            self.debug("Saving raw response to temporary file %s", 
                        responsefilename)
            fd = os.fdopen(rawfd, 'wb')
            fd.write(self.what.response)
            fd.close()
            delete_responsefile = True
        else: 
            delete_responsefile = False
            
        try: 
            params = ['--responsefile', responsefilename,
                      #'--max_upload_rate', maxUploadRate, 
                      '--saveas', self.destfilename,
                      '--timeout', 60.0,
                      '--timeout_check_interval', 10] + self.btoptions

            download.download(
                    params, 
                    self.filefunc, 
                    self.statusfunc, 
                    self.finfunc, 
                    self.errorfunc,
                    self.stopflag, # set to stop BitTorrent from keeping seeding
                    80, # used to format complaint to errorfunc if no params
                    pathFunc = self.pathfunc, 
                    paramfunc = self.paramfunc)

            if self.fraction_done < 1:
                #download.download() completed because the stopflag was set.
                self.warn("BitTorrent aborted: %s", self.what)
                self.doneflag.set() #prevents setting self.complete to True
                raise UserAborted, "download aborted"            

        finally:
            if delete_responsefile: 
                try: 
                    self.debug("Deleting temporary response file %s", 
                              responsefilename)
                    os.unlink(responsefilename)
                except OSError, ex:
                    pass

if __name__ == '__main__': 
    import BaseHTTPServer
    import SimpleHTTPServer
    import mimetypes
    import shutil
    import os
    import unittest
    import random
    import Queue
    import md5

    TESTPORT = 58585
    TRACKPORT = 47474

    logging.basicConfig()
    log.setLevel(logging.DEBUG)

    def yield_random_content(length): 
        """Build some random content of the required length."""
        m = md5.new()
        blocksize = 64*1024
        while length: 
            bytes = []
            size = min(blocksize, length)
            m.update(chr(random.randint(0, 255)))
            block = m.digest() * (blocksize/16 + 1)
            yield block[:size]
            #for idx in range(0, size, 16): 
            #    bytes.append(m.digest())
            #yield ''.join(bytes)[:size]
            #length -= size
            #bytes = []
            #for idx in range(size): 
            #    bytes.append(chr(random.randint(0,255)))
            #yield ''.join(bytes)
            length -= size

    def write_random_content(fd, length): 
        """Write random content to an open file."""
        for block in yield_random_content(length):
            fd.write(block)
        
    def random_content(length): 
        """Return random content.""" 
        sio = StringIO.StringIO()
        write_random_content(sio, length)
        return sio.getvalue()

    class RandomContentTester(unittest.TestCase): 
        """It always pays to test your test code, too."""
        def test_random_content(self): 
            """Test our ability to generate random content."""
            lengths = [0, 1, 2047, 2048, 2049, 8000, 12000, 100000]
            for length in lengths: 
                log.debug("Checking random_content(%d)", length)
                content = random_content(length)
                assert len(content) == length

    class GzipFileTester(unittest.TestCase): 
        """Test the new GzipFile object."""
        def test_gzipfile(self): 
            # Prepare the gzipped value
            copy_of_zipper_input = StringIO.StringIO()
            zipper_output = StringIO.StringIO()
            zipper = gzip.GzipFile(mode='wb', fileobj=zipper_output)
            for block in yield_random_content(32*1024): 
                copy_of_zipper_input.write(block)
                zipper.write(block)
            zipper.close()
            content = copy_of_zipper_input.getvalue()
            zippedcontent = zipper_output.getvalue()
            #log.info("zipped content looks like: %s", repr(zippedcontent[:32]))
            # Now read it back
            unzipper_input = StringIO.StringIO(zippedcontent)
            #log.info("header check: %s", repr(unzipper_input.read(2)))
            unzipper_input = StringIO.StringIO(zippedcontent)
            unzipper = GzipFile(mode='rb', fileobj=unzipper_input)
            unzipped_content = unzipper.read() # get all of it
            assert content == unzipped_content
            
    # This isn't quite a mock object, but it's pretty close. 

    class GrabberTestFakeFile(object): 
        """A fake file for Grabber testing."""

        def __init__(self, 
                     content = '', # content
                     headers = {}, # overrides to default headers
                     code = None, # overrides to code
                     message = None): # overrides to message
            self.content = content
            self.headers = headers
            self.code = code
            self.message = message
            
    class GrabberTestServer(threads.SelfLogger, BaseHTTPServer.HTTPServer): 
        """A test server for Grabbers."""
        
        def __init__(self, server_address, RequestHandlerClass): 
            """Initialise the test server."""
            BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
            threads.SelfLogger.__init__(self)
            self.name, self.port = server_address
            self.__contents = {}
            self.stopflag = threading.Event()
            self.doneflag = threading.Event()
            self.readyflag = threading.Event()
            self.promptqueue = Queue.Queue()
            
        def clear(self): 
            self.debug("Clearing contents...")
            server_address = (self.name, self.port)
            # Don't # self.stop()
            BaseHTTPServer.HTTPServer.__init__(self, server_address, GrabberTestRequestHandler)
            self.__contents = {} 

        def __setitem__(self, key, value): 
            self.__contents[key] = value

        def __getitem__(self, key): 
            return self.__contents[key]

        def get(self, key, default=None): 
            return self.__contents.get(key, default)
            
        def add(self, key, **kw): 
            assert key[:1] == '/'
            self.debug("Added fake file %s", key)
            self[key] = GrabberTestFakeFile(**kw)

        def prompt(self, count=1): 
            """Prompt the GrabberTestServer to serve count requests."""
            self.debug("prompted to serve %d request(s)", count)
            for idx in range(count): 
                self.promptqueue.put(None)
            # self.debug("now waiting for %d request(s)", self.promptqueue.qsize())
            self.readyflag.wait()
            self.readyflag.clear()

        def serve_forever(self):
            """Handle one request at a time until doomsday."""
            while not self.stopflag.isSet():
                try: 
                    prompt = self.promptqueue.get(True, 1)
                    self.debug("waiting to serve a request.")
                    self.readyflag.set()
                    self.handle_request()
                except Queue.Empty, ex: 
                    pass # loop around again
            self.debug("stopped.")
            self.server_close()
            self.doneflag.set()

        def stop(self, wait=True): 
            """Ask us to stop. Assumption: you're calling from another thread."""
            self.debug("asking the test server to stop...")
            self.stopflag.set()
            self.debug("asked.")
            if wait: 
                self.debug("waiting...")
                self.doneflag.wait()

    class GrabberTestRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler): 
        server_version = "iPodderGrabberTester/1.0"
        protocol_version = "HTTP/1.0"

        def __init__(self, request, client_address, server): 
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
            self.contents = {}
            
        def send_head(self):
            """Common code for GET and HEAD commands.

            This sends the response code and MIME headers.

            Return value is either a file object (which has to be copied
            to the outputfile by the caller unless the command was HEAD,
            and must be closed by the caller under all circumstances), or
            None, in which case the caller has nothing further to do.

            """
            fake = self.server.get(self.path)
            if fake is None: 
                self.send_error(404)
                return None

            code = fake.code
            if code is None: 
                code = 200

            message = fake.message # None => default

            ctype = self.guess_type(self.path)
            headers = {
                "Content-Type": ctype, 
                "Content-Length": len(fake.content)
                }
            headers.update(fake.headers)
            
            self.send_response(code, message)
            for key, value in headers.items(): 
                self.send_header(key, value)
            self.end_headers()

            return StringIO.StringIO(fake.content)

        extensions_map = mimetypes.types_map.copy()
        extensions_map.update({
            '.torrent': 'application/bittorrent',
            '.tor': 'application/bittorrent' # cheaty!
            })

    class BasicGrabberTests(unittest.TestCase): 
        def setUp(self): 
            addrinfo = ('', TESTPORT)
            self.httpd = GrabberTestServer(addrinfo, GrabberTestRequestHandler)
            self.tempdir = tempfile.mkdtemp('.tests', 'ipodder.grabber.')
            log.debug("Temporary directory is %s", self.tempdir)
            self.httpd_thread = httpd_thread = threads.OurThread(target=self.httpd.serve_forever)
            httpd_thread.setDaemon(True)
            log.debug("Starting HTTP daemon for test...")
            httpd_thread.start()

        def tearDown(self): 
            log.debug("Removing temporary directory %s...", self.tempdir)
            shutil.rmtree(self.tempdir, True, 
                    lambda fun, path, exc_info: \
                           log.error("%s can't delete %s: %s", fun, path, exc_info))
            self.httpd.stop(wait=False)
            log.debug("Waiting for httpd thread to terminate...")
            self.httpd_thread.join()

        def prep(self, filename, prompt=1, *a, **kw): 
            self.httpd.add("/%s" % filename, *a, **kw)
            if prompt: 
                self.httpd.prompt(prompt)
            return 'http://127.0.0.1:%s/%s' % (TESTPORT, filename)

        def tempify(self, filename): 
            return os.path.join(self.tempdir, filename)
            
        def test_grab1(self): 
            url = self.prep('rss.xml', content='This is a test')
            bg = BasicGrabber(url, self.tempify('rss.xml'))
            bg()

        def test_spaces(self):
            content = 'Hopefully, this spaces test will work.'
            url = self.prep('filename%20with%20spaces.xml', content=content)
            import urlparse, urllib2
            scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
            path = urllib2.unquote(path)
            url = urlparse.urlunsplit((scheme, netloc, path, query, fragment))
            target = self.tempify('filename with spaces.xml')
            bg = BasicGrabber(url, target)
            bg()
            assert file(target, 'rb').read() == content

        def test_grabmany(self):
            success = 0
            target = 10
            for i in range(target):
                try: 
                    self.test_grab1()
                    success += 1
                except GrabError: 
                    pass
            assert success == target, "%d < %d" % (success, target)

        def test_proxy1(self): 
            #raise AssertionError, "Not safe at all."
            content = "This is a test."
            url = self.prep('rss.xml', content=content)
            bg = BasicGrabber(url, self.tempify('rss.xml'))
            bg.set_proxy('http', '127.0.0.1', 3128)
            bg()

        def test_fp(self): 
            content = "This is a test."
            url = self.prep('rss.xml', content=content)
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio)
            bg()
            assert sio.getvalue() == content
            sio.close()

        def make_gzipped_content(self, maxlength=32*1024, minlength=1*1024): 
            # Prepare the gzipped value
            copy_of_zipper_input = StringIO.StringIO()
            zipper_output = StringIO.StringIO()
            zipper = gzip.GzipFile(mode='wb', fileobj=zipper_output)
            length = random.randint(minlength, maxlength)
            sofar = 0
            for block in yield_random_content(length): 
                copy_of_zipper_input.write(block)
                zipper.write(block)
            zipper.close()
            content = copy_of_zipper_input.getvalue()
            zippedcontent = zipper_output.getvalue()
            return content, zippedcontent
            
        def test_gzip(self): 
            content, zippedcontent = self.make_gzipped_content()
            #log.info("zipped content looks like: %s", repr(zippedcontent[:32]))
            url = self.prep('rss.xml', content=zippedcontent, headers={'Content-Encoding':'gzip'})
            # Grab it and check it
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio)
            bg()
            assert sio.getvalue() == content
            sio.close()
                    
        def test_redirect(self): 
            content = random_content(32*1024)
            # If you prep twice and prompt once each time, the testing framework 
            # will hang for some reason. So, I prep once without prompting and 
            # then prep and prompt twice. 
            url = self.prep('rss.xml', content=content, prompt=0)
            url2 = self.prep('redirect.xml', content="The redirect wasn't processed.", 
                    code=302, message="fnord", headers={'Location': url}, prompt=2)
            # Grab it and check it
            sio = StringIO.StringIO()
            bg = BasicGrabber(url2, sio)
            bg()
            value = sio.getvalue()
            assert value == content, value
            sio.close()

        def test_multiple_redirects(self): 
            content = random_content(32*1024)
            TIMES = 5
            
            url = self.prep('rss.xml', content=content, prompt=0)
            prompt = 0
            for i in range(1, TIMES+1): 
                if i == TIMES:
                    prompt = TIMES+1
                else: 
                    prompt = 0
                url = self.prep('redirect%i.xml' % i, content="Redirect %d" % i, 
                                code=302, message="Redirect %d" % i, 
                                headers = {'Location': url}, prompt=prompt)
            #
            #url2 = self.prep('redirect.xml', content="The redirect wasn't processed.", 
            #        code=302, message="fnord", headers={'Location': url}, prompt=0)
            #url3 = self.prep('redirect2.xml', content="The redirect wasn't processed.", 
            #        code=302, message="fnord", headers={'Location': url2}, prompt=3)
            # Grab it and check it
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio)
            bg()
            value = sio.getvalue()
            assert value == content, value
            sio.close()

        def test_cache(self): 
            content = random_content(random.randint(1024,CACHEMAX/2))
            log.debug("Content size: %d", len(content))
            headers = {
                'Etag': "haberdashery", 
                'Last-Modified': 'Mon, 29 Nov 2004 10:30:21 GMT'
                }
            url = self.prep('rss.xml', content=content, headers=headers)
            sio = StringIO.StringIO()
            state = {}
            bg = BasicGrabber(url, sio, state=state)
            fn, headers = bg()
            
            # Check the state object. This technique is sometimes called 
            # "Mock objects", but given that our state database is just 
            # a disk-based dict this hardly warrants the fancy term. 
            #state[state.keys()[0]]['content'] = '(stuff)'
            #import pprint
            #pprint.pprint(state)
            keys = state.keys()
            assert len(keys) == 1
            cstate = state[keys[0]]
            for key in ['checked', 'content', 'etag', 'headers', 'modified']: 
                assert cstate.has_key(key)

            # Fix the fake object to return a 304 with no content.
            self.httpd.clear()
            url = self.prep('rss.xml', 
                            content = 'Should really be empty.', 
                            code = 304, 
                            message = 'Not changed.', 
                            headers = headers)
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio, state=state)
            fn, headers = bg()

            # Make sure it got grabbed properly. 
            assert sio.getvalue() == content, sio.getvalue()
            #log.info("headers: %s", headers)

        def test_nocache_big(self): 
            raise NotImplementedError
        
        def test_cache_with_gzip(self): 
            while 1: 
                content, zippedcontent = \
                    self.make_gzipped_content(minlength=CACHEMAX-1024, maxlength=CACHEMAX-1)
                if len(zippedcontent) > CACHEMAX: 
                    log.debug("Whups! Zipped content too big (%d). "\
                              "Looping...", len(zippedcontent))
                else: 
                    break
            
            log.debug("Content size: %d", len(content))
            headers = {
                'Etag': "haberdashery", 
                'Last-Modified': 'Mon, 29 Nov 2004 10:30:21 GMT',
                'Content-Encoding': 'gzip'
                }
            url = self.prep('rss.xml', content=zippedcontent, headers=headers)
            sio = StringIO.StringIO()
            state = {}
            bg = BasicGrabber(url, sio, state=state)
            fn, headers = bg()
            assert sio.getvalue() == content
            
            #assert len(state.keys()) == 1, repr(state)
            #state[state.keys()[0]]['content'] = '(stuff)'
            #import pprint
            #pprint.pprint(state)
            
            # Fix the fake object to return a 304 with no content.
            self.httpd.clear()
            url = self.prep('rss.xml', 
                            content = 'Should really be empty.', 
                            code = 304, 
                            message = 'Not changed.', 
                            headers = headers)
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio, state=state)
            fn, headers = bg()

            # Make sure it got grabbed properly. 
            assert sio.getvalue() == content, sio.getvalue()
            #log.info("headers: %s", headers)

        def test_offline(self): 
            content = "This is a test."
            headers = {
                'Etag': "haberdashery", 
                'Last-Modified': 'Mon, 29 Nov 2004 10:30:21 GMT'
                }
            state = {}
            url = self.prep('rss.xml', content=content, 
                            headers=headers)
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio, state=state)
            bg()
            assert sio.getvalue() == content
            # Without an extra prompt, this will hang unless offline works. 
            sio = StringIO.StringIO()
            bg = BasicGrabber(url, sio, state=state, offline=True)
            bg()
            assert sio.getvalue() == content, sio.getvalue()

        def test_resume(self): 
            # Prepare the content
            content = random_content(random.randint(1024*256,1024*384))
            half = content[:int(len(content)/2)]
            log.debug("Content length %d", len(content))
            state = {}
            filename = 'foo.mp3'
            destpath = self.tempify(filename)
            url = self.prep(filename, content=content)
            
            # Create a BasicGrabber and hook 'updated' with something to 
            # stop it half way. 
            bg = BasicGrabber(url, destpath, state=state)
            def stopper(): 
                #log.debug("Stopper called at %.2fMB", bg.download_mb)
                half_mb = len(half)/1048576.0
                stopper._last_bytes = bg._last_bytes # abstraction violation!
                if bg.download_mb >= half_mb:
                    log.debug("Half way point reached; aborting download.")
                    bg.stop(wait=False)
            def check_download_statistics(): 
                assert 0 <= bg.fraction_done <= 1
            bg.hooks.add('updated', check_download_statistics)
            bg.hooks.add('updated', stopper)

            # Download half the file. 
            try: 
                bg()
            except UserAborted: 
                pass

            secondhalf = content[stopper._last_bytes:]
            # Check a few things
            assert len(state) == 1
            whatstate = state[state.keys()[0]]
            partial = whatstate['partial']
            assert partial > 0
            log.debug("whatstate['partial'] == %d", partial)

            # Create a new BasicGrabber and run it. 
            range = 'bytes %d-%d/%d' % (
                stopper._last_bytes, len(content), len(content)
                )
            headers = {
                'Content-Range': range,
                'Content-Length': len(secondhalf),
                }
            url = self.prep(filename, content=secondhalf, 
                    code=206, headers=headers)
            log.debug("create bg2...")
            bg2 = BasicGrabber(url, destpath, state=state)

            # hook the new grabber to double-check something
            def check_resume_statistics(): 
                assert 0 <= bg2.fraction_done <= 1
            bg2.hooks.add('updated', check_resume_statistics)

            # Finally...
            log.debug("... and run it.")
            bg2()

            # Check the destination's contents.
            results = file(destpath, 'rb').read()
            assert len(results) == len(content), "%d != %d" % (len(results), len(content))
            assert results == content
            
    class TorrentGrabberTestTracker(threads.SelfLogger): 
        def __init__(self, dfile, servedir, **kwargs): 
            """Initialise the tracker."""
            threads.SelfLogger.__init__(self)
            self.debug("initialising...")
            rawconfig = { 'port': TRACKPORT,
                          'dfile': dfile, 
                          #'allowed_dir': servedir,
                          'parse_allowed_interval': 1 }
            rawconfig.update(kwargs)
            self.args = []
            for key, value in rawconfig.items(): 
                self.args.extend(['--%s' % key, value])
            self.config, files = track.parseargs(self.args, track.defaults, 0, 0)
            # files is ignored in BitTorrent.track.track(), too. 
            self.stopflag = threading.Event()
            self.doneflag = threading.Event()
               
        def __call__(self): 
            """Run the tracker."""
            config = self.config
            r = track.RawServer(self.stopflag, 
                                config['timeout_check_interval'], 
                                config['socket_timeout'])
            t = track.Tracker(config, r)
            r.bind(config['port'], config['bind'], True)
            self.debug("started.")
            r.listen_forever(track.HTTPHandler(t.get, 
                config['min_time_between_log_flushes']))
            t.save_dfile()
            self.debug("shut down.")
            self.doneflag.set()
            
        def stop(self): 
            """Ask the tracker to stop."""
            self.stopflag.set()
            self.debug("waiting for shutdown...")
            self.doneflag.wait()
       
    class TorrentGrabberTests(unittest.TestCase): 
        def __init__(self, *a, **kw): 
            unittest.TestCase.__init__(self, *a, **kw)
            # TODO: figure out how to re-use servers or kill ports

        def setUp(self): 
            addrinfo = ('', TESTPORT)
            self.tempdir = tempfile.mkdtemp('.tests', 'ipodder.grabber.')
            self.servedir = os.path.join(self.tempdir, 'serve')
            self.grabdir = os.path.join(self.tempdir, 'consume')
            self.dfile = os.path.join(self.tempdir, 'dfile.txt')
            os.mkdir(self.servedir)
            os.mkdir(self.grabdir)
            log.debug("Temporary directory is %s", self.tempdir)
            self.tracker = TorrentGrabberTestTracker(self.dfile, self.servedir)
            self.tracker_thread = tracker_thread = threads.OurThread(
                    target = self.tracker)
            tracker_thread.setDaemon(True)
            log.debug("Starting tracker for test...")
            tracker_thread.start()
            self.httpd = GrabberTestServer(addrinfo, GrabberTestRequestHandler)
            self.httpd_thread = httpd_thread = threads.OurThread(target=self.httpd.serve_forever)
            httpd_thread.setDaemon(True)
            log.debug("Starting HTTP daemon for test...")
            httpd_thread.start()

        def tearDown(self): 
            log.debug("Removing temporary directory %s...", self.tempdir)
            self.httpd.stop()
            self.tracker.stop()
            shutil.rmtree(self.tempdir, True, 
                    lambda fun, path, exc_info: \
                           log.error("%s can't delete %s: %s", fun, path, exc_info))

        def makeResponse(self, filename, piecelength=None): 
            if piecelength is None: 
                piecelength = 2**18
            fd = open(filename, 'rb')
            pieces = []
            while 1: 
                block = fd.read(piecelength) 
                if len(block) or not len(pieces): 
                    sha_ = sha.new()
                    sha_.update(block)
                    pieces.append(sha_.digest())
                if not block:
                    break
            fd.close()

            response = {
                'announce': 'http://127.0.0.1:%d/announce' % TRACKPORT,
                'creation date': int(time.time()),
                'info': {
                    'pieces': ''.join(pieces),
                    'piece length': piecelength,
                    'name': os.path.basename(filename), 
                    'length': os.path.getsize(filename)
                    }
                }

            return bencode(response)

        def makeFileAndTorrent(self, filename=None, length=None): 
            """Make a file and torrent. 

            Returns filepath, responsefilecontents, torrenturl."""
            
            if filename is None: 
                filename = 'blah%d.mp3' % random.randint(1024*32,1024*128)
            base, ext = os.path.splitext(filename)
            if length is None: 
                length = random.randint(1024*6400, 1024*25600) ###
            filepath = os.path.join(self.servedir, filename)
            fd = open(filepath, 'wb')
            log.debug("Generating %d bytes of random content...", length)
            write_random_content(fd, length)
            log.debug("... done.")
            fd.close()
            response = self.makeResponse(filepath)
            torrentname = '%s.torrent' % base
            self.httpd.add("/%s" % torrentname, content=response) # next arg is header dict
            self.httpd.prompt()
            torrenturl = 'http://127.0.0.1:%s/%s' % (TESTPORT, torrentname) 
            return filepath, response, torrenturl
                
        def test_checkalreadygot(self): 
            """Make sure we can check what we already have."""
            filepath, response, torrenturl = self.makeFileAndTorrent()
            torrentpath = os.path.join(self.grabdir, 'test.torrent')
            # First, download the torrent file and torrentgrab it
            grabber = BasicGrabber(torrenturl, torrentpath)
            grabber()
            grabber = TorrentGrabber(TorrentFile(torrentpath), filepath)
            grabber()
            # Second, just use the raw response
            grabber = TorrentGrabber(TorrentFile(response), filepath)
            grabber()

        def test_download(self): 
            filepath, response, torrenturl = self.makeFileAndTorrent()
            torrentpath = os.path.join(self.grabdir, 'test.torrent')
            mp3path = os.path.join(self.grabdir, os.path.basename(filepath))
            # first, serve it up in another thread
            log.debug("Serving up %s", filepath)
            seeder = TorrentGrabber(TorrentFile(response), filepath, keepserving=True)#, btoptions=['--max_upload_rate', 64])
            seedthread = threads.OurThread(target=seeder)
            seedthread.setDaemon(True)
            seedthread.start()
            try: 
                # then, grab it
                log.debug("Grabbing %s", torrenturl)
                grabber = BasicGrabber(torrenturl, torrentpath)
                grabber.hooks.add('updated', lambda: log.debug("Downloaded %fMB", grabber.download_mb))
                grabber()
                log.debug("Grabbing target %s", mp3path)
                grabber = TorrentGrabber(TorrentFile(torrentpath), mp3path)
                grabber.hooks.add('updated', lambda: log.debug("Downloaded %fMB", grabber.download_mb))
                grabber()
                seedthread.catch()
                assert grabber.doneflag.isSet()
            finally: 
                # and tidy up
                seeder.stop()
                log.debug("Waiting for seeder thread...")
                seedthread.join()
                seedthread.catch()
            
    unittest.main()
