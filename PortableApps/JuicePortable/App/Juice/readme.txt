Juice -- The cross-platform Podcast receiver
--------------------------------------------

http://juicereceiver.sourceforge.net/
Version 2.2.2-a1 -- July 2006

New since 2.2.2-a1
------------------

* 1463540: handle filenames with spaces (thanks, vladekk!)

New in 2.2.2-a1
---------------

* Fixed problems with Unicode in feeds and filenames. 

* Made the log less verbose with respect to GUID matches on changed
  enclosure names.

* Added cleanup_sort_by_size option. 

* Fixed 1523785: problem with new FeedBurner URLs.

* Fixed 1524119: catch another kind of timeout. 

* Better error handling for oneclick registration and episode playing. 

* Removed Todd Maffin's OPML from the directory, as it's gone. Also added
  PodLook. 

* Fixed some problems with the updater. 

* Updated release process.

* Added Baris Atasoy's Turkish translation. 

* Fixed 1525166: Can't export non-ascii subscriptions to OPML.

New in 2.2
----------

1. iPodder -> Juice name change

2. Expanded support for various one-click subscription mechanisms.
   On Windows: a File Types tab in Preferences to set these behaviors.

3. Clipboard support for feed/podcast URLs on Windows/Mac

4. Winamp support for playing and enqueuing files. (Windows only)

5. User guide, linked from Start -> iPodder -> UserGuide on Windows.

6. Downloaded files are named after the final URL instead of the
   initial URL when HTTP redirects are encountered.

7. Enriched the history data we save, to allow us to support a number of
   new features.  For example, script-powered download URLs should work
   now.

8. The history database cleans up after itself, deleting history
   records for items that are both old and no longer present in
   the feed.

9. Allow re-downloading files that have gone missing by marking
   them as Removed.

10. New languages: Danish, Basque, Finnish, Italian, Korean, Greek

11. Added support for password-protected proxies (HTTP Basic and Digest).

12. Added support for password-protected feeds and downloads
   (HTTP Basic and Digest).  Please note: protected downloads must live
   on the same domain as the feed in order for this to work.

13. Download code now respects content-disposition header for download
   files whose names are different than the URL at which they're located.

14. Fixed BitTorrent abort/resume.  Partially downloaded BitTorrents now
   show up with Partial status instead of Downloaded.

15. Fixed a bug in Windows Media Player support that resulte in Date Added
   not getting set.  Date-based auto-playlists work now.

16. Feedmanager OPML fetcher now runs in a background thread unless we're
   about to do a download run.

17. Directory root for newly added directories, where we'll put
    directories that haven't yet been added to the stable release.

18. Moved scheduler configuration data into ipodder.cfg

19. Minor refactors: moved iPodder.py to ipodder/core.py,
    moved iPodderWindows.py to the gui directory.

20. Python24 compatibility fixes (ongoing)


------------------

BASIC INSTRUCTIONS:

1. Launch iPodder

2. Add podcast feeds.

a. Option 1.  Copy/paste podcast feed URLs into the text input box on the
   Status tab and click Add Feed.
   
b. Option 2.  Click on the Directory tab.  Navigate the tree
   by clicking or double-clicking on the name of the directory or the folder icons. 

   Podcast feeds will have a orange dash icon next to them.  When you select a
   feed, its URL will appear at the bottom of the window.  Add the feed
   to your subscriptions by clicking Add.  It should show up in the main
   subscriptions window with state "newly-subscribed".

3. Set scheduler options

A bit of magic happens when you pick up your MP3 player and fresh content
is already there waiting for you.  Use iPodder to schedule automatic downloads
by entering the times you'd like it to run in the Tools -> Scheduler menu option.
First check the box next to "Enable scheduler".  If you'd like
iPodder to run at specific times, select the "Check at these specific times" radio
button and enter the specific times.  If you plan to listen to podcasts on
your morning commute, you might set iPodder to perform downloads a few hours
before you leave.  Alternatively, you can set iPodder to run at regular
intervals.  Select the interval from the "Repeat every" menu.  Finally, click
"Save and Close" to apply the settings.

4. Walk away

Well, not literally.  But do hide or minimize iPodder and forget about it for
a while.  Based on your scheduler settings, iPodder will check for and download
new content and transfer it to your iTunes or Windows Media Player.  Of course
if you'd like you can check for new podcasts at any time, just be prepared to
stare the download progress bar for a bit.  

5. Listen!

When you're ready to listen, sync your MP3 player and you're on your way.
If you're running Windows and leave your iPod connected, iPodder will
automatically sync it after finishing its downloads.

6. Power user tip

To help manage the volume of new content, we suggest using your music management
software to create a smart playlist of the last N songs added.


IF UPGRADING FROM 1.1 through 2.0.5:

Nothing to say here.

IF UPGRADING FROM 1.0:

Windows: Ideally everything went well and your existing settings were migrated by
the installer.  Keep reading if your settings were lost.  In iPodder 1.0 the settings
were stored in the iPodder installation directory, probably
C:\Program Files\iPodder.  Starting with version 1.1 the configuration are placed outside
the installation directory, in a user-specific directory, if possible.  The default location
is the NT-style Application directory, usually
C:\Documents and Settings\yourname\Application Data\iPodder.  If your settings were lost,
try locating these three files in the previous installation directory and copying them to
the new configuration directory: favorites.txt, history.txt, schedule.txt.

Mac: Ideally everything went well and your existing settings were migrated by
the installer.  Keep reading if your settingswere lots.  In iPodder 1.0 the
settings were stored in the iPodder installation directory, probably
/Applications/iPodder.  Starting with 1.1 the configuration files are placed
outside the installation directory, in a user-specific directory, if possible.
The default location is /Users/yourname/.iPodder.  Note that this directory
will be hidden in the finder because it begins with a (.).  You may navigate
directory to this folder by selecting Go from the Finder menu and typing in
the folder location.  If your settings were lost, try locating these three 
files in the previous installation directory and copying them to the new
configuration directory: favorites.txt, history.txt, schedule.txt.

NEW IN RELEASE 2.1:

  - One-click subscription support enabled as voted on in the ipodder-dev
    Yahoo! groups list and documented here:
    http://pswg.jot.com/WikiHome/DraftPublications/OneClickSpec2

  - Synch subscriptions to remote OPML file (under File -> Preferences ->
    Feed manager).

  - Auto cleanup.  Ability to specify on a per-feed basis that episodes older
    than N days should be auto-cleaned up.  Cleanups take place immediately
    after each check for new episodes.  These options are set in the feed
    properties window, reachable by double-clicking on the feed or from the
    right-click menu for the feed.

  - Genre overriding in iTunes.  See File -> Preferences -> Player.

  - New translations: Spanish, Galego, Catalan, Russian, Serbo-Croation,
    Hungarian, Chinese, Swedish, Brazilian Portuguese, Polish.

  - Accessibility improvements: saner focus behavior, new Ctrl-L
    accelerator for the Scheduler, Shift-F10 for right-click, space bar
    toggling in the episodes window and downloads tab.

  - Feed manager OPML text entry box is drag and drop aware.

  - Catchup behavior is configurable: it can permanently (default)
    or temporarily skip older episodes.

  - Close window behavior is configurable: it can cause the app to
    go to the background (default) or cause the app to quit.

  - Hitting Del key in the feeds list deletes selected feeds.

  - Update checker can be disabled (under File -> Preferences).

  - Windows app will now wake rather than complain if a second copy is running.

  - New right-click option for feeds: Open downloads folder

  - Right-click menus in the episodes and downloads tab link to show
    notes and hyperlinks found within RSS item description.

  - A window now pops up when the disk space falls below the minimum,
    instead of seeming to freeze.

  - Cleaned up episodes are removed from Downloads tab.

  - iPodder/Mac now sets iTunes grouping to 'Podcast', just like Windows.

  - Updated Windows installer: detects running iPodder, new look.

  - Plugin architecture supporting the new right-click menus.  In progress.

  - New localization architecture supports drop-in .py catalog files.

  - New skinning code for store Level 2.

  - Better stability against iTunes version changes.

  - Partial fix for the UnicodeDecodeError for download directories
    with non-ascii characters.  May not work for non-Western encodings.

  - Partial fix for URLs with ? in them.  Downloads proceed but player
    integration still buggy.

  - Manual updates by dropping in an 700KB update file (lightly tested).

-----------------

OLDER RELEASES:

2.0 (March 16, 2005)

  - New resizable GUI.
  - Check/uncheck individual episodes
  - Downloads log
  - Catchup mode downloads just the latest episode from each feed.
  - Enhanced directory browsing including refresh
  - Cleanup tab
  - Internationalization
  - Multithreaded downloads
  - Cancel downloads
  - Resume interrupted downloads
  - Check for update

1.1.4 (November 17, 2004)

  - Enhanced, resizable podcast directory window.

1.1.3 (November 13, 2004)

- This is mostly a bugfix release, major issues resolved:
  - Changes to download directory should now be persistent in cases where it wasn't (Mac/Win)
  - Manually added feeds no longer have garbage at the end (Mac)
  - Auto-play feature can now be disabled from the Preferences tab.
  - Better handling of unicode feed titles
  - Logging improvements
  - User customizable directory roots.  Add a line like this to ipodder.cfg:
    podcast_directory_roots = [('http://some.root/','Some Root'),('http://some.other.root/','Some Other Root')]

1.1.2 (November 11, 2004)

Short-lived precursor to 1.1.3, with a minor bug.


1.1 (November 4, 2004):

- Select podcast feeds by using the integrated directory (OPML) inside
iPodder or add feeds manually from the GUI. 
- Choose your own download folder! 
- The feed list now displays the title, location, downloaded MB and
subscription state for each feed. 
- Enhanced download progress feedback. 
- Don't want to check all feeds? You can now check just one feed. 
- iPodder can now run on startup. 
- Advanced options for Power Users. 
- Automatic setting of Grouping: Podcast for iTunes/Win users. 






