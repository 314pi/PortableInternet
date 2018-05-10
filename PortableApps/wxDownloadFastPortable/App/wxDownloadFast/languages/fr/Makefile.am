## Process this file with automake to produce Makefile.in

localesdir = $(datadir)/locale/fr/LC_MESSAGES

install-data-local:
	$(mkinstalldirs) $(DESTDIR)$(localesdir) ; \
	$(INSTALL_DATA) wxDFast.mo $(DESTDIR)$(localesdir)/wxDFast.mo ;

uninstall-local:
	rm $(DESTDIR)$(localesdir)/wxDFast.mo ;
