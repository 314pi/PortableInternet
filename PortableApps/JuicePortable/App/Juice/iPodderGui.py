#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import wx
import wx.xrc as xrc
import wx.lib.filebrowsebutton as filebrowse
import wx.lib.ClickableHtmlWindow
import time
import threading
import os
import shutil
import urllib
import urlparse
import pickle, bsddb.db, bsddb.dbshelve
import logging, logging.handlers
import inspect
import os.path
import webbrowser
import StringIO
from  localization import LanguageModule
from localization import catalog
from xml.dom.minidom import parseString

from   wxPython.wx import *
import gui.iPodderWindows

# Parts of iPodder
from ipodder import core
from ipodder import conlogging
from ipodder.configuration import *
from ipodder import feeds
from ipodder import state as statemodule
from ipodder import players
from ipodder import hooks
from ipodder import misc
from ipodder import grabbers
from ipodder import itunes
import gui, gui.images, gui.tree
import gui.scheduler as scheduler
from gui import OptionsDialog
from gui import clipboard

# Third-party parts of iPodder
from ipodder.contrib import feedparser
from ipodder.contrib import GenericDispatch

# Platform-specific parts
#if wx.Platform == '__WXMAC__':
#    from mac import wxae

# Skinning

from gui.skin import \
    STRIPE_EVEN_COLOR,\
    STRIPE_ODD_COLOR, \
    PRODUCT_NAME, \
    CURRENT_VERSION_URL, \
    SPLASH_LIFETIME, \
    SPLASH_DESTROY, \
    CLEANUP_FG

from gui import skin

#Debug params - Edit me
DEBUG = False
TIMER_INTERVAL = 10000

#GUI params -- Don't edit me.
ID_EXIT = 101
ID_CHECKNOW = 102
ID_OPEN = 103
ID_MAC_EXIT = 104
DOWNLOADS_INDEX = 0
SUBSCRIPTIONS_INDEX = 1
DIRECTORY_INDEX = 2
CLEANUP_INDEX = 3
LOGPAGE_INDEX = 4
MAX_DOWNLOADS_DISPLAY = 500

#This needs to be kept in sync with the "Repeat every"
#pulldown on the Scheduler tab.
INTERVAL_HOURS = [12.0,8.0,4.0,2.0,1.5,1.0,.5]

log = logging.getLogger('Juice')
SPAM = logging.DEBUG / 2

def trimurl(url): 
    method, site, path, query, ign2 = urlparse.urlsplit(url)
    sitesplit = site.split('.')
    if len(sitesplit) and sitesplit[0].startswith('www'): 
        site = '.'.join(sitesplit[1:])
    trimmed = "%s%s" % (site, path)
    if len(query) > 0:
        trimmed += "?%s" % query
    return trimmed

class iPodderSubscribeListener(threading.Thread):
    def __init__(self,caller,config):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.caller = caller
        self.server = self.get_server(config)
        if self.server:
            self.server.register_function(self.addFeed)
            self.server.register_function(self.addFeedFromRss)
            self.server.register_function(self.addFeedFromPcast)
            self.server.register_function(self.openPath)
            self.server.register_function(self.getHwnd)
            self.server.register_function(self.wake)
        else:
            log.info("""Can't listen for one-click requests because we were unable to get a TCP port.  Sorry!""")

    def get_server(self,config):
        import random
        from SimpleXMLRPCServer import SimpleXMLRPCServer
        ports = []
        if config.listen_port:
            ports.append(config.listen_port)
        #IANA dynamic/private ports: 49152-65535
        #http://www.iana.org/assignments/port-numbers
        ports.extend(random.sample(xrange(49152,65535),10))
        for port in ports:
            try:
                server = SimpleXMLRPCServer(("localhost", port),logRequests=0)
                log.info("Server listening on port %d" % port)
                if port != config.listen_port:
                    config.listen_port = port
                    config.flush()
                return server
            except Exception, e:
                log.info("Failed to get port %d, exception was: %s" % (port,str(e)))
        return None
    
    def run(self):
        self.server.serve_forever()

    def getHwnd(self):
        return self.caller.frame.GetHandle()

    def wake(self):
        self.caller.ThreadSafeDispatch(self.caller.OnTaskBarActivate,None)
        return 1
    
    def addFeed(self,url):
        url = misc.url_cmdline_extract(url)
        self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        return 1

    def addFeedFromRss(self,path):
        url = misc.url_rssfile_extract(path)
        self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        return 1

    def addFeedFromPcast(self,path):
        url = misc.url_pcast_file_extract(path)
        self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        return 1

    def openPath(self,path):
        if path.startswith("pcast://"):
            url = misc.url_cmdline_extract(path)
            self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)            
        elif path.startswith("podcast://"):
            url = misc.url_cmdline_extract(path)
            self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        elif path.endswith(".pcast"):
            url = misc.url_pcast_file_extract(path)
            self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        elif path.endswith(".rss"):
            url = misc.url_rssfile_extract(path)
            self.caller.ThreadSafeDispatch(self.caller.AddFeedFromListener,url)
        else:
            log.exception("open: file type for %s not supported" % path)

class iPodderCancel(threading.Thread):
    def __init__(self,caller,encinfos_to_cancel):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.caller = caller
        self.encinfos_to_cancel = encinfos_to_cancel

    def run(self):
        self.caller.ipodder.cancel_scan()
        if len(self.encinfos_to_cancel) > 0:
            self.caller.ipodder.cancel(self.encinfos_to_cancel)
        self.caller.CancelThreadComplete(self,self.encinfos_to_cancel)

class iPodderFeedDownload(threading.Thread):
    def __init__(self,caller,feedinfo):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.caller = caller
        self.feedinfo = feedinfo
        
    def run(self):
        enclosures = []
        fsj = core.FeedScanningJob(None, self.feedinfo, enclosures, state=self.caller.ipodder.state)        
        fsj.m_ipodder = self.m_ipodder
        fsj.m_frame = self.m_frame
        fsj.hooks.add('autherror',self.caller.FeedDownloadAuthError)
        fsj.run()
        self.caller.FeedDownloadThreadComplete(self,enclosures,self.feedinfo)    
    
class iPodderDownload(threading.Thread):
    def __init__(self,caller,mask=None,catchup=0):
        threading.Thread.__init__(self)
        self.caller = caller
        self.mask = mask
        self.catchup = catchup
    def run(self):
        if "Win" in platform.system():
            import pythoncom
            pythoncom.CoInitialize()

        self.caller.ipodder.start(self.caller.progress,self.mask,self.catchup)
        self.caller.DownloadThreadComplete(self,self.mask)
        
        if "Win" in platform.system():
            pythoncom.CoUninitialize()

class MySplashScreen(wx.SplashScreen):
    def __init__(self,basepath,parent):
        bmp = wx.Image(os.path.join(basepath,"images","splashscreen.bmp")).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 SPLASH_LIFETIME, parent, -1)
        #calling routine may destroy me when ready to show main app.


class MyLogWindowHandler(logging.Handler):
    def __init__(self,gui):
        logging.Handler.__init__(self)
        self.gui = gui

    def emit(self,record):

        if record.levelno >= logging.ERROR: 
            self.gui.ThreadSafeDispatch(self.gui.showlogpage, True)
        self.gui.ThreadSafeDispatch(self.gui.AppendLogWindow, record)
        
        #if record.levelno == logging.ERROR:
        #    import traceback
        #    ei = sys.exc_info()
        #    info = "".join(traceback.format_exception(ei[0], ei[1], ei[2]))
        #    del ei
        #    self.gui.ThreadSafeDispatch(self.gui.AppendLogWindow,info)
            
    def flush(self):
        self.gui.ThreadSafeDispatch(self.gui.ClearLogWindow)
        
class iPodderStatusBar(wx.StatusBar):
    def __init__(self, parent, log):
        wx.StatusBar.__init__(self, parent, -1)

        self.SetFieldsCount(2)
        self.SetStatusWidths([-2, 130])
        self.log = log
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.g1 = wx.Gauge(self, -1, 100, (self.GetRect()[2]-125, 16), (105, 15))
        self.g1.SetBezelFace(1)
        self.g1.SetShadowWidth(1)
                
        #self.Reposition()
        
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        
        self.g1.Hide()
        self.autohide = True
        
    def OnIdle(self, evt):
        if self.autohide:
            if self.g1.GetValue()==0:
                if self.g1.IsShown():
                    self.g1.Hide()           
            else:
                if not self.g1.IsShown():
                    self.g1.Show()
       
    def OnSize(self, evt):
        self.Reposition()  

    def Reposition(self):
        rect = self.GetFieldRect(1)
        
        self.g1.SetPosition((self.GetRect()[2]-125, 4))   

class FeedManagerOpmlFetcher(threading.Thread):
    def __init__(self,url,gui):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.url = url
        self.gui = gui

    def run(self):
        sio = StringIO.StringIO()
        grabber = grabbers.BasicGrabber(self.url, sio, politeness=0)
        try: 
            grabber()
        except grabbers.GrabError, ex: 
            log.error("Can't grab %s: %s", self.url, ex.message)
            return
        self.gui.ThreadSafeDispatch(self.gui.ReplaceFromManagerOpmlEnsuringPopulate, self.url, sio.getvalue())
        
class UpdateChecker(threading.Thread):
    def __init__(self, event, stringtable, currentlanguage, frame, gui):
        threading.Thread.__init__(self) 
        self.setDaemon(True)
        self.event = event
        self.m_stringtable = stringtable
        self.m_currentlanguage = currentlanguage
        self.frame = frame
        self.gui = gui

    def run(self):
        def getText(nodelist):
            rc = ""
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc = rc + node.data
            return rc

        try:
            sio = StringIO.StringIO()
            bg = grabbers.BasicGrabber(CURRENT_VERSION_URL, sio)
            bg()
            updates = parseString(sio.getvalue())
            #import urllib2
            #url = urllib2.urlopen(CURRENT_VERSION_URL)
            #from xml.dom.minidom import parse, parseString
            #updates = parse(url) 
            current_version_win = getText(updates.getElementsByTagName("current_version_win")[0].childNodes)    
            current_version_mac = getText(updates.getElementsByTagName("current_version_mac")[0].childNodes)    
            current_version_other = getText(updates.getElementsByTagName("current_version_other")[0].childNodes)    

            link = getText(updates.getElementsByTagName("link")[0].childNodes)    
            description= getText(updates.getElementsByTagName("description")[0].childNodes)    
        
            new_version = False
            current = float(__version__) # from ipodder.configuration
            if "Win" in platform.system():
                if (current < float(current_version_win)):
                    new_version = True
            elif "Darwin" in platform.system():
                if (current < float(current_version_mac)):
                    new_version = True
            else:
                if (current < float(current_version_other)):
                    new_version = True

        except:
            log.info("Exception checking for update at url %s" % CURRENT_VERSION_URL)
            if self.event:
                self.gui.ThreadSafeDispatch(self.notify_gui_error)
            return

        if self.event or new_version:
            self.gui.ThreadSafeDispatch(self.notify_gui, new_version, link, description)

    def notify_gui(self, new_version, link, description):

        if new_version:
            user_message = self.m_stringtable.GetText(self.m_currentlanguage, "str_new_version_ipodder")
            user_message += "\n\n" + str(description)
        else:
            user_message = self.m_stringtable.GetText(self.m_currentlanguage, "str_no_new_version_ipodder")
            
        if new_version:
            alert = wx.MessageDialog(self.frame, user_message, style=wx.OK|wx.CANCEL)
        else:
            alert = wx.MessageDialog(self.frame, user_message, style=wx.OK)
        
        response = alert.ShowModal()
        alert.Destroy()
        if response == wx.ID_OK:
            if new_version:
                webbrowser.open(str(link))                    

    def notify_gui_error(self):
        errmsg = self.m_stringtable.GetText(self.m_currentlanguage, "str_error_checking_new_version")
        alert = wx.MessageDialog(self.frame, errmsg, style=wx.OK)
        response = alert.ShowModal()
        alert.Destroy()

class KeyWatchingCaller(threading.Thread):
    def __init__(self, themethod, param, currenttable, duration):
        threading.Thread.__init__(self) 
        self.m_method = themethod
        self.m_param = param
        self.m_table = currenttable
        self.m_duration = duration
    def run(self):
        import time
        time.sleep(self.m_duration)
        if len(self.m_table)==1:
            self.m_method(self.m_param)
        self.m_table.remove(self)
        
def timed_search_subs(self):
    query = self.searchboxfeeds.GetValue()
    
    self.feedslist.DeleteAllItems()
    self.episodes.DeleteAllItems() 
 
    if len(query)==0:
        self.PopulateFeedsList()
        return 
 
    fds = self.ipodder.feeds

    count = 0
    self.feedsdict = {}

    for feedinfo in fds:
        if feedinfo.title:
            search_title = feedinfo.title
        else:
            search_title = feedinfo.url
        #print dir(feedinfo)
        if (query.lower() in search_title.lower())|(query.lower() in feedinfo.url.lower())|(query.lower() in feedinfo.sub_state.lower()):            
            if feedinfo.sub_state in ['unsubscribed', 'disabled'] \
                and not self.ipodder.config.debug:
                continue
            #if sub_state == 'preview':
            #    continue
            id = wx.NewId()
            self.feedsdict[id] = feedinfo

            if feedinfo.title:
                index = self.feedslist.InsertImageStringItem(0,feedinfo.title,self.lemon_idle_idx)
            else:
                index = self.feedslist.InsertImageStringItem(0,feedinfo.url,self.lemon_idle_idx)
            for i in range(0,2):
                self.feedslist.SetStringItem(0,1,self._("str_" + feedinfo.sub_state))
                self.feedslist.SetStringItem(0,2,'%4.1f' % feedinfo.mb_on_disk())
                self.feedslist.SetStringItem(0,3,trimurl(feedinfo.url))
                self.feedslist.SetItemData(0,id)
    self.mainpanel.ResetSortMixin()

def search_subs(self):
    kwc = KeyWatchingCaller(timed_search_subs, self, self.m_sptl_subs_threads, 0.75)
    self.m_sptl_subs_threads.append(kwc)
    kwc.start()
    return

def timed_search_downloads(self):
    query = self.searchboxdownloads.GetValue()
    self.downloads.DeleteAllItems()
    for encinfo in self.m_encinfolist:
        if (query.lower() in str(encinfo.item_title).lower())|(query.lower() in str(encinfo.feed).lower())|(query.lower() in str(encinfo.url).lower())|(query.lower() in str(encinfo.status)):
            self.DownloadTabLog(encinfo,prune=False)
    self.DownloadTabPrune()
    
def search_downloads(self):
    kwc = KeyWatchingCaller(timed_search_downloads, self, self.m_sptl_dwnl_threads, 0.75)
    self.m_sptl_dwnl_threads.append(kwc)
    kwc.start()
    return

class IPG_Encoding:
    """Mixin class to provide encoding dialog."""

    def InitMixin(self, res, xrc):
        """Initialise the mixin with res, xrc."""
        self.encodingdlg = res.LoadDialog(None, "ENCODINGDIALOG")
        if hasattr(self.encodingdlg,'MacSetMetalAppearance'):
            self.encodingdlg.MacSetMetalAppearance(True)
        self.encodingdlg.Show(0)
        self.encodingdlg.Init(self)
        
class IPG_Preferences:
    """Mixin class to provide preferences dialog."""

    def InitMixin(self, res, xrc): 
        """Initialise the mixin with res, xrc."""
        self.preferences = res.LoadDialog(None, "PREFERENCES")
        if hasattr(self.preferences, 'MacSetMetalAppearance'):
            self.preferences.MacSetMetalAppearance(True)
        self.preferences.Show(0)
        self.preferences.Init(self.ipodder, self)

class IPG_Menu: 
    """Mixin class to provide the menu."""

    def InitMixin(self, res, xrc): 
        """Initialise the mixin with res, xrc."""

        # Quirky logic for wiring up special Mac menus.  Don't ask why, it just works.
        if wx.Platform == '__WXMAC__':
            # delete about entry in help menu
            self.menubar.GetMenu(4).DeleteItem(self.menubar.GetMenu(4).FindItemByPosition(9))

            # delete quit entry in file menu (is added with correct shortcut in correct place
            # but item there is not localizable)
            self.menubar.GetMenu(0).DeleteItem(self.menubar.GetMenu(0).FindItemByPosition(5))
            
            # delete preference entry in file menu
            self.menubar.GetMenu(0).DeleteItem(self.menubar.GetMenu(0).FindItemByPosition(2))

            self.SetMacExitMenuItemId(ID_MAC_EXIT)
            wx.EVT_MENU(self, ID_MAC_EXIT, self.OnExit)

            aboutmenu = wx.Menu()             
            item = aboutmenu.Append(wxID_ABOUT, 'About...','') 
            self.Bind(wx.EVT_MENU, self.OnMenuAbout, item) 
            self.menubar.Append(aboutmenu,'&Help')    

            filemenu = self.menubar.GetMenu(0)
            item = filemenu.Insert(2,wxID_PREFERENCES, '&Preferences','') 
            self.Bind(wx.EVT_MENU, self.OnMenuPreferences, item)

        else:
            wx.EVT_MENU(self,xrc.XRCID("MENUBARABOUT"), self.OnMenuAbout)
            wx.EVT_MENU(self,xrc.XRCID("MENUBARPREFERENCES"), self.OnMenuPreferences)
            wx.EVT_MENU(self,xrc.XRCID("MENUBARQUIT"), self.OnExit)
            
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCLOSE"), self.OnCloseWindow)
        wx.EVT_MENU(self,xrc.XRCID("MENUBAROPMLEXPORT"), self.OnMenuOpmlExport)
        wx.EVT_MENU(self,xrc.XRCID("MENUBAROPMLIMPORT"), self.OnMenuOpmlImport)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCHECKALL"), self.OnCheckNow)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCATCHUP"), self.OnCatchup)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARADDFEED"), self.OnMenuAddFeed)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARDOWNLOADS"), self.OnMenuDownloads)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARSUBSCRIPTIONS"), self.OnMenuSubscriptions)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCLEANUP"), self.OnMenuCleanup)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARLICENSE"), self.OnMenuLicense)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARDIRECTORY"), self.OnMenuDirectory)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARSCHEDULER"), self.OnMenuScheduler)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARHELP"), self.OnMenuHelp)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARFAQ"), self.OnMenuFaq)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARGOTOWEBSITE"), self.OnMenuGotoWebsite)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARDONATE"), self.OnMenuDonate)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARREPORTPROBLEM"), self.OnMenuReportProblem)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCHECKFORUPDATES"), self.OnMenuCheckForUpdates)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARFEEDPROPERTIES"), self.OnOpenFeedProperties)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARREMOVEFEED"), self.OnToggleChecked)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARSELECTALL"), self.OnMenuSelectAll)
        wx.EVT_MENU(self,xrc.XRCID("MENUBARCHECKSELECTED"), self.OnCheckSelected)

        #Edit menu
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self,xrc.XRCID("NOTEBOOK"), self.OnNotebookPageChanged)
        self.FrobMenus()

    def OnMenuPreferences(self,event):
        """Show the Preferences dialog."""
        oldfocus = self.frame.FindFocus()
        self.preferences.ShowModal()
        if oldfocus:
            oldfocus.SetFocus()
        
    def OnMenuOpmlExport(self,event):
        dlg = wx.FileDialog(self.frame,self.m_stringtable.GetText(self.m_currentlanguage, "str_choose_name_export_file"),self.ipodder.config.download_dir,"ipodder-subscriptions.opml","*.opml",style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
          self.ipodder.feeds.write_to_opml_file(dlg.GetPath())
          alert = wx.MessageDialog(self.frame, self.m_stringtable.GetText(self.m_currentlanguage, "str_subs_exported"), style=wx.OK)
          alert.ShowModal()
          alert.Destroy()
          
        dlg.Destroy()

    def OnMenuOpmlImport(self,event):
        dlg = wx.FileDialog(self.frame,self.m_stringtable.GetText(self.m_currentlanguage, "str_select_import_file"),self.ipodder.config.download_dir,"subscriptions.opml","*.opml",style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
          n = self.ipodder.feeds.absorb_from_opml_file(dlg.GetPath())
          if n == None:
              message = "There was an error importing the file.  Sorry it didn't work out."
          else:
              message = "%d feeds imported." % n
          alert = wx.MessageDialog(self.frame, message, style=wx.OK)
          alert.ShowModal()
          alert.Destroy()
          self.PopulateFeedsList()

        dlg.Destroy()

    def OnMenuAbout(self,event):
        oldfocus = self.frame.FindFocus()
        self.about.ShowModal()
        if oldfocus:
            oldfocus.SetFocus()
        
    def OnMenuAddFeed(self,event):
        oldfocus = self.frame.FindFocus()
        self.feedwindow.UpdateFeed(None,self.ipodder,newfeed="")
        if oldfocus:
            oldfocus.SetFocus()
        
    def OnMenuDownloads(self,event):
        self.notebook.SetSelection(DOWNLOADS_INDEX)

    def OnMenuSubscriptions(self,event):
        self.notebook.SetSelection(SUBSCRIPTIONS_INDEX)
        
    def OnMenuDirectory(self,event):
        self.notebook.SetSelection(DIRECTORY_INDEX)

    def OnMenuScheduler(self,event):
        oldfocus = self.frame.FindFocus()
        self.scheddialog.ShowModal()
        if oldfocus:
            oldfocus.SetFocus()
        
    def OnMenuCleanup(self,event):
        self.notebook.SetSelection(CLEANUP_INDEX)

    def OnMenuSubmitLang(self,event):
        webbrowser.open("http://juicereceiver.sourceforge.net/submitlanguage/")

    def OnMenuHelp(self,event):
        webbrowser.open("http://juicereceiver.sourceforge.net/docs/")

    def OnMenuFaq(self,event):
        webbrowser.open("http://juicereceiver.sourceforge.net/faq/")

    def OnMenuGotoWebsite(self,event):
        webbrowser.open("http://juicereceiver.sourceforge.net/")

    def OnMenuDonate(self,event):
        webbrowser.open("http://sourceforge.net/donate/index.php?group_id=118306")

    def OnMenuReportProblem(self,event):
        webbrowser.open("http://sourceforge.net/tracker/?group_id=118306&atid=681694")

    def OnMenuCheckForUpdates(self,event):
        upc = UpdateChecker(event, self.m_stringtable, self.m_currentlanguage, self.frame, self);
        upc.start()
        
class IPG_Language: 
    """Mixin class to provide language services."""
    
    def InitMixin(self, res, xrc): 
        pass###

    def OnMenuLang(self, event):
        self.SetLanguages(self.menulangdict[event.GetId()])

class IPG_DownloadRate: 
    """Mixin class to provide download rate hooks, etc."""

    def InitMixin(self, res, xrc, pb): 
        """Initialise the mixin with res, xrc."""
        log.debug("IPG_DownloadRate initialised.")
        self.__live = xrc.XRCCTRL(self.frame, "DL_LIVE")
        self.__ulspeed = xrc.XRCCTRL(self.frame, "DL_ULSPEED")
        self.__dlspeed = xrc.XRCCTRL(self.frame, "DL_DLSPEED")
        self.__pb = pb

    def hook_download_content_rate(self, live, ulrate, dlrate, percent): 
        """This is hooked to iPodder's download-content-rate by InitHooks."""
        dispatch = self.ThreadSafeDispatch
        dispatch(self.__live.SetLabel, "%1d" % live)
        dispatch(self.__ulspeed.SetLabel, "%.1fkB/s" % (ulrate/1024.0))
        dispatch(self.__dlspeed.SetLabel, "%.1fkB/s" % (dlrate/1024.0))
        dispatch(self.__pb.SetValue, percent)

class IPG_Skin:
    """Mixin class to provide a linked banner logo"""
    def InitMixin(self,xrc):
        toolbarbanner = xrc.XRCCTRL(self.frame, "TOOLBARBANNER")
        if not hasattr(skin, "GetBannerImage"):
            sizer = toolbarbanner.GetContainingSizer()
            sizer.Clear(True)
            notebook = xrc.XRCCTRL(self.frame, "NOTEBOOK")
            notebook.GetContainingSizer().Remove(sizer)
        else:
            toolbarbanner.DeleteTool(xrc.XRCID("TOOLBANNER"))
            bmp = skin.GetBannerImage().ConvertToBitmap()
            toolbarbanner.SetToolBitmapSize(bmp.GetSize())
            toolid = wx.NewId()
            toolbarbanner.AddSimpleTool(toolid,bmp)
            toolbarbanner.Realize()
            if hasattr(skin, "BANNER_URL"):
                wx.EVT_TOOL(self, toolid, self.OnBannerClick)

class iPodderGui(wx.App, 
                 GenericDispatch.GenericDispatchMixin, 
                 wx.Frame,
                 IPG_Preferences,
                 IPG_Menu,
                 IPG_DownloadRate,
                 IPG_Language,
                 IPG_Encoding,
                 IPG_Skin
                 ):

    def __init__(self,ipodder,options):
        self.ipodder = ipodder
        self.options = options
        
        # wxApp usually sends error messages to a wxWindow. This can be a problem if you are trying to debug 
        # a crash, the window disappears before you can see the traceback. The first argument to wxApp is 
        # redirect=True, the second is filename=None. You specify a filename to write to that file, or 
        # specify false to redirect to write to the console.
        wx.App.__init__(self, False, None)
        GenericDispatch.GenericDispatchMixin.__init__(self)
        
    def OnMenuLicense(self, event):
        oldfocus = self.frame.FindFocus()
        alert = wx.MessageDialog(self.frame, self.m_stringtable.GetText(self.m_currentlanguage, "str_license"), style=wx.OK, caption=self._("str_license_caption"))
        response = alert.ShowModal()
        alert.Destroy()
        if oldfocus:
            oldfocus.SetFocus()
        if response != wx.ID_OK:
            return

    def InitLanguageMenu(self):
        "Update language menu, it behaves as a radiomenu."

        langmenuitem = self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTLANGUAGE"))
        langmenu = langmenuitem.GetSubMenu()

        #Clear old items to handle Cancels.
        while langmenu.GetMenuItemCount():
            langmenu.DeleteItem(langmenu.FindItemByPosition(0))
        
        for lang in LanguageModule.supported_languages():
            id = wx.NewId()
            try: 
                langmenu.AppendRadioItem(id,catalog.get_language_name(lang))
                self.menulangdict[id] = lang
                wx.EVT_MENU(self, id, self.OnMenuLang)
                if self.m_currentlanguage == lang:
                    self.menubar.FindItemById(id).Check()
            except TypeError, ex: 
                log.exception("Can't append language menu item.")

        langmenu.AppendSeparator()
        id = wx.NewId()
        langmenu.Append(id, self._("str_submit_lang"))
        wx.EVT_MENU(self, id, self.OnMenuSubmitLang)

    def EnableLanguages(self, enable=True):
        langmenuitem = self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTLANGUAGE"))
        langmenu = langmenuitem.GetSubMenu()
        for i in range(langmenu.GetMenuItemCount()):
             langmenu.FindItemByPosition(i).Enable(enable)
             
    def SetLanguages(self, newlanguage=None):
        """Set the widget labels to the translations in self.m_currentlanguage.  Optionally
           prompt to change to newlanguage if it's not None."""

        if newlanguage:
            self.m_stringtable.LoadLanguage(newlanguage)
            alert = wx.MessageDialog(self.frame, self.m_stringtable.GetText(newlanguage, "str_localization_restart"), style=wx.OK|wx.CANCEL)
            response = alert.ShowModal()
            alert.Destroy()
            if response != wx.ID_OK:
                self.InitLanguageMenu()
                return
            else:
                self.ipodder.config.screen_language = self.m_currentlanguage = newlanguage
                self.ipodder.config.flush()
                self.OnExit(None)   

        # title
        self.frame.SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_ipodder_title"))
        
        # menus 
        self.menubar.SetLabelTop(0, self.m_stringtable.GetText(self.m_currentlanguage, "str_file"))                

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBAROPMLIMPORT")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBAROPMLIMPORT")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_import_opml"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBAROPMLIMPORT")).SetAccel(tmp_accell)   
        
        self.menubar.FindItemById(xrc.XRCID("MENUBAROPMLEXPORT")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_export_opml"))        

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_close_window"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).SetAccel(tmp_accell)   


        self.menubar.SetLabelTop(1, self.m_stringtable.GetText(self.m_currentlanguage, "str_edit"))                

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTALL")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTALL")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_select_all"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTALL")).SetAccel(tmp_accell)   

        self.menubar.SetLabelTop(3, self.m_stringtable.GetText(self.m_currentlanguage, "str_tools"))

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKALL")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKALL")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_check_all"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKALL")).SetAccel(tmp_accell)   

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARCATCHUP")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARCATCHUP")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_catch_up"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARCATCHUP")).SetAccel(tmp_accell)   

        self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKSELECTED")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_check_selected"))

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARREMOVEFEED")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARREMOVEFEED")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_remove_selected"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARREMOVEFEED")).SetAccel(tmp_accell)   

        self.menubar.FindItemById(xrc.XRCID("MENUBARFEEDPROPERTIES")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_feed_properties"))

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARADDFEED")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARADDFEED")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_add_feed"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARADDFEED")).SetAccel(tmp_accell)   

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARSCHEDULER")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARSCHEDULER")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_scheduler_menubar"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARSCHEDULER")).SetAccel(tmp_accell)   

        self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTLANGUAGE")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_select_language"))
        
        #self.menubar.SetLabelTop(3, self.m_stringtable.GetText(self.m_currentlanguage, "str_select_language"))                        

        self.InitLanguageMenu()

        self.menubar.SetLabelTop(2, self.m_stringtable.GetText(self.m_currentlanguage, "str_view"))                
        self.menubar.FindItemById(xrc.XRCID("MENUBARDOWNLOADS")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_downloads"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARSUBSCRIPTIONS")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_subscriptions"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARDIRECTORY")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_podcast_directory"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARCLEANUP")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_cleanup"))

        if wx.Platform == '__WXMAC__':
            #Regardless of language we have to set the Help menu label
            #to "&Help" to avoid duplication.
            self.menubar.SetLabelTop(4,"&Help")
        else:
            self.menubar.SetLabelTop(4, self.m_stringtable.GetText(self.m_currentlanguage, "str_help"))                        

        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARHELP")).GetAccel()
        self.menubar.FindItemById(xrc.XRCID("MENUBARHELP")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_online_help"))        
        self.menubar.FindItemById(xrc.XRCID("MENUBARHELP")).SetAccel(tmp_accell)   

        self.menubar.FindItemById(xrc.XRCID("MENUBARFAQ")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_faq"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKFORUPDATES")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_check_for_update"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARREPORTPROBLEM")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_report_a_problem"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARGOTOWEBSITE")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_goto_website"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARDONATE")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_make_donation"))
        
        self.menubar.FindItemById(xrc.XRCID("MENUBARLICENSE")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_menu_license"))

        if wx.Platform != '__WXMAC__':
            self.menubar.FindItemById(xrc.XRCID("MENUBARABOUT")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_about"))            
             
            # quit menu gets added on osx automatically // so not declared      
            # save the accelerator (bug in windows?)
            tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARQUIT")).GetAccel()
            self.menubar.FindItemById(xrc.XRCID("MENUBARQUIT")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_quit"))        
            self.menubar.FindItemById(xrc.XRCID("MENUBARQUIT")).SetAccel(tmp_accell)   
            self.menubar.FindItemById(xrc.XRCID("MENUBARPREFERENCES")).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_preferences_menubar")) 
        else:
            self.menubar.FindItemById(wxID_ABOUT).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_about")) 
            self.menubar.FindItemById(wxID_PREFERENCES).SetText(self.m_stringtable.GetText(self.m_currentlanguage, "str_preferences_menubar")) 
                   
        # set the tabs
        tabslist = [
            (self.notebook, DOWNLOADS_INDEX, "str_downloads"),
            (self.notebook, SUBSCRIPTIONS_INDEX, "str_subscriptions"),
            (self.notebook, DIRECTORY_INDEX, "str_podcast_directory"),
            (self.notebook, CLEANUP_INDEX, "str_cleanup"),
            (self.schednotebook, 0, "str_scheduler_tab")]
        en_loaded = False
        for (nb, idx, key) in tabslist:
            try:
                nb.SetPageText(idx, self._(key))
            except AssertionError:
                """Unfortunately wide characters and Notebooks don't mix well
                on Mac, so we fall back to English."""
                if not en_loaded:
                    self.m_stringtable.LoadLanguage(LanguageModule.ENGLISH)
                    en_loaded = True
                try:
                    nb.SetPageText(idx,self.m_stringtable.GetText(LanguageModule.ENGLISH,key))
                except AssertionError:
                    #This shouldn't happen but somehow does when shutting down
                    #after switching to German.  Go figure.
                    pass

        try: 
          self.notebook.SetPageText(LOGPAGE_INDEX, self.m_stringtable.GetText(self.m_currentlanguage, "str_log"))
        except:
            pass

        self.toolbarDownloads.SetToolShortHelp(xrc.XRCID("TOOLHISTPAUSESELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_pause_selected"))
        self.toolbarDownloads.SetToolShortHelp(xrc.XRCID("TOOLHISTCANCELSELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_cancel_selected_download"))
        self.toolbarDownloads.SetToolShortHelp(xrc.XRCID("TOOLHISTCLEARSELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_remove_selected_items"))

        xrc.XRCCTRL(self.frame, "DL_LIVE_LABEL").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_dltab_live"))
        xrc.XRCCTRL(self.frame, "DL_ULSPEED_LABEL").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_dltab_ul_speed"))
        xrc.XRCCTRL(self.frame, "DL_DLSPEED_LABEL").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_dltab_dl_speed"))

        self.frame.SetStatusText(self.m_stringtable.GetText(self.m_currentlanguage, "str_check_for_new_podcast_button"))
        self.toolbarSubscr.SetToolShortHelp(self.toolCheckAllId,self.m_stringtable.GetText(self.m_currentlanguage, "str_check_for_new_podcasts"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLADDFEED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_add_new_feed"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLTOGGLECHECKED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_remove_selected_feed"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLFEEDPROPERTIES"),self.m_stringtable.GetText(self.m_currentlanguage, "str_properties"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLCHECKSELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_check_selected_feed"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLCATCHUP"),self.m_stringtable.GetText(self.m_currentlanguage, "str_catch_up_mode"))

        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLHISTPAUSESELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_pause_selected"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLHISTCANCELSELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_cancel_selected_download"))
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLHISTCLEARSELECTED"),self.m_stringtable.GetText(self.m_currentlanguage, "str_remove_selected_items"))
        
        self.toolbarDirectory.SetToolShortHelp(xrc.XRCID("TOOLREFRESHDIR"), self._("str_refresh"))
        self.toolbarDirectory.SetToolShortHelp(xrc.XRCID("TOOLOPENDIRALL"), self._("str_open_all_folders"))
        self.toolbarDirectory.SetToolShortHelp(xrc.XRCID("TOOLCLOSEDIR"), self._("str_close_all_folders"))

        xrc.XRCCTRL(self.frame, "DIRECTORY_DESCRIPTION").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_directory_description"))
        xrc.XRCCTRL(self.frame, "ID_ADDFEED").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_add"))

        xrc.XRCCTRL(self.frame, "SELECTAFEED").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_select_a_feed"))
        xrc.XRCCTRL(self.frame, "CLEANUPREFRESH").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_refresh_cleanup"))
        xrc.XRCCTRL(self.frame, "LOOKFOREPISODES").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_look_in"))
        xrc.XRCCTRL(self.frame, "CLEANUPSRCPLAYER").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_player_library"))
        xrc.XRCCTRL(self.frame, "CLEANUPSRCFOLDER").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_downloads_folder"))
        xrc.XRCCTRL(self.frame, "CLEANUPDELLIBRARY").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_delete_library_entries"))
        xrc.XRCCTRL(self.frame, "CLEANUPDELFILES").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_delete_files"))
        xrc.XRCCTRL(self.frame, "CLEANUPCHECKALL").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_select_all_cleanup"))
        xrc.XRCCTRL(self.frame, "CLEANUPCHECKNONE").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_select_none_cleanup"))
        xrc.XRCCTRL(self.frame, "CLEANUPDELETE").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_delete"))

        xrc.XRCCTRL(self.frame, "ID_CLEARLOG").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_clear"))
        xrc.XRCCTRL(self.frame, "NEXTRUNLABEL").SetLabel(self.m_stringtable.GetText(self.m_currentlanguage, "str_next_run"))

        # Windows and Linux taskbar right-click menu
        if wx.Platform != '__WXMAC__':
            self.menu.FindItemById(ID_CHECKNOW).SetText(self._("str_check_now"))
            self.menu.FindItemById(ID_EXIT).SetText(self._("str_quit"))
            self.menu.FindItemById(ID_OPEN).SetText(self._("str_open_ipodder"))

        # Feed right-click menu
        for (id,key) in [(self.feedmenu_checknow_id,"str_check_now"),\
                         (self.feedmenu_remove_id,"str_remove"),\
                         (self.feedmenu_openinbrowser_id,"str_open_in_browser"),\
                         (self.feedmenu_openfolder_id,"str_open_downloads_folder"),\
                         (self.feedmenu_properties_id,"str_properties")]:
            self.feedmenu.FindItemById(id).SetText(self._(key))

        for (id,key) in [(self.directory_refresh_id,"str_refresh")]:
            self.directory_root_menu.FindItemById(id).SetText(self._(key))

        # Feed properties
        xrc.XRCCTRL(self.feedwindow, "FEEDWINGOTOSUBS").SetLabel(self._("str_goto_subs"))
        xrc.XRCCTRL(self.feedwindow, "FEEDWINCANCEL").SetLabel(self._("str_cancel"))
        xrc.XRCCTRL(self.feedwindow, "FEEDWINOK").SetLabel(self._("str_save"))
        self.feedwindow.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, xrc.XRCID("FEEDWINCANCEL"))
            ]))

        # Scheduler dialog
        
        xrc.XRCCTRL(self.scheddialog, "SCHEDDIALOG").SetLabel(self._("str_scheduler_dialog"))
        xrc.XRCCTRL(self.scheddialog, "SCHEDSELECTTYPE").SetLabel(self._("str_sched_select_type"))
        xrc.XRCCTRL(self.scheddialog, "LBL_LASTRUN").SetLabel(self._("str_latest_run"))
        xrc.XRCCTRL(self.scheddialog, "LBL_NEXTRUN").SetLabel(self._("str_next_run"))
        xrc.XRCCTRL(self.scheddialog, "SAVESCHED").SetLabel(self._("str_save"))
        xrc.XRCCTRL(self.scheddialog, "CANCELSCHED").SetLabel(self._("str_cancel"))
        xrc.XRCCTRL(self.scheddialog, "ENABLEAUTO").SetLabel(self._("str_enable_scheduler"))
        xrc.XRCCTRL(self.scheddialog, "SCHEDSPECIF").SetLabel(self._("str_sched_specific"))
        xrc.XRCCTRL(self.scheddialog, "SCHEDREG").SetLabel(self._("str_sched_reg"))
        xrc.XRCCTRL(self.scheddialog, "REPEATEVERY").SetLabel(self._("str_repeat_every"))
                    
        # donations
        xrc.XRCCTRL(self.donatedialog, "DONATEEXPL").SetLabel(self._("str_donate_expl"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSYES").SetLabel(self._("str_donate_yes"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSTWOWEEKS").SetLabel(self._("str_donate_two_weeks"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSALREADY").SetLabel(self._("str_donate_already"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSNO").SetLabel(self._("str_donate_no"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSONEDAY").SetLabel(self._("str_donate_one_day"))
        xrc.XRCCTRL(self.donatedialog, "DONATIONSPROCEED").SetLabel(self._("str_donate_proceed"))                

        sel = self.schedinterval.GetSelection()
        self.schedinterval.Clear()
        self.schedinterval.AppendItems([ \
            "12 %s" % self._("str_hours"),\
            "8 %s" % self._("str_hours"),\
            "4 %s" % self._("str_hours"),\
            "2 %s" % self._("str_hours"),\
            "90 %s" % self._("str_minutes"),\
            "60 %s" % self._("str_minutes"),\
            "30 %s" % self._("str_minutes") ])
        if sel != wx.NOT_FOUND:
            self.schedinterval.SetSelection(sel)

    def OnSearchKeyUp(self, event):
        search_subs(self)

    def OnSearchDownloadsKeyUp(self, event):
        search_downloads(self)
                    
    def OnInit(self):
        #if wx.Platform == '__WXMAC__':            
        #    wxae.setgurlhandler(self.handleMacGURL)
        if not self.ipodder.config.screen_language or \
            LanguageModule.supported_languages().count(self.ipodder.config.screen_language) == 0:
            self.ipodder.config.screen_language = LanguageModule.get_default(self.ipodder.config.screen_language)
            self.ipodder.config.flush()
        self.m_currentlanguage = self.ipodder.config.screen_language
        self.m_stringtable = LanguageModule.StringTable(self.m_currentlanguage)
        
        self.basepath = abspath(split(sys.argv[0])[0])
        if scheduler.ensure_config(self.ipodder.config,\
                                   self.ipodder.config.schedule_file):
            self.ipodder.config.flush()
        self.s = scheduler.Scheduler(self.ipodder.config)
        self.s.initScheduledRuns()
        self.t1 = wx.Timer(self)
        self.quitting = False
        self.waiting_for_quit = False
        self.ready_to_quit = False
        self.selected_tool_dict = {} #for Mac
        self.menulangdict = {}
        self.hooks = hooks.HookCollection()

        res = xrc.XmlResource(self.ipodder.config.guiresource_file)


        #put here all elements
        self.frame = res.LoadFrame(None,"TOPWINDOW")
        self.ipodder.m_gui = self
                
        self.splash = splash = MySplashScreen(self.basepath,self.frame)
        splash.Show()

        self.sb = iPodderStatusBar(self.frame, log)
        self.progressBar  = self.sb.g1
                        
        # Now we have both res and xrc, we can initialise any mixins 
        # (self.frame is also required as an argument to xrc.XRCCTRL). 
        #
        # Ultimately, we should be able to move all of the following code 
        # (~600 lines!) and associated methods and hooks into little 
        # mixin classes so we can easily find the code we want to work on. 
        IPG_Encoding.InitMixin(self, res, xrc)
        IPG_Preferences.InitMixin(self, res, xrc)
        IPG_DownloadRate.InitMixin(self, res, xrc, self.progressBar) 
        IPG_Skin.InitMixin(self, xrc)
        
        if hasattr(self.frame, 'MacSetMetalAppearance'):
            self.frame.MacSetMetalAppearance(True)
        
        self.frame.SetStatusBar(self.sb)

        self.menubar = res.LoadMenuBar("MENUBAR")
        
        self.about = res.LoadDialog(None,"ABOUT")
        if hasattr(self.about, 'MacSetMetalAppearance'):
            self.about.MacSetMetalAppearance(True)
        self.aboutversion = xrc.XRCCTRL(self.about,"ABOUTVERSION")
        self.aboutversion.SetLabel("Version: %s" % core.__version__)
        self.about.SetTitle(self._("str_about"))
        
        self.scheddialog = res.LoadDialog(None,"SCHEDDIALOG")
        if hasattr(self.scheddialog, 'MacSetMetalAppearance'):
            self.scheddialog.MacSetMetalAppearance(True)


        if wx.Platform == '__WXMAC__':
            self.donatedialog = res.LoadDialog(None,"DONATEDIALOG_MAC")
        else:
            self.donatedialog = res.LoadDialog(None,"DONATEDIALOG_WIN")

        if hasattr(self.donatedialog, 'MacSetMetalAppearance'):
            self.donatedialog.MacSetMetalAppearance(True)
        self.donatedialog.SetTitle(self._("str_donate"))
        
        self.frame.SetMenuBar(self.menubar)
        self.feedwindow = res.LoadDialog(self.frame,"FEEDWIN")
        if hasattr(self.feedwindow, 'MacSetMetalAppearance'):
            self.feedwindow.MacSetMetalAppearance(True)

        self.feedwindow.ipodder = self.ipodder
        self.mainpanel = xrc.XRCCTRL(self.frame,"MAINPANEL")
        self.feedslist = xrc.XRCCTRL(self.frame, "SUBSCTRL")
        self.episodes = xrc.XRCCTRL(self.frame, "EPISODES")
        self.downloads = xrc.XRCCTRL(self.frame, "DOWNLOADSCTRL")

        self.logwindow = xrc.XRCCTRL(self.frame, "LOGWINDOW")
        
        self.myTextCtrl = xrc.XRCCTRL(self.frame, "URLCTRL")
        
        self.schedPanel = xrc.XRCCTRL(self.scheddialog, "SCHEDULER")
        self.schedinterval = xrc.XRCCTRL(self.scheddialog, "SCHEDINTERVAL")
        self.repeatevery = xrc.XRCCTRL(self.scheddialog, "REPEATEVERY")
        self.schedspecific = xrc.XRCCTRL(self.scheddialog, "SCHEDSPECIF")
        self.schedreg = xrc.XRCCTRL(self.scheddialog, "SCHEDREG")
        self.savesched = xrc.XRCCTRL(self.scheddialog, "SAVESCHED")
        self.enableauto = xrc.XRCCTRL(self.scheddialog, "ENABLEAUTO")
        self.lastrun = xrc.XRCCTRL(self.scheddialog, "LASTRUN")
        self.nextrun = xrc.XRCCTRL(self.scheddialog, "NEXTRUN")
        self.nextrun2 = xrc.XRCCTRL(self.frame, "NEXTRUN2")

        self.oldPrefsPanel = xrc.XRCCTRL(self.frame, "PREFERENCES")

        #self.aboutTitle = xrc.XRCCTRL(self.frame, "ABOUTTITLE")
        self.toolbarSubscr = xrc.XRCCTRL(self.frame, "TOOLBARSUBSCR")
        self.toolCheckAllId = xrc.XRCID("TOOLCHECKALL")
        self.toolCatchupId = xrc.XRCID("TOOLCATCHUP")
        self.toolCheckSelectedId = xrc.XRCID("TOOLCHECKSELECTED")
        self.toolToggleCheckedId = xrc.XRCID("TOOLTOGGLECHECKED")
        self.toolFeedPropertiesId = xrc.XRCID("TOOLFEEDPROPERTIES")
        self.toolScheduler = self.toolbarSubscr.FindById(xrc.XRCID("TOOLSCHEDULER"))
        self.toolbarDirectory = xrc.XRCCTRL(self.frame, "TOOLBARDIRECTORY")
        self.toolRefreshDirId = xrc.XRCID("TOOLREFRESHDIR")
        self.toolOpenDirAllId = xrc.XRCID("TOOLOPENDIRALL")
        self.toolCloseDirId = xrc.XRCID("TOOLCLOSEDIR")
        self.aboutPanel = xrc.XRCCTRL(self.frame, "ABOUT")
        self.notebook = xrc.XRCCTRL(self.frame, "NOTEBOOK")
        self.schednotebook = xrc.XRCCTRL(self.scheddialog, "SCHEDNOTEBOOK")
        self.logPage = self.notebook.GetPage(LOGPAGE_INDEX)
        self.opmltree = xrc.XRCCTRL(self.frame, "OPMLTREE")
        self.searchboxfeeds = xrc.XRCCTRL(self.frame, "SEARCHBOXFEEDS")
        self.searchboxfeeds.Bind(wx.EVT_KEY_UP, self.OnSearchKeyUp)
        self.cleanupfeeds = xrc.XRCCTRL(self.frame, "CLEANUPFEEDS")
        self.cleanupepisodes = xrc.XRCCTRL(self.frame, "CLEANUPEPISODES")
        self.cleanupdelete = xrc.XRCCTRL(self.frame, "CLEANUPDELETE")
        self.cleanuprefresh = xrc.XRCCTRL(self.frame, "CLEANUPREFRESH")
        self.cleanupdellibrary = xrc.XRCCTRL(self.frame, "CLEANUPDELLIBRARY")
        self.cleanupdelfiles = xrc.XRCCTRL(self.frame, "CLEANUPDELFILES")
        self.cleanupsrcplayer = xrc.XRCCTRL(self.frame, "CLEANUPSRCPLAYER")
        self.cleanupsrcfolder = xrc.XRCCTRL(self.frame, "CLEANUPSRCFOLDER")
        self.toolbarDownloads = xrc.XRCCTRL(self.frame, "TOOLBARHIST")
        self.toolClearHistSelId = xrc.XRCID("TOOLHISTCLEARSELECTED")
        self.toolCancelHistSelId = xrc.XRCID("TOOLHISTCANCELSELECTED")
        self.menucheckall = self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKALL"))
        self.menucheckselected = self.menubar.FindItemById(xrc.XRCID("MENUBARCHECKSELECTED"))
        self.menuremovefeed = self.menubar.FindItemById(xrc.XRCID("MENUBARREMOVEFEED"))
        self.menufeedproperties = self.menubar.FindItemById(xrc.XRCID("MENUBARFEEDPROPERTIES"))
        self.menucatchup = self.menubar.FindItemById(xrc.XRCID("MENUBARCATCHUP"))
        self.menuselectall = self.menubar.FindItemById(xrc.XRCID("MENUBARSELECTALL"))
        self.cleanupsrcplayer.SetValue(1)
        self.cleanupsrcfolder.SetValue(1)
        self.cleanupdellibrary.SetValue(1)
        self.cleanupdelfiles.SetValue(1)
        
        #wiring: subscriptions tab
        wx.EVT_TOOL(self, xrc.XRCID("TOOLCHECKSELECTED"),self.OnCheckSelected)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLCHECKALL"),self.OnCheckNow)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLSCHEDULER"),self.OnMenuScheduler)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLCATCHUP"),self.OnCatchup)
        wx.EVT_BUTTON(self, xrc.XRCID("ID_HIDE"), self.OnHide)
        wx.EVT_BUTTON(self, xrc.XRCID("ID_EXIT"), self.OnExit)
        wx.EVT_BUTTON(self, xrc.XRCID("ID_ADDFEED"), self.OnAddFeed)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLADDFEED"), self.OnMenuAddFeed)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLTOGGLECHECKED"), self.OnToggleChecked)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLFEEDPROPERTIES"), self.OnOpenFeedProperties)
        wx.EVT_BUTTON(self, xrc.XRCID("SAVESCHED"), self.OnSaveCloseSched)
        wx.EVT_BUTTON(self, xrc.XRCID("CANCELSCHED"), self.OnCancelSched)
        wx.EVT_BUTTON(self, xrc.XRCID("ID_CLEARLOG"), self.OnClearLog)
        
        self.Bind(wx.EVT_TIMER,self.OnTimerSched)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSubscrSelect, self.feedslist)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSubscrDeselect, self.feedslist)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnEpisodesListRClick, self.episodes)
        self.Bind(wx.EVT_CHAR, self.OnEpisodesListChar, self.episodes)
        wx.EVT_LEFT_DOWN(self.episodes, self.OnEpisodesListLeftDown)

        if wx.Platform == '__WXMAC__':
            wx.EVT_MOTION(self.toolbarSubscr,self.OnToolMotionMac)
            wx.EVT_MOTION(self.toolbarDownloads,self.OnToolMotionMac)
            wx.EVT_MOTION(self.toolbarDirectory,self.OnToolMotionMac)
            wx.EVT_LEAVE_WINDOW(self.toolbarSubscr,self.OnToolLeaveMac)
            wx.EVT_LEAVE_WINDOW(self.toolbarDownloads,self.OnToolLeaveMac)
            wx.EVT_LEAVE_WINDOW(self.toolbarDirectory,self.OnToolLeaveMac)
        else:
            self.Bind(wx.EVT_TOOL_ENTER, self.OnToolEnter, self.toolbarSubscr)
            self.Bind(wx.EVT_TOOL_ENTER, self.OnToolEnter, self.toolbarDownloads)
            self.Bind(wx.EVT_TOOL_ENTER, self.OnToolEnter, self.toolbarDirectory)

        #wiring: downloads tab
        self.searchboxdownloads = xrc.XRCCTRL(self.frame, "SEARCHBOXDOWNLOADS")
        self.searchboxdownloads.Bind(wx.EVT_KEY_UP, self.OnSearchDownloadsKeyUp)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLHISTCLEARSELECTED"), self.OnHistClearSelected)
        wx.EVT_TOOL(self, xrc.XRCID("TOOLHISTCANCELSELECTED"), self.OnHistCancelSelected)
        wx.EVT_LEFT_DOWN(self.downloads,self.OnDownloadsTabLeftDown)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnDownloadsTabSel,self.downloads)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnDownloadsTabDesel,self.downloads)
        self.Bind(wx.EVT_CHAR, self.OnDownloadsChar, self.downloads)

        #wiring: directory
        wx.EVT_MENU(self,xrc.XRCID("TOOLOPENDIRALL"), self.OnDirectoryExpandAll)
        wx.EVT_MENU(self,xrc.XRCID("TOOLCLOSEDIR"), self.OnDirectoryCollapseAll)
        wx.EVT_MENU(self,xrc.XRCID("TOOLREFRESHDIR"), self.OnDirectoryRefresh)
        
        self.threads = []
        self.feedwindowthreads = []
        self.cancelthreads = []
        self.downloadsdict = {}
        
        #Main menu
        IPG_Menu.InitMixin(self, res, xrc)

        #Edit menu
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self,xrc.XRCID("NOTEBOOK"), self.OnNotebookPageChanged)
        self.FrobMenus()
        
       #cleanup
        self.Bind(wx.EVT_CHOICE,self.OnCleanupFeedChoice,self.cleanupfeeds)
        self.Bind(wx.EVT_CHECKBOX,self.OnCleanupFeedChoice,self.cleanupsrcplayer)
        self.Bind(wx.EVT_CHECKBOX,self.OnCleanupFeedChoice,self.cleanupsrcfolder)
        wx.EVT_BUTTON(self,xrc.XRCID("CLEANUPDELETE"),self.OnCleanupDelete)
        wx.EVT_BUTTON(self,xrc.XRCID("CLEANUPCHECKALL"),self.OnCleanupCheckAll)
        wx.EVT_BUTTON(self,xrc.XRCID("CLEANUPCHECKNONE"),self.OnCleanupCheckNone)
        wx.EVT_BUTTON(self,xrc.XRCID("CLEANUPREFRESH"),self.OnCleanupRefresh)

        #donations
        wx.EVT_BUTTON(self,xrc.XRCID("DONATIONSPROCEED"),self.OnDonationsProceed)

        #misc initialization
        self.feedwindow.SetParent(self)
        if hasattr(self.opmltree, 'ISNEW'): 
            #print "initnew "
            self.opmltree.Init(self.ipodder.config.podcast_directory_roots, self.ipodder.feeds, self.ipodder.state)
        else: 
            print "init"
            self.opmltree.Init(self.ipodder.config.podcast_directory_roots)
            self.opmltree.SetLogPanel(self.myTextCtrl)
        self.logwindow.SetMaxLength(0)
        #self.onlineInfo = wx.lib.ClickableHtmlWindow.PyClickableHtmlWindow(
        #    self.aboutPanel,-1,pos=(20,203),size=(470,115))
        #self.onlineInfo.SetPage('<font face="tahoma, arial, verdana" size="2"><table cellpadding="1" cellspacing="1" border="0" width="425"><tr><td bgcolor="#CCE6FF" height="15" width="200">&nbsp;&nbsp;Windows</td><td width="125" bgcolor="#E6F3FF" height="15">&nbsp;<a href="http://juicereceiver.sourceforge.net/update/#win">Check for updates</a></td><td align="center" rowspan="3" width="100"><a href="http://sourceforge.net/donate/index.php?group_id=118858"><img src="images/paypal.gif"></a><br><font size=1>(any amount)</font></td></tr><tr><td width="200" height="15" bgcolor="#CCE6FF">&nbsp;&nbsp;Mac</td><td width="125" height="15" bgcolor="#E6F3FF">&nbsp;<a href="http://juicereceiver.sourceforge.net/update/#mac">Check for updates</a></td></tr><tr><td bgcolor="#CCE6FF" height="15" width="200">&nbsp;&nbsp;Linux/BSD</td><td width="125" bgcolor="#E6F3FF" height="15">&nbsp;<a href="http://juicereceiver.sourceforge.net/update/#linux">Check for updates</a></td></tr><tr><td colspan=3" align="left" height="15"><img src="images/spacer.gif" height="2" width=1"><br><font size=2 face="tahoma, arial, verdana"><a href="http://sourceforge.net/donate/index.php?group_id=118858&amt=5&type=0">Donate $5 to get the development team an iPod!</a></font></td></tr></table></font>')
        #feedslist
        self.il = wx.ImageList(16, 16)

        def iladd(name): 
            icon = gui.geticon(name)
            try: 
                return self.il.Add(icon)
            except wx.PyAssertionError, ex:
                log.exception("Failed to add icon %s to image list; "\
                              "it's probably corrupt.", name)
                return self.il.Add(gui.geticon('smiles')) # probably OK
        
        self.lemon_idle_idx = iladd('icon_feed_idle')
        self.lemon_downloading_idx = iladd('icon_feed_downloading')
        self.lemon_disabled_idx = iladd('icon_feed_disabled')
        self.lemon_cross_idx = iladd('icon_feed_idle_empty')
        self.lemon_tick_idx = iladd('icon_feed_idle_empty')
        self.lemon_feed_checking_idx = iladd('icon_feed_checking')
        self.lemon_synced_idx = iladd('icon_feed_synced')
        
        #mainpanel needs these
        self.sm_up = iladd('sorting_arrow_up')
        self.sm_dn = iladd('sorting_arrow_down')
        
        self.feedslist.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        self.m_currentlanguage = self.m_currentlanguage
        
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_name")
        self.feedslist.InsertColumnInfo(0, info)
        
        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_state")
        info.m_format = 0
        self.feedslist.InsertColumnInfo(1, info)
        
        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_mb")
        info.m_format = wx.LIST_FORMAT_RIGHT
        self.feedslist.InsertColumnInfo(2, info)

        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_location")
        info.m_format = 0
        self.feedslist.InsertColumnInfo(3, info)

        self.feedslist.SetColumnWidth(0, 250)
        self.feedslist.SetColumnWidth(1, 80)
        self.feedslist.SetColumnWidth(2, 65)
        self.feedslist.SetColumnWidth(3, 90)

        #EPISODES
        self.displaying_episodes_for = None
        self.episodes_il = wx.ImageList(16, 16)
        self.box_unchecked_idx = self.episodes_il.Add(gui.geticon('box-unchecked'))
        self.box_checked_idx = self.episodes_il.Add(gui.geticon('box-checked'))
        self.play_file_idx = self.episodes_il.Add(gui.geticon('play-file'))
        self.episodes.SetImageList(self.episodes_il, wx.IMAGE_LIST_SMALL)
  
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_episode")
        self.episodes.InsertColumnInfo(0, info)
        
        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_state")
        info.m_format = 0
        self.episodes.InsertColumnInfo(1, info)
        
        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_mb")
        info.m_format = wx.LIST_FORMAT_RIGHT
        self.episodes.InsertColumnInfo(2, info)

        #info = wx.ListItem()
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_location")
        info.m_format = 0
        self.episodes.InsertColumnInfo(3, info)

        self.episodes.SetColumnWidth(0, 250)
        self.episodes.SetColumnWidth(1, 80)
        self.episodes.SetColumnWidth(2, 65)
        self.episodes.SetColumnWidth(3, 90)

        # DOWNLOADS
        self.downloads_il = wx.ImageList(16, 16)
        self.dl_downloading_idx = self.downloads_il.Add(gui.geticon('icon_episode_downloading'))
        self.dl_play_file_idx = self.downloads_il.Add(gui.geticon('play-file'))
        self.dl_blank_idx = self.downloads_il.Add(gui.geticon('icon_episode_blank'))
        self.dl_cancelled_idx = self.downloads_il.Add(gui.geticon('icon_episode_problem_broken'))
        self.downloads.SetImageList(self.downloads_il, wx.IMAGE_LIST_SMALL)

        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_name")
        self.downloads.InsertColumnInfo(0, info)

        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_state")
        info.m_format = 0
        self.downloads.InsertColumnInfo(1, info)

        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_progress")
        info.m_format = 0
        self.downloads.InsertColumnInfo(2, info)

        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_date")
        info.m_format = 0
        self.downloads.InsertColumnInfo(3, info)

        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_playlist")
        info.m_format = 0
        self.downloads.InsertColumnInfo(4, info)

        info.m_text = self.m_stringtable.GetText(self.m_currentlanguage, "str_lst_location")
        info.m_format = 0
        self.downloads.InsertColumnInfo(5, info)

        self.downloads.SetColumnWidth(0, 250)
        self.downloads.SetColumnWidth(1, 100)
        self.downloads.SetColumnWidth(2, 120)
        self.downloads.SetColumnWidth(3, 145)
        self.downloads.SetColumnWidth(4, 150)
        self.downloads.SetColumnWidth(5, 100)

        # SCHEDULE
        self.schedSpecif = []
        self.enableSpecif = []

        for i in range(1,4):
            timefield = xrc.XRCCTRL(self.scheddialog,"TEXTSCHEDSPECIF%d" % i)
            timefield.SetMaxLength(8)
            self.schedSpecif.append(timefield)
            checkbox = xrc.XRCCTRL(self.scheddialog,"CHECKBSCHEDSPECIF%d" % i)
            self.enableSpecif.append(checkbox)
            self.Bind(wx.EVT_CHECKBOX, self.OnSchedChk, self.enableSpecif[-1])

        # set accumlate lists of scheduler widgets for enable/disable
        self.schedSpecifGroup = []
        self.schedSpecifGroup.extend(self.schedSpecif)
        self.schedSpecifGroup.extend(self.enableSpecif)

        self.schedRegGroup = []
        self.schedRegGroup.append(self.schedinterval)
        self.schedRegGroup.append(self.repeatevery)

        self.schedWidgets = []
        self.schedWidgets.append(self.schedspecific)
        self.schedWidgets.append(self.schedreg)
        self.schedWidgets.extend(self.schedSpecifGroup)
        self.schedWidgets.extend(self.schedRegGroup)
        self.schedWidgets.append(self.lastrun)
        self.schedWidgets.append(self.nextrun)
        self.schedWidgets.append(self.nextrun2)

        # bind enable/disable checkbox and radiobuttons
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSchedRadioSpecif, self.schedspecific)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSchedRadioReg, self.schedreg)
        self.Bind(wx.EVT_CHECKBOX, self.OnAutoChk, self.enableauto)
        
        # initialize the scheduler widget states
        self.InitSchedWidgets()

        # clear the last run widget
        self.lastrun.SetLabel(self._("str_not_yet"))
        self.nextrun.SetLabel(asctimeOrNone(self.s.getNextRun()))
        self.nextrun2.SetLabel(asctimeOrNone(self.s.getNextRun()))

        self.scheddialog.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, xrc.XRCID("CANCELSCHED"))
            ]))

        # Set up the right-click menu for feeds
        self.feedmenu = wx.Menu()
        self.feedmenu_checknow_id = id = wx.NewId()
        self.feedmenu.Append(id,"Check now")
        wx.EVT_MENU(self.feedmenu, id, self.OnCheckSelected)
        self.feedmenu_remove_id = id = wx.NewId()
        self.feedmenu.Append(id,"Remove")
        wx.EVT_MENU(self.feedmenu, id, self.OnToggleChecked)
        self.feedmenu.AppendSeparator()
        if clipboard.enabled:
            id = wx.NewId()
            self.feedmenu.Append(id,self._("str_copy_location"))
            wx.EVT_MENU(self.feedmenu, id, self.OnCopyFeedLocation)
        self.feedmenu_openfolder_id = id = wx.NewId()
        self.feedmenu.Append(id,"Open downloads folder")
        wx.EVT_MENU(self.feedmenu, id, self.OnOpenFeedFolder)
        self.feedmenu_openinbrowser_id = id = wx.NewId()
        self.feedmenu.Append(id,"Open in browser")
        wx.EVT_MENU(self.feedmenu, id, self.OnOpenFeedInBrowser)
        self.feedmenu.AppendSeparator()
        self.feedmenu_properties_id = id = wx.NewId()
        self.feedmenu.Append(id,"Properties")
        wx.EVT_MENU(self.feedmenu, id, self.OnOpenFeedProperties)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnFeedsListRClick, self.feedslist)
        self.Bind(wx.EVT_CHAR, self.OnFeedsListChar, self.feedslist)
        self.feedslist.Bind(wx.EVT_LEFT_DCLICK, self.OnOpenFeedProperties)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.LaunchDownloadsRClickMenu, self.downloads)

        # Set up  right-click menu for Directory
        self.directory_root_menu = wx.Menu()
        self.directory_refresh_id = id = wx.NewId()
        self.directory_root_menu.Append(id, "Refresh")
        self.directory_selected_root = None 
        wx.EVT_MENU(self.directory_root_menu, id, self.OnOpmlRefresh)

        skin.set_skin_opts(self)

        self.frame.SetLabel("%s - Podcast receiver v%s" % (PRODUCT_NAME, core.__version__))

        # make the TaskBar icon and menu
        try:
            if "Win" in platform.system() or "Linux" in platform.system():
                self.tbIcon = wx.TaskBarIcon()
                icon = wx.Icon(os.path.join(self.basepath,'icons_status','icon_idle_empty.ico'), wx.BITMAP_TYPE_ICO)
                self.tbIcon.SetIcon(icon, PRODUCT_NAME)
    
                self.menu = wx.Menu()
                self.menu.Append(ID_CHECKNOW,"Check Now","Check Now")
                self.menu.Append(ID_OPEN,"Open %s" % PRODUCT_NAME,"Open %s" % PRODUCT_NAME)
                self.menu.AppendSeparator()
                self.menu.Append(ID_EXIT,"Quit","Quit")
                
                # wire up the events
                wx.EVT_TASKBAR_LEFT_DCLICK(self.tbIcon, self.OnTaskBarActivate)
                wx.EVT_TASKBAR_RIGHT_UP(self.tbIcon, self.OnTaskbarRClick)
                wx.EVT_MENU(self.tbIcon, ID_EXIT, self.OnExit)
                wx.EVT_MENU(self.tbIcon, ID_CHECKNOW, self.OnCheckNow)
                wx.EVT_MENU(self.tbIcon, ID_OPEN, self.OnTaskBarActivate)
        except:
            pass

        wx.EVT_CLOSE(self.frame, self.OnCloseWindow)

        self.SetLanguages()

        #Run me after SetLanguages()
        if self.ipodder.config.window_dimensions:
            self.frame.SetDimensions(self.ipodder.config.window_dimensions[0],
                                     self.ipodder.config.window_dimensions[1],
                                     self.ipodder.config.window_dimensions[2],
                                     self.ipodder.config.window_dimensions[3])
        else:
            self.frame.GetSizer().Fit(self.frame)

        if not wx.Platform == '__WXMAC__':
            self.frame.Maximize(self.ipodder.config.window_is_maximized)

        #self.schedPanel.GetSizer().Fit(self.schedPanel)
        self.donatedialog.GetSizer().Fit(self.donatedialog)

        self.ShowFrame(1)
        self.SetTopWindow(self.frame)

        # Set the window icon, tested on Windows
        try:
            icons = wx.IconBundle()
            icons.AddIcon(wx.Icon(os.path.join(self.basepath,'icons_status','application.ico'), wx.BITMAP_TYPE_ICO))
            icons.AddIcon(wx.Icon(os.path.join(self.basepath,'icons_status','application_small.ico'), wx.BITMAP_TYPE_ICO, 16, 16))
            for appwindow in [self.frame,self.preferences,self.scheddialog,self.about,self.feedwindow]:
                appwindow.SetIcons(icons)
        except:
            pass

        # repopulate subscriptions list
        self.PopulateFeedsList()
        self.ReplaceManagedFeeds()

        self.mainpanel.InitSortMixin(self.feedslist,self.sm_up,self.sm_dn)

        # Saved sort setting.
        if self.ipodder.config.feedslist_col_sort:
            self.mainpanel.SetState(self.ipodder.config.feedslist_col_sort)
         
        # set up logging
        self.InitLogging()

        # hook the ipodder
        self.InitHooks()

        # load the plugins
        self.LoadPlugins()
        
        # init the cleanup window
        self.InitCleanup()

        if self.ipodder.config.chkupdate_on_startup:
            self.OnMenuCheckForUpdates(None)
        
        if SPLASH_DESTROY:
            try:
                splash.Destroy()
            except wx._core.PyDeadObjectError:
                pass
            
        # populate the downloads tab with any history
        self.PopulateDownloadsTab()
        self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,False)               

        if self.ipodder.config.hide_on_startup and not platform.system()=='Darwin':
            self.frame.Show(0)

        if self.ipodder.config.scan_on_startup:
            self.OnCheckNow(None)

        self.feedwindow.Show(0)
        self.about.Show(0)
        self.scheddialog.Show(0)
        self.donatedialog.Show(0)

        if not self.preferences.showLogPage.GetValue():
            self.notebook.RemovePage(LOGPAGE_INDEX)
        
        #Run me after SetLanguages()
        self.InitScheduleTool()

        self.feeditembuffer = [];                
        
        # spotlight search downloads
        self.m_sptl_dwnl_threads = []
        self.m_sptl_subs_threads = []

        # register one-click handlers
        if "Win" in platform.system():
            self.do_win32_registrations()

        # set proxy config for feed previews and tree grabbers
        self.ipodder.init_proxy_config()
        
        self.ThreadSafeDispatch(self.frame.SetStatusText, self.m_stringtable.GetText(self.m_currentlanguage, "str_initialized"))

        if self.options.add_feed:
            self.ThreadSafeDispatch(self.AddFeedFromListener,self.options.add_feed)            
        if self.options.add_feed_from_rss:
            url = misc.url_rssfile_extract(self.options.add_feed_from_rss)
            self.ThreadSafeDispatch(self.AddFeedFromListener,url)
        if self.options.add_feed_from_pcast:
            url = misc.url_pcast_file_extract(self.options.add_feed_from_pcast)
            self.ThreadSafeDispatch(self.AddFeedFromListener,url)
        if self.options.open:
            if self.options.open.startswith("pcast://"):
                url = misc.url_cmdline_extract(self.options.open)
                self.ThreadSafeDispatch(self.AddFeedFromListener,url)            
            elif self.options.open.startswith("podcast://"):
                url = misc.url_cmdline_extract(self.options.open)
                self.ThreadSafeDispatch(self.AddFeedFromListener,url)
            elif self.options.open.endswith(".pcast"):
                url = misc.url_pcast_file_extract(self.options.open)
                self.ThreadSafeDispatch(self.AddFeedFromListener,url)
            elif self.options.open.endswith(".rss"):
                url = misc.url_rssfile_extract(self.options.open)
                self.ThreadSafeDispatch(self.AddFeedFromListener,url)
            else:
                log.exception("open: file type for %s not supported" % self.options.open)
                    
        return True


    def do_win32_registrations(self):            
        from win32 import oneclick
    
        try:
            try: 
                (are_we,was_anybody,unregistered_config_attrs) = oneclick.do_registrations(self.ipodder.config,self.ipodder.config.ensure_oneclick_handler)
            except TypeError: # oneclick failed
                return

            if not are_we and \
               not self.ipodder.config.ensure_oneclick_handler and \
               self.ipodder.config.ask_ensure_oneclick_handler:
                alert = OptionsDialog.OptionsDialog(\
                    self.frame, self._, "str_set_file_types", \
                    "str_set_file_types_warn",["str_yes","str_no"],\
                    optstyle=OptionsDialog.RADIOBOX,\
                    defaults=[0])
                response = alert.ShowModal()
                alertval = alert.GetValue()
                alertask = alert.AskAgain()
                alert.Destroy()
                if response == wx.ID_OK:
                    config_is_dirty = False
                    if len(alertval) == 1 and alertval[0] == 0:
                        for attr in unregistered_config_attrs:
                            setattr(self.ipodder.config,attr,False)
                        self.preferences.ResetPrefs()
                        self.preferences.notebook.SetSelection(self.preferences.FILE_TYPES)
                        self.frame.SetFocus() #ensures proper return focus
                        self.preferences.OnPrefChange(None) #enable the Save button
                        self.OnMenuPreferences(None)
                    if not alertask:
                        self.ipodder.config.ask_ensure_oneclick_handler = False
                        config_is_dirty = True
                    if config_is_dirty:
                        self.ipodder.config.flush()
                        self.preferences.ResetPrefs()

            log.debug("Registering oneclick handlers: %s" % str(are_we))
        except:
            log.exception("Caught exception registering oneclick handlers.")

    def getcontent(self, url):
        url = urllib.urlopen (url)
        rs = ""
        for l in url:
            rs += str(l)
        return rs    

    def GetOPML(self,opml_url):
        if opml_url=="":
            return ""
        opml = self.getcontent(opml_url)
        return opml

    def ReplaceManagedFeeds(self,wait=False):
        """Launches a download thread which, when complete, replaces managed feeds with new ones."""
        if self.ipodder.config.feedmanager_enable and \
           self.ipodder.config.feedmanager_opml_url != '':
            self.ReplaceFromManagerUrl(self.ipodder.config.feedmanager_opml_url,wait)

    def ReplaceFromManagerUrl(self,opml_url,wait):
        opmlfetcher = FeedManagerOpmlFetcher(opml_url,self)
        opmlfetcher.start()
        if wait:
            opmlfetcher.join()

    def ReplaceFromManagerOpmlEnsuringPopulate(self,opml_url,opml):
        error = False
        try:
            numadded = self.ReplaceFromManagerOpml(opml_url,opml)
        except:
            log.exception("Error retrieving manager opml from server.")
            error = True

        if error or numadded == None:
            log.error("Error retrieving manager opml from server.")
            self.PopulateFeedsList()
            
    def ReplaceFromManagerOpml(self,opml_url,opml):

        result = self.ipodder.feeds.replace_from_manager_opml(opml_url,opml)
        self.PopulateFeedsList()          
        return result
    
    def RemoveManagedFeeds(self):
        """Disable any feed with a manager url is not None and set its
        manager url to None."""

        self.ipodder.feeds.remove_managed_feeds()
        self.PopulateFeedsList()
        
    def OnNotebookPageChanged(self, event):
        self.FrobMenus()

    def FrobMenus(self):
        self.menuselectall.Enable(self.notebook.GetSelection() == DOWNLOADS_INDEX)
        self.menufeedproperties.Enable(
            self.notebook.GetSelection() == SUBSCRIPTIONS_INDEX and
            self.feedslist.GetFirstSelected() != -1
            )
        self.menuremovefeed.Enable(
            self.notebook.GetSelection() == SUBSCRIPTIONS_INDEX and
            self.feedslist.GetFirstSelected() != -1
            )
        
    def SetLemon(self, feedinfo, state='', scroll=False): 
        statemap = {
            'scanning': self.lemon_feed_checking_idx, 
            'downloading': self.lemon_downloading_idx,
            '': self.lemon_idle_idx,
            'disabled': self.lemon_disabled_idx,
            'errors': self.lemon_cross_idx,
            'gotsome': self.lemon_tick_idx,
            }
        if not state: 
            if feedinfo.sub_state == 'disabled': 
                state = 'disabled'
        if feedinfo.manager_url != None and state == '':
            #Special styling for managed feeds.
            image_idx = self.lemon_synced_idx
        else:
            image_idx = statemap.get(state)

        if image_idx is None: 
            log.error("SetLemon reports: Invalid state %s", state)
            return
        list_idx = self.FeedInfoToIndex(feedinfo)
        if list_idx is None: 
            log.error("Couldn't SetLemon for feedinfo %s", feedinfo)
            return
        #log.debug("SetLemon: setting list index %s to image index %s", 
        #          list_idx, image_idx)
        self.feedslist.SetItemImage(list_idx, image_idx, image_idx)
        if not state: 
            self.feedslist.SetItemText(list_idx, unicode(feedinfo))
        else: 
            self.feedslist.SetItemText(list_idx, "%s [%s]" % (
                unicode(feedinfo), state))
        #if scroll and state: 
        #    self.feedslist.EnsureVisible(list_idx)

    def hook_scan_enclosures_begin(self):
        self.ThreadSafeDispatch(self.frame.SetStatusText, self._("str_scanning_feeds") + "...")
        self.ThreadSafeDispatch(self.SetTaskBarIcon,"icon_scanning_feeds.ico","str_scanning_feeds")
        
    def hook_scan_enclosures_announce(self, feedinfo):  
        self.ThreadSafeDispatch(self.SetLemon, feedinfo, 'scanning', True)

    def hook_scan_enclosures_backannounce(self, feedinfo): 
        #self.ThreadSafeDispatch(self.frame.SetStatusText, '')
        if feedinfo is not None: 
            self.ThreadSafeDispatch(self.SetLemon, feedinfo)

    def hook_download_content_critical_error(self,errno,*args):
        self.ThreadSafeDispatch(self.DownloadCriticalError,errno,*args)

    def hook_download_content_announce(self, encinfo): 
        #self.ThreadSafeDispatch(self.frame.SetStatusText, encinfo.url)
        self.ThreadSafeDispatch(self.SetLemon, encinfo.feed, 'downloading', True)

    def hook_download_content_backannounce(self, encinfo): 
        #self.ThreadSafeDispatch(self.frame.SetStatusText, '')
        if encinfo is not None: 
            self.ThreadSafeDispatch(self.SetLemon, encinfo.feed)

    def hook_download_torrent_announce(self, filename, encinfo): 
        #self.ThreadSafeDispatch(self.frame.SetStatusText, filename)
        self.ThreadSafeDispatch(self.SetLemon, encinfo.feed, 'downloading', True)
 
    def hook_download_torrent_backannounce(self, filename, encinfo): 
        #self.ThreadSafeDispatch(self.frame.SetStatusText, '')
        if encinfo is not None: 
            self.ThreadSafeDispatch(self.SetLemon, encinfo.feed)

    def hook_download_content_begin(self):
        self.ThreadSafeDispatch(self.SetTaskBarIcon,"icon_downloading.ico","str_downloading")
        self.ThreadSafeDispatch(self.frame.SetStatusText, self.m_stringtable.GetText(self.m_currentlanguage, "str_downloading_new_episodes") + "...")
        self.sb.autohide = False
        self.ThreadSafeDispatch(self.sb.g1.Show)

    def hook_download_content_end(self, grabbed):
        self.sb.autohide = True

    def LoadPlugins(self):
        base = os.path.abspath(os.path.split(sys.argv[0])[0])
        plugins = os.path.join(base,'plugins')
        prefix = "hook_"
        if os.path.isdir(plugins):
            sys.path.append(plugins)
            for fname in os.listdir(plugins):
                if not fname.endswith(".py"):
                    continue
                mod = __import__(os.path.splitext(fname)[0])
                if hasattr(mod,"Plugin"):
                    pl = mod.Plugin()
                    # Look for hook methods and hook them. 
                    for att, method in inspect.getmembers(pl, inspect.ismethod): 
                        if not att.startswith(prefix): 
                            continue
                        hookname = att[len(prefix):].replace('_', '-')
                        log.debug("Hooking %s with %s", hookname, repr(method))
                        self.hooks.add(hookname, method)
        
    def InitHooks(self): 
        "Initialise our hooks to the ipodder object."
        dispatch = self.ThreadSafeDispatch
        hooks = self.ipodder.hooks
        
        hooks.add("download-content-begin", 
                lambda: setattr(self, 'switch_to_downloads_tab', True))

        hooks.add("download-content-downloaded", self.OnDownloadedContent)
        hooks.add("download-content-downloading", self.OnDownloadStart)

        #DownloadTabPruneFiles needs to be called before the files are
        #actually removed.
        hooks.add("removing-files", self.DownloadTabPruneFiles)
        
        class DownloadCounter: 
            """A download counter class. Only used in iPodderGui.InitHooks.
            That's only called once, so there's no harm defining this class 
            on the fly rather than in the module."""

            def __init__(self, gui, 
                    nouns=(self.m_stringtable.GetText(self.m_currentlanguage, "str_item"), self.m_stringtable.GetText(self.m_currentlanguage, "str_items")), 
                    verbs=(self.m_stringtable.GetText(self.m_currentlanguage, "str_downloading"), self.m_stringtable.GetText(self.m_currentlanguage, "str_downloaded")),
                    lang=LanguageModule.ENGLISH,
                    updateprogress=True): 
                "Initialise the DownloadCounter."
                self.gui = gui
                self.nouns = nouns
                self.verbs = verbs
                self.m_stringtable = LanguageModule.StringTable(lang)
                self.m_currentlanguage = lang
                self.updateprogress = updateprogress

            def cap(self, msg): 
                "Capitalise the first letter of a message."
                return msg[0:1].upper() + msg[1:]
            
            def __call__(self, encnum, maxnum): 
                "Update the progress bar as each feed is scanned."
                if not maxnum:
                    return
                gui = self.gui
                dispatch = gui.ThreadSafeDispatch
                if self.updateprogress:
                    percent = int(100.0 * encnum / float(maxnum))
                    dispatch(gui.progressBar.SetValue, percent)
                if encnum < maxnum: 
                    dispatch(gui.frame.SetStatusText, 
                             self.cap("%s %s %d %s %d" % (
                                 self.verbs[0], self.nouns[0], encnum+1, self.m_stringtable.GetText(self.m_currentlanguage, "str_of"), maxnum)))
                else: 
                    dispatch(gui.frame.SetStatusText, 
                             self.cap("%s %d %s" % (
                                 self.verbs[1], encnum, self.nouns[1])))

        def fin(grabbed): 
            "Finish the downloads."            
            plural = self.m_stringtable.GetText(self.m_currentlanguage, "str_enclosures")
            if grabbed == 1: 
                plural = self.m_stringtable.GetText(self.m_currentlanguage, "str_enclosure")
            message = "%d %s %s" % (grabbed, plural, self.m_stringtable.GetText(self.m_currentlanguage, "str_fetched"))
            dispatch(self.frame.SetStatusText, message)
            dispatch(self.progressBar.SetValue, 0) 
            
        # Look for hook methods and hook them. 
        prefix = 'hook_'
        for att, method in inspect.getmembers(self, inspect.ismethod): 
            if not att.startswith(prefix): 
                continue
            hookname = att[len(prefix):].replace('_', '-')
            log.debug("Hooking %s with %s", hookname, repr(method))
            hooks.add(hookname, method)
            
        # Add more hooks manually. 
        hooks.add('scan-enclosures-count',  DownloadCounter(self, 
                                                            nouns=( self.m_stringtable.GetText(self.m_currentlanguage, "str_feed"), self.m_stringtable.GetText(self.m_currentlanguage, "str_feeds") ), 
                                                            verbs=( self.m_stringtable.GetText(self.m_currentlanguage, "str_scanning"), self.m_stringtable.GetText(self.m_currentlanguage, "str_scanned") ), lang=self.m_currentlanguage))
        hooks.add('download-content-count', DownloadCounter(self, 
                                                            nouns=( self.m_stringtable.GetText(self.m_currentlanguage, "str_item"), self.m_stringtable.GetText(self.m_currentlanguage, "str_items") ), 
                                                            verbs=( self.m_stringtable.GetText(self.m_currentlanguage, "str_downloading"), self.m_stringtable.GetText(self.m_currentlanguage, "str_downloaded") ), lang=self.m_currentlanguage, updateprogress=False))
        hooks.add('download-content-end', fin)

        # Hook other objects. 
        
        self.ipodder.config.hooks.add('invoke-player-begin', 
                lambda: dispatch(self.frame.SetStatusText, self.m_stringtable.GetText(self.m_currentlanguage, "str_loading_mediaplayer")))
        self.ipodder.config.hooks.add('invoke-player-end', 
                lambda: dispatch(self.frame.SetStatusText, self.m_stringtable.GetText(self.m_currentlanguage, "str_loaded_mediaplayer")))

        self.opmltree.hooks.add('right-click', self.opmltree_rightclick)
        self.opmltree.hooks.add('select-before-scan', self.opmltree_select_before_scan)
        self.opmltree.hooks.add('node-activated', self.opmltree_node_activated)

    def opmltree_rightclick(self, opmltree, ID, treenode):
        try: 
            node = treenode.node
            value = ''
            if hasattr(node, 'url'): 
                if len(node):
                    if self.opmltree.IsOpmlUrl(node.url): 
                        # Candidate for refreshing
                        self.directory_selected_root = treenode
                        self.opmltree.PopupMenu(self.directory_root_menu)
        except: 
            log.exception("Please report this unpredicted failure:")

    def OnOpmlRefresh(self, event):
        self.directory_selected_root.rescan()

    def opmltree_node_activated(self, opmltree, ID, treenode): 
        """Hook node activation on the OPML tree."""
        try: 
            node = treenode.node
            value = ''
            if hasattr(node, 'url'): 
                if len(node):
                    # This should never happen
                    pass
                elif self.opmltree.IsOpmlUrl(node.url): 
                    # Node that hasn't been scanned yet
                    pass
                else:
                    oldfocus = self.frame.FindFocus()
                    self.OnAddFeed(None)
                    if oldfocus:
                        oldfocus.SetFocus()
        except: 
            log.exception("Please report this unpredicted failure:")

    def opmltree_select_before_scan(self, opmltree, ID, treenode): 
        """Hook node selection on the OPML tree."""
        try: 
            node = treenode.node
            value = ''
            if hasattr(node, 'url') and not len(node) and not self.opmltree.IsOpmlUrl(node.url): 
                value = node.url
            self.ThreadSafeDispatch(self.myTextCtrl.SetValue, value)
            self.ThreadSafeDispatch(self.opmltree_set_buttons, treenode)
        except: 
            log.exception("Please report this unpredicted failure:")

    def opmltree_set_buttons(self,treenode):
        try:
            node = treenode.node
            self.toolbarDirectory.EnableTool(self.toolRefreshDirId,
                hasattr(node, 'url') and self.opmltree.IsOpmlUrl(node.url))               
            self.toolbarDirectory.EnableTool(self.toolOpenDirAllId,
                (hasattr(node, 'url') and self.opmltree.IsOpmlUrl(node.url)) or
                treenode.opmltree.ItemHasChildren(treenode.id))
            self.toolbarDirectory.EnableTool(self.toolCloseDirId,
                (hasattr(node, 'url') and self.opmltree.IsOpmlUrl(node.url)) or
                treenode.opmltree.ItemHasChildren(treenode.id))
        except:
            log.exception("Please report this unpredicted failure:")            

    def InitLogging(self):
        newHandler = MyLogWindowHandler(self)
        otherHandlers = []
        for handler in log.handlers: 
            if isinstance(handler, logging.handlers.MemoryHandler): 
                handler.setTarget(newHandler)
                handler.flush()
            else: 
                otherHandlers.append(handler)
        log.handlers = otherHandlers
        log.addHandler(newHandler)

    def InitScheduleTool(self):
        self.toolScheduler.SetNormalBitmap(gui.geticon("tb_icon25_scheduler_%s" % self.ipodder.config.sched_enableAuto))
        self.toolbarSubscr.Realize()
        key = "str_scheduler_%s" % self.ipodder.config.sched_enableAuto        
        self.toolbarSubscr.SetToolShortHelp(xrc.XRCID("TOOLSCHEDULER"),self.m_stringtable.GetText(self.m_currentlanguage, key))
        
    def OnTaskbarRClick(self, event):
        self.tbIcon.PopupMenu(self.menu)
        
    def OnExit(self,event=None):        
        import traceback
        #traceback.print_stack(file=sys.stdout)
        #print "Exit", event
        if len(self.threads) and not self.waiting_for_quit:
            #Might be messy, alert the user.
            alert = wx.MessageDialog(self.frame, self.m_stringtable.GetText(self.m_currentlanguage, "str_really_quit"), style=wx.OK|wx.CANCEL)
            response = alert.ShowModal()
            alert.Destroy()
            if response != wx.ID_OK:
                return
            #Make an attempt to clean up before quitting.
            #OnExit will be called again from PostCancelUpdate()
            self.ipodder.quitting = True # influences iPodder cancel behavior.
            self.CancelRunningDownloads()
            self.waiting_for_quit = True
            self.quittimer = wx.PyTimer(self.CheckQuit)
            self.quittimer.Start(1000)
            
            return

        if self.quitting:
            #print "why are we getting called twice?"
            pass
            
        self.quitting = True
        
        #Save window state for next time.
        try:
            self.frame.Show(1)
            self.frame.Raise()
            self.ipodder.config.window_is_maximized = self.frame.IsMaximized()
            #Save unmaximized dimensions.
            if not wx.Platform == '__WXMAC__':
                #But not on Mac, which assigns a different meaning to this.
                self.frame.Maximize(False)
            self.ipodder.config.window_dimensions = self.frame.GetRect().Get()
            self.ipodder.config.feedslist_col_sort = self.mainpanel.GetState()
            self.ipodder.config.flush()
        except wx.PyDeadObjectError:
            #Catch exxed out Mac windows
            pass

        try:
            self.tbIcon.Destroy()
            del self.tbIcon
        except:
            pass

        #We want to use Destroy here, not close, because we're using
        #EVT_CLOSE to hide the window.  Destroy() safely
        #destroys the window.
        
        #Catch dead object errors to keep Mac happy.
        for obj in [self.about,self.preferences,self.encodingdlg,self.feedwindow,self.scheddialog,self.donatedialog,self.splash,self.frame]:
            try:
                if obj:
                    obj.Destroy()
            except wx.PyDeadObjectError:
                #Catch exxed out Mac windows
                print "== Do not touch the dead objects=="
                pass

    def CheckQuit(self):
        if self.ready_to_quit:
            self.quittimer.Stop()
            self.OnExit()
            
    def OnCloseWindow(self, event):
        if self.frame.IsShown() \
           and self.ipodder.config.ask_goto_background_on_close:
            if self.ipodder.config.goto_background_on_close:
                defaults = [0]
            else:
                defaults = [1]
            alert = OptionsDialog.OptionsDialog(\
                self.frame, self._, "str_goto_background_on_close_title", \
                "str_goto_background_on_close_warn",["str_yes","str_no"],\
                optstyle=OptionsDialog.RADIOBOX,\
                defaults=defaults)
            response = alert.ShowModal()
            alertval = alert.GetValue()
            alertask = alert.AskAgain()
            alert.Destroy()
            if response == wx.ID_CANCEL:
                return
            else:
                config_is_dirty = False
                oldval = self.ipodder.config.goto_background_on_close
                if len(alertval) == 1:
                    self.ipodder.config.goto_background_on_close = (alertval[0] == 0)
                if self.ipodder.config.goto_background_on_close != oldval:
                    config_is_dirty = True
                if not alertask:
                    self.ipodder.config.ask_goto_background_on_close = False
                    config_is_dirty = True
                if config_is_dirty:
                    self.ipodder.config.flush()
                    self.preferences.ResetPrefs()

        if self.ipodder.config.goto_background_on_close:
            self.OnHide(event)
        else:
            self.OnExit()

    def PopulateFeedsList(self):
        self.toolbarSubscr.EnableTool(self.toolCheckSelectedId,False)
        self.toolbarSubscr.EnableTool(self.toolToggleCheckedId,False)
        self.toolbarSubscr.EnableTool(self.toolFeedPropertiesId,False)
        self.menucheckselected.Enable(False)
        self.menuremovefeed.Enable(False)
        self.menufeedproperties.Enable(False)
        
        self.feedslist.DeleteAllItems()
        self.episodes.DeleteAllItems()
        self.displaying_episodes_for = None
        count = 0
        self.feedsdict = {}
        fds = self.ipodder.feeds
        
        for feedinfo in fds:
            if feedinfo.sub_state in ['unsubscribed', 'disabled'] \
                and not self.ipodder.config.debug:
                continue
            #if sub_state == 'preview':
            #    continue
            id = wx.NewId()
            self.feedsdict[id] = feedinfo
            if feedinfo.title:
                index = self.feedslist.InsertImageStringItem(count,feedinfo.title,self.lemon_idle_idx)
            else:
                index = self.feedslist.InsertImageStringItem(count,feedinfo.url,self.lemon_idle_idx)
            self.feedslist.SetStringItem(index,1,self._("str_" + feedinfo.sub_state))
            self.feedslist.SetStringItem(index,2,'%4.1f' % feedinfo.mb_on_disk())
            self.feedslist.SetStringItem(index,3,trimurl(feedinfo.url))
            self.feedslist.SetItemData(index,id)
            self.SetLemon(feedinfo) 
            count += 1
            if count % 2 == 1:
                #See also iPodderWindows.MainPanel for color assignments.
                self.feedslist.SetItemBackgroundColour(index,STRIPE_ODD_COLOR)
        self.mainpanel.ResetSortMixin()

    def UpdateFeedsListItem(self,feedinfo): 
        index = self.FeedInfoToIndex(feedinfo)
        if index > -1:
            if feedinfo.title:
                self.feedslist.SetStringItem(index,0,feedinfo.title)
            else:
                self.feedslist.SetStringItem(index,0,"Feed ID %d at %s" % (feedinfo.id,feedinfo.url))
            self.feedslist.SetStringItem(index,1,self._("str_" + feedinfo.sub_state))
            self.feedslist.SetStringItem(index,2,'%4.1f' % feedinfo.mb_on_disk())
            self.feedslist.SetStringItem(index,3,trimurl(feedinfo.url))
        
    def FeedInfoToIndex(self,feedinfo):
        for i in range(self.feedslist.GetItemCount()):
            id = self.feedslist.GetItemData(i)
            if self.feedsdict[id] == feedinfo:
                return i
        return -1
    
    def OnHide(self, event):
	if self.frame.IsShown():
            self.ShowFrame(0)
        else:
            self.ShowFrame(1)

    def OnTaskBarActivate(self, event):
        self.ShowFrame(1)
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Raise()
        time.sleep(1)
        #AG: let's see if this fixes repaint issues Martijn is seeing on Win2k3.
        self.frame.Refresh()

    def ShowFrame(self,isShown):
        """Just a helper method to make sure the menu Show/Close option
        is set correctly when we show the main frame.  This is mostly to
        provide a consistent way of handling show/close events while supporting
        Mac, which still displays the menubar even if the frame is hidden."""
        self.frame.Show(isShown)
        tmp_accell = self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).GetAccel()
        if isShown:
            self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).SetText(self._("str_close_window"))
        else:
            self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).SetText(self._("str_show_window"))
        self.menubar.FindItemById(xrc.XRCID("MENUBARCLOSE")).SetAccel(tmp_accell)   
        
    def SetTaskBarIcon(self, icon, key=""):
        label = PRODUCT_NAME
        if key != "":
            label += " - %s" % self._(key)
            
        try:
            icon = wx.Icon(os.path.join(self.basepath,'icons_status',icon), wx.BITMAP_TYPE_ICO)
            self.tbIcon.SetIcon(icon, label)
        except:
            pass
        
    def OnCheckNow(self,event):

        if hasattr(event,"iPodderCatchup"):
            catchup = event.iPodderCatchup
            if self.ipodder.config.ask_catchup_marks_downloaded:
                if self.ipodder.config.catchup_marks_downloaded:
                    defaults = [0]
                else:
                    defaults = [1]
                alert = OptionsDialog.OptionsDialog(\
                    self.frame, self._, "str_set_catchup_title", \
                    "str_set_catchup_description",["str_skip_permanently","str_skip_temporarily"],\
                    optstyle=OptionsDialog.RADIOBOX,\
                    defaults=defaults)
                response = alert.ShowModal()
                alertval = alert.GetValue()
                alertask = alert.AskAgain()
                alert.Destroy()
                config_is_dirty = False
                if response == wx.ID_OK:
                    oldval = self.ipodder.config.catchup_marks_downloaded
                    if alertval[0] == 0:
                        self.ipodder.config.catchup_marks_downloaded = True
                    else:
                        self.ipodder.config.catchup_marks_downloaded = False
                    if oldval != self.ipodder.config.catchup_marks_downloaded:
                        config_is_dirty = True
                    if not alertask:
                        self.ipodder.config.ask_catchup_marks_downloaded = False
                        config_is_dirty = True
                    if config_is_dirty:
                        self.ipodder.config.flush()
                        self.preferences.ResetPrefs()
                else:
                    #They cancelled.
                    return
        else:
            catchup = 0

        self.ReplaceManagedFeeds(wait=True)
        self.toolbarSubscr.EnableTool(self.toolCheckAllId,False)
        self.toolbarSubscr.EnableTool(self.toolCatchupId,False)
        self.menucheckall.Enable(False)    
        self.menucheckselected.Enable(False)    
        self.menucatchup.Enable(False)    
        self.searchboxdownloads.Enable(False)
        self.searchboxfeeds.Enable(False)

        self.EnableLanguages(False)
       
        #self.toolbarSubscr.EnableTool(self.toolCheckSelectedId,False)
        if len(self.threads):
            #We can be called by a button press or by the scheduler.  Only complain
            #if called by a button press.
            if event.GetId() == xrc.XRCID("ID_CHECKNOW"):
                alert = wx.MessageDialog(self.frame, self.m_stringtable.GetText(self.m_currentlanguage, "str_on_double_check"), style=wx.OK)
                response = alert.ShowModal()
                alert.Destroy()
            return

        if hasattr(event,"iPodderCheckSelectedMask"):
            mask = event.iPodderCheckSelectedMask
        else:
            mask = None

        if self.searchboxfeeds.GetValue().strip() != '':
            #Restrict to spotlighted feeds.
            mask = self.feedsdict.values()
            
        dl = iPodderDownload(self,mask,catchup)
        dl.ipodder = self.ipodder
        # make the thread terminate if the main thread does: 
        dl.setDaemon(True)
        self.progressBar.SetValue(0)
        dl.start()
        self.threads.append(dl)

        self.lastrun.SetLabel(time.asctime(time.localtime()))
        self.nextrun.SetLabel(asctimeOrNone(self.s.getNextRun()))
        self.nextrun2.SetLabel(asctimeOrNone(self.s.getNextRun()))

    def OnAddFeed(self,event):        
        url = self.myTextCtrl.GetValue().strip()
        if len(url) > 0:
            self.myTextCtrl.Clear()
            try:
                self.feedwindow.UpdateFeed(self.ipodder.feeds[url], self.ipodder)
            except KeyError:
                self.feedwindow.UpdateFeed(None, self.ipodder, newfeed=url)
            self.frame.SetFocus()
            
    def AddFeed(self,url,feed=None,title=None,raise_tab=False):
        url = url.strip()
        if len(url) > 0 and url != "http://":
            if not url.startswith("http://"):
                url = "http://" + url
            if url.endswith(".opml"):
                self.opmltree.AddDirectoryRoot("User-added root",url)
                return None
            if itunes.itunes_url_p(url):
                try:
                    log.info("Attempting to convert iTunes url: %s" % url)
                    oldurl = url
                    url = itunes.feedurl_from_itunes_url(url)
                    log.info("iTunes url %s is now known as %s" % (oldurl,url))
                except:
                    log.exception("Error converting iTunes url.  Sorry it didn't work out.")
                    return None
                if url == None:
                    log.exception("Error converting iTunes url.  Sorry it didn't work out.")
                    return None

            fds = self.ipodder.feeds
            for feedinfo in fds:
                if feedinfo.url == url:
                    feedinfo.sub_state = 'subscribed'
                    fds.flush()
                    self.PopulateFeedsList()
                    return feedinfo
            title = None
            #Note: feeds are added as "subscribed", not "newly subscribed",
            #because now the user can explicitly say what they want to happen.
            if feed and hasattr(feed,"feed") and hasattr(feed.feed,"title"):
                title = feed.feed.title
            if title:
                displayTitle = title
                feedinfo = fds.addfeed(url,title=title,sub_state='newly-subscribed')
            else:
                displayTitle = url
                feedinfo = fds.addfeed(url,sub_state='newly-subscribed')
                
            id = wx.NewId()
            self.feedsdict[id] = feedinfo
            index = self.feedslist.InsertStringItem(self.feedslist.GetItemCount(),displayTitle)
            self.feedslist.SetStringItem(index,1,feedinfo.sub_state)
            self.feedslist.SetItemData(index,id)
            self.SetLemon(feedinfo)
            while self.feedslist.GetFirstSelected() != -1:
                self.feedslist.Select(self.feedslist.GetFirstSelected(),False)
            self.feedslist.Select(index)
            self.mainpanel.ResetSortMixin()
            post_sort_index = self.FeedInfoToIndex(feedinfo)
            self.feedslist.EnsureVisible(post_sort_index)
            if raise_tab:
                self.notebook.SetSelection(SUBSCRIPTIONS_INDEX)
                self.feedslist.SetFocus()
            fds.flush()
            del fds
            return feedinfo
        
    def OnToggleChecked(self,event):
        for n in range(self.feedslist.GetItemCount()):
            if self.feedslist.IsSelected(n):
                id = self.feedslist.GetItemData(n)
                if self.feedsdict[id].sub_state == 'disabled':
                    self.feedsdict[id].sub_state = 'subscribed'
                else:
                    if self.feedsdict[id].title:
                        displayTitle = self.feedsdict[id].title
                    else:
                        displayTitle = self.feedsdict[id].url
                    alert = wx.MessageDialog(self.frame, "%s %s?" % (self._("str_really_delete"), displayTitle), style=wx.OK|wx.CANCEL)

                    response = alert.ShowModal()
                    alert.Destroy()
                    if response != wx.ID_OK:
                        return
                    self.feedsdict[id].sub_state = 'disabled'
        self.ipodder.feeds.flush()
        self.PopulateFeedsList()

    def FeedDownloadAuthError(self,feedinfo):
        self.ThreadSafeDispatch(self.HandleFeedDownloadAuthError,feedinfo)

    def HandleFeedDownloadAuthError(self,feedinfo):
        self.feedwindow.UpdateFeed(feedinfo, self.ipodder, tab=gui.iPodderWindows.FEEDWINDOW_AUTH_TAB)
        self.frame.SetFocus()
        
    def FeedDownloadThreadComplete(self,dl,enclosures,feedinfo):
        self.ThreadSafeDispatch(self.PostFeedDownloadUpdate,dl,enclosures,feedinfo)

    def PostFeedDownloadUpdate(self,dl,enclosures,feedinfo):
        if dl in self.feedwindowthreads:
            self.feedwindowthreads.remove(dl)
            del dl
        #Check to see if the user's selection changed.
        first = self.feedslist.GetFirstSelected()
        if first == -1:
            #no selection
            return
        selected_feedinfo = self.feedsdict[self.feedslist.GetItemData(first)]
        if selected_feedinfo != feedinfo:
            #new selection
            return

        #If we get here, we're ready to update the window.
        self.UpdateFeedsListItem(feedinfo)
        self.displaying_episodes_for = feedinfo
        self.episodes.DeleteAllItems()
        self.episodesdict = {}
        if not len(enclosures):
            self.episodes.InsertImageStringItem(0,self._("str_no_episodes_found"),-1)
            return
        count = 0
        for enclosure in enclosures:
            url = enclosure.url
            index = self.episodes.InsertStringItem(self.episodes.GetItemCount(),enclosure.item_title)
            id = wx.NewId()
            self.episodesdict[id] = enclosure
            self.episodes.SetItemData(index,id)
            self.episodes.SetStringItem(index,1,self._("str_dl_state_%s" % enclosure.status))
            if enclosure.status == 'downloaded' and os.path.exists(enclosure.filename):
                self.episodes.SetItemImage(index,self.play_file_idx,self.play_file_idx)
            elif enclosure.status in ['to_download','new','partial']:
                self.episodes.SetItemImage(index,self.box_checked_idx,self.box_checked_idx)
            else:
                self.episodes.SetItemImage(index,self.box_unchecked_idx,self.box_unchecked_idx)
            if hasattr(enclosure,'length'):
                mb = "%4.1f" % (int(enclosure.length)/(1024.0*1024))
                self.episodes.SetStringItem(index,2,mb)
            self.episodes.SetStringItem(index,3,url)

            count += 1
            if count % 2 == 1:
                self.episodes.SetItemBackgroundColour(index,STRIPE_ODD_COLOR)
            
        #We handled new feed behavior in the loop so iPodder.py should treat
        #the feed like any other.
        if feedinfo.sub_state == 'newly-subscribed':
            feedinfo.sub_state = 'subscribed'
            feedinfo.half_flush()
            
        self.UpdateFeedsListItem(feedinfo)
        if self.notebook.GetSelection() == SUBSCRIPTIONS_INDEX \
           and self.frame.FindFocus() not in [self.feedslist,self.episodes]:
            self.feedslist.SetFocus()

    def DownloadThreadComplete(self,dl,mask):
        self.ThreadSafeDispatch(self.PostDownloadUpdate,dl,mask)

    def PostDownloadUpdate(self,dl,mask):
        self.toolbarSubscr.EnableTool(self.toolCheckAllId,True)
        self.toolbarSubscr.EnableTool(self.toolCatchupId,True)
        self.menucheckall.Enable(True)    
        self.menucheckselected.Enable(True)    
        self.menucatchup.Enable(True)
        self.searchboxdownloads.Enable(True)
        self.searchboxfeeds.Enable(True)

        self.EnableLanguages(True)

        sel_idx = self.feedslist.GetFirstSelected()
        if sel_idx != -1:
            self.toolbarSubscr.EnableTool(self.toolCheckSelectedId,True)
            self.toolbarSubscr.EnableTool(self.toolToggleCheckedId,True)
            self.toolbarSubscr.EnableTool(self.toolFeedPropertiesId,True)

        if dl in self.threads:
            self.threads.remove(dl)
            del dl
        try:
            icon = wx.Icon(os.path.join(self.basepath,'icons_status','icon_idle_empty.ico'), wx.BITMAP_TYPE_ICO)
            self.tbIcon.SetIcon(icon, PRODUCT_NAME)
        except:
            pass

        log.info( self.m_stringtable.GetText(self.m_currentlanguage, "str_last_check") + " " + time.asctime(time.localtime()) )
        self.progressBar.SetValue(0)
        self.PopulateFeedsList()
        self.nextrun.SetLabel(asctimeOrNone(self.s.getNextRun()))
        self.nextrun2.SetLabel(asctimeOrNone(self.s.getNextRun()))
        if mask:
            feedinfo = mask[0]
            self.SelectSubscription(feedinfo)
        elif sel_idx != -1:
            feedinfo = self.feedsdict[self.feedslist.GetItemData(sel_idx)]
            self.SelectSubscription(feedinfo)
            
        self.MaybeShowDonateDialog()

        self.InitCleanup()
        
        if self.waiting_for_quit:
            self.ready_to_quit = True
        
    def SelectSubscription(self,feedinfo):
        for i in range(self.feedslist.GetItemCount()):
            if self.feedsdict[self.feedslist.GetItemData(i)] == feedinfo:
                self.feedslist.Select(i,False)
                self.feedslist.Select(i,True)
                self.feedslist.EnsureVisible(i)
                return

    def OnTimerSched(self, evt):
        if len(self.threads):
            #OnCheckNow isn't blocking so we bypass if a check is running.
            return
        #log.debug(time.asctime(time.localtime()) + ": Checking for scheduled run")
        if self.s.checkTimeToRun():
            log.debug(time.asctime(time.localtime()) + ": Running scheduled sync")
            self.s.logLastRun()
            self.OnCheckNow(evt)

    def OnSchedChk(self, evt):
        self.EnsureSchedChks()

    def OnAutoChk(self, evt):
        for widget in self.schedWidgets:
            widget.Enable(evt.IsChecked())
        if evt.IsChecked():
            if not self.t1.IsRunning():
                self.t1.Start(TIMER_INTERVAL)
        else:
            if self.t1.IsRunning():
                self.t1.Stop()
            return
        
        if self.ipodder.config.sched_runMode == "specific":
            evt = wx.PyCommandEvent(wx.wxEVT_COMMAND_RADIOBUTTON_SELECTED,xrc.XRCID("SCHEDSPECIF"))
            self.frame.GetEventHandler().ProcessEvent(evt)
        elif self.ipodder.config.sched_runMode == "regular":
            evt = wx.PyCommandEvent(wx.wxEVT_COMMAND_RADIOBUTTON_SELECTED,xrc.XRCID("SCHEDREG"))
            self.frame.GetEventHandler().ProcessEvent(evt)

    def EnsureSchedChks(self):
        if self.enableauto.GetValue():
            for i in range(len(self.schedSpecif)):
                self.enableSpecif[i].Enable(True)
                self.schedSpecif[i].Enable(self.enableSpecif[i].IsChecked())

    #AG: Due to some quirk in our xrc-based layout, the radio buttons
    #for checking at specific times vs. regular intervals must be treated
    #as coming from separate groups, rather than as a single group.  I think
    #this comes from the fact that the two RadioButtons aren't created in
    #sequence -- others controls are created in between.
    #
    #The upshot of all this is that we have to manage the selects/deselects
    #to ensure that this faked radiobutton group is in a consistent state.
    #We do this by only ever setting the values of the two controls from
    #the two event handlers below.

    def OnSchedRadioSpecif(self, evt):
        self.schedspecific.SetValue(True)
        self.schedreg.SetValue(False)
        self.EnsureSchedChks()
        for w in self.schedRegGroup:
            w.Enable(False)

    def OnSchedRadioReg(self, evt):
        self.schedspecific.SetValue(False)
        self.schedreg.SetValue(True)
        for w in self.schedRegGroup:
            w.Enable(True)
        for w in self.schedSpecifGroup:
            w.Enable(False)

    def InitSchedWidgets(self):
        for i in range(len(self.ipodder.config.sched_runTimes)):
            if i < len(self.schedSpecif):
                self.schedSpecif[i].SetValue(self.ipodder.config.sched_runTimes[i])
                self.enableSpecif[i].SetValue(self.ipodder.config.sched_runTimesEnable[i])

        self.schedinterval.SetSelection(INTERVAL_HOURS.index(self.ipodder.config.sched_intervalHours))

        evt = wx.PyCommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,xrc.XRCID("ENABLEAUTO"))
        if self.ipodder.config.sched_enableAuto == "off":
            self.enableauto.SetValue(False)
            evt.SetInt(0)
        else:
            self.enableauto.SetValue(True)
            evt.SetInt(1)
        self.frame.GetEventHandler().ProcessEvent(evt)

    def OnCancelSched(self,evt):
        self.InitSchedWidgets()
        self.scheddialog.EndModal(0)
        
    def OnSaveSched(self,evt):
        self.OnSaveSchedHelper(False)
        
    def OnSaveCloseSched(self,evt):
        self.OnSaveSchedHelper(True)
        
    def OnSaveSchedHelper(self,close):
        if self.enableauto.GetValue():
            self.ipodder.config.sched_enableAuto = "on"
        else:
            self.ipodder.config.sched_enableAuto = "off"
        if self.schedspecific.GetValue():
            self.ipodder.config.sched_runMode = "specific"
            newRunTimes = []
            for w in self.schedSpecif:
                (valid,normtime) = self.ValidateHourMinute(w.GetValue())
                if not valid:
                    alert = wx.MessageDialog(self.frame, "One of the scheduled times doesn't look right.  Valid times look like this: 10:02am, 16:43.", style=wx.OK)
                    alert.ShowModal()
                    alert.Destroy()
                    w.SetFocus()
                    return
                newRunTimes.append(normtime)
            newRunTimesEnable = []
            for w in self.enableSpecif:
                newRunTimesEnable.append(int(w.GetValue()))
            self.ipodder.config.sched_runTimes = newRunTimes
            self.ipodder.config.sched_runTimesEnable = newRunTimesEnable
        else:
            self.ipodder.config.sched_runMode = "regular"
            self.ipodder.config.sched_startingAt = time.strftime("00:%M",time.localtime(time.time()-120))
            self.ipodder.config.sched_intervalHours = INTERVAL_HOURS[self.schedinterval.GetSelection()]

        self.s.initScheduledRuns()
        self.ipodder.config.flush()
        self.nextrun.SetLabel(asctimeOrNone(self.s.getNextRun()))
        self.nextrun2.SetLabel(asctimeOrNone(self.s.getNextRun()))
        self.InitScheduleTool()
        
        if close:
            self.scheddialog.Show(0)
        else:
            alert = wx.MessageDialog(self.scheddialog, "Settings are saved.", style=wx.OK)
            alert.ShowModal()
            alert.Destroy()

    def OnClearLog(self,evt):
        self.ClearLogWindow()

    def ClearLogWindow(self):
        self.logwindow.Clear()

    def ValidateHourMinute(self,hourmin):
        """Check for proper time format and return a two-tuple containing
        the validation result, and a normalized hour:minute signature
        suitable for passing to the scheduler."""

        twentyfourhour = False
        clean = hourmin.replace(' ','')

        for fmt in ["%H:%M","%I:%M%p"]:
            try:
                tstruct = time.strptime(clean,fmt)
                return (True,time.strftime("%H:%M",tstruct))
            except ValueError:
                pass

        return (False,'')

    def AppendLogWindow(self, record): 
        if isinstance(record, logging.LogRecord): 
            level = record.levelno
            text = logging.Formatter().format(record)
        else: 
            level = logging.INFO
            text = unicode(record)
            
        try: 
            if self.logwindow.GetNumberOfLines() > 1000:
                self.logwindow.Clear()
        except wx._core.PyDeadObjectError: 
            pass

        color = wx.NullColor
        if SPAM <= level < logging.DEBUG: 
            color = wx.Color(192, 192, 192)
        if logging.DEBUG <= level < logging.INFO: 
            color = wx.Colour(128, 128, 128)
        elif logging.INFO <= level < logging.WARN: 
            color = wx.Colour(0, 0, 0) 
        elif logging.WARN <= level < logging.ERROR: 
            color = wx.Colour(64, 0, 0) 
        elif logging.ERROR <= level: 
            color = wx.Colour(128, 0, 0)

        self.logwindow.SetDefaultStyle(wx.TextAttr(color))
        timerep = "[%s] " % time.asctime(time.localtime())
        leveldesc = "%s " % logging.getLevelName(level)
        message = "%s%s%s\n" % (
                '', # timerep,
                '', # leveldesc, 
                text)
        #nlcount = len('\n'.split(message))
        self.logwindow.AppendText(message)
        sys.stdout.write(misc.encode(message)) 
        #self.logwindow.ShowPosition(self.logwindow.GetLastPosition())

    def UpdateProgress(self,percent):
        pass
    
    def progress(self, block_count, block_size, total_size):
        percent = int(100*block_count*block_size/float(total_size))
        #self.ThreadSafeDispatch(self.UpdateProgress,percent)

    def LaunchDownloadsRClickMenu(self,event):
        if self.downloads.GetFirstSelected() == -1:
            return
        if hasattr(self,"downloads_menu"):
            self.downloads_menu.Destroy()
        self.downloads_menu = wx.Menu()

        if self.downloads.GetSelectedItemCount() == 1:
            id = wx.NewId()
            self.downloads_menu.Append(id, self._("str_play_episode"))
            wx.EVT_MENU(self.downloads_menu, id, self.OnHistPlayRClick)
            self.downloads_menu.AppendSeparator()

            if clipboard.enabled:
                id = wx.NewId()
                self.downloads_menu.Append(id,self._("str_copy_location"))
                wx.EVT_MENU(self.downloads_menu, id, self.OnHistCopyLocation)

        id = wx.NewId()
        self.downloads_menu.Append(id,self._("str_clear_selected"))
        wx.EVT_MENU(self.downloads_menu, id, self.OnHistClearSelected)

        if self.downloads.GetSelectedItemCount() == 1:
            index = self.downloads.GetFirstSelected()
            enclosure = self.downloadsdict[self.downloads.GetItemData(index)]
            if (enclosure.item_link and (enclosure.item_link != enclosure.url)) or enclosure.description:
                id = wx.NewId()
                self.downloads_menu.Append(id,self._("str_show_notes"))
                wx.EVT_MENU(self.downloads_menu, id, self.OnDownloadShowNotes)            

            self.hooks('download-right-click',self.downloads_menu,enclosure)
       
        self.downloads.PopupMenu(self.downloads_menu)

    def OnDownloadShowNotes(self,event):
        if self.downloads.GetSelectedItemCount() == 1:
            index = self.downloads.GetFirstSelected()
            enclosure = self.downloadsdict[self.downloads.GetItemData(index)]
            self.LaunchShowNotesDialog(enclosure)
            
    def OnDownloadStart(self,encinfo):
        if encinfo is not None:
            self.ThreadSafeDispatch(self.DownloadTabLog, encinfo)
            # If switch_to_downloads_tab, do it. Be paranoid. 
            try: 
                if self.switch_to_downloads_tab: 
                    self.switch_to_downloads_tab = False
                    self.ThreadSafeDispatch(self.notebook.SetSelection, DOWNLOADS_INDEX)
            except AttributeError: 
                pass

            
    def OnDownloadedContent(self,encinfo,destfile):
        if self.preferences.dlCommandEnable.IsChecked() and encinfo.status == 'downloaded':
            command = self.preferences.dlCommand.GetValue().strip()
            if not command:
                return
            command = command.replace("%f",destfile)
            command = command.replace("%n",encinfo.feed.title)
            status = os.system(command)
            if status:
                log.info("There was an error running this command: %s" % command)

        if encinfo is not None: 
            self.ThreadSafeDispatch(self.DownloadTabLog, encinfo)
            self.ThreadSafeDispatch(self.UpdateEpisodeHistory, encinfo)
            
    def OnSubscrSelect(self, event):
        if not len(self.threads):
            self.toolbarSubscr.EnableTool(self.toolCheckSelectedId,True)
            self.menucheckselected.Enable(True)
        self.toolbarSubscr.EnableTool(self.toolToggleCheckedId,True)
        self.toolbarSubscr.EnableTool(self.toolFeedPropertiesId,True)
        self.menuremovefeed.Enable(True)
        self.menufeedproperties.Enable(True)
        

        feedinfo = self.feedsdict[self.feedslist.GetItemData(event.m_itemIndex)]
        if self.displaying_episodes_for != feedinfo:
            self.RefreshFeedWindowData(feedinfo)
        
    def OnSubscrDeselect(self, event):
        self.toolbarSubscr.EnableTool(self.toolCheckSelectedId,False)
        self.toolbarSubscr.EnableTool(self.toolToggleCheckedId,False)
        self.toolbarSubscr.EnableTool(self.toolFeedPropertiesId,False)
        self.menucheckselected.Enable(False)
        self.episodes.DeleteAllItems()
        self.displaying_episodes_for = None
        self.FrobMenus() #disables properties/remove menus if nothing's selected.

    def OnToolLeaveMac(self, event):
        """Simulate EVT_TOOL_ENTER for Mac"""
        key = event.GetEventObject().GetId()
        if self.selected_tool_dict.has_key(key):
            del self.selected_tool_dict[key]
        self.frame.SetStatusText("")

    def OnToolMotionMac(self, event):
        """Simulate EVT_TOOL_ENTER for Mac"""
        tool = event.GetEventObject().FindToolForPosition(event.GetX(),event.GetY())
        key = event.GetEventObject().GetId()
        if self.selected_tool_dict.has_key(key):
            old_message = self.selected_tool_dict[key]
        else:
            old_message = ""
        if tool:
            new_message = tool.GetShortHelp()
        else:
            new_message = ""

        if new_message != old_message:
            self.selected_tool_dict[key] = new_message
            self.frame.SetStatusText(new_message)

    def OnToolEnter(self, event):
        if event.GetSelection() != -1:
            self.frame.SetStatusText(event.GetEventObject().GetToolShortHelp(event.GetSelection()))
        else:
            self.frame.SetStatusText("")
            
    def OnCheckSelected(self, event):
        mask = []
        for n in range(self.feedslist.GetItemCount()):
            if self.feedslist.IsSelected(n):
                id = self.feedslist.GetItemData(n)
                mask.append(self.feedsdict[id])
        if len(mask):
           event.iPodderCheckSelectedMask = mask
           self.OnCheckNow(event)

    def OnCatchup(self,event):
        event.iPodderCatchup = 1
        self.OnCheckNow(event)
        
    def NotYetImplemented(self):
        alert = wx.MessageDialog(self.frame, "Sorry, this feature isn't implemented yet.", style=wx.OK)
        alert.ShowModal()
        alert.Destroy()

    def showlogpage(self, weshould): 
        """Show the log page if weshould."""

        logShown = False
        for n in range(self.notebook.GetPageCount()):
            testpage = self.notebook.GetPage(n) 
            if testpage == self.logPage:
                logShown = True
            
        if weshould:
            if not logShown: 
                self.notebook.InsertPage(LOGPAGE_INDEX,self.logPage,"Log",False)
        else:
            if logShown:
                if self.notebook.GetSelection() == LOGPAGE_INDEX:
                    #We have to change the selection first to avoid drawing errors.
                    self.notebook.SetSelection(0)
                self.notebook.RemovePage(LOGPAGE_INDEX)

        self.notebook.Refresh()
        
    def OnFeedsListChar(self, event):
        if event.GetKeyCode() == wx.WXK_F10 and event.ShiftDown():
            self.feedslist.PopupMenu(self.feedmenu)
        if event.GetKeyCode() == wx.WXK_DELETE:
            self.OnToggleChecked(event)
        event.Skip()
        
    def OnFeedsListRClick(self, event):
        self.feedslist.PopupMenu(self.feedmenu)

    def OnCopyFeedLocation(self, event):
        idx = self.feedslist.GetFirstSelected()
        if idx == -1:
            return
        feed = self.feedsdict[self.feedslist.GetItemData(idx)]
        clipboard.set_clipboard_text(feed.url)
        
    def OnOpenFeedFolder(self, event):
        idx = self.feedslist.GetFirstSelected()
        if idx == -1:
            return
        feed = self.feedsdict[self.feedslist.GetItemData(idx)]
        if "Win" in platform.system():
            os.spawnv(os.P_NOWAIT, \
                  os.environ["COMSPEC"], \
                  ["/Q","/C",'"explorer ""%s"""' % \
                  os.path.join(self.ipodder.config.download_dir,feed.dirname)])
        else:
            windowCmd = None
            if "Darwin" in platform.system():
                windowCmd = "/usr/bin/open"
            if "Linux" in platform.system():
                if os.system("which konqueror>/dev/null") == 0:
                    windowCmd = "konqueror"
                if os.system("which nautilus>/dev/null") == 0:
                    windowCmd = "nautilus"
            if windowCmd:
                retval = os.system(windowCmd +" \"" + os.path.join(self.ipodder.config.download_dir,feed.dirname)+"\"")
                if retval != 0:
                    alert = wx.MessageDialog(self.frame, "There was an error opening this folder.  Maybe it hasn't been created yet.  If this is the case, it will be created when the first file is downloaded", style=wx.OK)
                    alert.ShowModal()
                    alert.Destroy()
            else:
                alert = wx.MessageDialog(self.frame, "We couldn't figure out how to open the folder on your system.  Sorry!", style=wx.OK)
                alert.ShowModal()
                alert.Destroy()

    def OnOpenFeedInBrowser(self, event):
        first = self.feedslist.GetFirstSelected()
        if first != -1:
            feedinfo = self.feedsdict[self.feedslist.GetItemData(first)]
            webbrowser.open(feedinfo.url)

    def OnOpenFeedProperties(self,event):
        first = self.feedslist.GetFirstSelected()
        if first != -1:
            feedinfo = self.feedsdict[self.feedslist.GetItemData(first)]
            self.feedwindow.UpdateFeed(feedinfo, self.ipodder)
            self.frame.SetFocus()
            
    def RefreshFeedWindowData(self,feedinfo):
        if len(self.feedwindowthreads) > 5:
            log.error("RefreshFeedWindowData: Aborting because there are too many feed downloads.")
            return
        self.episodes.InsertImageStringItem(0,self.m_stringtable.GetText(self.m_currentlanguage, "str_downloading_episode_info"),-1)
        thr = iPodderFeedDownload(self,feedinfo)
        thr.m_ipodder = self.ipodder
        thr.m_frame = self.frame
        thr.start()
        self.feedwindowthreads.append(thr)
        if self.notebook.GetSelection() == SUBSCRIPTIONS_INDEX:
            self.feedslist.SetFocus()

    def OnBannerClick(self, event):
        webbrowser.open(skin.BANNER_URL)

    def OnEpisodesListChar(self,event):
        if event.GetKeyCode() == wx.WXK_F10 and event.ShiftDown():
            index = self.episodes.GetFirstSelected()
            if index == -1:
                return
            self.LaunchEpisodesRClickMenu(index)
        if event.GetKeyCode() == wx.WXK_SPACE:
            index = self.episodes.GetFirstSelected()
            if index != -1:
                self.ToggleEpisodesListItem(index)
        event.Skip()

    def OnEpisodesListLeftDown(self,event):
        (index, flags) = self.episodes.HitTest(event.GetPosition())
        if event.GetX() <= 16:
            self.ToggleEpisodesListItem(index)
        event.Skip()

    def ToggleEpisodesListItem(self,index):
        encinfo = self.episodesdict[self.episodes.GetItemData(index)]

        if encinfo.status == 'downloaded' and encinfo.filename != None:
            if encinfo.filename.endswith(".torrent"):
                path = encinfo.filename[:-8]
            else:
                path = encinfo.filename
            if os.path.exists(path):
                self.PlayEpisode(path)
        elif encinfo.status in ['skipped','cancelled','removed']:
            encinfo.status = 'to_download'
            encinfo.filename = None
            encinfo.marked = True
            self.ipodder.history.save_encinfo(encinfo)
            self.episodes.SetStringItem(index,1,self._("str_dl_state_%s" % encinfo.status))
            self.episodes.SetItemImage(index,self.box_checked_idx,self.box_checked_idx)            
        else:
            encinfo.status = 'skipped'
            encinfo.marked = False
            self.ipodder.history.save_encinfo(encinfo)
            self.episodes.SetStringItem(index,1,self._("str_dl_state_%s" % encinfo.status))
            self.episodes.SetItemImage(index,self.box_unchecked_idx,self.box_unchecked_idx)
            
    def OnEpisodesListRClick(self,event):
        if event.m_itemIndex != -1:
            self.LaunchEpisodesRClickMenu(event.m_itemIndex)

    def LaunchEpisodesRClickMenu(self,index):
        if hasattr(self,"feed_episode_menu"):
            self.feed_episode_menu.Destroy()
        self.feed_episode_menu = wx.Menu()
        enclosure = self.episodesdict[self.episodes.GetItemData(index)]
        if enclosure.filename and os.path.exists(enclosure.filename):
            id = wx.NewId()
            self.feed_episode_menu.Append(id,self._("str_play_episode"))
            wx.EVT_MENU(self.feed_episode_menu, id, self.OnPlayEpisode)
        if clipboard.enabled:
            id = wx.NewId()
            self.feed_episode_menu.Append(id,self._("str_copy_location"))
            wx.EVT_MENU(self.feed_episode_menu, id, self.OnCopyEpisodeLocation)
        while self.episodes.GetFirstSelected() != -1:
            self.episodes.Select(self.episodes.GetFirstSelected(),False)
        self.episodes.Select(index)
        self.feed_episode_menu_info = enclosure
        if (enclosure.item_link and (enclosure.item_link != enclosure.url)) or enclosure.description:
            id = wx.NewId()
            self.feed_episode_menu.Append(id,self._("str_show_notes"))
            wx.EVT_MENU(self.feed_episode_menu, id, self.OnShowNotes)            
        self.hooks('episode-right-click',self.feed_episode_menu,enclosure)
        self.episodes.PopupMenu(self.feed_episode_menu)

    def OnCopyEpisodeLocation(self,event):
        enclosure = self.feed_episode_menu_info
        clipboard.set_clipboard_text(enclosure.url)

    def OnPlayEpisode(self,event):
        enclosure = self.feed_episode_menu_info
        if enclosure.filename and os.path.exists(enclosure.filename):
            self.PlayEpisode(enclosure.filename)
        else:
            log.warn("OnPlayEpisode was called for url %s in feed %s but we couldn't find the file" % (feedinfo.title,url))

    def OnShowNotes(self,event):
        enclosure = self.feed_episode_menu_info
        self.LaunchShowNotesDialog(enclosure)
        
    def LaunchShowNotesDialog(self,enclosure):
        if enclosure.item_link and enclosure.item_link != enclosure.url:
             webbrowser.open(enclosure.item_link)
        elif enclosure.description:
            filename = os.path.join(self.ipodder.config.download_dir,"ShowNotes.html")
            fh = open(filename,"w")
            title = misc.encode(enclosure.item_title)
            desc = misc.encode(enclosure.description)
            fh.write("<html><head><title>%s</title>" \
                     "</head><body>%s</body></html>" % (title, desc))
            fh.close()
            webbrowser.open(filename)
            
    def PlayEpisode(self, path):
        try: 
            try:
                (base,ext) = os.path.splitext(path)
                browser = False
                if ext.lower() == ".torrent":
                    self.PlayEpisode(base)
                    return
                
                if ext.lower() in [".mov",".mpg",".wmv",".avi"]:
                    browser = True

                if browser == True:
                    webbrowser.open('file://' + misc.encode(path, replace=False))
                
                if browser == False:
                    self.ipodder.config.player.play_file(path,rude=True)
                    
            except NotImplementedError:
                log.warn("Your player doesn't support playing files.  Launching in your web browser instead.")
                webbrowser.open('file://' + misc.encode(path, replace=False))
        except UnicodeEncodeError: # raised via misc.encode
            msg = ( "Juice couldn't successfully convert all of a filename " 
                    "to ASCII to send to your browser to be played because "
                    "it had international characters not supported by your "
                    "system's current encoding. The filename was %s (with "
                    "the unsupported characters replaced with question "
                    "marks), and we tried code page %s." ) % (
                          misc.encode(path), 
                          locale_preferred_encoding
                      )
            log.error("%s", message)
            alert = wx.MessageDialog(None, message, style=wx.OK)
            response = alert.ShowModal()
            alert.Destroy()

    def InitCleanup(self,selected_feedinfo=None):
        self.cleanupfeeds.Clear()
        self.cleanupepisodes.Clear()
        filteredfeeds = []

        # First, calculate the feed contents. 
        totmb = 0
        for feedinfo in self.ipodder.feeds:
            mb = feedinfo.mb_on_disk() 
            totmb = totmb + mb
            if mb or feedinfo.sub_state == 'subscribed':
                filteredfeeds.append((feedinfo, mb))

        if self.ipodder.config.cleanup_sort_by_size: 
            # Comparer #1: take the second item of each tuple, which is a 
            # size in MB; and compare based on that. 
            comparer = lambda a, b: cmp(b[1], a[1])
        else: 
            # Comparer #2: take the first item of each tuple, which is a 
            # feedinfo; convert it to a string; and then compare based on 
            # that. 
            comparer = lambda a, b: cmp(str(a[0]), str(b[0]))

        # Now, sort:
        filteredfeeds.sort(comparer)
        
        # Start cleanupfeeds with one or two specials: 
        #everything = ("Everything (at least %4.1fMB)" % totmb, 'everything')
        #self.cleanupfeeds.Append(*everything)
        if hasattr(self.ipodder.config.player, 
                   'get_unchecked_tracks_under_directory'): 
            unchecked = ("Unchecked songs in iTunes", players.UNCHECKED_SONGS)
            self.cleanupfeeds.Append(*unchecked)
            
        # Append to cleanupfeeds information on each feed we prepared 
        # earlier.   
        for (feedinfo,mb_on_disk) in filteredfeeds:
            if feedinfo.title:
                display = "%s (%4.1fMB)" % (feedinfo.title,mb_on_disk)
            else:
                display = "%s (%4.1fMB)" % (feedinfo.url,mb_on_disk)

            self.cleanupfeeds.Append(display,feedinfo)
            if feedinfo == selected_feedinfo:
                self.cleanupfeeds.Select(self.cleanupfeeds.GetCount()-1)
            
    def OnCleanupFeedChoice(self,event):
        #We can be raised from either the selectlist or the radiobuttons.
        selected_idx = -1
        if event.GetEventType() == wx.wxEVT_COMMAND_CHOICE_SELECTED:
            selected_idx = event.GetSelection()
        else:
            selected_idx = self.cleanupfeeds.GetSelection()
        
        if  selected_idx != -1:
            feedinfo = self.cleanupfeeds.GetClientData(selected_idx)
            self.PopulateCleanupEpisodes(feedinfo)
        
    def PopulateCleanupEpisodes(self,feedinfo):
        self.cleanupepisodes.Clear()
        self.cleanupepisodesdict = {}
        files = []

        if self.cleanupsrcplayer.GetValue():
            player = self.ipodder.config.player
            if isinstance(feedinfo, str): 
                if feedinfo == players.UNCHECKED_SONGS: 
                    gutud = player.get_unchecked_tracks_under_directory
                    filenames = gutud(self.ipodder.config.download_dir)
                    files.extend(misc.get_fileinfos(filenames))
            else:
                files.extend(player.playlist_fileinfos(feedinfo.title))
            
        if self.cleanupsrcfolder.GetValue():
            if not isinstance(feedinfo, str): 
                #Weed out any duplicates with the player library.
                for fileinfo in feedinfo.getfiles():
                    if not files.count(fileinfo):
                        files.append(fileinfo)

        #Sort by creation time, to make it easy to delete the oldest
        #files first.
        files.sort(lambda a, b: cmp(a[2],b[2]))

        for (display,path,ctime,size) in files:
            display = self.ipodder.history.pretty_name_from_path(path)
            label = "%s (%4.1fMB; %s)" % (display,size/(1024.0*1024),time.strftime("%d %b %Y",time.localtime(ctime)))
            idx = self.cleanupepisodes.Append(label)
            self.cleanupepisodesdict[idx] = path
            if idx % 2 == 1:
                self.cleanupepisodes.SetItemBackgroundColour(idx,STRIPE_EVEN_COLOR)
            else:
                self.cleanupepisodes.SetItemBackgroundColour(idx,STRIPE_ODD_COLOR)
            if CLEANUP_FG:
                self.cleanupepisodes.SetItemForegroundColour(idx,CLEANUP_FG)

        if not len(files):
            idx = self.cleanupepisodes.Append(self._("str_no_episodes_found"))
            
    def OnCleanupDelete(self,event):
        feedinfo = self.cleanupfeeds.GetClientData(self.cleanupfeeds.GetSelection())
        files = []
        for idx in range(self.cleanupepisodes.GetCount()):
            if self.cleanupepisodes.IsChecked(idx):
                try:
                    files.append(self.cleanupepisodesdict[idx])
                except KeyError:
                    #they probably clicked Delete when no episodes were found.
                    pass
                
        if self.cleanupdellibrary.IsChecked():
            #On Windows we must delete the file from iTunes before deleting
            #from the local filesystem to avoid leaving a dead track behind.
            if isinstance(feedinfo, str): 
                title = feedinfo
            else: 
                title = feedinfo.title
            self.ipodder.config.player.remove_files([(title, files)])

        if self.cleanupdelfiles.IsChecked():
            self.ipodder.remove_files(files)
            
        self.InitCleanup(feedinfo)
        self.PopulateCleanupEpisodes(feedinfo)

    def OnCleanupCheckAll(self,event):
        for idx in range(self.cleanupepisodes.GetCount()):
            self.cleanupepisodes.Check(idx)

    def OnCleanupCheckNone(self,event):
        for idx in range(self.cleanupepisodes.GetCount()):
            self.cleanupepisodes.Check(idx,False)

    def OnCleanupRefresh(self,event):
        self.InitCleanup()

    def DownloadTabIndexFromEncinfo(self,encinfo):
        """Iterate through the download tab contents, looking for a matching
        encinfo.  Use with caution."""

        for i in range(self.downloads.GetItemCount()):
            id = self.downloads.GetItemData(i)
            candidate = self.downloadsdict[id]       
            if candidate.url == encinfo.url and \
               candidate.creation_time == encinfo.creation_time:
                return i
        return -1
    
    def DownloadTabLog(self,encinfo,prune=True):
        if encinfo.marked:
            index = -1
            if not encinfo.status == "queued":
                #encinfo should be logged, so let's try to find and update it.
                #In theory we could run this every time but it will get slower
                #and slower, so we skip it if we can.
                index = self.DownloadTabIndexFromEncinfo(encinfo)
            if index == -1:
                index = self.downloads.InsertStringItem(0,encinfo.item_title)
            self.downloads.SetStringItem(index,1,self._("str_dl_state_" + encinfo.status))
            self.downloads.SetStringItem(index,2,encinfo.GetStatusDownloadSpeed())
            if encinfo.download_completed:
                self.downloads.SetStringItem(index,3,time.strftime("%d %b %Y, %H:%M:%S",encinfo.download_completed))
            else:
                self.downloads.SetStringItem(index,3,"--")
            self.downloads.SetStringItem(index,4,unicode(encinfo.feed))
            self.downloads.SetStringItem(index,5,encinfo.url)
            if encinfo.status == "downloading":
                imgidx = self.dl_downloading_idx
            elif encinfo.status == "downloaded":
                imgidx = self.dl_play_file_idx
            elif encinfo.status == "cancelled":
                imgidx = self.dl_cancelled_idx
            elif encinfo.status == "partial":
                imgidx = self.dl_cancelled_idx
            else:
                imgidx = self.dl_blank_idx
            self.downloads.SetItemImage(index,imgidx,imgidx)

            id = wx.NewId()
            self.downloadsdict[id] = encinfo
            self.downloads.SetItemData(index,id)
            #set stripe
            if self.downloads.GetItemCount() == 1 or self.downloads.GetItemBackgroundColour(1) == STRIPE_EVEN_COLOR:
                self.downloads.SetItemBackgroundColour(0,STRIPE_ODD_COLOR)
            else:
                self.downloads.SetItemBackgroundColour(0,STRIPE_EVEN_COLOR)           

            if self.downloads.IsSelected(index):
                if encinfo.status == "downloading":
                    self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,True)
                else:
                    self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,False)               

        if prune:
            self.DownloadTabPrune()

    def DownloadTabPrune(self):
        if self.downloads.GetItemCount() > MAX_DOWNLOADS_DISPLAY:
            self.ClearHistoryItemsByIndex(range(MAX_DOWNLOADS_DISPLAY,self.downloads.GetItemCount()))

    def DownloadTabPruneFiles(self,files):
        """This function should be called by cleanup routines that delete
        files rom the hard disk.  This removes any downloads associated with
        those files from the Downloads tab."""
        log.debug("Files to prune: %s" % str(files))
        items_to_del = []
        for i in range(self.downloads.GetItemCount()):
            id = self.downloads.GetItemData(i)
            candidate = self.downloadsdict[id]       
            if candidate.filename in files:
                items_to_del.append(i)
        if len(items_to_del) > 0:
            log.debug("Deleting entries at these indexes: %s" % str(items_to_del))
            self.ClearHistoryItemsByIndex(items_to_del)
            
    def OnDownloadsChar(self,event):
        if event.GetKeyCode() == wx.WXK_F10 and event.ShiftDown():
            self.LaunchDownloadsRClickMenu(event)
        if event.GetKeyCode() == wx.WXK_SPACE:
            index = self.downloads.GetFirstSelected()
            if index != -1:
                self.OnHistPlayIndex(index)
        if event.GetKeyCode() == wx.WXK_DELETE:
            self.OnHistClearSelected(event)
            
        event.Skip()

    def OnDownloadsTabSel(self,event):
        index = event.m_itemIndex
        id = self.downloads.GetItemData(index)
        encinfo = self.downloadsdict[id]
        if encinfo.status == "downloading":
            self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,True)
        else:
            self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,False)               

    def OnDownloadsTabDesel(self,event):
        self.toolbarDownloads.EnableTool(self.toolCancelHistSelId,False)               

    def OnDownloadsTabLeftDown(self,event):
        (index, flags) = self.downloads.HitTest(event.GetPosition())
        if event.GetX() <= 16:
            #They clicked on an image.
            self.OnHistPlayIndex(index)
            
        event.Skip()

    def PopulateDownloadsTab(self):
        try:
            encinfolist = self.ipodder.state['latest_downloads']
            self.m_encinfolist = encinfolist
        except KeyError:
            migrate = False
            try:
                if self.ipodder.state.has_key('tmp_downloads'):
                    migrate= True
            except ImportError:
                migrate = True
            if migrate:
                log.info("PopulateDownloadsTab: Found 2x-style tmp_downloads list, attempting to migrate.")
                from ipodder import compatibility
                encinfolist = compatibility.migrate_2x_tmp_downloads(self.basepath,self.ipodder.state)
                self.m_encinfolist = encinfolist
                log.info("PopulateDownloadsTab: Finished migrating downloads.  Got %d enclosures." % len(encinfolist))
            else:
                self.m_encinfolist = []
                return
                
        for encinfo in encinfolist:
            self.DownloadTabLog(encinfo,prune=False)

        self.DownloadTabPrune()

    def OnHistCopyLocation(self,event):
        index = self.downloads.GetFirstSelected()
        if index != -1:
            id = self.downloads.GetItemData(index)
            encinfo = self.downloadsdict[id]
            clipboard.set_clipboard_text(encinfo.url)
            
    def OnHistPlayRClick(self,event):
        index = self.downloads.GetFirstSelected()
        if index != -1:
            self.OnHistPlayIndex(index)
        
    def OnHistPlayIndex(self,index):
        id = self.downloads.GetItemData(index)
        encinfo = self.downloadsdict[id]
        if not encinfo.status == "downloaded":
            return
        feedinfo = encinfo.feed
        path = encinfo.filename
        if path != None:
            if path.endswith(".torrent"):
                path = path[:-8]
            self.PlayEpisode(path)

    #UpdateEpisodeHistory() and ClearHistoryItemsByIndex() must be coordinated
    #because they re-assign a state db variable from an in-memory copy.
    #We rely on the event manager for the wx.App, calling UpdateEpisodeHistory
    #from the thread-safe dispatcher.
    def UpdateEpisodeHistory(self,encinfo):
        if encinfo.marked:
            state = self.ipodder.state
            try: 
                encinfolist = state.get('latest_downloads', [])
            except KeyError: 
                # This happens if a recorded download refers to a feed 
                # we've sinced ditched. 
                encinfolist = []
            encinfolist.append(encinfo)
            state['latest_downloads'] = encinfolist
            if hasattr(state, 'sync'): state.sync()
            self.m_encinfolist = encinfolist
            
    def OnHistClearSelected(self,event):
        start = i = self.downloads.GetFirstSelected()
        items_to_del = []
        encinfos_to_cancel = []
        while i != -1:
            id = self.downloads.GetItemData(i)
            encinfo = self.downloadsdict[id]
            if encinfo.status == 'downloading':
                encinfos_to_cancel.append(encinfo)
            else:
                items_to_del.insert(0,i)
                encinfo.status = 'clearing'
            i = self.downloads.GetNextSelected(i)
        self.ClearHistoryItemsByIndex(items_to_del)
        if len(encinfos_to_cancel):
            self.StartCancelThread(encinfos_to_cancel)
        #reset the focus
        if start < self.downloads.GetItemCount():
            self.downloads.Select(start)
        else:
            self.downloads.Select(self.downloads.GetItemCount()-1)
            
    def ClearHistoryItemsByIndex(self,items_to_del):
        #Items must be in reverse order to ensure that
        #deleting items from the listctrl doesn't change its indexing.
        items_to_del.sort()
        items_to_del.reverse()
        
        encinfolist = self.ipodder.state['latest_downloads']
        for i in items_to_del:
            id = self.downloads.GetItemData(i)
            encinfo = self.downloadsdict[id]
            for j in range(len(encinfolist)):
                candidate = encinfolist[j]
                if candidate.url == encinfo.url and \
                   candidate.download_completed == encinfo.download_completed:
                    del encinfolist[j]
                    break
            self.downloads.DeleteItem(i)
        self.ipodder.state['latest_downloads'] = encinfolist
        if hasattr(self.ipodder.state, 'sync'): self.ipodder.state.sync()

        #re-stripe if necessary
        if len(items_to_del) % 2 == 1:
            start = items_to_del[-1]
            count = self.downloads.GetItemCount()
            if start <= count - 1:
                for i in range(start,count):
                    if self.downloads.GetItemBackgroundColour(i) == STRIPE_EVEN_COLOR:
                        self.downloads.SetItemBackgroundColour(i,STRIPE_ODD_COLOR)
                    else:
                        self.downloads.SetItemBackgroundColour(i,STRIPE_EVEN_COLOR)           
                    
    def OnHistCancelSelected(self,event):
        i = self.downloads.GetFirstSelected()
        encinfos_to_cancel = []
        while i != -1:
            id = self.downloads.GetItemData(i)
            encinfo = self.downloadsdict[id]
            encinfos_to_cancel.append(encinfo)
            i = self.downloads.GetNextSelected(i)
        self.StartCancelThread(encinfos_to_cancel)
                
    def CancelRunningDownloads(self):
        for i in range(self.downloads.GetItemCount()):
            id = self.downloads.GetItemData(i)
            encinfo = self.downloadsdict[id]
            if encinfo.status == 'downloading':
                self.downloads.Select(i,True)
            if encinfo.status == 'queued':
                encinfo.status = 'clearing'
            
        self.OnHistCancelSelected(None)
            
    def StartCancelThread(self,encinfos_to_cancel):
        if len(self.threads):
            if len(self.cancelthreads) > 5:
                log.error("OnHistCancelSelected: Aborting because there are too many cancel threads.")
                return

        thr = iPodderCancel(self,encinfos_to_cancel)
        thr.start()
        self.cancelthreads.append(thr)

    def CancelThreadComplete(self,thr,encinfos_to_cancel):
        self.ThreadSafeDispatch(self.PostCancelUpdate,thr,encinfos_to_cancel)

    def PostCancelUpdate(self,thr,encinfos_to_cancel):
        log.debug("Cancelled %d downloads" % len(encinfos_to_cancel))
        if thr in self.cancelthreads:
            self.cancelthreads.remove(thr)
            del thr
        if len(encinfos_to_cancel) > 0:
            for encinfo in encinfos_to_cancel:
                self.DownloadTabLog(encinfo,prune=False)
        else:
            #We weren't downloading so we must set the quit flag here.
            if self.waiting_for_quit:
                self.ready_to_quit = True
            
    def _(self,key,args=None):
        return self.m_stringtable.GetText(self.m_currentlanguage,key,args=args)

    def IsSubscriptionsTabSelected(self):
        """Helps us decide whether to show the checkbox on the feed properties
           window."""
        return (self.notebook.GetSelection() == SUBSCRIPTIONS_INDEX)

    def OnDirectoryExpandAll(self, event):
        sel = self.opmltree.GetSelection()
        if sel and self.opmltree.GetChildrenCount(sel,False) > 0:
            fn = self.opmltree.Expand
            fn(sel)
            firstchild, cookie = self.opmltree.GetFirstChild(sel)
            self.DirectoryTreeTraverse(firstchild,fn,cookie)

    def OnDirectoryCollapseAll(self, event):
        """ collapse all nodes of the tree """
        sel = self.opmltree.GetSelection()
        if sel:
            fn = self.opmltree.Collapse
            fn(sel)
            firstchild, cookie = self.opmltree.GetFirstChild(sel)
            self.DirectoryTreeTraverse(sel, fn)

    def DirectoryTreeTraverse(self, traverseroot, function, cookie=0):
        """ recursivly walk tree control """
        function(traverseroot)
        #Not-downloaded OPML files break ItemHasChildren().
        #Use GetChildrenCount() instead.
        if self.opmltree.GetChildrenCount(traverseroot,False) > 0:
            firstchild, cookie = self.opmltree.GetFirstChild(traverseroot)
            self.DirectoryTreeTraverse(firstchild, function, cookie)

        # ... loop siblings
        child = self.opmltree.GetNextSibling(traverseroot)
        if child:
            self.DirectoryTreeTraverse(child, function, cookie)

    def OnDirectoryRefresh(self,event):
        sel = self.opmltree.GetSelection()
        if sel:
            treenode = self.opmltree.GetPyData(sel)
            node = treenode.node
            if hasattr(node, 'url'): 
                if len(node):
                    if self.opmltree.IsOpmlUrl(node.url): 
                        # Candidate for refreshing
                        treenode.rescan()

    def OnMenuSelectAll(self,event):
        self.notebook.SetSelection(DOWNLOADS_INDEX)
        for i in range(self.downloads.GetItemCount()):
            self.downloads.Select(i,True)

    def OnMenuShowDonationsDialog(self,event):
        self.donatedialog.Show(1)
        self.donatedialog.Raise()

    def MaybeShowDonateDialog(self):
        state = self.ipodder.state
        try:
            (enabled,when_to_alert) = state['donate_popup']
            if enabled and when_to_alert < time.time():
                self.donatedialog.Show(1)
                self.donatedialog.Raise()
        except KeyError:
            self.SetDonateNDaysAhead(30)

    def SetDonateNDaysAhead(self,n_days_ahead,enabled=True):
        state = self.ipodder.state
        state['donate_popup'] = (enabled,time.time() + n_days_ahead*24*3600)
        if hasattr(state, 'sync'): state.sync()

    def OnDonationsProceed(self,event):
        self.donatedialog.Show(0)
        choice = None
        for choice in ["YES","TWOWEEKS","ALREADY","NO","ONEDAY"]:
            if xrc.XRCCTRL(self.donatedialog, "DONATIONS" + choice).GetValue():
                break

        if choice == "YES":
            webbrowser.open("http://sourceforge.net/donate/index.php?group_id=118306")
            self.SetDonateNDaysAhead(0,enabled=False)
        elif choice == "TWOWEEKS":
            self.SetDonateNDaysAhead(14)
        elif choice == "ALREADY":
            self.SetDonateNDaysAhead(0,enabled=False)
        elif choice == "NO":
             self.SetDonateNDaysAhead(0,enabled=False)
        elif choice == "ONEDAY":
            self.SetDonateNDaysAhead(1)

    def DownloadCriticalError(self,errno,*args):
        if errno == core.CRITICAL_MINSPACE_EXCEEDED:
            message = self._("str_critical_error_minspace_exceeded", args=(args[0], args[1]))                               
        else:
            message = self._("str_critical_error_unknown")
            
        alert = wx.MessageDialog(self.frame, message, style=wx.OK)
        response = alert.ShowModal()
        alert.Destroy()

    def AddFeedFromListener(self,url):
        if self.feedwindow.IsShown():
            log.info("Already adding a feed, please try again later.")
        else:
            self.ShowFrame(1)
            self.frame.Raise()
            try:
                self.feedwindow.UpdateFeed(self.ipodder.feeds[url], self.ipodder)
            except KeyError:
                self.feedwindow.UpdateFeed(None, self.ipodder, newfeed=url)
            self.frame.SetFocus()

    def MacOpenFile(self, path):
        log.debug(path) #code to load filename goes here.
        url = misc.url_rssfile_extract(path)
        log.debug(url)
        self.ThreadSafeDispatch(self.AddFeedFromListener,url)

    def handleMacGURL(self,url):
        url = misc.url_cmdline_extract(url)
        self.ThreadSafeDispatch(self.AddFeedFromListener,url)

def asctimeOrNone(dt):
    if dt == None:
        return "<none>"
    else:
        return time.asctime(dt)

def main():
    # Initialise the logging module and configure it for our console logging.
    # I'll factor this out soon so it's less convoluted.
    # There's probably a better way of doing this with the Gui version, 
    # but we have to start somewhere. :) - gtk
    # logging.basicConfig()
    handler = logging.handlers.MemoryHandler(65536)
    #handler.formatter = conlogging.ConsoleFormatter("%(message)s", wrap=False)
    log.addHandler(handler)
    log.propagate = 0
    logging.addLevelName(SPAM, "SPAM")

    # Parse our configuration files.
    # I'll factor this out soon so it's less convoluted.
    parser = makeCommandLineParser()
    options, args = parser.parse_args()
    if options.debug: 
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    try:
        config = Configuration(options)
    except RunTwiceError, e:
        quiet = False
        config = e.value
        if "Win" in platform.system() and config["listen_port"]:
            #Try to raise the app.
            import xmlrpclib, win32gui
            try:
                s = xmlrpclib.Server("http://localhost:%d" % config["listen_port"])
                s.wake()
                h = s.getHwnd()
                win32gui.SetForegroundWindow(h)
                quiet = True
                if options.add_feed:
                    s.addFeed(options.add_feed)
                elif options.add_feed_from_rss:
                    s.addFeedFromRss(options.add_feed_from_rss)
                elif options.add_feed_from_pcast:
                    s.addFeedFromPcast(options.add_feed_from_pcast)
                elif options.open:
                    s.openPath(options.open)
            except:
                pass

        if not quiet:
            app = wx.App()
            app.MainLoop()

            currentlanguage = LanguageModule.ENGLISH
            #TODO: Safely read the screen language.  State is currently
            #being used by the other running process.
            stringtable = LanguageModule.StringTable(currentlanguage)
            alert = wx.MessageDialog(None, stringtable.GetText(currentlanguage, "str_other_copy_running"), style=wx.OK)
            response = alert.ShowModal()
            alert.Destroy()
        sys.exit(0)
        
    if options.debug: # just in case config file over-rode it
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # Open our state database.
    state = statemodule.open(config)
    
    ipodder = core.iPodder(config,state)

    try: 
        myApp = iPodderGui(ipodder,options)
        listener = iPodderSubscribeListener(myApp,config)
        listener.start()
        myApp.MainLoop()
    finally: 
        state.close()
        ipodder.history.close()

if __name__ == '__main__':
    main()
