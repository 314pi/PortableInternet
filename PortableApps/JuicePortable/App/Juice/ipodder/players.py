#
# iPodder player handling module
#

import platform
import os
import logging
import re
import misc

if "Win" in platform.system():
    import win32com.client
    import win32con
    import win32process
    
log = logging.getLogger('Juice')

UNCHECKED_SONGS = "__UNCHECKED_SONGS__"

class CannotInvoke(AssertionError): 
    """Player objects raise this in __init__ if they can't be invoked 
    on this system."""
    pass

class Player(object): 
    """Generic dict-style interface to media players."""

    def __init__(self): 
        """Raise CannotInvoke if you can't be used."""
        object.__init__(self)
        raise NotImplementedError

    def append_and_create(self, filename, playlistname, playnow=True): 
        """Add the tune to the playlist. Create the list if necessary.
        Don't add the tune if it's there already."""
        raise NotImplementedError

    def get_rating(self, filename, playlistname): 
        """Get the rating (0-100) for a particular entry in a 
        particular playlist. Probably iTunes specific, but perhaps 
        not."""
        raise NotImplementedError

    def playlist_filenames(self, playlistname): 
        """Return a list of files referred to by a particular 
        playlist."""
        raise NotImplementedError

    def playlist_fileinfos(self, playlistname, max_days=None):
        """Return a list of files and timestamps in the format
        (stub,full path,ctime,size).  Files are not sorted."""
        files = []
        try:
            filenames = self.playlist_filenames(playlistname)
            files.extend(misc.get_fileinfos(filenames, min_age=max_days))
        except NotImplementedError:
            log.debug("playlist_fileinfo: Player doesn't implement playlist_filenames method.")
        except KeyError:
            #No matching playlist; ignore.
            pass

        return files
    
    def play_file(self,filename, rude=False): 
        """Play a file."""
        raise NotImplementedError

    def remove_files(self,filesinfo):
        """Remove a list of files."""
        raise NotImplementedError
    
    def sync(self): 
        """Synchronise changes to the media player."""
        raise NotImplementedError

def makeOS9abspath(path):
    """Returns an ":" delimited, OS 9 style absolute path."""
    import Carbon.File, os.path
    rv = []
    fss = Carbon.File.FSSpec(path)
    while 1:
        vrefnum, dirid, filename = fss.as_tuple()
        rv.insert(0, filename)
        if dirid == 1: break
        fss = Carbon.File.FSSpec((vrefnum, dirid, ""))
    if len(rv) == 1:
        rv.append('')
    return ':'.join(rv)

def execute_applescript(script): 
    """Execute some AppleScript on Darwin."""
    scriptlines = [line.strip() for line in script.split('\n')]
    scriptlines = [line for line in scriptlines if line]
    
    cmd = '/usr/bin/osascript %s >/dev/null' % ' '.join(
           ['-e "%s"'  % re.sub(r'([$`"\\])',r'\\\1',line)
            for line in scriptlines])
    
    log.debug("Running command: %s", cmd)
    result = os.system(cmd)
    log.debug("Return code was %d", result)

class iTunesForDarwin(Player): 
    """Player interface to iTunes for Mac OSX."""

    def __init__(self): 
        """Initialise the iTunes player interface on Darwin."""
        self.safeplaylistchars = " '0123456789abcdefghijklmnopqrstuvwxyz"

    def append_and_create(self, filename, playlistname, playnow=True): 
        """Add the tune to the playlist. Create the list if necessary.
        Don't add the tune if it's there already."""

        playlistname = sanitize(playlistname, self.safeplaylistchars)
        log.debug("Ensuring playlist %s has file %s", playlistname, filename)
        song = makeOS9abspath(filename)
        genre = self.ow_genre
        if self.ow_genre_enable and self.ow_genre:
            set_genre = "true"
        else:
            set_genre = "false"

        script = """\
            tell application "System Events"
              set was_running to false
              if exists process "iTunes" then
                set was_running to true
              end if
              tell application "iTunes"
                if not was_running then
                  set visible of front window to false 
                end if
                if (not (exists user playlist "%(playlist)s")) then 
                  make new playlist with properties {name:"%(playlist)s"}
                end if
                set newtrack to (add "%(song)s" to playlist "%(playlist)s")
                set the Grouping of newtrack to "Podcast"
                if %(set_genre)s then
                  set the Genre of newtrack to "%(genre)s" 
                end if
              end tell 
            end tell
            """ % {
                'song': song, 
                'playlist': playlistname,
                'set_genre': set_genre,
                'genre': genre
                }
        execute_applescript(script)

        if playnow: 
            self.play_file(filename)

    def sync(self): 
        """Synchronise changes to the media player."""
        return # the script is lacking some parameters...
        
        # Can anyone fix this script? 
        # Let me know if you really need the parameters. - gtk
        script = """
            tell application "iTunes"
              repeat with i from 1 to the count of source
                if the kid of source i is iPod then
                  set thePod to the name of source i as text
                end if
              end repeat
              copy (get a reference to (every track in "%(playlist)s")) to theTracks
              duplicate theTracks to playlist "%(playlist)s" in source thePod
            end tell
            """ % {
                'playlist': "no idea what to put here"
                }
        execute_applescript(script)  

    # def get_rating_darwin(self, filename, playlistname)
    # def playlist_filenames_darwin(self, playlistname)

    def play_file(self, filename, rude=False):
        """Play the file."""
        song = makeOS9abspath(filename)
        script = """\
            tell application "iTunes"
              if player state is not playing or (player state is playing and %(rude)s) then
                play "%(song)s"
              end if
            end tell
            """ % {
                'song': song,
                'rude': rude
                }
        execute_applescript(script)

    def playlist_filenames(self,playlistname):
        """Okay this is a bit convoluted.  We use the user's hard disk to communicate between
           applescript and python, writing and then reading a temp file.
        """
        filenames = [] 
        playlistname = sanitize(playlistname, self.safeplaylistchars)

        import tempfile
        (fd,tfile) = tempfile.mkstemp()
        os.close(fd)
        os9tfile = makeOS9abspath(tfile) #file must exist

        script = """\
            tell application "iTunes"
              if (exists user playlist "%(playlistname)s") then
                tell source "Library"
                  tell playlist "%(playlistname)s"
                    set ref_num to open for access file "%(os9tfile)s" with write permission
                    set eof of ref_num to 0
                    repeat with i from 1 to the count of tracks
                      write (POSIX path of (the location of track i as string) as string) to ref_num
                      write ASCII character 13 & ASCII character 10 to ref_num
                    end repeat
                    close access ref_num
                  end tell
                end tell
              end if
            end tell
            """ % {
                'playlistname': playlistname,
                'os9tfile': os9tfile
                }
        execute_applescript(script)

	#now build the list
        fh = open(tfile,"r")
        for line in fh:
            filename = line.rstrip()
            #convert os9 style path to unix path
            filenames.append(filename)
        fh.close()

        os.remove(tfile) 

        return filenames
        
    def remove_files(self,filesinfo):
        if not len(filesinfo):
            return

        listdef = """set thePlaylists to {}
            set thePlaylistsRef to a reference to thePlaylists
            set theFiles to {}
            set theFilesRef to a reference to theFiles
            """ 

        for (playlistname,files) in filesinfo:
            playlistname = sanitize(playlistname, self.safeplaylistchars)
            fileslist = "{" + ",".join(['"%s"' % file for file in files]) + "}"
            listdef += """copy "%s" to the end of thePlaylistsRef
                copy %s to the end of theFilesRef
                """ %  (playlistname,fileslist)

        script = """\
            %(listdef)s
            set tracksToDelete to {}
            set tracksToDeleteRef to a reference to tracksToDelete
            tell application "iTunes"
              tell source "Library"
                repeat with i from 1 to the count of thePlaylists
                  set thisPlaylist to item i of thePlaylists 
                  if (exists user playlist thisPlaylist) then
                    tell playlist thisPlaylist
                      set thisPlaylistsFiles to item i of theFiles
                      repeat with j from 1 to the count of tracks
                        set thisTrack to track j 
                        set thisFile to the POSIX path of (the location of thisTrack as string) as string
                        if thisPlaylistsFiles contains thisFile or (the location of thisTrack is missing value)
                          set nameToCheck to the name of thisTrack
                          tell playlist "Library" of source "Library" of application "iTunes"
                            set theseTracks to (every track whose name is equal to nameToCheck)
                            repeat with k from 1 to the count of theseTracks
                              if the location of item k of theseTracks equals the location of thisTrack
                                copy item k of theseTracks to the end of tracksToDeleteRef
                              end if 
                            end repeat
                          end tell
                        end if
                      end repeat
                    end tell
                  end if
                end repeat
                repeat with l from (the count of tracksToDelete) to 1 by -1
                  delete item l of tracksToDelete
                end repeat
              end tell
            end tell
            """ % {
                'listdef': listdef
                }

        execute_applescript(script)

         
    def remove_files_darwin_old(self,filesinfo):
        """NOTE: This will not work if iTunes is set to copy files to the iTunes folder.
        We have to remove the file from the main library in
        order to free up space on the ipod.  This also removes
        the file from any playlists the file appears in."""
        if not len(filesinfo):
            return
        listdef = """set theList to {}
            """
        for (playlist,files) in filesinfo:
            for filename in files:
                listdef += """copy theList & "%s" to theList
                    """ % filename

        script = """\
            %(listdef)s 
            tell application "iTunes"
              set the stored_setting to fixed indexing
              set fixed indexing to true
              tell source "Library"
                tell playlist "Library"
                  -- delete (any track whose location is in the list)
                  repeat with i from the (count of tracks) to 1 by -1
                    try
                      if (POSIX path of (the location of track i as string) as string) is in theList then
                        delete track i
                      end if
                    end try
                  end repeat
                end tell
              end tell
              set fixed indexing to the stored_setting
            end tell
            """ % {
                'listdef': listdef
                }
        execute_applescript(script)

class iTunesForWindows(Player): 
    """Player interface to iTunes on Windows."""

    def __init__(self):
        """Initialise the Player object for operation on Windows."""
        self.safeplaylistchars = " '0123456789abcdefghijklmnopqrstuvwxyz"
        self.__iTunes = None
        self.iTunes # This will throw CannotInvoke if appropriate

    def _return_iTunes(self): 
        """Return a connection to iTunes. Tries to avoid re-creating the 
        connection each time, but checks to make sure it's still OK each 
        time."""
        import win32com.client
        try: 
            # Evaluating self.__iTunes.Version will handily bomb out 
            # with AttributeError if __iTunes is None or if the 
            # connection has broken for whatever reason. 
            self.__iTunes.Version
        except (AttributeError, win32com.client.pythoncom.com_error), ex: 
            try: 
                iface = "iTunes.Application"
                self.__iTunes = win32com.client.dynamic.Dispatch(iface)
            except ImportError, ex: 
                raise CannotInvoke, "Can't import win32com.client"
            except win32com.client.pythoncom.error, ex: 
                raise CannotInvoke, "Can't dispatch %s" % iface
        return self.__iTunes

    iTunes = property(fget=_return_iTunes, doc="A live connection to iTunes")
            
    def post_track_add_windows(self, filename, playlistname, addresult, playnow=True):
        """Do some post-add work."""
        if hasattr(addresult, 'Tracks'): 
            try: 
                for idx in range(1, addresult.Tracks.Count+1): 
                    track = addresult.Tracks.Item(idx)
                    track.Grouping = 'Podcast'
                    if self.ow_genre_enable and self.ow_genre:
                        track.Genre = self.ow_genre
            except: 
                log.exception("Failure trying to set grouping of added tracks.")
        else: 
            log.warn("Can't set Grouping=\"Podcast\", as iTunes didn't let "\
                     "us know which tracks got added.")
        if playnow: 
            self.play_file(filename)
        return
    
    def append_and_create(self, filename, playlistname, playnow=True): 
        """Add the tune to the playlist. Create the list if necessary.
        Don't add the tune if it's there already."""
        playlistname = sanitize(playlistname, self.safeplaylistchars)
        log.debug("Ensuring playlist %s has file %s", playlistname, filename)
        try: 
            plitems = self.mine_playlist_windows(playlistname)
            if plitems is None: 
                return
        except KeyError: 
            log.info("Creating new playlist %s", playlistname)
            iTunesPlaylist = self.iTunes.CreatePlaylist(playlistname)
            res = iTunesPlaylist.AddFile(filename)
            return self.post_track_add_windows(filename, playlistname, res, playnow)

        for location, item in plitems: 
            if location == filename:
                break
        else: 
            log.debug("Updating existing playlist %s", playlistname)
            iTunesPlaylist = self.get_playlist_windows(playlistname)
            if iTunesPlaylist is None:
                return
            res = iTunesPlaylist.AddFile(filename)
            while res and res.InProgress:
                pass
            return self.post_track_add_windows(filename, playlistname, res, playnow)
        
    def sync(self):
        """Synchronise changes to the media player."""
        self.iTunes.UpdateIPod()
        log.debug("Asked iTunes to update the iPod.")
        # I'm not catching exceptions until they're reported. - gtk

    def get_playlist_windows(self, playlistname):
        playlistname = sanitize(playlistname, self.safeplaylistchars)
        iTunesPlaylists = self.iTunes.LibrarySource.Playlists
        iTunesPlaylist = iTunesPlaylists.ItemByName(playlistname)
        if not iTunesPlaylist:
            raise KeyError
        return iTunesPlaylist
    
    def mine_playlist_windows(self, playlistname):
        """Return a list of (filename, ob) pairs or raise KeyError."""
        playlistname = sanitize(playlistname,self.safeplaylistchars)
        iTunesPlaylist = self.get_playlist_windows(playlistname)
        if iTunesPlaylist is None: 
            raise KeyError

        res = []
        for j in range(1,len(iTunesPlaylist.Tracks)+1):
            item = iTunesPlaylist.Tracks.Item(j)
            if hasattr(item, 'Location') and item.Location and os.path.isfile(item.Location): 
                location = item.Location
            else: 
                location = None
            res.append((location, item))
        return res

    def get_rating(self, filename, playlistname): 
        """Get the rating (0-100) for a particular entry in a 
        particular playlist (Windows version)."""
        # get the playlist; might raise KeyError
        plitems = self.mine_playlist_windows(playlistname)
        plitems = [item for location, item in plitems
                   if location == filename]
        count = len(plitems)
        if count < 0: 
            raise KeyError
        if count > 1: 
            log.warn("Playlist %s has %d copies of %s!", 
                     playlistname, count, filename)
        return plitems[0].Rating

    def playlist_filenames(self, playlistname): 
        """Return a list of files referred to by a particular 
        playlist."""
        plitems = self.mine_playlist_windows(playlistname)
        return [location for location, item in plitems]

    def play_file(self, filename, rude=False): 
        """Play a file."""
        if self.iTunes.PlayerState > 0: 
            playing = True
        else: 
            playing = False
        if not playing or rude: 
            # This adds the file to the library, which is a little rude if 
            # we're about to delete it. :) 
            log.debug("Asking iTunes to play...")
            self.iTunes.PlayFile(filename)

    def remove_files(self, filesinfo):
        """Remove the file from the main library which cascades
        to all other playlists.
        
        filesinfo -- sequence of (playlistname, filenames) 
                     tuples.
        """
        for (playlistname, files) in filesinfo:
            # Build a dict mapping lowercase filenames to tracks. 
            # At this point, all the tracks are None. 
            filemap = {}
            filemap[""] = [] #remove dead tracks too
            for file in files: 
                filemap[file.lower()] = []
            # Try to narrow the list of tracks to check, since
            # getting the track.Location forces an i/o hit which
            # slows things down dramatically for large libraries.
            if playlistname == UNCHECKED_SONGS:
                mainlibtracks = self._narrow_by_unchecked_status()
                playlisttracks = []
            else:
                (mainlibtracks,playlisttracks) = self._narrow_by_playlist(playlistname,files)
            # Traverse the narrowed list. Adjust filemap whenever we 
            # find a track for which the location matches one 
            # of the files we're interested in.
            # AG: Must delete playlist tracks BEFORE mainlibtracks to handle
            # dead tracks correctly.
            alltracks = playlisttracks
            alltracks.extend(mainlibtracks)
            for track in alltracks:
                loc = track.Location.lower()
                if filemap.has_key(loc): 
                    filemap[loc].append(track)
            # Delete any tracks we just found. 
            for file, tracks in filemap.items(): 
                for track in tracks:
                    try:
                        track.Delete()
                    except:
                        #Delete bombed out.  Oh well, we tried.
                        pass
                    
    def _narrow_by_playlist(self,playlistname,files):
        """Return a two-tuple containing a list of main library
        tracks and playlist tracks matching the files passed in.
        Also returns dead tracks."""
        
        #Build up the list of main library tracks to delete from
        #the file paths.  New approach: we're going to locate the
        #tracks in their native playlists, then use the track
        #names to search the main library.  Let's see if this is
        #faster than cycling through the entire iTunes library.
        ITPlaylistSearchFieldSongNames = 5
        iTunesPlaylists = self.iTunes.LibrarySource.Playlists
        mainlibtracks = []
        playlisttracks = []
        
        playlistname = sanitize(playlistname, self.safeplaylistchars)
        playlist = iTunesPlaylists.ItemByName(playlistname)
        if not playlist:
            log.error("Couldn't find iTunes playlist %s" % playlistname)
            return (mainlibtracks,playlisttracks)
        
        for track in playlist.Tracks:
            if files.count(track.Location) > 0 or track.Location == "":
                #Found the track in the playlist, now locate it
                #in the main library by first narrowing down to
                #tracks with the same name and then checking for
                #a matching location.
                search_results = self.iTunes.LibraryPlaylist.Search(track.Name,ITPlaylistSearchFieldSongNames)
                for result_track in search_results:
                    if result_track.Location == track.Location:
                        mainlibtracks.append(result_track)
                        playlisttracks.append(track)

        return (mainlibtracks,playlisttracks)

    def _narrow_by_unchecked_status(self):
        """Return a list of library playlist tracks that
        are unchecked."""
        return [track for track in self.iTunes.LibraryPlaylist.Tracks
                if not track.Enabled]
        
    def remove_files_windows_old(self,filesinfo):
        """We have to remove the file from the main library in
        order to free up space on the ipod.  This also removes
        the file from any playlists the file appears in."""
        ## is the iTunes object connected to the app?
        filenames = []
        for (playlist,files) in filesinfo:
            filenames.extend(files)

        #Build up a list of tracks to delete first, to avoid modifying

        #the structure we're iterating through.
        tracks_to_delete = []
        for track in self.iTunes.LibraryPlaylist.Tracks:
            #Problem: slow but this is the best we can do until iTunes
            #provides a COM interface for locating a track by its file path.
            if filenames.count(track.Location) > 0:
                tracks_to_delete.append(track)

        #Now actually delete the tracks.
        for track in tracks_to_delete:
            track.Delete()

    def get_unchecked_tracks_under_directory(self, path): 
        """Return the filenames of all unchecked tracks for which the 
        Location is underneath 'path'."""
        results = []
        lpath = path.lower()
        unchecked = [track for track in self.iTunes.LibraryPlaylist.Tracks
                     if not track.Enabled]
        log.debug("%d unchecked tracks in iTunes", len(unchecked))
        for track in unchecked: 
            if track.Location.lower().startswith(lpath): 
                results.append(track.Location)
        log.debug("%d start with %s", len(results), lpath)
        return results

    
class iTunes(object): 
    """Player interface to iTunes."""

    def __init__(self): 
        """Initialise the iTunes player interface."""

        try: 
            plat = self.__class__.platform
        except AttributeError: 
            plat = platform.system()

        if plat in ['Windows', 'Microsoft', 'Microsoft Windows']: 
            self.version = iTunesForWindows
        elif plat in ['Darwin']: 
            self.version = iTunesForDarwin
        else: 
            raise CannotInvoke, "Unknown platform %s" % plat

class WindowsMedia(Player): 
    def __init__(self): 
        """Initialise the Windows Media player interface."""
        self.iface = iface = "WMPlayer.OCX.7"
        try: 
            import win32com.client
            win32com.client.Dispatch(iface)
            self.__win32com = win32com
        except ImportError, ex: 
            raise CannotInvoke, "Can't import win32com.client"
        except win32com.client.pythoncom.error, ex:  
            raise CannotInvoke, "Can't dispatch %s" % iface
        self.safeplaylistchars = " 0123456789abcdefghijklmnopqrstuvwxyz"

    def append_and_create(self, filename, playlistname, playnow=True): 
        """Add the tune to the playlist. Create the list if necessary.
        Don't add the tune if it's there already."""
        playlistname = sanitize(playlistname, self.safeplaylistchars)
        log.debug("Ensuring playlist %s has file %s", playlistname, filename)
        file = filename
        file.replace("\\", "\\\\")
        try:
            wmp = self.__win32com.client.Dispatch(self.iface)
            try:
                playlistArray = wmp.playlistCollection.getByName(playlistname)
                if playlistArray.count == 0:
                    play_l = wmp.playlistCollection.newPlaylist(playlistname)
                else:
                    play_l = playlistArray.Item(0)
                file_to_add = wmp.mediaCollection.add(file)
                play_l.appendItem(file_to_add)
                wmp.close()
            except:
                log.exception("Couldn't tell Windows Media Player to update its playlist.")
                wmp.close()
        except:
            log.exception("Couldn't dispatch Windows Media Player.")

        if playnow:
            self.play_file(filename)
            
    def sync(self): 
        """Synchronise changes to the media player."""
        pass # Not necessary

    def play_file(self,filename,rude=False):
       try:
           wmp = self.__win32com.client.Dispatch(self.iface)
           try:
               wmp.openPlayer(filename)
               wmp.close()
           except:
               log.exception("Couldn't tell Windows Media Player to play the file.")
               wmp.close()
       except:
           log.exception("Couldn't dispatch Windows Media Player.")

    def playlist_filenames(self,playlistname):
        filenames = []
        playlistname = sanitize(playlistname,self.safeplaylistchars)
        try:
            wmp = self.__win32com.client.Dispatch(self.iface)
            try:
                playlistArray = wmp.playlistCollection.getByName(playlistname)
                if playlistArray.count == 0:
                    log.error("WindowsMedia: couldn't find playlist %s" % playlistname)
                    return filenames
 
                playlist = playlistArray.Item(0)
                for idx in range(playlist.count):
                    filenames.append(playlist.Item(idx).sourceURL)
                wmp.close()
            except:
                log.exception("Couldn't tell Windows Media Player to update its playlist.")
                wmp.close()
        except:
            log.exception("Couldn't dispatch Windows Media Player.")
        
        return filenames
    
    def remove_files(self,filesinfo):
        """Removing an item from the media library doesn't result in it
        getting removed from the playlist, so we remove it from both."""
        try:
            wmp = self.__win32com.client.Dispatch(self.iface)
            try:
                mc = wmp.mediaCollection
                for (playlistname,filenames) in filesinfo:

                    #Remove files from the media collection.
                    for filename in filenames:
                        playlist = mc.getByAttribute('sourceURL',filename)
                        for idx in range(playlist.count):
                            #Items shift each time; grab the top one.
                            item = playlist.Item(0)
                            mc.remove(item,True)

                    #Remove files from the playlist.
                    playlistname = sanitize(playlistname,self.safeplaylistchars)
                    playlistArray = wmp.playlistCollection.getByName(playlistname)
                    if playlistArray.count == 0:
                        log.warn("Failed to find playlist %s" % playlistname)
                        continue
                    playlist = playlistArray.Item(0)

                    for idx in range(playlist.count):
                        #Items shift each time; grab the top one.
                        item = playlist.Item(0)
                        if filenames.count(item.sourceURL):
                            playlist.removeItem(item)
                            
                wmp.close()
            except:
                log.exception("Couldn't tell Windows Media Player to update its playlist.")
                wmp.close()
        except:
            log.exception("Couldn't dispatch Windows Media Player.")

class NoPlayer(Player): 
    """For when the user doesn't want player integration or
    has a player we don't yet support."""

    def __init__(self):
        return
    
    def append_and_create(self, filename, playlistname, playnow=True): 
        """Returns quietly without doing anything."""
        return

    def playlist_filenames(self, playlistname): 
        """Returns an empty list."""
        return []

    def remove_files(self,filesinfo):
        """Returns quietly without doing anything."""
        return
    
    def sync(self): 
        """Returns quietly without doing anything."""
        return

class Winamp(Player): 
    """Basic interface to the Winamp player (Windows only)."""

    def __init__(self):
        if "Win" not in platform.system():
            raise CannotInvoke, "Winamp only available on Windows systems"

        self.play_command = None
        self.enqueue_command = None
        
        import _winreg
        openkeys = []
        try:    
            try:
                key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT,r'Winamp.File\shell\open\command',0,_winreg.KEY_QUERY_VALUE)
                openkeys.insert(0,key)
                self.play_command,type = _winreg.QueryValueEx(key, "")
                key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT,r'Winamp.File\shell\Enqueue\command',0,_winreg.KEY_QUERY_VALUE)
                openkeys.insert(0,key)
                self.enqueue_command,type = _winreg.QueryValueEx(key, "")
            finally:
                for key in openkeys:
                    _winreg.CloseKey(key)
        except WindowsError, e:
            errno, message = e.args
            if errno != 2:
                raise e
        
        return
    
    def append_and_create(self, filename, playlistname, playnow=True): 
        """Returns quietly without doing anything."""
        return

    def playlist_filenames(self, playlistname): 
        """Returns an empty list."""
        return []

    def remove_files(self,filesinfo):
        """Returns quietly without doing anything."""
        return
    
    def sync(self): 
        """Returns quietly without doing anything."""
        return

    def play_file(self,filename,rude=False):

        if self.enqueues and self.enqueue_command != None:
            play_command = self.enqueue_command
        else:
            play_command = self.play_command
            
        play_file_command = play_command.replace("%1",filename)
        log.debug("Playing file using command:\n%s" % play_file_command)

        si = win32process.STARTUPINFO()
        si.wShowWindow = win32con.SW_HIDE
        win32process.CreateProcess (None, play_file_command, None, None, 1, win32con.NORMAL_PRIORITY_CLASS, None, None, si )

        return
    

class CommandLinePlayer(Player): 
    """A basic player that supports the 'play' function from the
    command line.  The command line syntax is specified by
    basic_player_command in ipodder.cfg."""

    def __init__(self):
        self.play_command = None
        return
    
    def append_and_create(self, filename, playlistname, playnow=True): 
        """Returns quietly without doing anything."""
        return

    def playlist_filenames(self, playlistname): 
        """Returns an empty list."""
        return []

    def remove_files(self,filesinfo):
        """Returns quietly without doing anything."""
        return
    
    def sync(self): 
        """Returns quietly without doing anything."""
        return

    def play_file(self,filename,rude=False):
        if self.play_command:
            command = self.play_command
            if "Win" in platform.system():
                import win32api
                filename = win32api.GetShortPathName(filename)
            if command.find("%f") == -1:
                #Append filename as the last arg if command line doesn't
                #contain it.
                command = command + " %f"
            command = command.replace("%f",filename)
            status = os.system(command)
            if status:
                log.exception("There was an error running this command: '%s'" % command)
        else:
            log.info("CommandLinePlayer command not set -- not playing file %s." % filename)
        
    def set_play_command(self, command):
        """Set the system command for the player.  We need this because the
        player object doesn't have access to the configuration object."""
        self.play_command = command
        
def sanitize(string, safechars): 
    """Sanitize the string according to the characters in `safe`."""
    # First, get the function's cache dict. 
    try: 
        safecache = sanitize.safecache
    except AttributeError: 
        safecache = sanitize.safecache = {}
    # Next, fetch or set a dict version of the safe string. 
    safehash = safecache.get(safechars)
    if safehash is None: 
        safehash = safecache[safechars] = {}
        for char in safechars: 
            safehash[char.lower()] = 1
    # Finally, sanitize the string.
    reslist = []
    for char in string: 
        lower = char.lower()
        if safehash.get(lower, 0): 
            reslist.append(char)
    return ''.join(reslist)
    
player_classes = [iTunes, WindowsMedia, NoPlayer, CommandLinePlayer, Winamp]

def all_player_types(): 
    """Return a list of all defined player classes, workable or not."""
    return [pclass.__name__ for pclass in player_classes]

def player_types(): 
    """Return a list of invokable player classes for this system."""
    valid = []
    log.debug("Looking for invokable players...")
    for pclass in player_classes: 
        name = pclass.__name__
        try: 
            if pclass.__name__=="iTunes":
		pclass().version()
	    else:
		pclass()
            log.debug("Successfully invoked player %s.", name)
            valid.append(name)
        except CannotInvoke: 
            log.debug("Can't invoke %s.", name)
    return valid

def get(name): 
    """Get a player object by class name. Returns None if it can't 
    be invoked. Raises KeyError if it doesn't exist."""
    matches = [pclass for pclass in player_classes 
               if pclass.__name__.lower() == name.lower()]
    assert len(matches) <= 1
    if not matches: 
        log.debug("Couldn't locate requested player class %s", name)
        raise KeyError
    pclass = matches[0]
    try: 
	if pclass.__name__ == "iTunes":
		return pclass().version()
	else:
        	return pclass()
    except CannotInvoke, ex: 
        log.debug("Couldn't invoke requested player class %s", name)
        return None

if __name__ == '__main__': 
    # test code
    import conlogging
    logging.basicConfig()
    handler = logging.StreamHandler()
    handler.formatter = conlogging.ConsoleFormatter("%(message)s", wrap=False)
    log.addHandler(handler)
    log.propagate = 0
    log.setLevel(logging.DEBUG)
    log.info("Defined player classes: %s", ', '.join(all_player_types()))
    log.info("Invokable player classes: %s", ', '.join(player_types()))

    # edj: debugging session leftovers
    #it = iTunes()
    #it.append_and_create_darwin("/", "testje")

    player = get(player_types()[0])
