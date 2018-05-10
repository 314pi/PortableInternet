from os.path import abspath, split, isfile, join
from gui import images
import wx
import sys

import logging
log = logging.getLogger('Juice.gui')

class IconBucket(object): 
    "Our application's icon bucket."
    
    typemap = {
        '.gif': wx.BITMAP_TYPE_GIF,
        '.ico': wx.BITMAP_TYPE_ICO,
        '.png': wx.BITMAP_TYPE_PNG,
        '.jpg': wx.BITMAP_TYPE_JPEG
        }

    def __init__(self): 
        """Initialise the icon bucket."""
        self.basepath = abspath(split(sys.argv[0])[0]) # UGH!

    def geticon(self, name): 
        """Get an icon by name."""

        # First, look for the icon file in the icons_status directory. 
        path = join(self.basepath, 'icons_status', name)
        for ext in ('.gif', '.png', '.jpg', '.ico'): 
            filename = path + ext
            if isfile(filename): 
                log.debug("Found image %s as %s", name, filename)
                return wx.Bitmap(filename, self.typemap[ext])

        # Second, look for inbuilt art. 
        attname = 'ART_' + '_'.join(name.upper().split(' '))
        try: 
            art = getattr(wx, attname)
            iconsize = (16, 16)
            return wx.ArtProvider_GetBitmap(art, wx.ART_OTHER, iconsize)
        except AttributeError: 
            pass

        # Finally, try the images module.
        log.debug("No image matching %s found.", name)
        words = name.split(' ')
        capwords = [word[:1].upper() + word[1:].lower()
                    for word in name.split(' ')]
        methodname = 'get%sBitmap' % ''.join(capwords)
        log.debug("Trying images.%s", methodname)
        try: 
            method = getattr(images, methodname)
            log.debug("Found!")
            return method()
        except AttributeError: 
            pass
            
        # Give up.
        log.warn("Couldn't find an icon named %s", repr(name))
        return images.getNoIconBitmap()
        
    def __getattr__(self, name): 
        """Load icons into the bucket's attributes on request."""

        icon = self.geticon(name)
        setattr(self, name, icon)
        return icon
    
icons = IconBucket()
geticon = icons.geticon
