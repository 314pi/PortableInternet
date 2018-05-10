# iPodder package directory

__version__ = 'ignored; see ipodder.core.__version__'
__feedsinstance__ = None

def get_feeds_instance():
    return __feedsinstance__

def set_feeds_instance(feedsinstance):
    global __feedsinstance__
    __feedsinstance__ = feedsinstance

# Before moving everything from iPodder.py to ipodder/core.py, Enclosure 
# was a valid attribute of the iPodder module. As the shelve module used 
# for the state database is fussy about that kind of thing, I'm making 
# sure it can be resolved. That iPodder.Enclosure can be found via 
# ipodder (note the case!) is part of the reason I did the renaming in 
# the first place -- some recent change seems to have stuffed up my 
# ability to import iPodder separately from ipodder. :( 
#
#   -- Garth
from ipodder.core import Enclosure 
