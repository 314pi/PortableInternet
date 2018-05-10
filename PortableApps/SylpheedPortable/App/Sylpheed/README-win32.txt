-------------------------------------------------------------------------------
[ Name           ] Sylpheed 3.7-win32
[ Developer      ] Hiroyuki Yamamoto
[ Location       ] http://sylpheed.sraoss.jp/
[ Contact        ] hiro-y@kcn.ne.jp
[ Required       ] Microsoft Windows 7 / 8 / 10
[ Category       ] E-Mail client (free software)
[ Compression    ] ZIP
[ Redistribution ] GNU GPL (see COPYING), etc.
[ Copyright      ] (C) 1999-2018 Hiroyuki Yamamoto
-------------------------------------------------------------------------------


Description
===========

Sylpheed is an e-mail client (mailer, MUA).
It is simple, lightweight but featureful, and easy-to-use.

It supports various protocols such as POP3, IMAP4rev1, and NNTP.
SSL is also supported.

Sylpheed also supports internationalization (i18n) and multilingualization
(m17n). It is currently translated to 29+ languages. The Japanese processing
is highly supported. For example, code guessing (ISO-2022-JP/EUC-JP/
Shift_JIS/UTF-8), and the support for the environment-dependent characters.

Powerful filtering and search function, and learning-type junk mail control
function which utilizes external commands are also implemented.

PGP features are available if GnuPG is installed. 


License
=======

Sylpheed conforms to GNU GPL. See COPYING for detail.

GLib, GTK+, Pango, libiconv, GPGME, and LibSylph library conform to GNU LGPL.
See COPYING.LIB for detail.

Oniguruma library conform to the BSD license. See COPYING.onig for detail.

Refer to LICENSE.SSL for the license of OpenSSL library.

Refer to LICENSE.curl for Curl.

Bsfilter is distributed under the GNU GPL. See COPYING for detail.


Install
=======

(Installer version)
Execute the exe file of the installer. When it launched, follow the
instructions.

(Zip archive version)
Extract the zip archive under the appropriate location.
Then, execute sylpheed.exe.


Update
======

(Installer version)
Run the installer while Sylpheed is not running.
After the previous version is automatically uninstalled, installation
will start.

(Zip archive version)
Overwrite the contents of zip archive to the folder of the previous version
while Sylpheed is not running.
On major update, copying the new version after deleting the previous one
is recommended because redundant files may be left.

By default, Sylpheed will query to server whether a new version is released
and display dialog if exists.


Usage
=====

Execute Sylpheed by the desktop icon, or "Start Menu - Sylpheed - Sylpheed".
See "Start Menu - Sylpheed - Sylpheed Manual" or "Help - Manual" for detail.


Configuration files
===================

The configuration files and the mailboxes are saved under the following
location (%APPDATA%\Sylpheed) by default.

C:\Users\(user name)\AppData\Roaming\Sylpheed

If you want to change the location of the configuration files, you can
specify it by the command line option: --configdir "directory name".
Create a shortcut of sylpheed.exe, and append the option to the link target
like the following:

"C:\Program Files\Sylpheed\sylpheed.exe" --configdir "D:\Sylpheed"

If sylpheed.ini file exists at the same location of sylpheed.exe, it will be
loaded at startup. Using this, you can make Sylpheed completely portable
independent of drive letters etc, and you can install it in removable media
such as USB memory.
(Note: The installer version, and GnuPG and GPGME use registry)

The sample INI file is included in the package as sample-sylpheed.ini.
Please copy or rename it to use.
'ipcport' specifies the port number of socket for IPC (default is 50215).
'configdir' specifies the location of configuration files as a relative
path from the folder in which sylpheed.exe is located, or an absolute path.


Junk mail control
=================

If you want to enable junk mail control, you have to install
SylFilter ( http://sylpheed.sraoss.jp/sylfilter/ ) or
bsfilter ( http://bsfilter.org/index-e.html ) additionally.
As an easy way of installation, copy sylfilter.exe or bsfilterw.exe into the
directory which contains sylpheed.exe.

Sylpheed installer includes SylFilter or bsfilter, so you only need to enable
the settings to start using it. SylFilter is recommended from the point of
performance and detection accuracy.

SylFilter
---------

There is no important precaution for SylFilter.
The configuration and the database are saved into the following location:

C:\Users\(user name)\AppData\Roaming\SylFilter

bsfilter
--------

If you have installed bsfilter into another location,  please note that
the location of database files will be changed.

The files confirmed to work with Sylpheed are also distributed at the following
location:

  http://sylpheed.sraoss.jp/sylpheed/others/bsfilter-1.0.17.rc4.tgz
  http://sylpheed.sraoss.jp/sylpheed/others/bsfilter-1.0.17.rc4/
    bsfilter/bsfilterw.exe

Note: bsfilterw.exe which is included in bsfilter-1.0.16.tgz has problem.
      Please use bsfilter-1.0.17.rc4 or later.


PGP feature
===========

If you want to enable PGP features, you have to install GnuPG
( http://www.gnupg.org/(en)/download/index.html#auto-ref-1 ).


Association of mailto link and .eml file
========================================

If you want to register Sylpheed as a handler for mailto: protocol and
associate .eml file after you have installed it from zip archive,
add the entries to the registry by double-clicking the included file
"sylpheed-mailto-protocol_admin.reg" and "sylpheed-mailto-protocol_user.reg"
You can automatically register them when using the installer.

If you want to revert Sylpheed to default after other mail clients has been
set to default, add the entries to the registry as above.

If you have installed Sylpheed into a location other than C:\Program Files\Sylpheed\sylpheed.exe, modify the paths.


Uninstall
=========

(Installer version)
Select Sylpheed from "Add or Remove Programs" in the Control Panel, and
click "Change or Remove".

(Warning: if the installed version is equal or less than 2.2.3, all files in
the installed folder will be removed, so please be careful if you have created
mailboxes under the installed folder, or you are using bsfilter etc. Other than
the files or folders created by the installer will not be removed since 2.2.4.)

(Zip archive version)
Delete the all files with the extracted folder.
Delete the configuration files and the mailboxes too if they are not
required anymore.


How to add SSL certificates
===========================

Sylpheed uses OpenSSL library for SSL communication. Because of it, Sylpheed
cannot use the Windows certificate store for the verification of certificates.
Use the following method to add certificates to Sylpheed:

1. Open a CA certificate file, and export it as "Base 64 encoded X509 (.CER)"
   format.
2. Open etc\ssl\certs\certs.crt file under the Sylpheed installed folder
   with a text editor which supports LF linebreak code.
3. Open the exported file in 1., and add it at the head or tail of the
   certs.crt file.
4. Overwrite certs.crt with the edited file.
   If you want to manage certificates per user, save it as:
   C:\Users\(user name)\AppData\Roaming\Sylpheed\certs.crt

Additionally, if you select 'Always accept' when the verification of
certificates fails, the certificates will be saved to the local settings and
they will be accepted automatically from the next session.


Other notices
=============

At the current version, some features implemented in the Unix version, such as
Actions, are not implemented yet.

Sylpheed for Windows implements inter-process communication for remote
operation using TCP socket. Because of this, port 50215 of the loopback
address (127.0.0.1) will be consumed.

Please supply the information of "Tools/Log window", or the contents of
sylpheed.log, which is located under the configuration folder, when
reporting bugs.
