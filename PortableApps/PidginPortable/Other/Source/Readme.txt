Pidgin Portable Launcher
========================
Copyright 2004-2010 John T. Haller

Website: http://PortableApps.com/PidginPortable

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


ABOUT Pidgin PORTABLE
===================
The Pidgin Portable Launcher allows you to run Pidgin from a removable drive whose
letter changes as you move it to another computer.  The program can be entirely
self-contained on the drive and then used on any Windows computer.


LICENSE
=======
This code is released under the GPL.  The full code is included with this
package as PidginPortable.nsi.


INSTALLATION / DIRECTORY STRUCTURE
==================================
By default, the program expects this directory structure:

-\ <--- Directory with PidginPortable.exe
	+\App\
		+\Pidgin\
		+\Aspell\
	+\Data\
		+\settings\


It can be used in other directory configurations by including the PidginPortable.ini file in the
same directory as PidginPortable.exe and configuring it as details in the INI file section below.


PidginPortable.INI CONFIGURATION
==============================
The Pidgin Portable Launcher will look for an ini file called PidginPortable.ini within its
directory.  If you are happy with the default options, it is not necessary, though.  The INI
file is formatted as follows:

[PidginPortable]
AdditionalParameters=
AllowMultipleInstances=false
DisableSplashScreen=false

The AdditionalParameters entry allows you to pass additional commandline parameter entries
to Pidgin.exe.  Whatever you enter here will be appended to the call to Pidgin.exe.

The AllowMultipleInstances entry allows you to let multiple instances of Pidgin run
simultaneously.  Not that this may cause files to be left behind on the PC or custom GTK configuration
options to be lost.

The DisableSplashScreen entry allows you to disable the splash screen by setting it to
true (lowercase).


PROGRAM HISTORY / ABOUT THE AUTHORS
===================================
This launcher contains elements from multiple sources.  It is loosely based on the
Firefox Portable launcher and contains some ideas from mai9 and tracon on the mozillaZine
forums.