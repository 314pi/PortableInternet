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

    ##_________________________________________________________

    add("str_copy_location", u"Kopiplacering")
    add("str_set_file_types", u"Sæt filtyper")
    add("str_set_file_types_warn", \
        u"%s er ikke sat til at håndtere visse filtyper. \n" \
        u"Vil du slå dem til nu?" % PRODUCT_NAME)
    add("str_subscription_options", u"Et-kliks-abonnementsindstillinger:")
    add("str_enforce_settings", u"Gennemtving disse indstillinger ved opstart")
    add("str_file_types", u"Filtyper")
    add("str_play_button_enqueues", u"Afspil-knappen sætter det valgte spor i kø")
    add("str_authentication", u"Autentifikation")
    add("str_dl_state_skipped", u"Oversprunget")
    add("str_dl_state_removed", u"Fjernet")
    
    add("str_username", u"Brugernavn")
    add("str_password", u"Adgangskode")
    add("str_missing_proxy_password", u"Der er angivet et proxy-brugernavn, men ingen proxy-adgangskode. \n" \
        u"Slet enten brugernavnet eller angiv en adgangskode.")

    add("str_goto_background_on_close_title", u"Indstil nedlukningsopførsel")
    add("str_goto_background_on_close_warn", \
        u"%s kan fortsætte med at køre i baggrunden efter hovedvinduet \n" \
        u"er lukket. Eller %s kan afslutte.  Vil du have at %s skal \n" \
        u"fortsætte med at køre?" % (PRODUCT_NAME,PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"Fortsæt med at køre i baggrunden, når jeg lukker hovedvinduet")
    add("str_yes", u"Ja")
    add("str_no", u"Nej")
    add("str_dont_ask", u"Spørg mig ikke igen")
    add("str_ok", u"O.k.")
    add("str_hide_window", u"Skjul vindue")
    add("str_show_window", u"Vis vindue")

    add("str_catchup_pref", u"Indhentning springer ældre episoder over permanent")
    add("str_set_catchup_title", u"Indstil indhentningsopførsel")
    add("str_set_catchup_description", \
        u"Når der tjekkes i indhentningstilstand, vil %s springe alle andre \n" \
        u"punkter end det øverste i hver kanal over. Angiv hvordan %s skal behandle \n" \
        u"de oversprungne punkter." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"Spring over permanent")
    add("str_skip_temporarily", u"Spring kun over denne gang")
    
    add("str_set_oneclick_handler", u"Sæt et-kliks-håndtering")
    add("str_set_oneclick_handler_warn",\
        u"%s er ikke p.t. din et-kliks-håndtering for podcasts. \n" \
        u"Skal vi indstille %s til at starte ved klik på en abonnements-henvisning?" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"Benyt altid %s til et-kliks-abonnement" % PRODUCT_NAME)
    
    add("str_txt_feedmanager", u"Kompatible kanalhåndteringer:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Søg eller gennemse podcasts, et-kliks-abonnementer")

    add("str_open_downloads_folder", u"Åbn hentemappe")
    add("str_chkupdate_on_startup", u"Tjek for nye versioner af programmet under opstarten")
    add("str_bad_feedmanager_url", u"Angiv en gyldig URL til kanalhåndteringen.")
    add("str_feed_manager", u"Kanalhåndtering")
    add("str_feedmanager_enable", u"Synkronisér mine abonnementer med en fjernservice")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"Sæt episodegenre til")
    add("str_auto_delete", u"Slet automatisk episoder, der er mere end")
    add("str_days_old", u"dage gamle")
    
    add("str_show_notes", u"Vis noter")
    add("str_close", u"Luk")

    add("str_critical_error_minspace_exceeded", \
        u"Stoppede hentning; Den fri plads er %dMB mindre " \
        u"end de minimale %dMB.  Frigør noget plads på din disk " \
        u"med Oprydning eller justér lagerindstillingerne")
    add("str_critical_error_unknown", u"Ukendt kritisk fejl under hentningen.")
    
    add("str_error_checking_new_version", u"Der var desværre et problem med at tjekke for en ny version. Prøv igen senere.")
    add("str_hours", u"timer")
    add("str_minutes", u"minutter")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Skanner")
    add("str_scanned", u"Skannede")
    add("str_feed", u"kanal")
    add("str_feeds", u"kanaler")
    
    add("str_downloading_new_episodes", u"Henter nye episoder")
    add("str_sched_specific", u"Tjek på bestemte tidspunkter")
    add("str_sched_reg", u"Tjek med jævne mellemrum")
    add("str_repeat_every", u"Tjek hver")
    add("str_next_run_label", u"Næste kørsel:")
    
    add("str_license", u"Dette program er fri software. Du kan redistribuere det og/eller ændre det ifølge betingelserne i GNU General Public License fra Free Software Foundation. Enten version 2 af licensen, eller (efter dit eget valg) enhver senere version. Dette program distribueres i håbet om at det vil være nyttigt, men helt uden garanti, selv ikke en underforstået garanti for brugbarhed til noget som helst formål. \n\nSe detaljerne i GNU General Public License.")

    add("str_donate", u"Donér til %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Det er vigtigt at beholde almenhedens %s-programmer på nettet og bevare denne friheden for denne nye måde at bruge medier på. Ethvert pengebeløb vil glæde udviklerne og tilskynde dem til at arbejde på nye funktioner og services!" % PRODUCT_NAME)
    add("str_donate_yes", u"Ja, send mig til donationssiden nu!")
    add("str_donate_two_weeks", u"Jeg skal stadig kigge lidt mere på det. Vis mig dette igen om to uger")
    add("str_donate_already", u"Jeg har allerede doneret, vis mig ikke dette vindue igen")
    add("str_donate_no", u"Nej, jeg vil ikke donere. Vis mig aldrig dette vindue igen")
    add("str_donate_one_day", u"Ikke nu, giv mig en påmindelse om en dag")
    add("str_donate_proceed", u"Fortsæt")

    add("str_scheduler_dialog", u"Tidsstyring")
    add("str_scheduler_tab", u"Indstillinger")

    add("str_select_import_file", u"Vælg importfil")    
    add("str_add_feed_dialog", u"Tilføj kanal")
    add("str_edit_feed", u"Kanalegenskaber")

    add("str_really_delete", u"Vil du virkelig slette")

    add("str_license_caption", u"Licens")

    add("str_ep_downloaded", u"Hentet")
    add("str_ep_skipped_removed_other", u"Oversprunget/Fjernet/AndenKanal")
    add("str_dl_state_to_download", u"Skal hentes")

    add("str_select_none_cleanup", u"Vælg ingen")
    add("str_submit_lang", u"Indsend et sprog")
    
    add("str_dltab_live", u"Hentes i øjeblikket: ")
    add("str_dltab_ul_speed", u"Sendehastighed: ")
    add("str_dltab_dl_speed", u"Hentehastighed: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Fil")
    add("str_import_opml", u"Importér kanaler fra opml...")
    add("str_export_opml", u"Eksportér kanaler som opml...")
    add("str_preferences_menubar", u"Indstillinger...")
    add("str_close_window", u"Skjul vindue")
    add("str_quit", u"Afslut")

    add("str_edit", u"Redigér")
    add("str_select_all", u"Vælg alle")

    add("str_tools", u"Værktøjer")
    add("str_check_all", u"Tjek alle")
    add("str_catch_up", u"Indhent")
    add("str_check_selected", u"Tjek valgte")
    add("str_add_feed", u"Tilføj kanal...")
    add("str_remove_selected", u"Fjern kanal")
    add("str_feed_properties", u"Kanalegenskaber...")
    add("str_scheduler_menubar", u"Tidsstyring...")
    
    add("str_select_language", u"Vælg sprog")

    ## these are also used for the tabs
    add("str_view", u"Vis")
    add("str_downloads", u"Hentede filer")
    add("str_subscriptions", u"Abonnementer")
    add("str_podcast_directory", u"Podcast-fortegnelser")
    add("str_cleanup", u"Oprydning")

    add("str_help", u"Hjælp")
    add("str_online_help", u"Hjælp på nettet")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Tjek for opdatering...")
    add("str_report_a_problem", u"Indrapportér et problem")
    add("str_goto_website", u"Gå til hjemmesiden")
    add("str_make_donation", u"Donér")
    add("str_menu_license", u"Licens...")
    add("str_about", u"Om...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Fjern valgte punkter")
    add("str_cancel_selected_download", u"Afbryd valgte hentning")
    add("str_pause_selected", u"Sæt valgte i bero")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Ny")
    add("str_dl_state_queued", u"Sat i kø")
    add("str_dl_state_downloading", u"Henter")
    add("str_dl_state_downloaded", u"Hentet")
    add("str_dl_state_cancelled", u"Afbrudt")
    add("str_dl_state_finished", u"Afsluttet")
    add("str_dl_state_partial", u"Delvist hentet")
    add("str_dl_state_clearing", u"Fjerner")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Tjek for nye podcasts")
    add("str_catch_up_mode", u"Indhent - Hent kun de nyeste abonnementer")

    add("str_add_new_feed", u"Tilføj ny kanal");
    add("str_remove_selected_feed", u"Fjern valgte kanal")
    add("str_properties", u"Egenskaber")
    add("str_check_selected_feed", u"Tjek valgte kanal")

    add("str_scheduler_on", u"Tidsstyring - Aktiv")
    add("str_scheduler_off", u"Tidsstyring - Inaktiv")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Næste kørsel:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Henter episode-oplysninger...")
    add("str_no_episodes_found", u"Fandt ingen episoder.")


    ## Directorytab Toolbar
    add("str_refresh", u"Genindlæs")
    add("str_open_all_folders", u"Åbn alle mapper")
    add("str_close_all_folders", u"Luk alle mapper")
    add("str_add", u"Tilføj")

    ## Directorytab Other items
    add("str_directory_description", u"Klik på en kanal i træet eller skriv eller indsæt i feltet ovenfor og klik tilføj.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Vælg en kanal")
    add("str_refresh_cleanup", u"Genindlæs")
    
    add("str_look_in", u"Se efter episoder i")        
    add("str_player_library", u"Afspillerbibliotek")
    add("str_downloads_folder", u"Hentemappe")
    add("str_delete_library_entries", u"Slet biblioteksposter")
    add("str_delete_files", u"Slet filer")
    add("str_select_all_cleanup", u"Vælg alle")
    add("str_delete", u"Slet")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Slet")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Navn")
    add("str_lst_date", u"Dato")        
    add("str_lst_progress", u"Fremgang")
    add("str_lst_state", u"Tilstand")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Placering")
    add("str_lst_episode", u"Episode")
    add("str_lst_playlist", u"Spilleliste")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Abonnerer")
    add("str_disabled", u"Deaktiveret")
    add("str_newly-subscribed", u"Nyt abonnement")
    add("str_unsubscribed", u"Afbrudt abonnement")
    add("str_preview", u"Forhåndsvisning")
    add("str_force", u"Tving")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Vælg et navn til eksportfilen")
    add("str_subs_exported", u"Eksporterede abonnementerne.")
    
    ## Preferences Dialog
    add("str_preferences", u"Indstillinger")
    
    add("str_save", u"Gem")
    add("str_cancel", u"Afbryd")
    
    # General
    add("str_general", u"Generelt")
    add("str_gen_options_expl", u"Sæt %s-programmets generelle indstillinger" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Vis kun %s i systempanelet ved opstart" % PRODUCT_NAME)

    add("str_run_check_startup", u"Tjek for nye podcasts, når programmet startes")
    add("str_play_after_download", u"Afspil filer, så snart de er hentet")
    add("str_location_and_storage", u"Placering og lagerhåndtering")
    add("str_stop_downloading", u"Stop hentning, hvis harddisken når under")
    add("str_bad_megabyte_limit_1", u"Megabyte-grænsen ligner desværre ikke et heltal")
    add("str_bad_megabyte_limit_2", u"Prøv igen.")

    add("str_download_folder", u"Hent podcasts til denne mappe")
    add("str_browse", u"Gennemse")
    add("str_bad_directory_pref_1", u"Vi kunne desværre ikke finde den mappe, du angav")
    add("str_bad_directory_pref_2", u"Opret den og prøv igen.")

    
    # Threading
    add("str_threads", u"Samtidighed")
    add("str_multiple_download", u"Indstillinger for samtidig hentning")
    add("str_max_feedscans", u"samtidige kanalskanninger")
    add("str_max_downloads", u"filer kan hentes samtidig")
   
    # Network settings
    add("str_networking", u"Netværksindstillinger")
    add("str_coralize_urls", u"Coralize URL'er (eksperimentelt)")
    add("str_proxy_server", u"Brug en proxyserver")
    add("str_proxy_address", u"Adresse")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Brugernavn")
    add("str_proxy_password", u"Adgangskode")
    add("str_bad_proxy_pref", u"Du har aktiveret proxyunderstøttelse, men har ikke angivet en proxyserver og -port. Gå tilbage til fanebladet netværksindstillinger og angiv proxyserver og -port.")

    # Player
    add("str_player", u"Afspiller")
    add("str_choose_a_player", u"Vælg en afspiller")
    add("str_no_player", u"Ingen afspiller")
    
    # Advanced
    add("str_advanced", u"Avanceret")
    add("str_options_power_users", u"Disse indstillinger kan bruges af superbrugere")
    add("str_run_command_download", u"Udfør denne kommando, hver gang en fil er hentet")
    add("str_rcmd_full_path", u"%f = Fuld sti til hentet fil")
    add("str_rcmd_podcast_name", u"%n = Podcast-navn")
    add("str_other_advanced_options", u"Andre avancerede indstillinger")
    add("str_show_log", u"Vis log-faneblad i programmet")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titel")
    add("str_url", u"URL")
    add("str_goto_subs", u"Gå til abonnements-fanebladet for at se denne kanals episoder")
    add("str_feed_save", u"Gem")
    add("str_feed_cancel", u"Afbryd")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Aktivér tidsstyring")
    add("str_sched_select_type", u"Vælg mellem tjek på faste tidspunkter eller med faste mellemrum:")
    add("str_check_at_specific_times", u"Tjek på disse faste tidspunkter")
    add("str_check_at_regular_intervals", u"Tjek med jævne mellemrum")
    add("str_repeat_every:", u"Gentag hver:")
    add("str_latest_run", u"Seneste kørsel:")
    add("str_next_run", u"Næste kørsel:")
    add("str_not_yet", u"Ikke endnu")
    #--- Cancel
    add("str_save_and_close", u"Gem og luk")
    #--- Save

    add("str_time_error", u"En af de valgte tidspunkter ser forkert ud. Gyldige tidspunkter ser således ud: 16:43, 10:02am.")


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
    add("str_check_for_new_podcast_button", u"Tjek for nye podcasts ved at trykke på den grønne tjekknap")
    add("str_last_check", u"Sidste tjek blev afsluttet")
    add("str_of", u", u")
    add("str_item", u"punkt")
    add("str_items", u"punkter")
    add("str_downloading", u"henter")
    add("str_downloaded", u"hentet")
    add("str_enclosure", u"episode")
    add("str_enclosures", u"episoder")
    add("str_fetched", u"hentet")
    add("str_loading_mediaplayer", u"Indlæser din medieafspiller...")
    add("str_loaded_mediaplayer", u"Din medieafspiller blev indlæst...")        
    add("str_initialized", u"%s klar" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + " - Podcast-modtager v" + __version__)
    add("str_localization_restart", u"For at oversætte alle %s knapper, skal %s genstartes. Tryk O.k. for at lukke ned, eller afbryd for at fortsætte." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_really_quit", u"Der hentes stadig. Vil du virkelig afslutte?");
    add("str_double_check", u"Det ser ud til at der stadig hentes filer.");
    
    # check for update
    add("str_new_version_ipodder", u"Der er kommet en ny version af %s. Tryk O.k. for at gå til den side, hvorfra den kan hentes." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Denne version af %s behøver ingen opdatering" % PRODUCT_NAME)
    add("str_other_copy_running", u"Der kører en anden kopi af %s. Hent den frem, vent til den er afsluttet, eller dræb den." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Tjek nu")        
    add("str_open_ipodder", u"Åbn %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Skanner kanaler")

    # Feed right-click menu
    add("str_remove", u"Fjern")        
    add("str_open_in_browser", u"Åbn i browser")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Afspil episode i medieafspiller")
    add("str_clear_selected", u"Fjern valgte episoder")
    







