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

    add("str_txt_feedmanager", u"Kompatybilne feed managery :")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Szukanie podcastów, subskrypcja jednym kliknięciem.")

    add("str_open_downloads_folder", u"Otwórz folder Ściągnięte")
    add("str_chkupdate_on_startup", u"Prze starcie sprawdzaj czy sa dostępne nowe wersje aplikacji.")
    add("str_bad_feedmanager_url", u"Wprowadz poprawny URL dla feed managera.")
    add("str_feed_manager", u"Feed manager")
    add("str_feedmanager_enable", u"Zsynchronizuj moje subskrypcje ze zdalną usługą")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"Ustaw rodzaj utworu na")
    add("str_auto_delete", u"Automatycznie kasuj epizody starsze niż")
    add("str_days_old", u"dni")
    
    add("str_show_notes", u"Pokaż Notes")
    add("str_close", u"Zamknij")
    
    add("str_critical_error_minspace_exceeded", \
        u"Ściąganie wstrzymane; Na twardym dysku zostało %dMB wolnego " \
        u"miejsca. Minimum określiłeś na %dMB.  Zwolnij miejsce na " \
        u"dysku używając opcji Czyszczenie " \
        u"lub zmień ustawienia")
    add("str_critical_error_unknown", u"Nieznany bład krytyczny przy ściąganiu.")
    
    add("str_error_checking_new_version", u"Przepraszamy, ale wystąpił problem ze sprawdzeniem czy sa dostępne nowe wersje. Prosimy spróbować później.")
    add("str_hours", u"godzin")
    add("str_minutes", u"minut")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Skanowanie")
    add("str_scanned", u"Przeskanowane")
    add("str_feed", u"feed")
    add("str_feeds", u"feed'y")
    
    add("str_downloading_new_episodes", u"Sciaganie nowych epizodów")
    add("str_sched_specific", u"Sprawdzaj w określonym czasie")
    add("str_sched_reg", u"Sprawdzaj w regularnych odstępach")
    add("str_repeat_every", u"Powtarzaj co")
    add("str_next_run_label", u"Następny raz:")
    
    add("str_license", u"Ten program jest darmowy; możesz go redystrybuować i/lub modyfikować na zasadach Licencji GNU General Public jako publikacje Free Software Foundation; na podstawie drugiej wersji Licencji, lub (jeśli wolisz) jakiejkolwiek późniejszej wersji. Ten program jest dystrybuowany z przekonaniem, że będzie pomocny, ale niestety nie możemy udzielać na niego jakiejkolwiek gwarancji. \n\nZobacz Licencje GNU General Public by dowiedzieć się szczegółów.")

    add("str_donate", u"Wspomórz %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Jest ważnym, by utrzymać program %s przy życiu i tymsamym popierać wolność słowa w Internecie. Jakakolwiek kwota pieniędzy sprawi, że twórcy programu będa szczęśliwi i zdopingowani do pracy nad nowymi funkcjami programu!" % PRODUCT_NAME)
    add("str_donate_yes", u"Tak, skieruj mnie do strony gdzie będę mógł finansowo wesprzeć ten projekt!")
    add("str_donate_two_weeks", u"Potrzebuje więcej czasu na sprawdzenie programu, pokaż ten komunikat za 2 tygodnie")
    add("str_donate_already", u"Już wsparłem finansowo ten projekt, więcej nie pokazuj tego okna")
    add("str_donate_no", u"Nie chce wam pomagać, więcej nie pokazuj tego okna")
    add("str_donate_one_day", u"Nie teraz, przypomnij mi jutro")
    add("str_donate_proceed", u"Dalej")

    add("str_scheduler_dialog", u"Planner")
    add("str_scheduler_tab", u"Ustawienia")

    add("str_select_import_file", u"Wybierz plik do importu")    
    add("str_add_feed_dialog", u"Dodaj Feed")
    add("str_edit_feed", u"Właściwości Feed")

    add("str_really_delete", u"Naprawdę skasuj")

    add("str_license_caption", u"Licencja")

    add("str_ep_downloaded", u"Ściągnięte")
    add("str_ep_skipped_removed_other", u"Pominięty/Skasowany/InnyFeed")
    add("str_dl_state_to_download", u"Do ściągnięcia")

    add("str_select_none_cleanup", u"Odznacz")
    add("str_submit_lang", u"Wyślij plik językowy")
    
    add("str_dltab_live", u"Obecne ściągnięcia: ")
    add("str_dltab_ul_speed", u"Szybkość wysyłania: ")
    add("str_dltab_dl_speed", u"Szybkość ściągania: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Plik")
    add("str_import_opml", u"Importuj feed z opml...")
    add("str_export_opml", u"Exportuj feed jako opml...")
    add("str_preferences_menubar", u"Ustawienia...")
    add("str_close_window", u"Zamknij okno")
    add("str_quit", u"Wyjdź")

    add("str_edit", u"Edytuj")
    add("str_select_all", u"Wybierz wszystko")

    add("str_tools", u"Narzędzia")
    add("str_check_all", u"Zaznacz wszystko")
    add("str_catch_up", u"Catch-up")
    add("str_check_selected", u"Zaznacz wybrane")
    add("str_add_feed", u"Dodaj Feed...")
    add("str_remove_selected", u"Usuń Feed")
    add("str_feed_properties", u"Właściwości feed...")
    add("str_scheduler_menubar", u"Planner...")
    
    add("str_select_language", u"Wybierz język")

    ## these are also used for the tabs
    add("str_view", u"Zobacz")
    add("str_downloads", u"Ściągnięte")
    add("str_subscriptions", u"Subskrypcje")
    add("str_podcast_directory", u"Katalog podcastów")
    add("str_cleanup", u"Czyszczenie")

    add("str_help", u"Pomoc")
    add("str_online_help", u"Pomoc Online")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Sprawdź uaktualnienie...")
    add("str_report_a_problem", u"Zgłoś problem")
    add("str_goto_website", u"Idź do strony WWW")
    add("str_make_donation", u"Wspomóż projekt")
    add("str_menu_license", u"Licencja...")
    add("str_about", u"O programie...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Skasuj wybrane")
    add("str_cancel_selected_download", u"Anuluj wybrane")
    add("str_pause_selected", u"Wstrzymaj wybrane")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Nowy")
    add("str_dl_state_queued", u"Oczekuje")
    add("str_dl_state_downloading", u"Ściągam")
    add("str_dl_state_downloaded", u"Ściągnięte")
    add("str_dl_state_cancelled", u"Skasowane")
    add("str_dl_state_finished", u"Skończone")
    add("str_dl_state_partial", u"Częściowo ściągnięte")
    add("str_dl_state_clearing", u"Czyszcze")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Sprawdź czy sa dostępne nowe podcasty")
    add("str_catch_up_mode", u"Catch-up - Ściągnij tylko ostatnie nowe epizody")

    add("str_add_new_feed", u"Dodaj nowy feed");
    add("str_remove_selected_feed", u"Skasuj wybrany feed")
    add("str_properties", u"Właściwości")
    add("str_check_selected_feed", u"Sprawdź wybrany feed")

    add("str_scheduler_on", u"Planner - Właczony")
    add("str_scheduler_off", u"Planner - Wyłaczony")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Następny:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Ściągam listę dostępnych plików...")
    add("str_no_episodes_found", u"Nic nie znaleziono.")


    ## Directorytab Toolbar
    add("str_refresh", u"Odśwież")
    add("str_open_all_folders", u"Otwórz wszystkie foldery")
    add("str_close_all_folders", u"Zamknij wszystkie foldery")
    add("str_add", u"Dodaj")

    ## Directorytab Other items
    add("str_directory_description", u"Kliknij na feed na liśie lub wpisz/wklej powyżej i naciśnij przycisk Dodaj.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Wybierz feed")
    add("str_refresh_cleanup", u"Odśwież")
    
    add("str_look_in", u"Szukaj epizodów w")        
    add("str_player_library", u"Bibliotece odtwarzacza")
    add("str_downloads_folder", u"Folderze Ściągnięte")
    add("str_delete_library_entries", u"Wykasuj wpisy w Bibliotece")
    add("str_delete_files", u"Skasuj pliki")
    add("str_select_all_cleanup", u"Wybierz wszystko")
    add("str_delete", u"Skasuj")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Wyczyść")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nazwa")
    add("str_lst_date", u"Data")        
    add("str_lst_progress", u"Postęp")
    add("str_lst_state", u"Stan")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Ścieżka")
    add("str_lst_episode", u"Epizod")
    add("str_lst_playlist", u"Playlista")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Subskrybuowane")
    add("str_disabled", u"Zablokowane")
    add("str_newly-subscribed", u"Nowe subskrybcje")
    add("str_unsubscribed", u"Już niesubskrybuowane")
    add("str_preview", u"Zajawka")
    add("str_force", u"Na siłę")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Wybierz nazwę dla pliku do exportu")
    add("str_subs_exported", u"Subskrybcja wyeksportowana.")
    
    ## Preferences Dialog
    add("str_preferences", u"Ustawienia")
    
    add("str_save", u"Zapisz")
    add("str_cancel", u"Anuluj")
    
    # General
    add("str_general", u"Ogólne")
    add("str_gen_options_expl", u"Ustaw ogólne opcje dla aplikacji %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Przy starcie pokazuj aplikacje %s w pasku" % PRODUCT_NAME)

    add("str_run_check_startup", u"Sprawdź czy nie ma nowych podcastów przy starcie aplikacji")
    add("str_play_after_download", u"Odtwarzaj pliki zaraz po ich ściągnięciu")
    add("str_location_and_storage", u"Zarządzanie dyskiem")
    add("str_stop_downloading", u"Nie ściągaj gdy dostępna powierzchnia twardego dysku osiągnie mniej niż")
    add("str_bad_megabyte_limit_1", u"Przepraszam, ale limit megabajtów nie wyglada na liczbę całkowitą")
    add("str_bad_megabyte_limit_2", u"Spróbuj ponownie.")

    add("str_download_folder", u"Ściągaj podcasty do tego folderu")
    add("str_browse", u"Przejrzyj")
    add("str_bad_directory_pref_1", u"Przepraszam, nie mogę znaleść folderu który określiłeś")
    add("str_bad_directory_pref_2", u"Stwórz folder i spróbuj ponownie.")

    
    # Threading
    add("str_threads", u"Wątki")
    add("str_multiple_download", u"Ustawienia multi ściągania")
    add("str_max_feedscans", u"maksymalna liczba skanowanych wątków na sesje")
    add("str_max_downloads", u"maksymalna liczba ściągnięć na sesje")
   
    # Network settings
    add("str_networking", u"Ustawiena sieci")
    add("str_coralize_urls", u"Koralizuj URL (w fazie testów)")
    add("str_proxy_server", u"Użyj serwera proxy")
    add("str_proxy_address", u"Adres")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Nazwa użytkownika")
    add("str_proxy_password", u"Hasło")
    add("str_bad_proxy_pref", u"Wybrałeś wspomaganie przez serwer proxy, lecz nie podałeś nazwy hosta i numeru portu. Wróć do zakładki Ustawienia sieci, ustaw nazwę hosta proxy oraz jego port.")

    # Player
    add("str_player", u"Odtwarzacz")
    add("str_choose_a_player", u"Wybierz odtwarzacz")
    add("str_no_player", u"Brak odtwarzacza")
    
    # Advanced
    add("str_advanced", u"Zaawansowane")
    add("str_options_power_users", u"Te opcje mogą być używane tylko przez zaawansowanych użytkowników")
    add("str_run_command_download", u"Wykonaj tą komendę po każdym ściągnięciu")
    add("str_rcmd_full_path", u"%f = Pełna ścieżka do ściągniętego pliku")
    add("str_rcmd_podcast_name", u"%n = Nazwa podcastu")
    add("str_other_advanced_options", u"Inne zaawansowane opcje")
    add("str_show_log", u"Pokaż zakładkę Log w aplikacji")



    ## Feed Dialog (add/properties)
    add("str_title", u"Tytuł")
    add("str_url", u"URL")
    add("str_goto_subs", u"Idź do zakładki Subskrybcje, by zobaczyć epizody z tego feed'a")
    add("str_feed_save", u"Zapisz")
    add("str_feed_cancel", u"Anuluj")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Aktywuj planner")
    add("str_sched_select_type", u"Zaznacz okienka, by sprawdzać o określonych porach i w regularnych odstępach:")
    add("str_check_at_specific_times", u"Sprawdź o tych godzinach")
    add("str_check_at_regular_intervals", u"Sprawdź w regularnych odstępach")
    add("str_repeat_every:", u"Powtórz co:")
    add("str_latest_run", u"Ostatnio:")
    add("str_next_run", u"Następne:")
    add("str_not_yet", u"Jeszcze nie wykonywano")
    #--- Cancel
    add("str_save_and_close", u"Zapisz i zamknij")
    #--- Save

    add("str_time_error", u"Jeden z zaplanowanych czasów jest nieprawidłowy. Prawidłowy zapis czasu powinien wygladać tak: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Sprawdź czy są dostępne nowe podcasty naciskając zieloną ikonkę z dwiema strzałkami")
    add("str_last_check", u"Ostatnio sprawdzano")
    add("str_of", u"z")
    add("str_item", u"plik")
    add("str_items", u"plików")
    add("str_downloading", u"ściąganie")
    add("str_downloaded", u"ściągnięto")
    add("str_enclosure", u"załącznik")
    add("str_enclosures", u"załączniki")
    add("str_fetched", u"wyodrębnione")
    add("str_loading_mediaplayer", u"Uruchamianie twojego odtwarzacza...")
    add("str_loaded_mediaplayer", u"Twój odtwarzacz uruchomiony...")        
    add("str_initialized", u"%s gotowy" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"By dostosować wszystkie opcje w programie %s, wymagany jest restart aplikacji. Naciśnij Ok by zakończyć pracę aplikacji, lub Anuluj by kontynuować." % PRODUCT_NAME)
    add("str_really_quit", u"Jestem w trakcie ściągania.  Naprawdę wyjść z programu?");
    add("str_double_check", u"Wyglada na to, że ściąganie jest już w trakcie.");
    
    # check for update
    add("str_new_version_ipodder", u"Nowa wersja programu %s jest dostępna, naciśnij Ok by przejść do strony producenta." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Ta wersja aplikacji %s jest najnowsza" % PRODUCT_NAME)
    add("str_other_copy_running", u"Inna sesja aplikacji %s jest już uruchomiona. Przywołaj ją, poczekaj aż wykona wszystkie zadania, lub zamknij." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Sprawdź teraz")        
    add("str_open_ipodder", u"Otwórz %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Skanowanie feed")

    # Feed right-click menu
    add("str_remove", u"Usuń")        
    add("str_open_in_browser", u"Otwórz w przegladarce")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Sprawdź ten epizod w Odtwarzaczu")
    add("str_clear_selected", u"Wyczyść wybrane pliki")
    



