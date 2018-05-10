"""
Bloglines Blogroll Extractor
Author: Nick Codignotto
Date: October 19, 2004
URL: http://www.primordia.com/blog
Notes: Some code taken from ActiveState forums
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/267197
"""

import sys
import getopt
import httplib
import xml.dom.minidom
import urllib2
import re
import base64
from urlparse import urlparse
import optparse

# I wanted to touch a particular web page (in order to open/
# close a database connection inside of Zope) so I came
# up with this module which uses urllib2 to make the
# web connection
#
# I was not sure what a 'realm' was, so first I made the
# HTTPRealmFinder to find out what the realm is.
# The HTTPinger calls my required page and acts according
# to the http return code.

class HTTPinger:
    def safeping(self, url, webuser, webpass): 
        "Safe ping. Prints stuff rather than throwing exceptions."
        try:
            return self.ping(url, webuser, webpass)
        except urllib2.HTTPError, e:
            if e.code == 401:
                print 'not authorized'
            elif e.code == 404:
                print 'not found'
            elif e.code == 503:
                print 'service unavailable'
            else:
                print 'unknown error: '
        else:
            print 'success'
        return 0
        
    def ping(self, url, webuser, webpass):
        "Risky ping. Throws exceptions gleefully."
        scheme, domain, path, x1, x2, x3 = urlparse(url)
        
        finder = HTTPRealmFinder(url)
        realm = finder.get()
        
        handler = urllib2.HTTPBasicAuthHandler()
        handler.add_password(realm, domain, webuser, webpass)
        
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        return urllib2.urlopen(url)

class HTTPRealmFinderHandler(urllib2.HTTPBasicAuthHandler):
    def http_error_401(self, req, fp, code, msg, headers):
        realm_string = headers['www-authenticate']
        
        q1 = realm_string.find('"')
        q2 = realm_string.find('"', q1+1)
        realm = realm_string[q1+1:q2]
        
        self.realm = realm

class HTTPRealmFinder:
    def __init__(self, url):
        self.url = url
        scheme, domain, path, x1, x2, x3 = urlparse(url)
        
        handler = HTTPRealmFinderHandler()
        handler.add_password(None, domain, 'foo', 'bar')
        self.handler = handler
        
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

    def ping(self, url):
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            pass

    def get(self):
        self.ping(self.url)
        try:
            realm = self.handler.realm
        except AttributeError:
            realm = None
        
        return realm

    def prt(self):
        print self.get()
    
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def extractsubs(username, password, podcastFolder):
    pinger = HTTPinger()
    u = pinger.ping('http://rpc.bloglines.com/listsubs', username, password)
    # print >> sys.stderr, repr(u)
    data = u.read()
    
    dom = xml.dom.minidom.parseString(data)
    outlines = dom.getElementsByTagName("outline")
    spotted = False
    for outline in outlines:
        title = outline.getAttribute("title")
        if title == podcastFolder:
            spotted = True
            podcasts = outline.getElementsByTagName("outline")
            for podcast in podcasts:
                xmlurl = podcast.getAttribute("xmlUrl")
                if xmlurl != "":
                    yield xmlurl
    if not spotted: 
        raise KeyError, podcastFolder

def makeCommandLineParser(): 
    usage = "usage: %prog --username=U --password=P --folder=F"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('--username', 
                      dest = 'bl_username', 
                      action = 'store', 
                      type = 'string', 
                      default = '',
                      help = "Bloglines username")

    parser.add_option('--password',
                      dest = 'bl_password', 
                      action = 'store', 
                      type = 'string', 
                      default = '',
                      help = "Bloglines password")

    parser.add_option('--folder', 
                      dest = 'bl_folder', 
                      action = 'store', 
                      type = 'string', 
                      default = '',
                      help = "Bloglines folder")

    return parser

def main(argv=None):
    parser = makeCommandLineParser()
    options, args = parser.parse_args()
    for opt in ['username', 'password', 'folder']: 
        att = 'bl_%s' % opt
        if not getattr(options, att): 
            parser.error("compulsory option --%s not supplied." % opt)
    for sub in extractsubs(options.bl_username, options.bl_password, options.bl_folder): 
        print sub
    return 0

if __name__ == "__main__":
    sys.exit(main())
