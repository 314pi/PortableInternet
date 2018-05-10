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



    add("str_error_checking_new_version", u"Es tut uns leid, aber es gab ein Problem beim Überprüfen auf eine neue Version. Bitte versuchen Sie es später noch einmal.")
    add("str_hours", u"Stunden")
    add("str_minutes", u"Minuten")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Durchsuchen")
    add("str_scanned", u"Durchsucht")
    add("str_feed", u"Feed")
    add("str_feeds", u"Feeds")
    
    add("str_downloading_new_episodes", u"Download neuer Episoden")
    add("str_sched_specific", u"Zu bestimmten Zeiten checken")
    add("str_sched_reg", u"In regelmäßigen Intervallen checken")
    add("str_repeat_every", u"Wiederholen alle")
    add("str_next_run_label", u"Nächster Lauf:")
    
    add("str_license", u"This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.")

    add("str_donate", u"Für %s spenden" % PRODUCT_NAME)
    add("str_donate_expl", u"Es ist wichtig, diese der Allgemeinheit gehörenden, auf %s basierenden Programme frei für alle zur Verfügung stellen zu können, denn jeder soll die Möglichkeit haben, auf diese neue Art Audio, Video und mehr nutzen zu können. Jeder Betrag macht das Team glücklich und motiviert die Teilnehmer, für Sie an neuen Features und Diensten zu arbeiten!" % PRODUCT_NAME)
    add("str_donate_yes", u"Ja, ich möchte jetzt die Spenden-Seite besuchen!")
    add("str_donate_two_weeks", u"Ich möchte die Software noch weiter testen, bitte erinnere mich in 2 Wochen wieder")
    add("str_donate_already", u"Ich habe bereits gespendet, zeige diesen Dialog nicht wieder an.")
    add("str_donate_no", u"No, Ich will nicht spenden, zeige diesen Dialog nicht wieder an.")
    add("str_donate_one_day", u"Nicht jetzt, aber erinnere mich in einem Tag")
    add("str_donate_proceed", u"Fortfahren")

    add("str_scheduler_dialog", u"Terminplaner")
    add("str_scheduler_tab", u"Einstellungen")

    add("str_select_import_file", u"Import-Datei auswählen")    
    add("str_add_feed_dialog", u"Feed hinzufügen")
    add("str_edit_feed", u"Feed-Eigenschaften")

    add("str_really_delete", u"Wirklich löschen")

    add("str_menu_license", u"Lizenz...")
    add("str_license_caption", u"Lizenz")

    add("str_ep_downloaded", u"Heruntergeladen")
    add("str_ep_skipped_removed_other", u"Übersprungen/Entfernt/AndererFeed")
    add("str_dl_state_to_download", u"Noch herunterzuladen")

    add("str_select_none_cleanup", u"Nichts auswählen")
    add("str_submit_lang", u"Eine weitere Sprache hinzufügen")
    
    add("str_dltab_live", u"Aktive Downloads: ")
    add("str_dltab_ul_speed", u"Upload-Geschwindigkeit: ")
    add("str_dltab_dl_speed", u"Download-Geschwindigkeit: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________



    ## File menu
    add("str_file", u"Datei")
    add("str_import_opml", u"Feeds aus OPML importieren")
    add("str_export_opml", u"Feeds als OPML exportieren")
    add("str_preferences_menubar", u"Einstellungen...")
    add("str_close_window", u"Fenster schließen")
    add("str_quit", u"Beenden")

    add("str_edit", u"Bearbeiten")
    add("str_select_all", u"Alles auswählen")

    add("str_tools", u"Werkzeuge")
    add("str_check_all", u"Alle Feeds überprüfen")
    add("str_catch_up", u"Nur letzten Eintrag laden (Catch-Up)")
    add("str_check_selected", u"Ausgewählte Feeds überprüfen")
    add("str_add_feed", u"Hinzufügen Feed ...")
    add("str_remove_selected", u"Feed entfernen")
    add("str_feed_properties", u"Feed-Eigenschaften")
    add("str_scheduler_menubar", u"Terminplaner...")

    add("str_select_language", u"Sprache auswählen")

    ## these are also used for the tabs
    add("str_view", u"Fenster")
    add("str_downloads", u"Downloads")
    add("str_subscriptions", u"Abonnierte Feeds")
    add("str_podcast_directory", u"Podcast-Verzeichnis")
    add("str_cleanup", u"Aufräumen")

    add("str_help", u"Hilfe")
    add("str_online_help", u"Online-Hilfe")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Auf Aktualisierung prüfen")
    add("str_report_a_problem", u"Problem melden")
    add("str_goto_website", u"Gehe zur Webseite")
    add("str_make_donation", u"%s unterstützen" % PRODUCT_NAME)
    add("str_about", u"Info/Über")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Selektierte Einträge entfernen")
    add("str_cancel_selected_download", u"Selektierte Downloads abbrechen")
    add("str_pause_selected", u"Selektierte Downloads anhalten")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Neu")
    add("str_dl_state_queued", u"Queue")
    add("str_dl_state_downloading", u"Lädt")
    add("str_dl_state_downloaded", u"Heruntergeladen")
    add("str_dl_state_cancelled", u"Abgebrochen")
    add("str_dl_state_finished", u"Fertig")
    add("str_dl_state_partial", u"Teilweise heruntergeladen")
    add("str_dl_state_clearing", u"Säubern")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Auf neue Podcasts prüfen")
    add("str_catch_up_mode", u"Catch-up - nur den jeweils neuesten Eintrag herunterladen")

    add("str_add_new_feed", u"Feed hinzufügen")
    add("str_remove_selected_feed", u"Feed entfernen")
    add("str_properties", u"Feed-Eigenschaften")
    add("str_check_selected_feed", u"Feed überprüfen")

    add("str_scheduler_on", u"Terminplaner - An")
    add("str_scheduler_off", u"Terminplaner - Aus")

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Nächster Lauf:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Lädt Episoden-Information")
    add("str_no_episodes_found", u"Keine Episoden gefunden.")


    ## Directorytab Toolbar
    add("str_refresh", u"Aktualisieren")
    add("str_open_all_folders", u"Alle Ordner öffnen")
    add("str_close_all_folders", u"Schließen aller Ordner")
    add("str_add", u"Hinzufügen")

    ## Directorytab Other items
    add("str_directory_description", u"Klicken Sie auf einen Feed in dem Baum, oder geben Sie ihn ein in das obige Feld. Wählen Sie dann hinzufügen.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Einen Feed auswählen")
    add("str_refresh_cleanup", u"Aktualisieren")

    add("str_look_in", u"Nach Episoden schauen in ")
    add("str_player_library", u"Medienbibliothek des Players")
    add("str_downloads_folder", u"Ordner für Downloads")
    add("str_delete_library_entries", u"Lösche Medienbibliothek-Einträge")
    add("str_delete_files", u"Lösche Dateien")
    add("str_select_all_cleanup", u"Alles auswählen")
    add("str_delete", u"Löschen")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Log löschen")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Name")
    add("str_lst_date", u"Datum")
    add("str_lst_progress", u"Fortschritt")
    add("str_lst_state", u"Status")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Pfad")
    add("str_lst_episode", u"Episode")
    add("str_lst_playlist", u"Playlist")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Abonniert")
    add("str_disabled", u"inaktiv")
    add("str_newly-subscribed", u"Neu abonniert")
    add("str_unsubscribed", u"Abbestellt")
    add("str_preview", u"Vorschau")
    add("str_force", u"Erzwingen")


    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________


    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Namen für Export-Datei auswählen")
    add("str_subs_exported", u"Feed-Liste exportiert.")

    ## Preferences Dialog
    add("str_preferences", u"Einstellungen")
    add("str_save", u"Speichern")
    add("str_cancel", u"Abbrechen")

    # General
    add("str_general", u"Allgemein")
    add("str_gen_options_expl", u"Generelle Einstellungen für %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Nach dem Start in Systemtray minimieren")

    add("str_run_check_startup", u"Beim Start auf neue Episoden überprüfen")
    add("str_play_after_download", u"Spiele Downloads ab, sobald sie fertig geladen sind")
    add("str_location_and_storage", u"Ablagepfad-Verwaltung")
    add("str_stop_downloading", u"Herunterladen abbrechen, wenn freier Platz auf der Festplatte folgenden Wert unterschreitet")
    add("str_bad_megabyte_limit_1", u"Leider keine gültige ganze Zahl")
    add("str_bad_megabyte_limit_2", u"Bitte noch einmal versuchen.")

    add("str_download_folder", u"Podcasts in diesem Ordner speichern")
    add("str_browse", u"Durchsuchen")
    add("str_bad_directory_pref_1", u"Leider konnten das angegebene Verzeichnis nicht gefunden werden.")
    add("str_bad_directory_pref_2", u"Bitte anlegen und es danach noch einmal versuchen.")


    # Threading
    add("str_threads", u"Threading")
    add("str_multiple_download", u"Einstellungen für gleichzeitige Downloads")
    add("str_max_feedscans", u"maximale Anzahl gleichzeitiger Zugriffe für Feed lesen")
    add("str_max_downloads", u"maximale Anzahl gleichzeitiger Downloads pro Session")

    # Network settings
    add("str_networking", u"Netzwerk-Einstellungen")
    add("str_coralize_urls", u"Coralize URLs (experimental)")
    add("str_proxy_server", u"Proxyserver verwenden")
    add("str_proxy_address", u"Adresse")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Username")
    add("str_proxy_password", u"Passwort")
    add("str_bad_proxy_pref", u"Sie haben den Proxy-Support aktiviert, aber leider keinen Proxy-Server bzw. Port angegeben. Bitte gehen Sie zurück zu den Netzwerk-Einstellungen und füllen Sie diese Felder.")

    # Player
    add("str_player", u"Medien-Player")
    add("str_choose_a_player", u"Medien-Player auswählen")
    add("str_no_player", u"Kein Player")

    # Advanced
    add("str_advanced", u"Erweitert")
    add("str_options_power_users", u"Diese Optionen können von Power-Usern verwendet werden")
    add("str_run_command_download", u"Diesen Befehl nach jedem Download starten")
    add("str_rcmd_full_path", u"%f = kompletter Pfad zur heruntergeladenen Datei")
    add("str_rcmd_podcast_name", u"%n = Name des Podcasts")
    add("str_other_advanced_options", u"Mehr erweiterte Einstellungen")
    add("str_show_log", u"Eigenes Tab für Log anzeigen")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titel")
    add("str_url", u"URL")
    add("str_goto_subs", u"Gehe zu Abonnements um die Eigenschaften dieses Feeds zu sehen")
    add("str_feed_save", u"Speichern")
    add("str_feed_cancel", u"Abbrechen")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Aktiviere Terminplaner")
    add("str_sched_select_type", u"Wann soll der Terminplaner auf Aktualisirungen prüfen:")
    add("str_check_at_specific_times", u"Zu festen Uhrzeiten")
    add("str_check_at_regular_intervals", u"in regelmäßigen Intervallen")
    add("str_repeat_every:", u"Wiederholen alle")
    add("str_latest_run", u"Letzter Lauf:")
    add("str_next_run", u"Nächster Lauf:")
    add("str_not_yet", u"Noch nicht")
    #--- Cancel
    add("str_save_and_close", u"Speichern und Schließen")
    #--- Save

    add("str_time_error", u"Eine der angegebenen Zeiten ist falsch, gültige Zeiten sehen so aus 16:43, 10:02am.")

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
    #--- Programming: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDesign: Martijn Venrooy\nContent strategist: Mark Alexander Posth\nConcept: Adam Curry, Dave Winer\nThanks to all translators for their commitments!\n\nBased on Feedparser and BitTorrent technology.\nThis program is free software you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.




    ## Statusbar items
    add("str_check_for_new_podcast_button", u"Drücken Sie auf den grünen Button, um auf neue Podcast zu überprüfen")
    add("str_last_check", u"Letze Überprüfung beendet am")
    add("str_of", u"von")
    add("str_item", u"Einträgen")
    add("str_items", u"Einträgen")
    add("str_downloading", u"herunterladen")
    add("str_downloaded", u"heruntergeladen")
    add("str_enclosure", u"Enclosure")
    add("str_enclosures", u"Enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"Media-Player laden ...")
    add("str_loaded_mediaplayer", u"Media-Player geladen ...")
    add("str_initialized", u"%s ist bereit" % PRODUCT_NAME)


    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast-Lader v" + __version__)
    add("str_localization_restart", u"Um alle Einstellungen zu lokalisieren, ist ein Neustart von %s notwendig. Klicken Sie OK um %s zu beenden, Abbrechen um weiterzuarbeiten." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_really_quit", u"Mindestens ein Download ist aktiv.  Wirklich beenden?");
    add("str_double_check", u"Ein Download findet bereits statt.");

    # check for update
    add("str_new_version_ipodder", u"Es ist eine neue Version von %s verfügbar, drücken Sie OK, um auf die Webseite zu wechseln." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Ihre %s-Version ist die aktuelleste!" % PRODUCT_NAME)
    add("str_other_copy_running", u"Eine andere Instanz von %s ist bereits gestartet. Bitte verwenden Sie diese, warten Sie darauf daß es erscheint oder beenden Sie den Prozeß." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Jetzt überprüfen")
    add("str_open_ipodder", u"%s öffnen" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Feeds überprüfen")

    # Feed right-click menu
    add("str_remove", u"Entfernen")
    add("str_open_in_browser", u"In Browser öffnen")

    # Downloads right-click menu
    add("str_play_episode", u"Episode abspielen")
    add("str_clear_selected", u"Selektierte Einträge löschen")




