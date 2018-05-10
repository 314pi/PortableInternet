# iPodder GUI -- tree code
#
# Based on edj's amazing resizable OPMLOutliner code. 
# Heavily mutated by gtk. 

from wxPython.wx import *
import types
from xml.sax import make_parser, handler
import wx
import logging
import StringIO
import os.path
import sys

from ipodder import outlines
from ipodder import grabbers
from ipodder import threads
from ipodder import hooks
from ipodder.contrib import urlnorm
from ipodder.contrib import GenericDispatch
import gui
from gui import images
from skin import \
    DIRECTORY_LINK_SCANNED,\
    DIRECTORY_LINK_UNSCANNED,\
    DIRECTORY_LINK_SCANNING
               
log = logging.getLogger('Juice.Outliner')
basepath = os.path.abspath(os.path.split(sys.argv[0])[0])

ACTIVE_FEED_SUB_STATES = ['subscribed', 'newly-subscribed', 'preview', 'force']

class TreeNode:
    """A GUI tree node that points to the abstract tree node."""

    def __init__(self, parent, node): 
        """Initialise the TreeNode.
        
        parent -- the parent TreeNode or, if this node is the root, the 
                  OPMLTree itself.
        node -- the outlines.Node underlying this GUI tree node.
        """

        self.appending = False
        
        # Check the node is a node. 
        assert isinstance(node, outlines.Node)

        # Handle the parent.
        if isinstance(parent, OPMLTree): 
            opmltree = parent
            parent = None
            id = opmltree.AddRoot(node.text)
        elif isinstance(parent, TreeNode): 
            opmltree = parent.opmltree
            id = opmltree.AppendItem(parent.id, node.text)
        else: 
            raise ValueError, parent
        #log.debug("id: %s", repr(id))
        opmltree.SetPyData(id, self)

        self.opmltree = opmltree
        self.node = node
        self.parent = parent
        self.id = id
        self.scanned = False # only useful for links to OPML
        self.scanthread = None
        
        node.hooks.add('changed', self.nodechanged)
        node.hooks.add('child-changed', self.childnodechanged)
        self.nodechanged(node) # forces scan of our abstract node
        self.childnodechanged(node, None) # ... and of our children

    def nodechanged(self, node): 
        """Deal with the underlying abstract node changing."""
        self.opmltree.ThreadSafeDispatch(self._nodechanged, node)
        
    def _nodechanged(self, node): 
        """Deal with the underlying abstract node changing."""
        if self.appending:
            self.appending = False
            TreeNode(self,node[-1])
            return
        self.seticon()
        for child in node: 
            TreeNode(self, child)
        #AG HACK to expand the Directory root node on startup.
        if self.parent == None:
            self.opmltree.Expand(self.id)
            
    def childnodechanged(self, node, child): 
        """Deal with a child of the underlying abstract node changing."""
        self.opmltree.ThreadSafeDispatch(self._childnodechanged, node, child)
        
    def _childnodechanged(self, node, child): 
        """Deal with a child of the underlying abstract node changing."""
        self.seticon()
                
    def seticon(self, expanding=False): 
        """Set our icon."""
        # TODO: we need a plain text node icon
        opmltree = self.opmltree
        id = self.id
        node = self.node
        image = None
        colour = wx.NullColor
        
        if len(node):
            image = opmltree.fldridx
            opmltree.SetItemHasChildren(id, TRUE)
        else: 
            image = opmltree.textidx
            opmltree.SetItemHasChildren(id, FALSE)

        if node.type in ['link','rss']: 
            if self.opmltree.IsOpmlUrl(node.url): 
                image = opmltree.netfldridx
                if self.scanned: 
                    colour = DIRECTORY_LINK_SCANNED
                    if len(node): 
                        opmltree.SetItemHasChildren(id, TRUE)
                    else: 
                        opmltree.SetItemHasChildren(id, FALSE)
                else: 
                    opmltree.SetItemHasChildren(id, TRUE)
                    colour = DIRECTORY_LINK_UNSCANNED
            else: 
                image = opmltree.remoteidx
                if opmltree.feeds is not None: 
                    try: 
                        feed = opmltree.feeds[node.url]
                        if feed.sub_state in ACTIVE_FEED_SUB_STATES: 
                            image = opmltree.tickidx
                        else: 
                            image = opmltree.crossidx
                    except KeyError: 
                        pass

        if expanding: 
            image = opmltree.openidx
            colour = DIRECTORY_LINK_SCANNING
            
        if image is not None: 
            #log.debug("Setting icon image to %s", repr(image))
            opmltree.SetItemImage(id, image)
        opmltree.SetItemTextColour(id, colour)
        opmltree.Refresh()

    def scan(self): 
        """Ask for our remote component to be scanned."""
        log.debug("%s: scan requested.", repr(self))
        if self.scanthread is not None: 
            log.debug("We already have a scan thread.")
            self.scanthread.catch()
            return
        if self.scanned: 
            log.debug("Already scanned.")
            return
        node = self.node
        if not node.type == 'link': 
            log.debug("No. We're not a link.")
            return
        if not self.opmltree.IsOpmlUrl(node.url): 
            log.debug("No. We don't aim at OPML.")
            return
        self.scanthread = threads.OurThread(target=self._scan)
        self.scanthread.setDaemon(True)
        self.scanthread.start()

    def setmessage(self, message=None): 
        """Append a message to our text."""
        if not message: 
            self.opmltree.SetItemText(self.id, self.node.text)
        else: 
            self.opmltree.SetItemText(self.id, "%s [%s]" % (
                self.node.text, message))
        
    def _scan(self): 
        """Asynchronous scan method."""
        node = self.node
        self.seticon(expanding=True)
        self.setmessage("downloading...")
        sio = StringIO.StringIO()
        grabber = grabbers.BasicGrabber(node.url, sio, state=self.opmltree.state, offline=False)
        grabber.hooks.add('updated', lambda: self.setmessage(
            "downloading %d%%" % (100*grabber.fraction_done)))
        try: 
            res = grabber()
        except grabbers.GrabError, ex: 
            log.error("Grab failed (%s) for %s", ex.message, node.url)
            self.seticon(expanding=False)
            self.setmessage(ex.message)
            self.scanthread = None
            return
        filename, headers = res 
        # filename will be None
        # no point looking at headers, really :) 
        opml = sio.getvalue()
        sio.close()
        try: 
            node = outlines.Head.fromopml(opml)
            self.update_user_root_title(node)
        except (AssertionError, outlines.xml.sax._exceptions.SAXParseException), ex: 
            log.error("Couldn't parse XML or OPML for node: %s", node.url)
            #log.info(node.url)
            #log.info(opml)
            self.seticon(expanding=False)
            self.setmessage("parsing failure")
            self.scanthread = None
            return
        orphans = []
        for child in node: 
            child.parent = None
            orphans.append(child)
        self.scanned = True
        self.setmessage()
        self.node.extend(orphans)
        self.opmltree.ThreadSafeDispatch(self.opmltree.Expand, self.id)
        self.scanthread = None # time to die! :) 

    def rescan(self):
        self.node.DeleteChildren()
        self.opmltree.DeleteChildren(self.id)
        self.scanned = False
        self.scan()

    def append(self,node):
        self.appending = True
        self.node.append(node)

    def update_user_root_title(self,head):
        """New roots may come in with bogus titles.  Try to update them here."""
        if isinstance(self.parent, TreeNode) and self.parent.parent == None:
            if hasattr(head,"title"):
                from ipodder import configuration
                node = self.node
                defaults = configuration.configDefaults['podcast_directory_roots']
                for root in defaults:
                    if root[0] == node.url:
                        return
                actual = self.opmltree.feeds.config.podcast_directory_roots
                for root in actual:
                    if root[0] == node.url:
                        actual.remove(root)
                        actual.append((node.url,head.title))
                        self.node.text = head.title
                        return
                        
class OPMLTree(GenericDispatch.GenericDispatchMixin, wxTreeCtrl):
    '''Lazy Tree is a simple "Lazy Evaluation" tree,
    that is, it only adds items to the tree view when
    they are needed.'''

    ISNEW = 1

    def __init__(self, *a, **kw): 
        # Stops us from being able to run interactively, 
        # but at least works in iPodderGui. 
        p = wx.PreTreeCtrl()
        self.PostCreate(p)
    #    wxTreeCtrl.__init__(self, *a, **kw)
    #    GenericDispatch.GenericDispatchMixin.__init__(self)
        self.hooks = hooks.HookCollection()
      
    def Init(self, roots, feeds, state): 
        self.feeds = feeds
        self.state = state
        EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpandNode)
        EVT_TREE_SEL_CHANGED(self, self.GetId(), self.OnSelectNode)
        EVT_TREE_ITEM_ACTIVATED(self, self.GetId(), self.OnActivateNode)
        GenericDispatch.EVT_DISPATCH(self, self.OnDispatchEvent)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        
        def iladd(name): 
            icon = gui.geticon(name)
            try: 
                return il.Add(icon)
            except wx.PyAssertionError, ex:
                log.exception("Failed to add icon %s to image list; "\
                              "it's probably corrupt.", name)
                return il.Add(gui.geticon('smiles')) # probably OK

        self.textidx     = iladd('normal file')
        self.fldridx     = iladd('folder')
        self.fldropenidx = iladd('file open')
        self.openidx     = self.fldropenidx
        self.fileidx     = iladd('report view')
        self.smileidx    = iladd('smiles')
        self.netfldridx  = iladd('netflder')
        self.remoteidx   = iladd('remote')
        self.tickidx     = iladd('remote-sub')
        self.crossidx    = iladd('icon_feed_disabled')
       
        self.SetImageList(il)
        self.il = il
        self.logpanel = -1
        
        self.DeleteAllItems()
        self.InitMenus()

        rootNode = outlines.Node('Directory')

        if 0: 
            # Add feeds information
            active = []
            inactive = []
            for feed in feeds: 
                tup = (str(feed), feed)
                if feed.sub_state in ACTIVE_FEED_SUB_STATES: 
                    active.append(tup)
                else:
                    inactive.append(tup)
            active.sort(); inactive.sort()
            subsnode = outlines.Node('My Subscriptions')
            for title, feed in active: 
                subsnode.append(outlines.Link(title, url=feed.url))
            rootNode.append(subsnode)

        for url, title in roots: 
            rootNode.append(outlines.Link(title, url=url))
        
        self.root = TreeNode(self, rootNode)
        #AG: Doesn't work.  TreeNode invokes the thread-safe dispatcher,
        #which appears to run after this command.
        #self.Expand(self.root.id)

    def InitMenus(self): 
        """Initialise the menus."""
        
        def addmenu(menu, text, callable): 
            """Add an item to the menu"""
            id = wx.NewId()
            menu.Append(id, text)
            wx.EVT_MENU(menu, id, callable)
            
        nm = self.nodemenu = wx.Menu()
        addmenu(nm, "Subscribe", self.Null)
        addmenu(nm, "Unsubscribe", self.Null)

        dm = self.dirmenu = wx.Menu()
        addmenu(nm, "Add shortcut", self.Null)
        addmenu(nm, "Remove shortcut", self.Null)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick, self)

    def OnRightClick(self, event): 
        # TODO:
        # choose a menu
        # customise it
        # pop it up
        ID = event.GetItem()
        treenode = self.GetPyData(ID)
        self.hooks('right-click', self, ID, treenode)

    def Null(self):
        """Do nothing."""
        pass
        
    def SetLogPanel(self, logpanel):
        self.logpanel = logpanel
        
    def OnExpandNode(self, event):
        """Expand a node. This does nothing at the moment."""
        ID = event.GetItem()
        node = self.GetPyData(ID)
        if 0: 
            log.warn("Trying to scan the kids...")
            # This doesn't work, I think because the way we import node trees 
            # stuffs up the parental relationships. 
            for child in node.node: ###
                log.warn("Here's a kid.")
                child.scan()
            
    def OnSelectNode(self, event):
        """When the user selects a node, scan it."""
        ID = event.GetItem()
        try:
            treenode = self.GetPyData(ID)
        except wx._core.PyAssertionError:
            # Windows doesn't behave well if you right-click a non-selected node.
            event.Skip()
            return
        self.hooks('select-before-scan', self, ID, treenode)
        treenode.scan()
        
    def OnActivateNode(self, event):
        """When a user double-clicks a node, call a hook."""
        ID = event.GetItem()
        treenode = self.GetPyData(ID)
        self.hooks('node-activated', self, ID, treenode)
        
    def GetName( self, node ):
        return str(node)
     
    def GetChildren( self, node ):
        if type(node) in (types.ListType, types.TupleType):
            return node
        else:
            return []

    def IsOpmlUrl(self,url):
        if url.lower().endswith('.opml'):
            return True
        #If it's in the config directory, assume it's OPML.
        for root in self.feeds.config.podcast_directory_roots:
            if root[0] == url:
                return True
        return False

    def AddDirectoryRoot(self,title,url):
        self.root.append(outlines.Link(title, url=url))
        self.feeds.config.podcast_directory_roots.append((url,title))
        
class TestApplication (wxPySimpleApp):
    def __init__(self, feeds):
        self.feeds = feeds
        wxPySimpleApp.__init__(self)
        
    def OnInit(self):
        frame = wxFrame (NULL, -1, "test", size = (600,700))
        panel = wxPanel(frame, -1)
        sizer = wxBoxSizer( wxVERTICAL)

        roots = [
            ('http://www.indiepodder.org/discuss/reader$4.opml', 
             'IndiePodder.org: Podcasting Central'), 
            ('http://juice.sf.net/opml/juice.opml', 
             'Juice Team Directory'), 
            ('http://directory.ipodderx.com/opml/iPodderX_Picks.opml', 
             'iPodderX Top Picks'), 
            ('http://directory.ipodderx.com/opml/iPodderX_Popular.opml', 
             'iPodderX Most Popular'), 
            ('http://www.thesportspod.com/opml/sports.opml',
             'TheSportsProd'), 
            ('http://www.gigadial.net/public/opml/dial.opml', 
             'GigaDial')
            ]
        
        lazy_tree = OPMLTree(panel)
        lazy_tree.Init(roots, self.feeds, {})

        sizer.Add(lazy_tree, 1, wxEXPAND)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(true)
        frame.Show(1)
        self.SetTopWindow(frame)
        return 1

def main():
    from ipodder import configuration
    from ipodder import feeds
    import shelve
    import pickle
    logging.basicConfig()
    log = logging.getLogger('Juice')
    log.setLevel(logging.DEBUG)
    parser = configuration.makeCommandLineParser()
    options, args = parser.parse_args()
    if args: 
        parser.error("only need options; no arguments.")
    config = configuration.Configuration(options)
    state = shelve.open(config.state_db_file, 'c', 
                        writeback=False, protocol=pickle.HIGHEST_PROTOCOL)
    feeds = feeds.Feeds(config, state)

    app = TestApplication(feeds)
    app.MainLoop()
    
if __name__ == "__main__":
    main()
