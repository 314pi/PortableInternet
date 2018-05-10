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

    add("str_sched_specific", "Provjeri u naznacenim vremenima")
    add("str_sched_reg", "Provjeri u vremenskim razmacima")
    add("str_repeat_every", "Ponovi svakih")
    add("str_next_run_label", "Iduce pokretanje:")
    
    add("str_menu_license", "Licenca")
    add("str_license", "Ovaj program je besplatan software; mozete ga distribuisati i/ili modifikovati pod uslovima od GNU General Public Licence kao sto je publikovano od strane Free Software Foundation; verzijom 2 Licence, ili bilo kojom iducom verzijom. Ovaj program je distribuisan sa nadom da ce biti koristan, ali bez ikakve garancije; cak i bez implicitne garancije za odgovarajucu upotrebu. \n\nZa vise detalja pogledajte GNU General Public Licencu.")
    add("str_donate", "Donirajte %s-u" % PRODUCT_NAME)
    add("str_donate_expl", "Vazno je odrzati %s aplikacije koje su u vlasnistvu opste zajednice online i zadrzati ovaj novi nacin media besplatan kao sto je i govor. Svaki novcani iznos ce usreciti nas tim i podsteci ih da rade na daljem razvoju %s-a." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_donate_yes", "Da, odvedi me na stranicu za donacije!")
    add("str_donate_two_weeks", "Zelim jos malo da pogledam ovu aplikaciju ali prikazi mi ovo ponovo za dvije sedmice.")
    add("str_donate_already", "Vec sam donirao/la zaustavi prikazivanje ovog dialoga.")
    add("str_donate_no", "Ne, ne zelim da doniram, zaustavi prikazivanje ovog dialoga")
    add("str_donate_one_day", "Ne sad, podsjeti me ponovo za jedan dan.")
    add("str_donate_proceed", "Nastavi")

    add("str_preferences", "Preference")
    add("str_preferences_menubar", "Preference...")

    add("str_scheduler_dialog", "Podesavanja")
    add("str_scheduler_tab", "Podesavanja")
    add("str_scheduler_menubar", "Podesavanja...")

    add("str_select_import_file", "Selektuj fajl za import")    
    add("str_add_feed_dialog", "Dodaj feed")
    add("str_edit_feed", "Feed osobine")

    add("str_really_delete", "Zaista obrisi")

    add("str_license_caption", "Licenca")

    add("str_ep_downloaded", "Downloadovano")
    add("str_ep_skipped_removed_other", "Preskoceno/Uklonjeno/DrugiFeed")
    add("str_dl_state_to_download", "Za download")

    add("str_select_none_cleanup", "Deselektuj")
    add("str_submit_lang", "Posalji jezik")
    
    
    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", "Fajl")
    add("str_import_opml", "Importuj feedove iz opml...")
    add("str_export_opml", "Exportuj feedove kao opml...")
    add("str_preferences_menubar", "Podesavanja...")
    add("str_close_window", "Zatvori prozor")
    add("str_quit", "Zatvori")

    add("str_edit", "Edituj")
    add("str_select_all", "Selektuj sve")

    add("str_tools", "Alati")
    add("str_check_all", "Provjeri sve")
    add("str_catch_up", "Provjeri zaostale")
    add("str_check_selected", "Provjeri selektovane")
    add("str_add_feed", "Dodaj Feed...")
    add("str_remove_selected", "Ukloni Feed")
    add("str_feed_properties", "Feed osobine...")
    add("str_scheduler_menubar", "Podesavanja...")
    

    add("str_select_language", "Jezik")

    ## these are also used for the tabs
    add("str_view", "Pogled")
    add("str_downloads", "Downloadi")
    add("str_subscriptions", "Prijavljeno")
    add("str_podcast_directory", "Podcast direktorijum")
    add("str_cleanup", "Ciscenje")

    add("str_help", "Pomoc")
    add("str_online_help", "Online Pomoc")
    add("str_faq", "FAQ")
    add("str_check_for_update", "Provjeri za update...")
    add("str_report_a_problem", "Prijavi problem")
    add("str_goto_website", "Idi na Website")
    add("str_make_donation", "Doniraj")
    add("str_menu_license", "Licenca...")
    add("str_about", "Podaci o...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", "Ukloni selekciju")
    add("str_cancel_selected_download", "Otkazi selekciju")
    add("str_pause_selected", "Pauziraj slekciju")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", "Novi")
    add("str_dl_state_queued", "U redu cekanja")
    add("str_dl_state_downloading","Downloaduje se")
    add("str_dl_state_downloaded","Downloadovan")
    add("str_dl_state_cancelled", "Otkazan")
    add("str_dl_state_finished", "Zavrsen")
    add("str_dl_state_partial", "Djelomicno downloadovan")
    add("str_dl_state_clearing", "Ciscenje")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", "Provjeri za nove podcasts")
    add("str_catch_up_mode", "Provjeri zaostale - downloaduj samo nove podcasts")

    add("str_add_new_feed", "Dodaj feed");
    add("str_remove_selected_feed", "Ukloni feed")
    add("str_properties", "Osobine")
    add("str_check_selected_feed", "Provjeri feed")

    add("str_scheduler_on", "Auto provjera - Ukljucena")
    add("str_scheduler_off", "Auto provjera - Iskljucena")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", "Iduce pokretanje:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", "Downloadujem informaciju o epizodi...")
    add("str_no_episodes_found", "Epizode nisu pronadjene.")


    ## Directorytab Toolbar
    add("str_refresh", "Osvjezi")
    add("str_open_all_folders", "Otvori sve direktorijume")
    add("str_close_all_folders", "Zatvori sve direktorijume")
    add("str_add", "Dodaj")

    ## Directorytab Other items
    add("str_directory_description", "Klikni na feed ili ukucaj/kopiraj u prostor iznad i onda klikni na dodaj.")




    ## Cleanuptab items
    add("str_select_a_feed", "Selektuj feed")
    add("str_refresh_cleanup", "Osvjezi")
    
    add("str_look_in", "Pogledaj za epizode u")        
    add("str_player_library", "Player biblioteka")
    add("str_downloads_folder", "Download direktorijum")
    add("str_delete_library_entries", "Pobrisi stavke u biblioteci")
    add("str_delete_files", "Pobrisi fajlove")
    add("str_select_all_cleanup", "Selektuj sve")
    add("str_delete", "Pobrisi")




    ## Logtab items
    add("str_log", "Loguj")
    add("str_clear", "Pobrisi")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", "Ime")
    add("str_lst_date", "Datum")        
    add("str_lst_progress", "Napredak")
    add("str_lst_state", "Stanje")
    add("str_lst_mb", "MB")
    add("str_lst_location", "Lokacija")
    add("str_lst_episode", "Epizoda")
    add("str_lst_playlist", "Playlista")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed","Prijavljen")
    add("str_disabled", "Onemogucen")
    add("str_newly-subscribed", "Novo prijavljen")
    add("str_unsubscribed", "Odjavljen")
    add("str_preview", "Pregled")
    add("str_force", "Natjeraj")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", "Izaberi ime za export fajl")
    add("str_subs_exported", "Lista prijavljivanja je eksportovana.")
    
    ## Preferences Dialog
    add("str_preferences", "Osobine")
    
    add("str_save", "Snimi")
    add("str_cancel", "Otkazi")
    
    # General
    add("str_general", "Glavne osobine")
    add("str_gen_options_expl", "Postavi glavne osobine za %s aplikaciju" % PRODUCT_NAME)
    add("str_hide_on_startup", "Prilikom pokretanja prikazi %s samo kao sistemsku ikonu" % PRODUCT_NAME)

    add("str_run_check_startup", "Provjeri nove podcasts prilikom startanja aplikacije")
    add("str_play_after_download", "Slusaj podcasts cim su downloadovani")
    add("str_location_and_storage", "podesi lokaciju i kapacitet")
    add("str_stop_downloading", "Zaustavi download ako harddisk dostigne minimum od ")
    add("str_bad_megabyte_limit_1", "Megabajt limit nije broj")
    add("str_bad_megabyte_limit_2", "Molimo vas pokusajte ponovo.")

    add("str_download_folder", "Downloaduj podcasts u ovaj folder")
    add("str_browse", "Selektuj")
    add("str_bad_directory_pref_1", "Direktorijum koji ste unijeli ne postoji")
    add("str_bad_directory_pref_2", "Molimo vas kreirajte ga i pokusajte ponovo.")

    
    # Threading
    add("str_threads", "Threading")
    add("str_multiple_download", "Podesi visestruki download")
    add("str_max_feedscans", "maximalni broj paralelnih skeniranja po sesiji")
    add("str_max_downloads", "maximalni broj downloada po sesiji")
   
    # Network settings
    add("str_networking", "Mrezna podesavanja")
    add("str_coralize_urls", "Coralizuj URLs (experimentalno)")
    add("str_proxy_server", "Koristi proxyserver")
    add("str_proxy_address", "Adresa")
    add("str_proxy_port", "Port")
    add("str_proxy_username", "Korisnicko ime")
    add("str_proxy_password", "Lozinka")
    add("str_bad_proxy_pref", "Omogucili ste proxy podrsku ali niste definisali proxy host i port. Molimo vas vratite se na Mrezna podesavanja i podesite proxy host i port.")

    # Player
    add("str_player", "Player")
    add("str_choose_a_player", "Odaberite player")
    add("str_no_player", "Bez player-a")
    
    # Advanced
    add("str_advanced", "Napredno")
    add("str_options_power_users", "ove opcije mogu korisiti Power Users")
    add("str_run_command_download", "Pokreni ovu komandu poslije svakog downloada")
    add("str_rcmd_full_path", "%f = Puna putanja do downloadovanog fajla")
    add("str_rcmd_podcast_name", "%n = Ime podcast-a")
    add("str_other_advanced_options", "Druge napredne opcije")
    add("str_show_log", "Prikazi log tab u aplikaciji")



    ## Feed Dialog (add/properties)
    add("str_title", "Naslov")
    add("str_url", "URL")
    add("str_goto_subs","Idi na tab za prijavljivanje da pogledas epizode za ovaj feed")
    add("str_feed_save", "Snimi")
    add("str_feed_cancel", "Otkazi")




    ## Scheduler Dialog
    add("str_enable_scheduler", "Omoguci auto provjeru")
    add("str_sched_select_type", "Selektuj opcije da bi se provjera vrsila u specificirano vrijeme ili u jednakim intervalima:")
    add("str_check_at_specific_times", "Provjeri u ovim specificiranim vremenima")
    add("str_check_at_regular_intervals", "Provjeri u jednakim intervalima")
    add("str_repeat_every:", "Ponovi svakih:")
    add("str_latest_run", "Zadnje pokretanje:")
    add("str_next_run", "Iduce pokretanje:")
    add("str_not_yet", "Jos ne")
    #--- Cancel
    add("str_save_and_close", "Snimi i zatvori")
    #--- Save

    add("str_time_error","Jedan od definisanih vremena ne izgleda ispravno. Ispravan format je: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", "Provjeri za nove podcasts ako kliknes na zeleno dugme")
    add("str_last_check", "Zadnja provjera zavrsena")
    add("str_of", "ili")
    add("str_item", "stavka")
    add("str_items", "stavke")
    add("str_downloading", "downloaduje se")
    add("str_downloaded", "downloadovano")
    add("str_enclosure", "enclosure")
    add("str_enclosures", "enclosures")
    add("str_fetched", "prikupljeno")
    add("str_loading_mediaplayer", "Startujem media player...")
    add("str_loaded_mediaplayer", "Ucitan media player...")        
    add("str_initialized", "%s je spreman" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + " - Podcast prijemnik v" + __version__)
    add("str_localization_restart", "Za lokalizovanje svih %s kontrola potreban je restart. Klikni na Ok za zatvaranje, otkazi za nastavak." % PRODUCT_NAME)
    add("str_really_quit", "Download je u toku. Zaista zatvori?");
    add("str_double_check", "Download je u toku.");
    
    # check for update
    add("str_new_version_ipodder", "Nova verzija je dostupna, klikni ok da odes na download stranicu.")
    add("str_no_new_version_ipodder", "Ova verzija je zadnja verzija.")
    add("str_other_copy_running", "Jos jedna kopija %s-a je aktivna. Sacekaj dok zavrsi ili zaustavi proces." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now","Provjeri sad")        
    add("str_open_ipodder","Otvori %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", "Provjeravam feed")

    # Feed right-click menu
    add("str_remove","Ukloni")        
    add("str_open_in_browser","Otvori u browseru")
    
    

    # Downloads right-click menu
    add("str_play_episode", "Slusaj epizodu u media player-u")
    add("str_clear_selected", "Ukloni selekciju")
    




