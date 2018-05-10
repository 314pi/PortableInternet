import logging
from ipodder import outlines

log = logging.getLogger('Juice')

class ManagedFeeds(object):
    """A mixin class for ipodder.feeds.Feeds, that provides helper methods
    for the feed manager."""
    
    def replace_from_manager_opml(self,opml_url,opml):

        #Step 1: Parse the remote OPML.
        if opml=="":
            return                   

        tree = outlines.Head.fromopml(opml)
        if not tree:
            return None

        #Step 2: Utility functions.
        def url_and_title_from_node(node):
            url = ''
            title = ''
            if node.type == "link":
                title = node.text
                url = node.url
            if node.type == "rss":
                title = node.title
                url = node.xmlUrl
            return (url,title)

        def extract_traverse(node,urls):
            if not isinstance(node, outlines.Node):
                return urls
            if not hasattr(node,"type"):
                return urls

            (url,title) = url_and_title_from_node(node)

            urls.append(url)

            for child in node:
                urls = extract_traverse(child,urls)
                
            return urls
        
        def add_traverse(node,numadded):
            if not isinstance(node, outlines.Node):
                return numadded
            if not hasattr(node,"type"):
                return numadded

            (url,title) = url_and_title_from_node(node)
            
            if url:
                active_feed = False
                for feed in [feed for feed in self \
                             if feed.sub_state not in ['disabled','unsubscribed']]:
                    if feed.url.lower() == url.lower():
                        active_feed = True
                        if feed.manager_url != None and feed.manager_url != opml_url:
                            feed.manager_url = opml_url
                        break
                if not active_feed:
                    log.debug("Feed manager: adding feed %s" % url)
                    self.addfeed(url,title=title,quiet=True, \
                    sub_state='newly-subscribed', \
                    manager_url=opml_url)
                    numadded += 1
                

            for child in node:
                numadded = add_traverse(child,numadded)

            return numadded

        #Step 3: Prune our feeds that are not in remote OPML.
        urls = extract_traverse(tree,[])
        
        for feed in [feed for feed in self \
            if feed.sub_state not in ['disabled','unsubscribed'] and \
               feed.manager_url != None]:

            #Active feeds with non-empty manager urls are candidates
            #for deletion.  Later if we allow multiple managers
            #we can preserve subscriptions managed by other URLs.
            
            if feed.url not in urls:
                log.debug("Feed manager: removing feed %s" % feed.url)
                feed.sub_state = 'disabled'
       
        #Step 4: Add feeds from remote OPML that aren't in our list.
        numadded = add_traverse(tree,0)

        self.flush()         

        return numadded
    
    def remove_managed_feeds(self):
        """Disable any feed with a manager url is not None and set its
        manager url to None."""
        for feed in [feed for feed in self \
            if feed.manager_url != None]:
            feed.manager_url = None
            feed.sub_state = 'disabled'

        self.flush()
