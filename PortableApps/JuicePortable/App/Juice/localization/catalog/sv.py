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

    add("str_set_track_genre", u"Sätt genre till:")
    add("str_auto_delete", u"Ta automatiskt bort avsnitt äldre än")
    add("str_days_old", u"dagar")
    
    add("str_show_notes", u"Visa kommentarer")
    add("str_close", u"Stäng")
    
    add("str_critical_error_minspace_exceeded", \
        u"Nedladdning avbruten: ledigt utrymme (%dMB) mindre " \
        u"än minsta tillåtna (%dMB).")
    add("str_critical_error_unknown", u"Allvarligt okänt fel vid nedladdning.")
    
    add("str_error_checking_new_version", u"Det uppstod tyvärr ett fel vid sökning efter ny version. Var vänlig försök igen senare.")
    add("str_hours", u"timmar")
    add("str_minutes", u"minuter")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Uppdaterar ...")
    add("str_scanned", u"Uppdaterad")
    add("str_feed", u"flöde")
    add("str_feeds", u"flöden")
    
    add("str_downloading_new_episodes", u"Laddar ned nya avsnitt")
    add("str_sched_specific", u"Kontrollera vid specifika tider")
    add("str_sched_reg", u"Kontrollera regelbundet")
    add("str_repeat_every", u"Upprepa varje")
    add("str_next_run_label", u"Nästa:")
    
    add("str_license", u"Detta är en fri programvara; du får omdistribuera och/eller modifiera under reglerna från GNU General Public License, publicerad av Free Software Foundation;  antingen version 2, eller någon senare version. Detta program är distribuerat i hopp om att det ska vara användbart, men utan garanti;  \n\nVi hänvisar till GNU General Public License för mer information.")

    add("str_donate", u"Donera till %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Det är viktigt att hålla gemenskapsägda %s-applikationer online och behålla detta nya sätt att konsumera fri media. Donerade pengar håller vårat team glatt och sporrar oss att jobba på nya funktioner och tjänster." % PRODUCT_NAME)
    add("str_donate_yes", u"Ja, ta mig till donationssidan nu!")
    add("str_donate_two_weeks", u"Jag är inte riktigt säker än; fråga igen om 2 veckor.")
    add("str_donate_already", u"Jag har redan donerat; visa inte den här dialogen igen.")
    add("str_donate_no", u"Nej, jag vill inte donera. Visa inte den här dialogen igen.")
    add("str_donate_one_day", u"Inte nu; fråga om en dag.")
    add("str_donate_proceed", u"Fortsätt")

    add("str_scheduler_dialog", u"Schemaläggare")
    add("str_scheduler_tab", u"Inställningar")

    add("str_select_import_file", u"Välj importeringsfil")    
    add("str_add_feed_dialog", u"Lägg till flöde")
    add("str_edit_feed", u"Flödesegenskaper")

    add("str_really_delete", u"Vill du ta bort")

    add("str_license_caption", u"Licens")

    add("str_ep_downloaded", u"Nedladdad")
    add("str_ep_skipped_removed_other", u"Skippad/Borttagen/AnnatFlöde")
    add("str_dl_state_to_download", u"Väntar på nedladdning")

    add("str_select_none_cleanup", u"Välj ingen")
    add("str_submit_lang", u"Bidra med översättning")
    
    add("str_dltab_live", u"Livenedladdningar: ")
    add("str_dltab_ul_speed", u"Hastighet uppströms: ")
    add("str_dltab_dl_speed", u"Hastighet nedströms: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Akriv")
    add("str_import_opml", u"Importera flöden från OPML ...")
    add("str_export_opml", u"Exportera flöden till OPML...")
    add("str_preferences_menubar", u"Egenskaper ...")
    add("str_close_window", u"Stäng fönster")
    add("str_quit", u"Avsluta")

    add("str_edit", u"Redigera")
    add("str_select_all", u"Markera alla")

    add("str_tools", u"Verktyg")
    add("str_check_all", u"Kontrollera alla")
    add("str_catch_up", u"Kom-ikapp")
    add("str_check_selected", u"Kontrollera markerade")
    add("str_add_feed", u"Lägg till flöde ...")
    add("str_remove_selected", u"Ta bort flöde")
    add("str_feed_properties", u"Flödesegenskaper ...")
    add("str_scheduler_menubar", u"Schemaläggare...")
    
    add("str_select_language", u"Välj språk")

    ## these are also used for the tabs
    add("str_view", u"Visa")
    add("str_downloads", u"Nedladdningar")
    add("str_subscriptions", u"Prenumerationer")
    add("str_podcast_directory", u"Podradiokatalog")
    add("str_cleanup", u"Rensa upp")

    add("str_help", u"Hjälp")
    add("str_online_help", u"Onlinehjälp")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Sök efter nya versioner ...")
    add("str_report_a_problem", u"Rapportera problem")
    add("str_goto_website", u"Gå till webbplatsen")
    add("str_make_donation", u"Donera")
    add("str_menu_license", u"Licens...")
    add("str_about", u"Om...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Ta bort markerade")
    add("str_cancel_selected_download", u"Avbryt markerad nedladdning")
    add("str_pause_selected", u"Pausa markerad")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Ny")
    add("str_dl_state_queued", u"Köad")
    add("str_dl_state_downloading", u"Laddar ned")
    add("str_dl_state_downloaded", u"Nedladdad")
    add("str_dl_state_cancelled", u"Avbruten")
    add("str_dl_state_finished", u"Färdig")
    add("str_dl_state_partial", u"Halvt nedladdad")
    add("str_dl_state_clearing", u"Rensar")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Uppdatera flöden")
    add("str_catch_up_mode", u"Kom-ikapp - Ladda bara ned de senaste avsnitten")

    add("str_add_new_feed", u"Lägg till flöde");
    add("str_remove_selected_feed", u"Ta bort markerat flöde")
    add("str_properties", u"Egenskaper")
    add("str_check_selected_feed", u"Kontrollera markerat flöde")

    add("str_scheduler_on", u"Schemaläggare - På")
    add("str_scheduler_off", u"Schemaläggare - Av")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Nästa:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Söker info ...")
    add("str_no_episodes_found", u"Inga nya avsnitt.")


    ## Directorytab Toolbar
    add("str_refresh", u"Uppdatera")
    add("str_open_all_folders", u"Öppna alla kataloger")
    add("str_close_all_folders", u"Stäng alla kataloger")
    add("str_add", u"Lägg till")

    ## Directorytab Other items
    add("str_directory_description", u"Klicka på ett flöde i trädet eller ange det ovan och klicka på Lägg till.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Markera ett flöde")
    add("str_refresh_cleanup", u"Uppdatera")
    
    add("str_look_in", u"Kontrollera efter avsnitt i")        
    add("str_player_library", u"Spelarkatalog")
    add("str_downloads_folder", u"Nedladdatkatalogen")
    add("str_delete_library_entries", u"Ta bort katalogfiler")
    add("str_delete_files", u"Ta bort filer")
    add("str_select_all_cleanup", u"Markera alla")
    add("str_delete", u"Ta bort")




    ## Logtab items
    add("str_log", u"Logg")
    add("str_clear", u"Rensa")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Titel")
    add("str_lst_date", u"Datum")        
    add("str_lst_progress", u"Förlopp")
    add("str_lst_state", u"Status")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Plats")
    add("str_lst_episode", u"Avsnitt")
    add("str_lst_playlist", u"Radio")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Prenumererad")
    add("str_disabled", u"Avstängd")
    add("str_newly-subscribed", u"Nyligen prenumererad")
    add("str_unsubscribed", u"Oprenumererad")
    add("str_preview", u"Förhandsvisa")
    add("str_force", u"Tvinga")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Välj ett namn för exportfilen")
    add("str_subs_exported", u"Prenumerationer exporterade.")
    
    ## Preferences Dialog
    add("str_preferences", u"Egenskaper")
    
    add("str_save", u"Spara")
    add("str_cancel", u"Avbryt")
    
    # General
    add("str_general", u"Allmänt")
    add("str_gen_options_expl", u"Ändra allmäna inställningar för %sapplikationer." % PRODUCT_NAME)
    add("str_hide_on_startup", u"Visa %s endast i meddelandefältet vid uppstart." % PRODUCT_NAME)

    add("str_run_check_startup", u"Kontrollera podradiostationer vid start")
    add("str_play_after_download", u"Spela avsnitt direkt efter nedladdning")
    add("str_location_and_storage", u"Plats- och sparningsinställningar")
    add("str_stop_downloading", u"Avbryt nedladdningar om hårddiskutrymmet underskrider")
    add("str_bad_megabyte_limit_1", u"Begränsningen måste vara ett heltal.")
    add("str_bad_megabyte_limit_2", u"Var vänlig försök igen.")

    add("str_download_folder", u"Spara avsnitt till denna katalog")
    add("str_browse", u"Bläddra")
    add("str_bad_directory_pref_1", u"Kan inte hitta katalog")
    add("str_bad_directory_pref_2", u"Var vänlig att skapa den och försök igen.")

    
    # Threading
    add("str_threads", u"Aktiviteter")
    add("str_multiple_download", u"Akitivtetsinställnigar")
    add("str_max_feedscans", u"flödeskontroller åt gången")
    add("str_max_downloads", u"nedladdningar åt gången")
   
    # Network settings
    add("str_networking", u"Nätverksinställningar")
    add("str_coralize_urls", u"Använd proxytjänst för URL (rekommenderas inte)")
    add("str_proxy_server", u"Använd proxyserver")
    add("str_proxy_address", u"Adress")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Användarnamn")
    add("str_proxy_password", u"Lösenord")
    add("str_bad_proxy_pref", u"Du har valt att använda en proxyserver, men glömde att ange en värd och port.  Var vänlig återgå till Nätverksinställningar och ange en värd och port för proxyservern.")

    # Player
    add("str_player", u"Spelare")
    add("str_choose_a_player", u"Välj en spelare")
    add("str_no_player", u"Ingen spelare")
    
    # Advanced
    add("str_advanced", u"Avancerat")
    add("str_options_power_users", u"Dessa inställningar bör endast ändras av experter")
    add("str_run_command_download", u"Kör detta kommando efter varje nedladdning")
    add("str_rcmd_full_path", u"%f = Full sökväg till nedladdad fil")
    add("str_rcmd_podcast_name", u"%n = Podradions namn")
    add("str_other_advanced_options", u"Övrigt")
    add("str_show_log", u"Visa logg-flik")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titel")
    add("str_url", u"URL")
    add("str_goto_subs", u"Gå till prenumerationsfliken för att se denna podradios avsnitt")
    add("str_feed_save", u"Spara")
    add("str_feed_cancel", u"Avbryt")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Använd schemaläggare")
    add("str_sched_select_type", u"Justera för att automatiskt kontrollera vid specifika eller regelbundna tider:")
    add("str_check_at_specific_times", u"Kontrollera vid specfika tider")
    add("str_check_at_regular_intervals", u"Kontrollera regelbundet")
    add("str_repeat_every:", u"Upprepa varje:")
    add("str_latest_run", u"Senaste:")
    add("str_next_run", u"Nästa:")
    add("str_not_yet", u"Inte än")
    #--- Cancel
    add("str_save_and_close", u"Spara och stäng")
    #--- Save

    add("str_time_error", u"En av de schemalagda tiderna verkar vara felaktigt. Kontrollera tiderna och försök igen.")


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
    add("str_check_for_new_podcast_button", u"Kontrollera efter nya avsnitt genom att klicka på den gröna kontrollknappen")
    add("str_last_check", u"Senaste kontroll")
    add("str_of", u"av")
    add("str_item", u"fil")
    add("str_items", u"filer")
    add("str_downloading", u"laddar ned")
    add("str_downloaded", u"nedladdad")
    add("str_enclosure", u"bifogning")
    add("str_enclosures", u"bifogningar")
    add("str_fetched", u"mottagen")
    add("str_loading_mediaplayer", u"Laddar mediaspelare ...")
    add("str_loaded_mediaplayer", u"Mediaspelare laddad...")        
    add("str_initialized", u"%s klar" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podradiomottagare v" + __version__)
    add("str_localization_restart", u"För att alla inställningar ska uppdateras krävs en omstart. Klicka Ok för att stänga ned eller avbryt för att fortsätta.")
    add("str_really_quit", u"Du har en pågående nedladdning.  Vill du verkligen avsluta?");
    add("str_double_check", u"Det verkar som att du har en pågående nedladdning.");
    
    # check for update
    add("str_new_version_ipodder", u"En ny version av %s finns tillgänglig - tryck Ok för att gå till sajten." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Du har den senaste versionen")
    add("str_other_copy_running", u"En annan instans av %s körs. Var vänlig avsluta den först." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Kontrollera nu")        
    add("str_open_ipodder", u"Öppna %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Kontrollerar flöden")

    # Feed right-click menu
    add("str_remove", u"Ta bort")        
    add("str_open_in_browser", u"Öppna i webbläsaren")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Spela upp")
    add("str_clear_selected", u"Rensa markerade avsnitt")
    



