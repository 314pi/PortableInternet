# Outline code for iPodder

"""
Let's embrace outlines fully in iPodder: not just for the feed management,
but also for playlist management, listing items, and so on. 
"""

import xml.sax
import xml.dom.minidom
import StringIO

import logging
log = logging.getLogger('Juice.Outline')
SPAM = logging.DEBUG >> 1
spam = lambda *a, **kw: log.log(SPAM, *a, **kw)

# Other parts of iPodder
import hooks

class Node(object): 
    """An outliner node."""
    
    reserved_atts = ('parent', 'hooks')

    def __init__(self, *args, **kwargs): 
        """Initialise the outliner node. 

        kwargs -- used to initialise the attributes. 'hooks' is 
                reserved; 'parent' is treated differently.
        args -- each argument is assumed to be a Node, and is added as 
                a member. If the first element is a string, the node 
                type is set to 'text' and the 'text' attribute is set 
                to the first element. 
        """
        object.__init__(self)
        self._hooks = hooks.HookCollection()
        self._parent = None
        self._children = []
        # Node attributes, exported to OPML
        self._atts = {'type': '', 'text': ''}
        assert not kwargs.has_key('type') # force subclasses to set .type
        self.update(kwargs)
        # Members
        spam("Node.__init__: args = %s", repr(args))
        if len(args): 
            if isinstance(args[0], str) or isinstance(args[0], unicode): 
                self.text = args[0]
                self.type = 'text'
                args = args[1:]
        self.extend(args)
        
    def attadd(self, key, more): 
        """Add more to self[key], defaulting self[key] to ''."""
        self[key] = self.get(key, '') + more
     
    def notifychanges(self): 
        """Issue change notifications."""
        self.hooks("changed", self)
        parent = self.parent
        if parent is not None: 
            self.parent.hooks("child-changed", parent, self)

    # Probably not necessary, as self.hooks.add() will work as expected. 
    # def addhook(self, key, callable): 
    #     """Add a callable to the `key` hook."""
    #     self._hooks.add(key, callable)
            
    # Dict-style access
    def get(self, key, default=None): return self._atts.get(key, default)
    def has_key(self, key): return self._atts.has_key(key)
    def items(self): return self._atts.items()
    def keys(self): return self._atts.keys()
    def values(self): return self._atts.values()
    
    def update(self, otherdict): 
        """Update our node attributes from another dict."""
        try: 
            for key in otherdict: 
                if key in Node.reserved_atts: 
                    raise ValueError, key
                val = otherdict[key]
                self._atts[key] = val
        finally: 
            self.notifychanges()

    # Dict / List style access
    def __getitem__(self, key): 
        """Get an item. Reserved keys are forbidden."""
        if key in Node.reserved_atts: 
            raise ValueError, key
        if isinstance(key, (int, slice)): 
            return self._children.__getitem__(key)
        else: 
            return self._atts[key]
        
    def __setitem__(self, key, value): 
        """Set an item. Reserved keys are forbidden."""
        if key in Node.reserved_atts: 
            raise ValueError, key
        try: 
            if isinstance(key, (int, slice)): 
                self._children.__setitem__(key, value)
            else: 
                self._atts[key] = value
        finally: 
            self.notifychanges()
            
    def __delitem__(self, key): 
        try: 
            if isinstance(key, (int, slice)): 
                self._children.__delitem__(key)
            else: 
                del self._atts[key]
        finally: 
            self.notifychanges()
        
    # List style methods
    def append(self, node): 
        """Append a node to our list of children, setting its parent."""
        assert isinstance(node, Node)
        assert node.parent is None, "Node already has parent."
        node.parent = self
        self._children.append(node)
        self.notifychanges()
    
    def extend(self, nodes): 
        """Extend our list of children, setting parents as we go."""
        # Take a copy in case we were passed an iterator or generator
        nodes = [n for n in nodes]
        # Don't do anything unless we can do everything
        for node in nodes: 
            assert isinstance(node, Node)
            assert node.parent is None
        # Do the work. 
        for node in nodes: 
            node.parent = self
            self._children.append(node)
        self.notifychanges()

    def DeleteChildren(self):
        self._children = []

    def __iter__(self): 
        """Return an iterator for ourself."""
        return iter(self._children)

    def __len__(self): 
        """Count our children."""
        return len(self._children)

    # Att-style access
    def __getattr__(self, att): 
        """Get an attribute. 
        
        Uses the conventions explained in the documentation for 
        `__setattr__`.
        """
        if att in Node.reserved_atts: 
            return object.__getattribute__(self, '_%s' % att)
        if att[:1] == '_': 
            return object.__getattribute__(self, att)
        try: 
            return object.__getattribute__(self, '_atts')[att]
        except KeyError: 
            raise AttributeError, att
        
    def __setattr__(self, att, value): 
        """Set an attribute. 

        Attributes in the reserved list are stored as _att. 
        Attributes beginning with _ are stored as-is. 
        Other attributes are stored as outline node attributes, 
        as if you treated the Node as a dict and said::
        
            node[att] = value
        """
        if att in Node.reserved_atts: 
            object.__setattr__(self, '_%s' % att, value)
        elif att[:1] == '_': 
            object.__setattr__(self, att, value)
        else: 
            object.__getattribute__(self, '_atts')[att] = value
            self.notifychanges()

    def __delattr__(self, att): 
        """Delete an attribute."""
        assert not att in Node.reserved_atts, \
                "Can't delete reserved attributes."
        assert not att[:1] == '_', \
                "Can't delete _special attributes."
        try: 
            del self._atts[att]
            self.notifychanges()
        except KeyError: 
            raise AttributeError, att
            
    # Other special methods
    def __repr__(self): 
        atts = self._atts
        attnames = atts.keys() # take a copy
        attnames.sort()
        bits = ['%s=%s' % (attname, repr(atts[attname]))
                for attname in attnames]
        bits.extend([repr(member) for member in self])
        return '[%s]' % ', '.join(bits)

    def __ne__(self, other): 
        """Are we not men? We are DEVO!"""
        return not self == other
        
    def __eq__(self, other): 
        """Compare one tree of Nodes with another tree of Nodes.
        Ignores class, just in case we read from OPML."""
        spam("comparing...")
        if len(self) != len(other): 
            spam("Length mismatch: %d != %d", len(self), len(other))
            return False 
        myattnames = self.keys()
        myattnames.sort()
        attnames = other.keys()
        attnames.sort()
        if attnames != myattnames: 
            spam("Attribute names mismatch.")
            return False
        for attname in myattnames: 
            if self[attname] != other[attname]: 
                spam("Attribute %s doesn't match", attname)
                return False
        # Finally, compare the kids.
        for index in range(len(self)): 
            if self[index] != other[index]: 
                spam("Child #%d mismatch", index)
                spam("Ours: %s", repr(self[index]))
                spam("Theirs: %s", repr(other[index]))
                return False
        return True

class Link(Node): 
    def __init__(self, text, href='', *args, **kwargs): 
        Node.__init__(self, text, href=href, *args, **kwargs)
        self.type = 'link'

class Text(Node): 
    def __init__(self, text, *args, **kwargs): 
        Node.__init__(self, text, *args, **kwargs)
        self.type = 'text'

class Head(Node): 
    def __init__(self, title, *args, **kwargs): 
        Node.__init__(self, title=title, *args, **kwargs)
        self.type = 'head'
    
    def toopml(self): 
        """Convert everything under the Head to XML."""
        impl = xml.dom.minidom.getDOMImplementation()
        doc = impl.createDocument(None, 'opml', None)
        top = doc.documentElement
        head = doc.createElement('head')
        top.appendChild(head)
        headbits = {}
        headbits.update(self)
        if not headbits.has_key('dateCreated'):  
            pass # we should do something
        if not headbits.has_key('dateModified'):  
            pass # we should do something
        if headbits.has_key('type'):
            del headbits['type']
        for bit, value in headbits.items(): 
            elem = doc.createElement(bit)
            data = doc.createTextNode(str(value).strip())
            elem.appendChild(data)
            head.appendChild(elem)
        body = doc.createElement('body')
        top.appendChild(body)
        
        def suck(node): 
            elem = doc.createElement('outline')
            atts = {}
            atts.update(node)
            #if node is self: 
            #    if atts.has_key('title'): 
            #        if not atts.has_key('text'): 
            #            atts['text'] = atts['title']
            #        del atts['title']
            #    atts['type'] = 'text'
            if atts['type'] == 'text': 
                del atts['type']
            attnames = atts.keys()
            attnames.sort()
            for attname in attnames: 
                value = atts[attname]
                elem.setAttribute(attname, str(value).strip())
            for child in node: 
                elem.appendChild(suck(child))
            return elem

        for node in self:
            body.appendChild(suck(node))
        #body.appendChild(suck(self))

        # return doc.toxml()
        outs = StringIO.StringIO()
        doc.writexml(outs, '', '    ', '\n')
        return outs.getvalue()

    def trimlinkchildren(self, node=None, stack=[]): 
        """Trim all children of links."""
        if node is None: 
            node = self
        if node.get('type', '') == 'link': 
            if len(node): 
                log.warn("Trimming children of link node %s", 
                         '/'.join(stack))
                del node[:]
                assert len(node) == 0
        else: 
            for child in node: 
                assert child is not None
                self.trimlinkchildren(child, stack + [child.get('text', '')])
        
    def fromopml(self, resource): 
        """Return a Head corresponding to an OPML file.
           Return None if parsing fails for some reason.
           
        resource -- XML string, or a stream."""
        
        opmlhandler = OPMLEventHandler()
        # TODO: check ex.args against ('undefined entity',)
        #       insert tricky stuff
        
        if isinstance(resource, str): 
            try: 
                sio = StringIO.StringIO(resource)
                xml.sax.parse(sio, opmlhandler)
                sio.close()
            except xml.sax._exceptions.SAXParseException, ex:
                if ex.args == ('undefined entity',): 
                    # try again
                    raise
                else: 
                    log.exception("Caught exception parsing opml file.")
                    return None
        else:
            try:
                xml.sax.parse(resource, opmlhandler)
            except xml.sax._exceptions.SAXParseException:
                log.exception("Caught exception parsing opml file.")
                return None
        head = opmlhandler.head
        head.trimlinkchildren()
        return head

    fromopml = classmethod(fromopml)

        
class OPMLEventHandler(xml.sax.handler.ContentHandler): 
    def __init__(self): 
        xml.sax.handler.ContentHandler.__init__(self)
        self.stack = []
        self.context = []
        self.onchars = None
    def startElement(self, name, atts): 
        stack = self.stack
        context = self.context
        self.onchars = None # reset it
        slen = len(stack)
        if not slen: 
            assert name == 'opml'
            # no effect on context
        elif slen == 1: 
            assert name in ['head', 'body']
            if name == 'head': 
                self.head = Head('')
                context.append(self.head)
        elif slen == 2: 
            if stack[1] == 'head': 
                assert name != 'outline'
                head = context[0]
                self.onchars = lambda chars: head.attadd(name, chars)
            else: 
                assert name == 'outline'
                self.startOutline(atts)
        else: 
            assert stack[-1] == 'outline'
            assert name == 'outline'
            self.startOutline(atts)
        self.stack.append(name)
        spam("starting %s", name)
        for att, val in atts.items():
            spam("  %s = %s", att, repr(val))
    def startOutline(self, atts): 
        parent = self.context[-1]
        child = Node()
        for att, val in atts.items(): 
            child[att] = val
        #AG: this is a little ugly.  To make "rss" nodes look like
        #other types, we map the xmlUrl attribute to url if the
        #former is present and the latter is not.
        if hasattr(child,"type") and child.type == "rss" \
           and hasattr(child,"xmlUrl") and not hasattr(child,"url"):
            child["url"] = child.xmlUrl
        parent.append(child)
        self.context.append(child)
    def endElement(self, name): 
        spam("ending %s", name)
        assert self.stack[-1] == name
        if name == 'outline': 
            self.context.pop()
        self.stack.pop()
    def characters(self, chars): 
        if self.onchars is not None: 
            spam("handling characters: %s", repr(chars))
            self.onchars(chars.strip())
        else: 
            spam("ignoring characters: %s", repr(chars))
        
if __name__ == '__main__': 
    import unittest
    
    class NodeTest(unittest.TestCase): 

        def test_create_noargs(self): 
            node = Node()
            assert node.type == ''
            
        def test_create_autotext(self): 
            node = Node('boingoingoing')
            assert node.type == 'text'
            assert node.text == 'boingoingoing'

        def test_head(self): 
            tree = Head('title')

        def test_nest(self): 
            tree = Node('title', Node('boing'))

        def create_tree(self): 
            tree = Head("Playlists", 
                #Node("Playlists", 
                    Link("iPodder.org: Podcasting Central", 
                         href="http://www.ipodder.org/discuss/reader$4.opml"),
                    Link("Juice Team Directory", 
                         href="http://ipodder.sf.net/opml/ipodder.opml"),
                    Link("iPodderX Top Picks", 
                         href="http://directory.ipodderx.com/opml/iPodderX_Picks.opml"), 
                    Link("iPodderX Most Popular", 
                         href="http://directory.ipodderx.com/opml/iPodderX_Popular.opml"),
                #    )
                )
            return tree

        def test_create_tree(self): 
            self.create_tree()
            
        def test_tree_repr(self): 
            tree = self.create_tree()
            repr(tree)

        def test_tree_toopml(self): 
            tree = self.create_tree()
            tree.toopml()

        def test_tree_fromopml(self): 
            opml = """<?xml version="1.0" ?>
                <opml>
                    <head>
                        <text>

                        </text>
                        <title>
                            Playlists
                        </title>
                    </head>
                    <body>
                        <outline href="http://www.ipodder.org/discuss/reader$4.opml" 
                         text="iPodd er.org: Podcasting Central" type="link"/>
                        <outline href="http://ipodder.sf.net/opml/ipodder.opml" 
                         text="iPodder Team Directory" type="link"/>
                    </body>
                </opml>
                """            
            tree = Head.fromopml(opml)

        def test_ignore_link_children(self): 
            opml = """<?xml version="1.0" ?>
                <opml>
                    <head>
                        <text>

                        </text>
                        <title>
                            Playlists
                        </title>
                    </head>
                    <body>
                        <outline href="http://www.ipodder.org/discuss/reader$4.opml" 
                         text="iPodder.org: Podcasting Central" type="link">
                            <outline text="Ignore me!"/>
                            <outline text="Ignore me, too!"/>
                        </outline>
                    </body>
                </opml>
                """            
            tree = Head.fromopml(opml)
            linknode = tree[0]
            assert len(linknode) == 0, "kids not ignored"
            
        def test_tree_eq_silly(self): 
            tree = self.create_tree()
            tree2 = self.create_tree()
            assert tree == tree2
            
        def test_tree_fromopml(self): 
            tree = self.create_tree()
            xml = tree.toopml()
            spam(xml)
            newtree = Head.fromopml(xml)
            spam(tree)
            spam(newtree)
            assert newtree == tree

        def test_protected_attributes(self): 
            # Protect on initialisation
            self.failUnlessRaises(ValueError, lambda: Node(parent="this"))
            self.failUnlessRaises(ValueError, lambda: Node(hooks="this"))
            # Protect on update
            node = Node("")
            def sneaky(): node.update({'parent':1})
            self.failUnlessRaises(ValueError, sneaky)
            # Protect on direct assignment
            def blatant(): node['hooks'] = 1
            self.failUnlessRaises(ValueError, blatant)

        def test_autoparentification(self): 
            node = Node("parent", Node("child"))
            # Make sure it worked on initialisation. 
            child = node[0]
            assert child.text == "child"
            assert child.parent == node
            # Append a child and make sure it worked. 
            child2 = Node("child2")
            assert child2.parent is None
            node.append(child2)
            assert child2.parent is node
            # Extend by more children and make sure it worked. 
            morechildren = [Node("child3"), Node("child4")]
            node.extend(morechildren)
            for child in morechildren: 
                assert child.parent is node

        def test_nodualparents(self): 
            parent = Node("parent")
            parent2 = Node("other parent")
            child = Node("child")
            parent.append(child)
            self.failUnlessRaises(AssertionError, 
                    lambda: parent2.append(child))

        def test_delete_atts(self): 
            node = Node(a=1, b=2)
            # Delete 'a' as if it's an item, then check it's gone by att.
            del node['a']
            assert not hasattr(node, 'a')
            # Delete 'b' as if it's an att, then check it's gone by key. 
            del node.b
            assert not node.has_key('b')
            # Make sure that deletion of non-existent atts fails. 
            def stupid(): del node.c
            self.failUnlessRaises(AttributeError, stupid)
            def asstupid(): del node['c']
            self.failUnlessRaises(KeyError, asstupid)

        def test_delete_items(self): 
            tree = self.create_tree()
            length = len(tree)
            # First, delete just one item.
            third = tree[3]
            del tree[2]
            assert len(tree) == length-1
            assert tree[2] == third
            # Second, delete a slice. 
            last = tree[-1]
            del tree[:-1]
            assert tree[0] == last

        def test_hook_simple(self): 
            node = Node()
            def creosote(): raise IOError # it barfs!
            node.hooks.add("bucket", creosote)
            self.failUnlessRaises(IOError, node.hooks.get("bucket"))

        def test_notify(self): 
            class NotificationFailure(Exception): pass
            class Tracker: 
                def __init__(self, child, parent): 
                    self.child = child
                    self.parent = parent
                    child.hooks.add('changed', self.changed)
                    parent.hooks.add('child-changed', self.child_changed)
                    self.reset()
                def changed(self, child): 
                    assert child is self.child
                    self.caught_change = True
                def child_changed(self, parent, child): 
                    assert parent is self.parent
                    assert child is self.child
                    self.caught_child_change = True
                def reset(self): 
                    self.caught_change = False
                    self.caught_child_change = False
                def check(self): 
                    if not self.caught_change: 
                        raise NotificationFailure, "Didn't catch change."
                    if not self.caught_child_change: 
                        raise NotificationFailure, "Didn't catch change of child."
                    self.reset()
            
            tester = Node('tester', hair='lots')
            parent = Node('parent', tester)
            tracker = Tracker(tester, parent)
            self.failUnlessRaises(NotificationFailure, tracker.check)
            # Attribute assignment
            tester.text = 'ouch!'
            tracker.check()
            # Attribute removal. 
            del tester.text
            tracker.check()
            # Key removal. 
            del tester['hair']
            tracker.check()
            # Key assignment. 
            tester['hair'] = 'thinning'
            tracker.check()
            # Adding a child
            tester.append(Node())
            tracker.check()
            # Deleting a child.
            del tester[0]
            tracker.check()
            # Adding multiple children at once. 
            tester.extend([Node(), Node()])
            tracker.check()

    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    logging.addLevelName(SPAM, "SPAM")
    unittest.main()
