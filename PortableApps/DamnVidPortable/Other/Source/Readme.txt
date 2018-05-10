DamnVid Portable Launcher
========================
Copyright 2004-2010 John T. Haller
Copyright 2010 Michael Secord

Website: http://PortableApps.com/DamnVidPortable

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


ABOUT DamnVid PORTABLE
====================
The DamnVid Portable Launcher allows you to run DamnVid from a removable drive whose
letter changes as you move it to another computer.  The program can be entirely
self-contained on the drive and then used on any Windows computer.


LICENSE
=======
This code is released under the GPL.  The full code is included with this
package as DamnVidPortable.nsi.


INSTALLATION / DIRECTORY STRUCTURE
==================================
By default, the program expects this directory structure:

-\ <--- Directory with DamnVidPortable.exe
	+\App\
		+\DamnVid\
		+\DefaultData\
		+\AppInfo\
	+\Data\
		+\settings\


DamnVidPORTABLE.INI CONFIGURATION
===============================
The DamnVid Portable Launcher will look for an ini file called DamnVidPortable.ini within its
directory.  If you are happy with the default options, it is not necessary, though.  The INI
file is formatted as follows:

[DamnVidPortable]
AdditionalParameters=
DisableSplashScreen=false
LocalTemp=true

The AdditionalParameters entry allows you to pass additional commandline parameter entries
to DamnVid.exe.  Whatever you enter here will be appended to the call to DamnVid.exe.

The DisableSplashScreen entry allows you to disable the splash screen by setting it to
true (lowercase).

The LocalTemp entry allows you to specify whether or not to use the local machine's temp folder
to convert files instead of the current media. It is advisable to leave this as true if you are
running from portable media to save the number of reads/writes to the drive.

PROGRAM HISTORY / ABOUT THE AUTHORS
===================================
This launcher contains elements from multiple sources.  It is loosely based on the
KVIrc Portable launcher.