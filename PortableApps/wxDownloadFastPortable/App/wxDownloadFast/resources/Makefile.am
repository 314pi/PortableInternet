## Process this file with automake to produce Makefile.in

SUBDIRS = xpm RipStop

pixmapdir = $(datadir)/pixmaps

CLEANFILES = Resources.cpp

EXTRA_DIST = \
	wxdfast.desktop

Applicationsdir = $(datadir)/applications
Applications_DATA = wxdfast.desktop

wxdfast_XRC = \
	boxabout.xrc\
	boxnew.xrc\
	boxoptions.xrc\
	mainwindow.xrc\
	menubar.xrc\
	toolbar.xrc\
	images.xrc

if NOXRCMODE
dist_noinst_DATA = Resources.cpp
## Create Resources.cpp
Resources.cpp: $(wxdfast_XRC)
	$(WXRC) -c -o Resources.cpp $(wxdfast_XRC)
endif

## dist_pixmap_DATA = \
## 	wxdfast.xpm

dist_pkgdata_DATA = \
	$(wxdfast_XRC)
## 	wxdfast.xpm \
##	wxdfast.ico \
##	boxabout.xpm
