Thunderbird Portable Launcher
=============================
Copyright 2004-2015 John T. Haller of PortableApps.com

Website: http://PortableApps.com/ThunderbirdPortable

This software is OSI Certified Open Source Software.
OSI Certified is a certification mark of the Open Source Initiative.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

ABOUT THUNDEBIRD PORTABLE
=========================
The Thunderbird Portable Launcher allows you to run Thunderbird from a removable drive
whose letter changes as you move it to another computer.  The email client and the
profile can be entirely self-contained on the drive and then used on any Windows
computer.  Specific configuration changes are made to the chrome.rdf so that your
extensions will still work as the drive letter changes.


LICENSE
=======
This code is released under the GPL.  Within the ThunderbirdPortableSource directory you
will find the code (ThunderbirdPortable.nsi) as well as the full GPL license
(License.txt).  If you use the launcher or code in your own product, please give proper
and prominent attribution.


INSTALLATION / DIRECTORY STRUCTURE
==================================
By default, the program expects the following directory structure:

-\ <--- Directory with ThunderbirdPortable.exe
	+\App\
	    +\thunderbird\
		+\gpg\ (optional)
	+\Data\
		+\plugins\
	    +\profile\
		+\gpg\ (optional)
	    +\userprofile\ (optional)
	
It can be used in other directory configurations by including the ThunderbirdPortable.ini
file in the same directory as ThunderbirdPortable.exe and configuring it as details in
the INI file section below.


THUNDERBIRDPORTABLE.INI CONFIGURATION
=================================
The Thunderbird Portable Launcher will look for an ini file called
ThunderbirdPortable.ini within its directory.  If you are happy with the default options,
it is not necessary, though.  There is an example INI included with this package to get
you started.  The INI file is formatted as follows:

[ThunderbirdPortable]
ThunderbirdDirectory=App\thunderbird
ThunderbirdExecutable=thunderbird.exe
AdditionalParameters=
GPGPathDirectory=App\gpg
ProfileDirectory=Data\profile
PluginsDirectory=Data\plugins
SettingsDirectory=Data\settings
GPGHomeDirectory=Data\gpg
DisableSplashScreen=false
AllowMultipleInstances=false
DisableIntelligentStart=false
SkipChromeFix=false
SkipCompregFix=false
RunLocally=false

The ThunderbirdDirectory, ProfileDrectory, PluginsDirectory and SettingsDirectory entries
should be set to the *relative* path to the directories containing Thunderbird.exe, your
profile, your plugins, etc. from the current directory.  All must be a subdirectory (or
multiple subdirectories) of the directory containing ThunderbirdPortable.exe.  The
default entries for these are described in the installation section above.

The GPGPathDirectory and GPGHomeDirectory allow you to specify paths to the GPG binaries
and your keyring/trustdbs for using GPG with the Enigmail extension. Note that the
GPGPathDirectory will be overridden if Thunderbird Portable is used in the layout of the
PortableApps.com Platform and the shared GPG Portable release is located within the
$PortableApps\CommonFiles\GPG directory and Thunderbird Portable is located in the 
$PortableApps\ThunderbirdPortable directory (or similar).

The ThunderbirdExecutable entry allows you to set the Thunderbird Portable Launcher to
use an alternate EXE call to launch Thunderbird.  This is helpful if you are using a
machine that is set to deny Thunderbird.exe from running.  You'll need to rename the
Thunderbird.exe file and then enter the name you gave it on the Thunderbirdexecutable=
line of the INI.

The AdditionalParameters entry allows you to pass additional commandline parameter
entries to Thunderbird.exe.  Whatever you enter here will be appended to the call to 
hunderbird.exe.

The LocalHomepage entry allows you to set Thunderbird Portable to use a local file on
your portable drive as your homepage.  The file must be a path relative to the launcher.
If you were to set it to a file in the same directory as ThunderbirdPortable.exe, you
would use LocalHomepage=homepage.html  If it was in a subdirectory called homepage, you
would enter LocalHomepage=homepage/homepage.html  If it were in a directory above
ThunderbirdPortable.exe, it would be LocalHomepage=../homepage.html

The DisableSplashScreen entry allows you to run the Thunderbird Portable Launcher without
the splash screen showing up.  The default is false.

The AllowMultipleInstances entry will allow Thunderbird Portable to run alongside your
regular local copy of Thunderbird if you set it to true (lowercase).  The default is
false.  This will disable the registry handling ability of the launcher, so Thunderbird
may check if it is the default mail client.  For this reason, use of
AllowMultipleInstance is not normally recommended for PCs you don't own.

The DisableIntelligentStart entry allows you to to have Thunderbird Portable run its chrome
and component registry fixes on every start.  Normally, it tracks when you've moved to a
new path (switching PCs for instance) and only processes the chrome and component
registry when you do.  By skipping it when the path is the same, Thunderbird Portable starts
up faster.  But, if you copy a profile into Thunderbird Portable between sessions (it handles
a copy in on first run automatically), it won't know to process these.  This usually
happens if you copy a profile into Thunderbird Portable from your local PC on a regular basis
with a sync utility that doesn't work with Thunderbird Portable (like Portable Apps Sync
does).  Setting this to true causes Thunderbird Portable to process each on every start.

The SkipChromeFix entry allows you to set Thunderbird Portable not to adjust the
chrome.rdf for extension compatibility on launch.  Set it to true (lowercase) to skip
chrome.rdf processing.  The default is false.

The SkipCompregFix entry allows you to set Thunderbird Portable not to adjust the
component registry (compreg.dat) for certain extension compatibility on launch.  It is
useful if you are not using extensions which make use of the component registry (like
Forecast Fox or the Mozilla Calendar) as Thunderbird Portable will launch more quickly.
Set it to true (lowercase) to skip chrome.rdf processing.  The default is false.

The RunLocally entry allows you to set Thunderbird Portable to copy your profile, plugins
and Thunderbird binaries to the local machine's temp directory.  This can be useful for
instances where you'd like to run Thunderbird Portable from a CD (aka Thunderbird
Portable Live) or when you're working on a machine that may have spyware or viruses and
you'd like to keep your device set to read-only mode.  The only caveat is, of course,
that any changes you make that session (settings, email downloaded, etc) aren't saved
back to your device.  When done running, the local temp directories used by Thunderbird
Portable are removed.  Setting RunLocally to true automatically sets WaitForThunderbird
to true.  RunLocally does not currently work with AllowMultipleInstances as it cannot
track which version of Thunderbird is running.


PROGRAM HISTORY / ABOUT THE AUTHORS
===================================
This launcher contains elements from multiple sources.  It began as a batch file launcher
written by myself (John T. Haller) and posted to the mozillaZine.org thread about running
Firefox from a USB key.  tracon later released a launcher called fflaunch which I
enhanced and re-released as Portable Firefox.  mai9 later improved on fflaunch's
techniques and released it as Free The Fox.  Multiple suggestions back and forth as well
as improvements from mai9, myself and others lead to the launcher we have today.  The
current versions is more original work by myself, but still builds on some of the
original ideas.


CURRENT LIMITATIONS
===================
INCOMPATIBLE EXTENSIONS - Certain extensions use additional local files or prefs.js to
store information, neither of which are handled by the Thunderbird Portable launcher when
moving between machines.