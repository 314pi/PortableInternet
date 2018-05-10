========================================================================

    FeedRoller 0.65
    A Lightweight RSS Feed Ticker
        
    Danny Ben Shitrit (Sector-Seven) 2013
    db@sector-seven.net

    http://sector-seven.net/software/feedroller
        
========================================================================

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
  OF THIRD PARTY RIGHTS. 
  
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
  CLAIM, 

  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
  THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
========================================================================


------------------------------------------------------------------------  
  INTRODUCTION
------------------------------------------------------------------------  
  
  FeedRoller is a lightweight RSS feed ticker.
  It is designed to show scrolling headlines from your favorite news 
  sites, and blogs, directly on your desktop.
  
  FeedRoller is a freeware.


------------------------------------------------------------------------  
  Features
------------------------------------------------------------------------  

  • Supports RSS and Atom feed format.
  • Supports subscribing to feeds directly from Firefox.
  • Shows news title, summary, age and source.
  • Customizable interface.
  • May be "pinned" to the desktop (always visible) or automatically 
    hide when the computer is in use.
  • May be set to automatically hide when in full screen applications 
    (games, movies etc.)
  • May snap to top or bottom of your desktop.
  • Customizable keyboard shortcuts to pause the scrolling, pin the 
    ticker, visit the news item and more.
  • Can import and export feeds from other feed readers (using OPML).
  • Portable.

  
------------------------------------------------------------------------  
  Getting Started
------------------------------------------------------------------------  

  FeedRoller comes pre-configured with several news feeds.
  When you run it for the first time, it will download these RSS feeds 
  and start showing them on your desktop.
  
  • Right click on FeedRoller's system tray icon to access common 
    actions.
  • To Pause the ticker, press the Pause key on your keyboard.
  • To Pin/Unpin the ticker, press the Scroll Lock key on your 
    keyboard.
  • To Visit the displayed item's page, press the Print Screen key on 
    your keyboard.
  • To manage your feeds, press F12. Checked feeds are active.
  
  View the Options dialog (F8) and the system tray icon for more
  shortcut keys and options.



------------------------------------------------------------------------  
  REVISION HISTORY
------------------------------------------------------------------------  

  2013 03 09 - 0.65
    Added: Global hotkey to toggle pin (Advanced tab, thanks Eric)
    Added: Custom action to launch an article (Advanced tab, thanks Eric)

  2013 01 29 - 0.64
    Fixed: Feed links with a comma did not work.

  2010 09 04 - 0.63
		Removed: Twitter support (due to changed authentication requirements).

  2010 08 26 - 0.62
		Changed: Increased maximum number of items per feed.

  2010 05 12 - 0.61
    Added  : Double click on system tray may be configured to visit displayed
             item.

  2010 04 17 - 0.60
    Changed: Default installation folder to Portable Program Files
    Changed: Transparency and Animation can now be enabled at the same time.
             This may still cause flickering on Windows XP, but works nicely
             on Windows 7 and Vista.

  2009 10 08 - 0.55
    Fixed  : In some multi-monitor configurations, the roller was hiding itself
             when not needed.              

  2009 09 29 - 0.54
    Added  : Support for SSL (https) feeds. Broken in 0.52 since we started 
             using cURL.
             In order to avoid the additional large cURL SSL libraries, we are
             now downloading https feeds using the internal UrlDownloadToFile
             function in AutoHotkey, which means that SSL feeds cannot be 
             accessed when using proxy.

  2009 09 14 - 0.53
    Fixed  : Atom links were not extracted properly.
    Fixed  : When for some reason the link is not valid, a run time error box
             was displayed. Now using ErrorLevel on all Run/RunWait commands.

  2009 09 12 - 0.52
    Changed: Now using the external cURL for all download tasks to provide 
             support for more advanced download features.
    Added  : Configuration for connection and download timeouts
    Added  : Support for proxy servers.   

  2009 09 06 - 0.51 (never released)
    Changed: Minor changes.

  2009 09 05 - 0.50
    Fixed  : UTF-8 encoded OPML files did not import names properly.
    Changed: Handling of OPML import - should now be faster and support more 
             file structures including nested Google Reader structure.
    Changed: Status dialog, now with progress bar to provide better indication
             when importing large files.
    Changed: Edit Feeds dialog now supports multiple selections (with Shift or
             Ctrl).

  2009 09 05 - 0.43
    Added  : Option to snap to bottom.
    Fixed  : When the Windows taskbar is on top, and we are snapped to top we 
             will no longer hide the taskbar.

  2009 09 05 - 0.42
    Fixed  : Can now also import OPMLs that have nested outline tags (up to 3 
             levels deep).
    Changed: When Options or Manage Feeds dialog are open, we will abort any
             feed download process in order to allow for smooth editing.
             Cycle is restarted when dialogs are closed.
    Added  : Since Twitter limits to 150 requests per client per hour, we will
             now attempt to identify this situation and avoid calling it too 
             often (by not deleting the cache).
             If you get rate-limited, you should either remove some of your 
             twitter RSS feeds or increase the default Cache Life in Options 
             (or complain to Twitter...).
    Changed: When importing, we will now switch to the Status message, instead
             of staying in the Import/Export window. Required for large imports
             that take more than a second or two.
    Added  : Warnings section in Options. Can now enable/disable Feed warnings
             (such as Empty Feed warning).
    Changed: Warnings are now disabled by default.

  2009 09 04 - 0.41
    Fixed  : Ctrl as a navigation modifier did not work.
    Changed: Ctrl to be the default navigation modifier (upon clean 
             installation) in order to not collide with Gridy's default keys.   

  2009 09 01 - 0.40
    Added  : Support for Twitter feeds.
    Changed: Some GUI changes in Manage Feeds dialog to accommodate the new 
             Twitter feed.
    Changed: Internal feed format recognition function.
    Changed: When adding through Firefox, instead of a confirmation message box 
             we will show the message in the ticker itself.
    Changed: Internal date formatter to recognize Twitter format.
    Added  : Check All checkbox in Manage Feeds dialog.
    Added  : When the ticker is paused, you can now navigate through items using
             the mouse wheel or keyboard arrow keys. See Options -> Navigation.
    Added  : Quick Help HTML page, automatically generated to consider the 
             current settings.
    Added  : When starting, we will hide if there is no internet connection.
             Will retry once a minute. Useful for dialup connections when 
             FeedRoller starts on startup.

  2009 08 30 - 0.31
    Added  : Command line argument. If it is a feed address, the feed will be
             added to the list.
             This enables subscribing through the Firefox Subscribe menu.
    Added  : Import now supports files with opml extension (not only xml).
    Fixed  : UTF-8 encoded feeds were not always detected.

  2009 08 29 - 0.30
    First release candidate
    Added  : One time Welcome tip

  2009 08 28 - 0.23
    Added  : Better handling of empty XMLs (due to faulty download).
    
  2009 08 26 - 0.22
    Changed: In Edit Feed, URL field from disabled to read only
    Added  : Feed Max Age may now be -1, to ignore age completely. 
    Fixed  : When the desktop was visible, we thought we are in full screen.
    Fixed  : Animation Slide In Down did not work.
    Added  : Layout configuration - can hide summary and meta.
    Fixed  : Feeds were shown as empty when internet connection was offline.
    
  2009 08 26 - 0.21
    Added  : Auto suspend on Full Screen windows.
    Changed: Time stamp parser - should now be more compatible with many 
             formats.
    Fixed  : In Manage Feeds, the state of active/inactive is now stored before
             adding, editing, moving or deleteing a feed.
              
  2009 08 ?? - 0.15
    First beta release

========================================================================
------------------------------------------------------------------------  
