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

    add("str_goto_background_on_close_title", u"Ezarri ateratzeko jarrera")
    add("str_goto_background_on_close_warn", \
        u"%s atzeko planoan lan egiten jarraitu dezake, nahiz eta leiho nagusia itxi . \n" \
        u" Edo %sretik atera zaitezke.  %s martxan jarraitzea  \n" \
        u"nahi duzu?" % (PRODUCT_NAME,PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"Atzeko planoan lan egiten mantendu leiho nagusia itxi arren")
    add("str_yes", u"Bai")
    add("str_no", u"Ez")
    add("str_dont_ask", u"Ez galdetu berriro")
    add("str_ok", u"Ados")
    add("str_hide_window", u"Leihoa itxi")
    add("str_show_window", u"Leihoa erakutsi")

    add("str_catchup_pref", u"Catchup funtzioak ez ditu programa zaharrak kontutan hartuko")
    add("str_set_catchup_title", u"Catchup funtzioaren jarrera ezarri")
    add("str_set_catchup_description", \
        u"Bilaketa Catchup funtzioaren bitartez egiten denean, kontutan hartuko diren programa bakarrak \n" \
        u"jario bakoitzan goian dauenak dira.  Mesedez, zehaztu ezazu %srek nola kudeatu behar dituen\n" \
        u"kontutan hartu ez diren elementuak." % PRODUCT_NAME)
    add("str_skip_permanently", u"Ez hartu kontutan betirako")
    add("str_skip_temporarily", u"Ez hartu kontutan orain")
    
    add("str_set_oneclick_handler", u"Ezarri klik-bakarreko maneiatzailea")
    add("str_set_oneclick_handler_warn",\
        u"%s ez da klik-bakarreko podcast harpidetze maneiatzailea. \n" \
        u"Klik-bakarreko harpidetza loturak kudeatzeko %s erabili nahi duzu??" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"Always use %s for one-click subscription" % PRODUCT_NAME)
    
    add("str_txt_feedmanager", u"Jario irakurgailu bateragarriak:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Bilatu edo ikusi podcastak, klik-bakarreko harpidetzarekin")

    add("str_open_downloads_folder", u"Ireki jaitsieren katalogoa")
    add("str_chkupdate_on_startup", u"Begiratu aplikazioaren bertsio berriak hasieratzean.")
    add("str_bad_feedmanager_url", u"Mesedez, jario irakurgailuarentzat URL baliogarri bat sartu.")
    add("str_feed_manager", u"Jario irakurtzailea")
    add("str_feedmanager_enable", u"Sinkronizatu harpidetzak urruneko zerbitzu batekin")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"Ezarri abesti/programaren mota")
    add("str_auto_delete", u"Ezabatu automatikoki baldintza hau betetzen duten programak")
    add("str_days_old", u"egun zahar")
    
    add("str_show_notes", u"Oharrak erakutsi")
    add("str_close", u"Itxi")

    add("str_critical_error_minspace_exceeded", \
        u"Jaitsiera etenda; %dMB libre dituzu " \
        u"%dMBeko minimoa baino gutxiago.  Mesedez ustu " \
        u"zure diska edo aldatu biltegiratze ezaugarriak " \
        u"Lehentasun ataleko kudeatze ezaugarrietan")
    add("str_critical_error_unknown", u"Ezezaguna den errore kritikoa fitxategia jaistean.")
    
    add("str_error_checking_new_version", u"Barkatu, baina errore bat gertatu da bertsio berria bilatzen.  Mesedez saiatu beranduago.")
    add("str_hours", u"orduak")
    add("str_minutes", u"minutuak")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Eskaneatzen")
    add("str_scanned", u"Eskaneatuta")
    add("str_feed", u"Jarioa")
    add("str_feeds", u"jarioak")
    
    add("str_downloading_new_episodes", u"Programa berriak jaisten")
    add("str_sched_specific", u"Begiratu denbora konkretu batean")
    add("str_sched_reg", u"Begirtatu denbora tarte konkretuetan")
    add("str_repeat_every", u"Errepikatze maiztasuna:")
    add("str_next_run_label", u"Hurrengo martxan jartzea:")
    
    add("str_license", u"This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.")

    add("str_donate", u"%s-i dohaintza bat egin" % PRODUCT_NAME)
    add("str_donate_expl", u"It's important to keep community-owned %s applications online and keep this new way of consuming media free as in speech. Any amount of money will make the team happy and encourage them to work on new features and services!" % PRODUCT_NAME)
    add("str_donate_yes", u"Bai, eraman nazazu dohaintza egiteko orrira orain")
    add("str_donate_two_weeks", u"Pixkat gehiago begiratu behar dut, erakutsi berriro bi astetan")
    add("str_donate_already", u"Jadanik dohaintza bat egin dut, ez erakutsi hau berriro")
    add("str_donate_no", u"Ez, ez dut dohaintza bat egin nahi, ez erakutsi hau berriro")
    add("str_donate_one_day", u"Ez orain, erakutsi hau berriro egun batean")
    add("str_donate_proceed", u"Jarraitu")

    add("str_scheduler_dialog", u"Planifikatzailea")
    add("str_scheduler_tab", u"Konfigurazioa")

    add("str_select_import_file", u"Aukeratu inportatzeko fitxategia")    
    add("str_add_feed_dialog", u"Jario bat gehitu")
    add("str_edit_feed", u"Jarioaren ezaugarriak")

    add("str_really_delete", u"Benetan ezabatu")

    add("str_license_caption", u"Lizentzia")

    add("str_ep_downloaded", u"Jaitsia")
    add("str_ep_skipped_removed_other", u"Pasatakoa/Ezabatua/BesteIturriBatetik")
    add("str_dl_state_to_download", u"Jaisteko")

    add("str_select_none_cleanup", u"Ezer ez aukeratu")
    add("str_submit_lang", u"Hizkuntza bat bidali")
    
    add("str_dltab_live", u"Orain jaisten: ")
    add("str_dltab_ul_speed", u"Igotze abiadura: ")
    add("str_dltab_dl_speed", u"Jaiste abiadura: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Fitxategia")
    add("str_import_opml", u"Opml fitxategi batetik jaitsi jarioak...")
    add("str_export_opml", u"Jarioak opml fitxategi batean esportatu..")
    add("str_preferences_menubar", u"Ezaugarriak...")
    add("str_close_window", u"Lehioa ezkutatu")
    add("str_quit", u"Atera")

    add("str_edit", u"Editatu")
    add("str_select_all", u"Denak hautatu")

    add("str_tools", u"Tresnak")
    add("str_check_all", u"Denak markatu")
    add("str_catch_up", u"Catch-up")
    add("str_check_selected", u"Markatu aukeratuak")
    add("str_add_feed", u"Jario bat gehitu...")
    add("str_remove_selected", u"Jario bat ezabatu...")
    add("str_feed_properties", u"Jarioaren ezaugarriak...")
    add("str_scheduler_menubar", u"Planifikatzailea...")
    
    add("str_select_language", u"Hizkuntza aukeratu")

    ## these are also used for the tabs
    add("str_view", u"Ikusi")
    add("str_downloads", u"Jaitsierak")
    add("str_subscriptions", u"Harpidetzak")
    add("str_podcast_directory", u"Podcast katalogoa")
    add("str_cleanup", u"Garbitu")

    add("str_help", u"Laguntza")
    add("str_online_help", u"Online Laguntza")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Begiratu berrikuntzarik dagoen...")
    add("str_report_a_problem", u"Arazo bat igorri")
    add("str_goto_website", u"Webgunera joan")
    add("str_make_donation", u"Dohaintza bat egin")
    add("str_menu_license", u"Lizentzia...")
    add("str_about", u"Honi buruz...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Ezabatutako hautatutako elementuak")
    add("str_cancel_selected_download", u"Hautatutako jaitsiera eten")
    add("str_pause_selected", u"Gelditu hautatutakoa")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Berria")
    add("str_dl_state_queued", u"Ilaran")
    add("str_dl_state_downloading", u"Jaisten")
    add("str_dl_state_downloaded", u"Jaitsita")
    add("str_dl_state_cancelled", u"Ezeztatua")
    add("str_dl_state_finished", u"Amaitua")
    add("str_dl_state_partial", u"Erdizka jaitsia")
    add("str_dl_state_clearing", u"Garbitzen")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Podcast berriak aurkitu")
    add("str_catch_up_mode", u"Catch-up - Only download the last new subscriptions")

    add("str_add_new_feed", u"Jario berria gehitu");
    add("str_remove_selected_feed", u"Hautatutako jarioa ezabatu")
    add("str_properties", u"Ezaugarriak")
    add("str_check_selected_feed", u"Markatu hautatutako jarioak")

    add("str_scheduler_on", u"Planifikatzailea - Gaitua")
    add("str_scheduler_off", u"Planifikatzailea - Ezgaitua")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Hurrengo martxan jartzea:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Programari buruzko informazioa jaisten...")
    add("str_no_episodes_found", u"Ez dira programak aurkitu.")


    ## Directorytab Toolbar
    add("str_refresh", u"Berritu")
    add("str_open_all_folders", u"Katalogo guztiak ireki")
    add("str_close_all_folders", u"Katalogo guztiak hautatu")
    add("str_add", u"Gehitu")

    ## Directorytab Other items
    add("str_directory_description", u"Zuhaitzeko jario batean klik egin edo ondoan dagoen zuriunean idatzi/itsatsi jarioaren helbidea eta ondoren Gehitu klikatu.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Jario bat aukeratu")
    add("str_refresh_cleanup", u"Berritu")
    
    add("str_look_in", u"Programak bilatu hemen,")        
    add("str_player_library", u"Erreproduzigailuaren liburutegia")
    add("str_downloads_folder", u"Jaitsitakoen katalogoa")
    add("str_delete_library_entries", u"Ezabatu liburutegiko sarrerak")
    add("str_delete_files", u"Ezabatu fitxategiak")
    add("str_select_all_cleanup", u"Denak hautatu")
    add("str_delete", u"Ezabatu")




    ## Logtab items
    add("str_log", u"Loga")
    add("str_clear", u"Garbitu")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Izena")
    add("str_lst_date", u"Data")        
    add("str_lst_progress", u"Progresua")
    add("str_lst_state", u"Egoera")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Kokalekua")
    add("str_lst_episode", u"Programa")
    add("str_lst_playlist", u"Lista")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Harpidetua")
    add("str_disabled", u"Ezgaitua")
    add("str_newly-subscribed", u"Berriki harpidetua")
    add("str_unsubscribed", u"Harpidetza ezeztatua")
    add("str_preview", u"Aurrikusi")
    add("str_force", u"Behartu")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Esportatzeko fitxategiarentzat izen bat aukeratu")
    add("str_subs_exported", u"Harpidetzak esportatuak.")
    
    ## Preferences Dialog
    add("str_preferences", u"Ezaugarriak")
    
    add("str_save", u"Gorde")
    add("str_cancel", u"Ezeztatu")
    
    # General
    add("str_general", u"Orokor")
    add("str_gen_options_expl", u"%s aplikazioarentzat aukera orokorrak" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Hasieran %s system tray-ean bakarrik erakutsi" % PRODUCT_NAME)

    add("str_run_check_startup", u"Begiratu ea podcast berriak dauden programa hasieratzean")
    add("str_play_after_download", u"Entzun jaitsitako programak jaitsi eta berehala")
    add("str_location_and_storage", u"Kokaleku eta biltegiratze kudeaketa")
    add("str_stop_downloading", u"Gelditu jaisten disko gogorra minimo honetara iristen bada: ")
    add("str_bad_megabyte_limit_1", u"Barkatu, megabyte muga ez dirudi osoko balio bat")
    add("str_bad_megabyte_limit_2", u"Mesedez saiatu berriro.")

    add("str_download_folder", u"Jaitsi podcast hau katalogo honetan")
    add("str_browse", u"Arakatu")
    add("str_bad_directory_pref_1", u"Barkatu, ezin izan dugu sartutako katalogoa aurkitu")
    add("str_bad_directory_pref_2", u"Mesedez sortu ezazu eta saiatu berriro.")

    
    # Threading
    add("str_threads", u"Threading")
    add("str_multiple_download", u"Hainbat jaitsierentzat ezaugarriak")
    add("str_max_feedscans", u"maximal threads for feedscanning per session")
    add("str_max_downloads", u"Jaitsiera muga sesio bakoitzeko")
   
    # Network settings
    add("str_networking", u"Sare konfigurazioa")
    add("str_coralize_urls", u"URLak Coralizatu (experimentala)")
    add("str_proxy_server", u"Proxy zerbitzari bat erabili")
    add("str_proxy_address", u"Helbidea")
    add("str_proxy_port", u"Portua")
    add("str_proxy_username", u"Erabiltzailea")
    add("str_proxy_password", u"Pasahitza")
    add("str_bad_proxy_pref", u"Proxy zerbitzaria erabiltzeko eskatu duzu baina ez dituzu proxyaren helbidea eta portua zehaztu. Mesedez Sare konfigurazio fitxara eta proxyaren helbidea eta portua zehaztu")

    # Player
    add("str_player", u"Erreproduzigailua")
    add("str_choose_a_player", u"Erreproduzigailu bat aukeratu")
    add("str_no_player", u"Erreproduzigailurik ez")
    
    # Advanced
    add("str_advanced", u"Aurreratua")
    add("str_options_power_users", u"Aukera hauek Erabiltzaile Jakintsuek (Power Users) erabiltzeko dira")
    add("str_run_command_download", u"Exekutatu komando hau jaitsi eta gero")
    add("str_rcmd_full_path", u"%f = Jaitsitako fitxategiaren helbide osoa")
    add("str_rcmd_podcast_name", u"%n = Podcastaren izena")
    add("str_other_advanced_options", u"Beste aukera aurreratu batzuk")
    add("str_show_log", u"Erakutsi log fitxa aplikazioan")



    ## Feed Dialog (add/properties)
    add("str_title", u"Izenburua")
    add("str_url", u"URL")
    add("str_goto_subs", u"Joan harpidetza fitxara podcast honi buruzko programa ezberdinak ikusteko")
    add("str_feed_save", u"Gorde")
    add("str_feed_cancel", u"Ezeztatu")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Planifikatzailea gaitu")
    add("str_sched_select_type", u"Markatu ondoko radio botoi hauek momentu konkretu batean edo denbora tarte konkretu batzuetan podcasta ikuskatzeko:")
    add("str_check_at_specific_times", u"Momentu konkretu batean ikuskatu")
    add("str_check_at_regular_intervals", u"Denbora tarte konkretu batzuetan ikuskatu")
    add("str_repeat_every:", u"Errepikatze maiztasuna:")
    add("str_latest_run", u"Azken martxan jartzea:")
    add("str_next_run", u"Hurrengo martxan jartzea:")
    add("str_not_yet", u"Ez oraindik")
    #--- Cancel
    add("str_save_and_close", u"Gorde eta itxi")
    #--- Save

    add("str_time_error", u"Hauetako planifikazio denbora batek ez dirudi ondo dagoela. Horrela izan beharko luke: 10:02am, 16:43.")


    ## Donations Dialog
    #--- Donate to iPodder
    #--- It's important to keep non-commercial iPodder applications online and keep this new way of consuming media free. Any amount of money will make the team happy and encourage them to work on new features!
    #--- Yes, take me to the donations page now!
    #--- I still have to check it a bit more, show this again in two weeks
    #--- I allready made a donation, don't show this dialog again
    #--- No, I don't want to donate, never show this dialog again
    #--- Not now, notify me again in 1 day
    #--- OK




    ## About Dialog
    #--- Version:
    #--- Programming: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDesign: Martijn Venrooy\nContent strategist: Mark Alexander Posth\nConcept: Adam Curry, Dave Winer\nThanks to all translators for their commitments!\n\nBased on Feedparser and BitTorrent technology.\nThis program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.




    ## Statusbar items
    add("str_check_for_new_podcast_button", u"Ikuskatu podcast berriak dauden botoi berria sakatuz")
    add("str_last_check", u"Azkeneko ikuskaketa:")
    add("str_of", u"nongoa:")
    add("str_item", u"elementu")
    add("str_items", u"elementuak")
    add("str_downloading", u"jaisten")
    add("str_downloaded", u"jaitsita")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"Zure musika errepoduzigailua abiarazten...")
    add("str_loaded_mediaplayer", u"Zure musika errepoduzigailua abiarazita...")        
    add("str_initialized", u"%s prest" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + " - Podcast irakurgailua v" + __version__)
    add("str_localization_restart", u"%sren kontrol guztiak lokalizatzeko berabiatzea beharrezkoa da. OK sakatu ondo ixteko, edo ezeztatu jarraitzeko." % PRODUCT_NAME)
    add("str_really_quit", u"Jaitsiera bidean, benetan atera nahi duzu?");
    add("str_double_check", u"Badirudi jadanik programa hau jaisten ari zarela");
    
    # check for update
    add("str_new_version_ipodder", u"%s bertsio berri bat dagoela dirudi, jaisteko gunera joan OK zapalduz" % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"%s bertsio hau eguneraturik dago" % PRODUCT_NAME)
    add("str_other_copy_running", u"%s beste bertsio bat martxan dago. Esnatu ezazu, itxaron amaitzea, edo hil ezazu." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Egiaztatu orain")        
    add("str_open_ipodder", u"%s ireki" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Jarioak eskaneatzen")

    # Feed right-click menu
    add("str_remove", u"Ezabatu")        
    add("str_open_in_browser", u"Ireki nabigatzailean")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Programak ireki musika erreproduzigailuan")
    add("str_clear_selected", u"Garbitu aukeratutakoak")
    




