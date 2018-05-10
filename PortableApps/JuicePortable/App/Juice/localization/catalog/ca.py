#! python
# -*- coding: utf-8 -*-

g_strtable = -1
language_code = __name__.split('.')[-1]

from ipodder.configuration import __version__
from gui.skin import PRODUCT_NAME


def add(label, txt):
    global g_strtable
    g_strtable.AddText(language_code, label, txt)

def AddStrings(strtable):
    global g_strtable
    g_strtable = strtable

    #############################################
    ## MV: 11:25 PM 2/20/2005
    ## READ THIS BEFORE EDITING/ADDING!!
    ## If you add new items, add them in the 'New strings' part.
    ## We can easily send them to the translators that way.
    #############################################

    ##_________________________________________________________
    ##
    ##     New strings
    ##_________________________________________________________

    add("str_txt_feedmanager", u"Administradors de fonts compatibles:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Buscar o veure podcasts, subscripció amb un únic clic.")

    add("str_open_downloads_folder", u"Obrir la carpeta de descàrregues")
    add("str_chkupdate_on_startup", u"Comprobar si hi han noves versions al arrancar.")
    add("str_bad_feedmanager_url", u"Entreu una adreça vàlida per l'administrador de fonts.")
    add("str_feed_manager", u"Administrador de fonts")
    add("str_feedmanager_enable", u"Sincronitzar les subscripcions amb un servei remot")
    add("str_opml_url", u"Adreça OPML")
    add("str_set_track_genre", u"Enviar el tipus de pista a")
    add("str_auto_delete", u"Esborrar automàticament episodis de mes de")
    add("str_days_old", u"dias.")
    
    add("str_show_notes", u"Mostrar les notes")
    add("str_close", u"Tancar")

    add("str_critical_error_minspace_exceeded", \
        u"Descàrrega ignorada; l'espai lliure està %dMB per sota " \
        u"del mínim de %dMB. Si us plau allibereu espai en el " \
        u"vostre disc utilitzant Neteja o ajusteu les preferencies " \
        u"de gestió d'espai")
    add("str_critical_error_unknown", u"Error crític desconegut durant la descàrrega.")
    
    add("str_error_checking_new_version", u"Ho sentim però hi ha hagut un error en la busqueda de noves versions. Torneu a probar-ho mes endavant.")
    add("str_hours", u"hores")
    add("str_minutes", u"minuts")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Comprovant")
    add("str_scanned", u"Comprovat")
    add("str_feed", u"font")
    add("str_feeds", u"fonts")
    
    add("str_downloading_new_episodes", u"Descarrega de nous episodis")
    add("str_sched_specific", u"Comprobar a hores determinades")
    add("str_sched_reg", u"Comprovar periòdicament")
    add("str_repeat_every", u"Repetir cada")
    add("str_next_run_label", u"Propera execució:")
    
    add("str_license", u"Aquesta aplicació es programari lliure; el podeu redistribuir i/o modificar sota les condicions de la Llicencia Pública General de GNU tal i com es publicada per la Free Software Foundation; sigui la versió 2 de la llicencia o, sota el vostra criteri, qualsevol versió posterior. Aquesta aplicació es distribueix amb l'esperança de que resulti útil, pero sense cap mena de garantia, ni tan sols la garantia implícita de mercandibilitat ni de adequació per cap propòsit particular. \n\nPer a mes detalls veieu la Llicencia Pública General de GNU.")

    add("str_donate", u"Fer una donació a %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Es important mantenir en linea les aplicacions %s de la comunitat i mantenir aquest modus de consumir mitjans gratuits. Qualsevol quantitat de diners encoratjarà al equip a treballar en noves prestacions i serveis!" % PRODUCT_NAME)
    add("str_donate_yes", u"Si, porta'm a la pàgina de donacions ara mateix!")
    add("str_donate_two_weeks", u"Encara vull provar-lo una mica mes, tornam-ho a recordar en dues setmanes")
    add("str_donate_already", u"Ja he fet una donació, no em tornis a mostrar aquest dialeg")
    add("str_donate_no", u"No, no vull pas donar. No em tornis a mostrar aquest dialeg mai mes")
    add("str_donate_one_day", u"Ara no, recordam-ho demà")
    add("str_donate_proceed", u"Fer-ho ara")

    add("str_scheduler_dialog", u"Programador")
    add("str_scheduler_tab", u"Configuració")

    add("str_select_import_file", u"Selecció")    
    add("str_add_feed_dialog", u"Afegir una font")
    add("str_edit_feed", u"Propietats de la font")

    add("str_really_delete", u"Esborrar realment")

    add("str_license_caption", u"Llicencia")

    add("str_ep_downloaded", u"Descarregat")
    add("str_ep_skipped_removed_other", u"Ignorat/Eliminat/Altre Font")
    add("str_dl_state_to_download", u"A Descarregar")

    add("str_select_none_cleanup", u"No seleccionar-ne cap")
    add("str_submit_lang", u"Enviar un idioma")
    
    add("str_dltab_live", u"Descàrregues en procés: ")
    add("str_dltab_ul_speed", u"Velocitat de càrrega: ")
    add("str_dltab_dl_speed", u"Velocitat de descàrrega: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Fitxer")
    add("str_import_opml", u"Importar fonts des d'un opml...")
    add("str_export_opml", u"Exportar fonts com a opml...")
    add("str_preferences_menubar", u"Preferencies...")
    add("str_close_window", u"Tancar finestra")
    add("str_quit", u"Sortir")

    add("str_edit", u"Editar")
    add("str_select_all", u"Seleccionar-ho tot")

    add("str_tools", u"Eines")
    add("str_check_all", u"Comprovar-ho tot")
    add("str_catch_up", u"Posar-se al dia")
    add("str_check_selected", u"Comprovar la selecció")
    add("str_add_feed", u"Afegir una font...")
    add("str_remove_selected", u"Eliminar la font")
    add("str_feed_properties", u"Propietats de la font...")
    add("str_scheduler_menubar", u"Programador...")
    
    add("str_select_language", u"Seleccionar l'idioma")

    ## these are also used for the tabs
    add("str_view", u"Veure")
    add("str_downloads", u"Descàrregues")
    add("str_subscriptions", u"Subscripcions")
    add("str_podcast_directory", u"Directori Podcast")
    add("str_cleanup", u"Neteja")

    add("str_help", u"Ajuda")
    add("str_online_help", u"Ajuda en linea")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Comprobar si hi han actualitzacions...")
    add("str_report_a_problem", u"Informar d'un problema")
    add("str_goto_website", u"Anar a la pàgina web")
    add("str_make_donation", u"Fer una donació")
    add("str_menu_license", u"Llicència...")
    add("str_about", u"Quan a...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Eliminar els elements seleccionats")
    add("str_cancel_selected_download", u"Cancel·lar la descarrega de la selecció")
    add("str_pause_selected", u"Pausar la selecció")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Nou")
    add("str_dl_state_queued", u"En qua")
    add("str_dl_state_downloading", u"Descarregant")
    add("str_dl_state_downloaded", u"Descarregat")
    add("str_dl_state_cancelled", u"Cancel·lat")
    add("str_dl_state_finished", u"Finalitzat")
    add("str_dl_state_partial", u"Descarregat parcialment")
    add("str_dl_state_clearing", u"Netejant")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Comprovar si hi han nous podcasts")
    add("str_catch_up_mode", u"Posar al dia - Descarregar únicament les últimes subscripcions")

    add("str_add_new_feed", u"Afegir una font");
    add("str_remove_selected_feed", u"Eliminar la font seleccionada")
    add("str_properties", u"Propietats")
    add("str_check_selected_feed", u"Comprovar la font seleccionada")

    add("str_scheduler_on", u"Programador - Activat")
    add("str_scheduler_off", u"Programador - Desactivat")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Propera execució:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Descarregant informació d'episodis...")
    add("str_no_episodes_found", u"No s'ha trobat cap episodi.")


    ## Directorytab Toolbar
    add("str_refresh", u"Actualitzar")
    add("str_open_all_folders", u"Obrir totes les carpetes")
    add("str_close_all_folders", u"Tancar totes les carpetes")
    add("str_add", u"Afegir")

    ## Directorytab Other items
    add("str_directory_description", u"Feu clic en una font a l'arbre o copieu/enganxeu en el espai superior i feu clic a Afegir.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Seleccioneu una font")
    add("str_refresh_cleanup", u"Actualitzar")
    
    add("str_look_in", u"Buscar episodis a")        
    add("str_player_library", u"Arxiu del reproductor")
    add("str_downloads_folder", u"Carpeta de descàrregues")
    add("str_delete_library_entries", u"Esborrar entrades de la llibreria")
    add("str_delete_files", u"Esborrar fitxers")
    add("str_select_all_cleanup", u"Seleccionar-ho tot")
    add("str_delete", u"Esborrar")




    ## Logtab items
    add("str_log", u"Registre")
    add("str_clear", u"Buidar")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nom")
    add("str_lst_date", u"Data")        
    add("str_lst_progress", u"Progrés")
    add("str_lst_state", u"Estat")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Lloc")
    add("str_lst_episode", u"Episodi")
    add("str_lst_playlist", u"Llista de reproducció")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Subscrit")
    add("str_disabled", u"Desabilitat")
    add("str_newly-subscribed", u"Subscripció recent")
    add("str_unsubscribed", u"Subscripció anul·lada")
    add("str_preview", u"Previsualitzat")
    add("str_force", u"Forçat")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Seleccioneu el fitxer a importar

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Esculliu un nom per al fitxer d'exportació")
    add("str_subs_exported", u"Subscripcions exportades.")
    
    ## Preferences Dialog
    add("str_preferences", u"Preferencies")
    
    add("str_save", u"Desa")
    add("str_cancel", u"Cancel·la")
    
    # General
    add("str_general", u"General")
    add("str_gen_options_expl", u"Configuració de les opcions generals del %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Reduir a la Barra de Sistema al arrancar")

    add("str_run_check_startup", u"Comprova si hi han nous podcasts quant s'arranqui l'aplicació")
    add("str_play_after_download", u"Reprodueix les descàrregues tant bon punt s'hagin descarregat")
    add("str_location_and_storage", u"Configuració de lloc i emmagatzemament")
    add("str_stop_downloading", u"Deixa de descarregar si el disc baixa d'un mínim de")
    add("str_bad_megabyte_limit_1", u"Ho sento, El límit de megabytes no sembla un nombre sencer.")
    add("str_bad_megabyte_limit_2", u"Si us plau, torneu-ho a provar.")

    add("str_download_folder", u"Carpeta on es descarregaran els podcasts")
    add("str_browse", u"Navega")
    add("str_bad_directory_pref_1", u"Ho sento, no trobo la carpeta que heu entrat")
    add("str_bad_directory_pref_2", u"Si us plau, torneu-la a crear i torneu-ho a provar.")

    
    # Threading
    add("str_threads", u"Descàrregues simultaneas")
    add("str_multiple_download", u"Configuració de descàregues múltiples")
    add("str_max_feedscans", u"Nombre màxim de comprovacions de font simultaneas")
    add("str_max_downloads", u"Nombre màxim de descàrregeus per sessió")
   
    # Network settings
    add("str_networking", u"Configuració de Xarxa")
    add("str_coralize_urls", u"Coralitza les URLs (experimental)")
    add("str_proxy_server", u"Usa un servidor intermediari")
    add("str_proxy_address", u"Adreça")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Nom d'usuari")
    add("str_proxy_password", u"Contrasenya")
    add("str_bad_proxy_pref", u"Heu habilitat l'us de servidors intermediaris pero no heu proporcinat un servidor intermediari i un port. Si us plau, torneu al panell Configuració de Xarxa i poseu-hi un servidor intermediari i el seu port.")

    # Player
    add("str_player", u"Reproductor")
    add("str_choose_a_player", u"Esculliu un reproductor")
    add("str_no_player", u"No hi ha cap reproductor")
    
    # Advanced
    add("str_advanced", u"Avançat")
    add("str_options_power_users", u"Aquestes opcions poden esser usades pels usuaris avançats")
    add("str_run_command_download", u"Executa aquesta comanda després de cada descàrrega")
    add("str_rcmd_full_path", u"%f = Camí complert al fitxer descarregat")
    add("str_rcmd_podcast_name", u"%n = Nom del podcast")
    add("str_other_advanced_options", u"Altres opcions avançades")
    add("str_show_log", u"Mostrar panell de log a l'aplicació")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titol")
    add("str_url", u"URL")
    add("str_goto_subs", u"Per veure els episodis d'aquesta font aneu al panell de subscripcions.")
    add("str_feed_save", u"Desa")
    add("str_feed_cancel", u"Cancel·la")




    ## scheduler dialog
    add("str_enable_scheduler", u"Activar el programador")
    add("str_sched_select_type", u"Seleccioneu els següents botons per comprovar a hores específiques o a intervals regulars:")
    add("str_check_at_specific_times", u"Comprovar específicament a aquestes hores")
    add("str_check_at_regular_intervals", u"Comprovar a intervals regulars")
    add("str_repeat_every:", u"Repetir cada:")
    add("str_latest_run", u"Última execució:")
    add("str_next_run", u"Propera execució:")
    add("str_not_yet", u"Encara no")
    #--- cancel
    add("str_save_and_close", u"Desa i tanca")
    #--- save

    add("str_time_error", u"Un dels horaris programats no sembla correcte. Els horaris correctes segueixen el patró: 10:02am, 16:43.")


    ## Donations Dialog
    #--- Fer una donació a ipodder
    #--- Es important mantenir aplicacions no comercials d'iPodder en linea i mantenir aquesta manera de consumir mitjans gratuits. Qualsevol quantitat de diners farà feliç els membres del equip i els encoratjarà a ampliar-ne les posibilitats!
    #--- Si, porta'm ara mateix a la pàgina de donacions!
    #--- Encara l'haig de provar una mica més, recorda'm-ho dins de dues setmanes
    #--- Ja he fet una donació, no tornis a mostrar aquest dialeg
    #--- No, no vull fer cap donació, no tornis a mostrar aquest dialeg mai mes
    #--- Ara no, recorda'm-ho demà
    #--- D'acord




    ## About Dialog
    #--- Versió:
    #--- Programació: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDiseny: Martijn Venrooy\nEstratega de continguts: Mark Alexander Posth\nConcepte: Adam Curry, Dave Winer\nGracies a tots el traductors per el seu esforç!\n\nBasat en les tecnologies Feedparser i BitTorrent.\nAquest programari es lliure; el podeu distribuir i/o modificar sota els termes de la Llicencia Pública General GNU tal i com és publicada per la Free Software Foundation; tant la versió 2 de la llicencia, com (al seu criteri) qualsevol versió posterior. Aquest programari es distribueix amb l'esperança de que sigui útil però sense cap mena de garantia, ni tan sols la garantia implicita de "mercantabilitat" ni de adequació a cap proposit. \n\nPer a més detalls veure la Llicencia Pública General GNU.




    ## statusbar items
    add("str_check_for_new_podcast_button", u"Comproveu si hi ha nous episodis prement el botó vert")
    add("str_last_check", u"Última comprovació ")
    add("str_of", u"de")
    add("str_item", u"element")
    add("str_items", u"elements")
    add("str_downloading", u"descarregant")
    add("str_downloaded", u"descarregat")
    add("str_enclosure", u"paquet")
    add("str_enclosures", u"paquets")
    add("str_fetched", u"obtingut(s)")
    add("str_loading_mediaplayer", u"Carregant el reproductor multimèdia...")
    add("str_loaded_mediaplayer", u"S'ha carregat el reproductor multimèdia...")        
    add("str_initialized", u"%s inicialitzat" % PRODUCT_NAME)




    ## other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Descarregador de Podcasts v" + __version__)
    add("str_localization_restart", u"Per traduir tots els controls del %s cal reiniciar. premeu D'acord per apagar correctament o Cancel·lar per continuar." % PRODUCT_NAME)
    add("str_really_quit", u"Hi ha una descàrrega en marxa. esteu segur de voler sortir?");
    add("str_double_check", u"Sembla que ja hi ha una descàrrega en marxa.");
    
    # check for update
    add("str_new_version_ipodder", u"Hi ha disponible una nova versió de %s. Premeu D'acord per anar a la pàgina de descàrregues." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Aquesta versió de %s està al dia." % PRODUCT_NAME)
    add("str_other_copy_running", u"Ja s'està executant un altre copia de %s. Si us plau, porteu-la a primer pla i espereu que acabi o finalitzeu-la." % PRODUCT_NAME)

    # windows taskbar right-click menu
    add("str_check_now", u"Comprovar ara")        
    add("str_open_ipodder", u"Obrir %s" % PRODUCT_NAME)
    #--- downloading
    add("str_scanning_feeds", u"Comprobant les fonts")

    # feed right-click menu
    add("str_remove", u"eliminar")        
    add("str_open_in_browser", u"Obrir en navegador")
    
    

    # downloads right-click menu
    add("str_play_episode", u"Reproduir l'episodi en el reproductor multimèdia")
    add("str_clear_selected", u"Esborrar els elements seleccionats")
