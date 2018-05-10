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
    ## We can easily throw them to the translators that way.
    #############################################

    ##_________________________________________________________
    ##
    ##     New strings
    ##_________________________________________________________


    add("str_downloading_new_episodes", "Nieuwe afleveringen aan het downloaden...")
       
    add("str_dltab_live", "Huidig aantal downloads: ")
    add("str_dltab_ul_speed", "Upload snelheid: ")
    add("str_dltab_dl_speed", "Download snelheid: ")

    add("str_error_checking_new_version", u"Helaas was er een storing terwijl er een controle voor een nieuwe versie werd gedaan. Probeert u het later nog een keer alstublieft.")
    add("str_hours", "uren")
    add("str_minutes", "minuten")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", "Zoeken")
    add("str_scanned", "Gezocht")
    add("str_feed", "feed")
    add("str_feeds", "feeds")
    



    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", "Bestand")
    add("str_import_opml", "Importeer feeds van opml...")
    add("str_export_opml", "Exporteer feeds naar opml...")
    add("str_preferences_menubar", "Voorkeuren...")
    add("str_close_window", "Sluit Venster")
    add("str_quit", "Afsluiten")

    add("str_edit", "Bewerk")
    add("str_select_all", "Selecteer alles")

    add("str_tools", "Acties")
    add("str_check_all", "Controleer alles")
    add("str_catch_up", "Bijwerken")
    add("str_check_selected", "Markeer geselecteerde")
    add("str_add_feed", "Voeg Feed toe...")
    add("str_remove_selected", "Verwijder Feed")
    add("str_feed_properties", "Feed eigenschappen...")
    add("str_scheduler_menubar", "Rooster...")

    add("str_select_language", "Selecteer taal")
    add("str_submit_lang", "Voeg een taal toe")

    ## these are also used for the tabs
    add("str_view", "Beeld")
    add("str_downloads", "Downloads")
    add("str_subscriptions", "Abonnementen")
    add("str_podcast_directory", "Podcast adresboek")
    add("str_cleanup", "Opruimen")

    add("str_help", "Help")
    add("str_online_help", "Online Help")
    add("str_faq", "Veelgestelde Vragen")
    add("str_check_for_update", "Zoek naar een update...")
    add("str_report_a_problem", "Rapporteer een probleem")
    add("str_goto_website", "Ga naar de website")
    add("str_make_donation", "Maak een donatie")
    add("str_menu_license", "Licentie...")
    add("str_about", "Over...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", "Verwijder geselecteerde items")
    add("str_cancel_selected_download", "Annuleer geselecteerde download")
    add("str_pause_selected", "Pauseer geselecteerde items")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", "Nieuw")
    add("str_dl_state_queued", "In de wacht")
    add("str_dl_state_downloading","Downloading")
    add("str_dl_state_downloaded","Gedownload")
    add("str_dl_state_cancelled", "Geannuleerd")
    add("str_dl_state_finished", "Afgerond")
    add("str_dl_state_partial", "Gedeeltelijk gedownload")
    add("str_dl_state_clearing", "Ophelderen")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", "Zoek naar nieuwe afleveringen")
    add("str_catch_up_mode", "Catch-up - Download alleen de laatste nieuwe afleveringen")

    add("str_add_new_feed", "Voeg een nieuwe feed toe");
    add("str_remove_selected_feed", "Verwijder geselecteerde feed")
    add("str_properties", "Eigenschappen")
    add("str_check_selected_feed", "Controleer geselecteerde feed")

    add("str_scheduler_on", "Rooster - Aan")
    add("str_scheduler_off", "Rooster - Uit")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", "Volgende sessie:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", "Informatie wordt opgehaald...")
    add("str_no_episodes_found", "Geen afleveringen gevonden.")


    ## Directorytab Toolbar
    add("str_refresh", "Vernieuwen")
    add("str_open_all_folders", "Open alle folders")
    add("str_close_all_folders", "Sluit alle folders")
    add("str_add", "Toevoegen")

    ## Directorytab Other items
    add("str_directory_description", "Klik op een feed in de boom of typ/plak de feed in de ruimte hierboven, klik daarna op toevoegen.")




    ## Cleanuptab items
    add("str_select_a_feed", "Selecteer een feed")
    add("str_refresh_cleanup", "Vernieuwen")
    
    add("str_look_in", "Voor afleveringen kijk in")        
    add("str_player_library", "Media speler bibliotheek")
    add("str_downloads_folder", "Download folder")
    add("str_delete_library_entries", "Verwijder verwijzingen")
    add("str_delete_files", "Verwijder bestanden")
    add("str_select_all_cleanup", "Selecteer alles")
    add("str_select_none_cleanup", "Deselecteer alles")
    add("str_delete", "Verwijder")




    ## Logtab items
    add("str_log", "Log")
    add("str_clear", "Wissen")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", "Naam")
    add("str_lst_date", "Datum")        
    add("str_lst_progress", "Progressie")
    add("str_lst_state", "Status")
    add("str_lst_mb", "MB")
    add("str_lst_location", "Locatie")
    add("str_lst_episode", "Aflevering")
    add("str_lst_playlist", "Speellijst")

    ## Episode states
    add("str_ep_downloaded", "Gedownload")
    add("str_ep_skipped_removed_other", "Overgeslagen/Verwijderd/Anders")
    add("str_dl_state_to_download", "Klaar voor Download")


    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed","Aangemeld")
    add("str_disabled", "Onbruikbaar")
    add("str_newly-subscribed", "Nieuw Aangemeld")
    add("str_unsubscribed", "Afgemeld")
    add("str_preview", "Vooruitblik")
    add("str_force", "Forceren")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    add("str_select_import_file", "Selecteer import bestand")

    ## OPML Export Dialog
    add("str_choose_name_export_file", "Geef een naam voor het export bestand")
    add("str_subs_exported", "Subscripties geexporteerd.")
    
    ## Preferences Dialog
    add("str_preferences", "Voorkeuren")
    add("str_save", "Opslaan")
    add("str_cancel", "Annuleren")

    # General
    add("str_general", "Algemeen")
    add("str_gen_options_expl", "Algmeme opties voor de %s applicatie" % PRODUCT_NAME)
    add("str_hide_on_startup", "Toon %s alleen in de sytem tray bij een opstart" % PRODUCT_NAME)

    add("str_run_check_startup", "Zoek direct naar nieuwe afleveringen als de applicatie is opgestart")
    add("str_play_after_download", "Speel de afleveringen nadat ze zijn gedownload")
    add("str_location_and_storage", "Locatie en opslag management")
    add("str_stop_downloading", "Stop met downloaden als de harde schijf minimaal dit bereikt:")
    add("str_bad_megabyte_limit_1", "Sorry, de opgegeven waarde is geen rond getal")
    add("str_bad_megabyte_limit_2", "Probeer het nogmaals.")

    add("str_download_folder", "Download afleveringen in deze folder")
    add("str_browse", "Bladeren")
    add("str_bad_directory_pref_1", "Sorry, we konden de opgegeven locatie niet vinden")
    add("str_bad_directory_pref_2", "Maak deze locatie eerst aan en probeer het opnieuw.")


    # Threading
    add("str_threads", "Threading")
    add("str_multiple_download", "Multiple download opties")
    add("str_max_feedscans", "feedscans per sessie maximaal")
    add("str_max_downloads", "downloads per sessie maximaal")
   
    # Network settings
    add("str_networking", "Netwerk opties")
    add("str_coralize_urls", "Coralize URLs (experimenteel)")
    add("str_proxy_server", "Gebruik een proxyserver")
    add("str_proxy_address", "Adres")
    add("str_proxy_port", "Poort")
    add("str_proxy_username", "Gebruikersnaam")
    add("str_proxy_password", "Wachtwoord")
    add("str_bad_proxy_pref", "Je hebt proxy ondersteuning aangezet maar nog geen proxy host en poort ingevuld. Ga naar de Netwerk opties tab en vul de proxy host en poort in.")

    # Player
    add("str_player", "Media speler")
    add("str_choose_a_player", "Kies een media speler")
    add("str_no_player", "Geen media speler")
    
    # Advanced
    add("str_advanced", "Geavanceerd")
    add("str_options_power_users", "Deze opties kunnen gebruikt worden door Power Users")
    add("str_run_command_download", "Run dit commando na elke download")
    add("str_rcmd_full_path", "%f = Volledig path naar gedownload bestand")
    add("str_rcmd_podcast_name", "%n = Podcast naam")
    add("str_other_advanced_options", "Andere geavanceerde opties")
    add("str_show_log", "Toon de log tab in de applicatie")



    ## Feed Dialog (add/properties)
    add("str_add_feed_dialog", "Voeg een Feed toe")
    add("str_edit_feed", "Feed eigenschappen")
    add("str_title", "Titel")
    add("str_url", "URL")
    add("str_goto_subs","Ga naar de abonnementen tab om direct de afleveringen te zien")
    add("str_feed_save", "Opslaan")
    add("str_feed_cancel", "Annuleren")

    ## Remove Feed dialog
    add("str_really_delete", "Verwijder")


    ## Scheduler Dialog
    add("str_scheduler_dialog", "Rooster")
    add("str_scheduler_tab", "Opties")
    add("str_enable_scheduler", "Activeer rooster")
    add("str_sched_select_type", "Controleer op specifieke tijden of op interval:")
    add("str_sched_specific", "Op deze specifieke tijden")
    add("str_sched_reg", "Op deze interval")
    add("str_repeat_every", "Herhaal elke:")
    add("str_latest_run", "Laatste sessie:")
    add("str_next_run", "Volgende sessie:")
    add("str_not_yet", "--")

    add("str_time_error","Een of meerdere ingeroosterde tijden lijken niet goed te zijn. Valide tijden zien er zo uit: 10:02am, 16:43.")


    ## Donations Dialog
    add("str_donate", "Doneer %s" % PRODUCT_NAME)
    add("str_donate_expl", "Het is belangrijk om de %s applicatie publiekelijk te houden om deze manier van media consumptie ongebonden te houden. Elk bedrag dat u wilt doneren wordt zeer gewaardeerd door het team." % PRODUCT_NAME)
    add("str_donate_yes", "Ja, ga direct door naar de donatie pagina!")
    add("str_donate_two_weeks", "Ik wil eerst het programma beter leren kennen, toon dit in twee weken weer")
    add("str_donate_already", "Ik heb al gedoneerd, laat dit venster niet meer zien")
    add("str_donate_no", "Nee, ik wil niet doneren, laat dit venster niet meer zien")
    add("str_donate_one_day", "Niet op dit moment, toon dit venster morgen opnieuw!")
    add("str_donate_proceed", "Doorvoeren")





    ## License Dialog
    add("str_license_caption", "Licentie")
    add("str_license", "Dit Programma is vrije software; U kan het verspreiden en/of wijzigen onder de bepalingen van de GNU Algemene Publieke Licentie, zoals uitgegeven door de Free Software Foundation; oftewel versie 2 van de Licentie,of (naar vrije keuze) een latere versie. ")




    ## Statusbar items
    add("str_check_for_new_podcast_button", "Zoek naar nieuwe afleveringen door op de groene knop te klikken")
    add("str_last_check", "Laatste controle gedaan op")
    add("str_of", "van")
    add("str_item", "item")
    add("str_items", "items")
    add("str_downloading", "downloaden")
    add("str_downloaded", "gedownload")
    add("str_enclosure", "aflevering")
    add("str_enclosures", "afleveringen")
    add("str_fetched", "binnengehaald")
    add("str_loading_mediaplayer", "Media speler wordt opgestart...")
    add("str_loaded_mediaplayer", "Media speler is opgestart...")        
    add("str_initialized", "Klaar")




    ## Other application strings
    add("str_ipodder_title", "%s - Podcast receiver v" % PRODUCT_NAME + __version__)
    add("str_localization_restart", "Om van taal te veranderen is een herstart nodig. Klik op OK om deze applicatie af te sluiten.")
    add("str_really_quit", "Er worden nog afleveringen gedownload.  Weet u zeker dat u wil afsluiten?");
    add("str_double_check", "Er wordt reeds een download uitgevoerd.");
    
    # check for update
    add("str_new_version_ipodder", "Een nieuwere versie van %s is aanwezig, druk op Ok op naar de downloadpagina te gaan." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", "Deze versie van %s is up-to-date!" % PRODUCT_NAME)
    add("str_other_copy_running", "U heeft reeds een andere versie draaien. Sluit die eerst af.")

    # Windows taskbar right-click menu
    add("str_check_now","Controleer nu")        
    add("str_open_ipodder","Open %s" % PRODUCT_NAME)
    #--- Downloaden
    add("str_scanning_feeds", "Abonnementen aan het scannen")

    # Feed right-click menu
    add("str_remove","Verwijder")        
    add("str_open_in_browser","Open in een browser")        

    # Downloads right-click menu
    add("str_play_episode", "Beluister aflevering in mijn media speler")
    add("str_clear_selected", "Verwijder geselecteerde items")
    



