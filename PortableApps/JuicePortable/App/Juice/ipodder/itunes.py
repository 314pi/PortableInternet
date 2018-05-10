from sgmllib import SGMLParser
import grabbers
import StringIO
import re
import urllib2,httplib

class ITMSHandler(urllib2.AbstractHTTPHandler):

    def itms_open(self, req):
        return self.do_open(httplib.HTTP, req)

# Code for extracting feedURLs out of itms xml.
class BaseItmsProcessor(SGMLParser):
    def reset(self):
        self.lasttag = None
        self.thistag = None
        self.lastkey = ""
        self.done = False
        self.result = ""
        self.text = ""
        SGMLParser.reset(self)
        
    def unknown_starttag(self, tag, attrs):
        self.lasttag = self.thistag
        self.thistag = tag

    def handle_data(self, text):
        self.text = self.text + text
        
    def unknown_endtag(self, tag):
        self.text = self.text.strip()
        if not self.done and tag == "string" and self.lasttag == "key" and self.lastkey == "feedURL":
            self.done = True
            self.result = self.text
        if tag == "key":
            self.lastkey = self.text
        self.text = ""

def itunes_url_p(url):
    return url.startswith('http://phobos.apple.com/')

def feedurl_from_itunes_url(itunes_url):
    if not itunes_url_p(itunes_url):
        return None

    sio = StringIO.StringIO()
    grabber = grabbers.BasicGrabber(itunes_url,sio)
    grabber()
    
    itms_url = None
    p = re.compile(".*open\('(itms://[^']+)'")
    for line in sio.getvalue().splitlines():
        m = re.match(p,line)           
        if m:
            itms_url = m.group(1)
            break

    if not itms_url:
        return None

    sio = StringIO.StringIO()
    grabber = grabbers.BasicGrabber(itms_url,sio)
    grabber()
    p = BaseItmsProcessor()
    p.feed(sio.getvalue())
        
    return p.result

if __name__ == '__main__': 
    try:
        result = feedurl_from_itunes_url('http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=73797923&s=143441')
        print result
    except grabbers.GrabError, ex:
        print ex[1]
