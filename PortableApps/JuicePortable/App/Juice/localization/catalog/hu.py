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

   add("str_critical_error_minspace_exceeded", \
       u"A letöltés megszakítva: a szabad terület %dMB, " \
       u"kevesebb, mint %dMB.  Kérlek szabadíts fel területet Please free up space on " \
       u"törléssel vagy módosítsd a tárolókezelést" \
       u"a Beállítások menüpontban")
   add("str_critical_error_unknown", u"Ismeretlen hiba a letöltéskor.")

   add("str_error_checking_new_version", u"Sajnálom, hibát találtam az új verzió keresése során. Kérem, próbálja újra késõbb!")
   add("str_hours", u"órák")
   add("str_minutes", u"percek")

   # The next 4 are for the status bar updates during the initial scan.
   add("str_scanning", u"Keresés")
   add("str_scanned", u"Keresett")
   add("str_feed", u"csatorna")
   add("str_feeds", u"csatornák")

   add("str_downloading_new_episodes", u"Új adás letöltése")
   add("str_sched_specific", u"Ellenõrzés konkrét idõponttól")
   add("str_sched_reg", u"Idõszak ellenõrzése")
   add("str_repeat_every", u"Ismételje minden")
   add("str_next_run_label", u"Következõ futás:")

   add("str_license", u"Ez egy szabad program; A dokumentum a Free Software Foundation által kiadott GNU Free Documentation License 2-es vagy újabb verziójában foglalt feltételek keretein belül másolható, terjeszthetõ és/vagy módosítható." \
        u"A programot annak reményében készítettük, hogy hasznos lesz, de garanciát nem vállalunk;  \n\nNézdd át a GNU General Public License -t a részletekért.")

   add("str_donate", u"%s támogatása" % PRODUCT_NAME)
   add("str_donate_expl", u"It's important to keep community-owned %s applications online and keep this new way of consuming media free as in speech. A fejlesztõ csapat minden pénzt szívesen fogad, ami ösztönöz minket arra, hogy új funciókkal és szolgáltatásokkal bõvítsük a programot!" % PRODUCT_NAME)
   add("str_donate_yes", u"Igen, menjünk a támogatói oldalra!")
   add("str_donate_two_weeks", u"Még egy kicsit gondolkodok rajta, figyelmeztess két hét múlva.")
   add("str_donate_already", u"Én már támogattam, ne jelenjen meg legközelebb ez az ablak.")
   add("str_donate_no", u"Nem, én nem akarom támogatni a programot,  ne jelenjen meg legközelebb ez az ablak")
   add("str_donate_one_day", u"Most nem, értesíts 1 nap múlva")
   add("str_donate_proceed", u"Tovább")

   add("str_scheduler_dialog", u"Idõzítés")
   add("str_scheduler_tab", u"Beállítások")

   add("str_select_import_file", u"Fájlok kiválasztása importáláshoz")
   add("str_add_feed_dialog", u"Csatorna hozzáadása")
   add("str_edit_feed", u"Csatorna tulajdonságok")

   add("str_really_delete", u"Tényleg törlöm")

   add("str_license_caption", u"Liszensz")

   add("str_ep_downloaded", u"Letöltve")
   add("str_ep_skipped_removed_other", u"Átugorva/Törölve/Másik csatorna")
   add("str_dl_state_to_download", u"Letöltésre")

   add("str_select_none_cleanup", u"Válassz egyet")
   add("str_submit_lang", u"Nyelv keresése")

   add("str_dltab_live", u"Futó letöltések: ")
   add("str_dltab_ul_speed", u"Feltöltés sebessége: ")
   add("str_dltab_dl_speed", u"Letöltés sebessége: ")

   ##_________________________________________________________
   ##
   ##     Main window (iPodder.xrc)
   ##_________________________________________________________

   ## File menu
   add("str_file", u"File")
   add("str_import_opml", u"Csatornák importálása opml-bõl...")
   add("str_export_opml", u"Csatornák exportálása opml-be...")
   add("str_preferences_menubar", u"Beállítások...")
   add("str_close_window", u"Ablak bezárása")
   add("str_quit", u"Kilépés")

   add("str_edit", u"Módosítás")
   add("str_select_all", u"Mindent kiválaszt")

   add("str_tools", u"Eszközök")
   add("str_check_all", u"Összes átvizsgálása")
   add("str_catch_up", u"Félbeszakít")
   add("str_check_selected", u"Kiválasztottak átvizsgálása")
   add("str_add_feed", u"Csatorna hozzáadása...")
   add("str_remove_selected", u"Csatorna törlése")
   add("str_feed_properties", u"Csatorna tulajdonságok...")
   add("str_scheduler_menubar", u"Idõzítés...")

   add("str_select_language", u"Nyelv kiválasztása")

   ## these are also used for the tabs
   add("str_view", u"Nézet")
   add("str_downloads", u"Letöltés")
   add("str_subscriptions", u"Elõfizetés")
   add("str_podcast_directory", u"Az adások könyvtára")
   add("str_cleanup", u"Takarítás")

   add("str_help", u"Segítség")
   add("str_online_help", u"Online segítség")
   add("str_faq", u"FAQ")
   add("str_check_for_update", u"Új verzió keresése...")
   add("str_report_a_problem", u"Hiba elküldése")
   add("str_goto_website", u"Ugrás a weboldalra")
   add("str_make_donation", u"Támogatás")
   add("str_menu_license", u"Liszensz...")
   add("str_about", u"Névjegy...")

   ## Downloadstab Toolbar
   add("str_remove_selected_items", u"Kiválasztott elemek törlése")
   add("str_cancel_selected_download", u"Kiválasztott letöltések megszakítása")
   add("str_pause_selected", u"Szünet kiválasztása")

   ## Downloadstab States (in columns)
   ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
   ## other strings, e.g. str_downloading above which isn't capitalized.
   add("str_dl_state_new", u"Új")
   add("str_dl_state_queued", u"Várakozás")
   add("str_dl_state_downloading", u"Letöltés")
   add("str_dl_state_downloaded", u"Letöltve")
   add("str_dl_state_cancelled", u"Megszakítva")
   add("str_dl_state_finished", u"Befejezve")
   add("str_dl_state_partial", u"Részben letöltve")
   add("str_dl_state_clearing", u"Takarítás")

   ## Subscriptionstab Toolbar
   add("str_check_for_new_podcasts", u"Új adás kijelölése")
   add("str_catch_up_mode", u"Félbeszakítás - CSak az új elõfizetések töltsd le!")

   add("str_add_new_feed", u"Új csatorna hozzáadása");
   add("str_remove_selected_feed", u"Kiválasztott csatorna törlése")
   add("str_properties", u"Tulajdonságok")
   add("str_check_selected_feed", u"Kiválasztott csatornák ellenõrzése")

   add("str_scheduler_on", u"Idõzítés - Be")
   add("str_scheduler_off", u"Idõzítés - Ki")

   ## Subscriptionstab Scheduler information
   add("str_next_run:", u"Következõ futás:")

   ## Subscriptionstab episode frame
   add("str_downloading_episode_info", u"Adás információk letöltése...")
   add("str_no_episodes_found", u"Nincs új adás.")

   ## Directorytab Toolbar
   add("str_refresh", u"Frissítés")
   add("str_open_all_folders", u"Összes könyvtár megnyitása")
   add("str_close_all_folders", u"Összes könyvtár bezárása")
   add("str_add", u"Add")

   ## Directorytab Other items
   add("str_directory_description", u"Kattints a csatornára a kibontásban vagy írd be / másold be a fenti területre és kattints a Hozzáadás gombra.")

   ## Cleanuptab items
   add("str_select_a_feed", u"Válassz csatornát")
   add("str_refresh_cleanup", u"Frissítés")

   add("str_look_in", u"Adás keresése")
   add("str_player_library", u"Lejátszó könyvtára")
   add("str_downloads_folder", u"Letöltések könyvtára")
   add("str_delete_library_entries", u"Könyvtár bejegyzések törlése")
   add("str_delete_files", u"Fájlok törlése")
   add("str_select_all_cleanup", u"Összes kiválasztása")
   add("str_delete", u"Törlés")

   ## Logtab items
   add("str_log", u"Log")
   add("str_clear", u"Takarítás")

   ## Columns (in downloads- and subscriptionstab)
   add("str_lst_name", u"Név")
   add("str_lst_date", u"Dátum")
   add("str_lst_progress", u"Folyamat")
   add("str_lst_state", u"Állapot")
   add("str_lst_mb", u"MB")
   add("str_lst_location", u"Hely")
   add("str_lst_episode", u"Adás")
   add("str_lst_playlist", u"Lejátszási lista")

   ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
   add("str_subscribed", u"Elõfizetve")
   add("str_disabled", u"Letiltva")
   add("str_newly-subscribed", u"Új hozzáadás")
   add("str_unsubscribed", u"Lemondva")
   add("str_preview", u"Elõnézet")
   add("str_force", u"Érvényes")

   ##_________________________________________________________
   ##
   ##   Dialog Windows
   ##_________________________________________________________

   ## OPML Import Dialog
   #--- Select import file

   ## OPML Export Dialog
   add("str_choose_name_export_file", u"Válassz nevet az export fájlhoz")
   add("str_subs_exported", u"Elõfizetés exportálva.")

   ## Preferences Dialog
   add("str_preferences", u"Beállítások")

   add("str_save", u"Mentés")
   add("str_cancel", u"Mégsem")

   # General
   add("str_general", u"Általános")
   add("str_gen_options_expl", u"Végrehajtja az %s általános beállításait" % PRODUCT_NAME)
   add("str_hide_on_startup", u"Indításkor csak a Tálcán jelenik meg.")

   add("str_run_check_startup", u"Új adások keresése a program indulásakor")
   add("str_play_after_download", u"Letöltés után azonnal játsza le.")
   add("str_location_and_storage", u"Hely- és tárolás kezelés")
   add("str_stop_downloading", u"Letöltés megállítása, ha a lemezkapacitás kevesebb, mint")
   add("str_bad_megabyte_limit_1", u"Bocs, de a határérték nem egész szám")
   add("str_bad_megabyte_limit_2", u"Kérlek, próbáld újra.")

   add("str_download_folder", u"Adások letöltése ebbe a könyvtárba")
   add("str_browse", u"Browse")
   add("str_bad_directory_pref_1", u"Bocs, de nem találom a megadott könyvtárat")
   add("str_bad_directory_pref_2", u"Kérlek, csináld meg és próbáld újra.")

   # Threading
   add("str_threads", u"Párhuzamos munkavégzés")
   add("str_multiple_download", u"Párhuzamos letöltések beállítása")
   add("str_max_feedscans", u"maximális folyamatok száma a csatornakeresés során")
   add("str_max_downloads", u"maximális letöltések száma a letöltések során")

   # Network settings
   add("str_networking", u"Hálózati beállítások")
   add("str_coralize_urls", u"Coralize URLs (kísérlet)")
   add("str_proxy_server", u"Proxy szerver használata")
   add("str_proxy_address", u"Cím")
   add("str_proxy_port", u"Port")
   add("str_proxy_username", u"Felhasználónév")
   add("str_proxy_password", u"Jelszó")
   add("str_bad_proxy_pref", u"Engedélyezted a proxy használatot, de nem adtál meg szervert és portot. Kérlek, menj vissza a Hálózati beállításokba és állítsd be a hiányzó értékeket.")

   # Player
   add("str_player", u"Lejátszó")
   add("str_choose_a_player", u"Válassz lejátszót!")
   add("str_no_player", u"Nincs lejátszó")

   # Advanced
   add("str_advanced", u"Haladó")
   add("str_options_power_users", u"Ezeket az opciókat csak haladó felhasználók használják!")
   add("str_run_command_download", u"Program futtatása minden letöltés után")
   add("str_rcmd_full_path", u"%f = A letöltött fájlok teljes elérési útvonala.")
   add("str_rcmd_podcast_name", u"%n = Adás neve")
   add("str_other_advanced_options", u"További haladó beállítások")
   add("str_show_log", u"Log fül megjelenítése az alkalmazásban")

   ## Feed Dialog (add/properties)
   add("str_title", u"Cím")
   add("str_url", u"URL")
   add("str_goto_subs", u"Menj az elõfizetések fülre, a csatorna adásainak megtekintéséhez!")
   add("str_feed_save", u"Mentés")
   add("str_feed_cancel", u"Mégsem")

   ## Scheduler Dialog
   add("str_enable_scheduler", u"Idõzítés engedélyezése")
   add("str_sched_select_type", u"Válaszd a lenti rádiógombokat az idõpont vagy a letöltések ismétlõdésének beállításához:")
   add("str_check_at_specific_times", u"Ellenõrzés ebben az idõpontban")
   add("str_check_at_regular_intervals", u"Ellenõrzés meghatározott ismétlõdéssel:")
   add("str_repeat_every:", u"Ismétlés minden:")
   add("str_latest_run", u"Utolsó futás:")
   add("str_next_run", u"Következõ futás:")
   add("str_not_yet", u"Még nem")
   #--- Cancel
   add("str_save_and_close", u"Mentés és bezárás")
   #--- Save

   add("str_time_error", u"A beállított idõpont nem megfelelõ. A helyes formátum: 10:02am, 16:43.")

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
   add("str_check_for_new_podcast_button", u"Új adások kereséséhez nyomd meg a zöld gombot!")
   add("str_last_check", u"Az utolsó ellenõrzések")
   add("str_of", u"of")
   add("str_item", u"adás")
   add("str_items", u"adások")
   add("str_downloading", u"letöltés")
   add("str_downloaded", u"letöltve")
   add("str_enclosure", u"melléklet")
   add("str_enclosures", u"mellékletek")
   add("str_fetched", u"elhozva")
   add("str_loading_mediaplayer", u"Média lejátszó betöltése ...")
   add("str_loaded_mediaplayer", u"Média lejátszó betöltve ...")
   add("str_initialized", u"%s kész" % PRODUCT_NAME)

   ## Other application strings
   add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
   add("str_localization_restart", u"A nyelvváltás után az %st újra kell indítani. Kattints az OK gombra, ha leálítod, Mégsemre ha folytatni akarod az %s használatát." % (PRODUCT_NAME,PRODUCT_NAME))
   add("str_really_quit", u"Letöltés folyamatban. Biztos, hogy kilépsz?");
   add("str_double_check", u"Úgy tûnik, hogy letöltés van folyamtban.");

   # check for update
   add("str_new_version_ipodder", u"Az %s új verziója letölthetõ, kattints az OK gombra a letöltéshez." % PRODUCT_NAME)
   add("str_no_new_version_ipodder", u"Nincs frissebb %s verzió" % PRODUCT_NAME)
   add("str_other_copy_running", u"Az %s már fut. Another copy of %s is running. Várdd meg amíg befejezi vagy lõdd le!" % (PRODUCT_NAME,PRODUCT_NAME))

   # Windows taskbar right-click menu
   add("str_check_now", u"Adások keresése")
   add("str_open_ipodder", u"%s megnyitása" % PRODUCT_NAME)
   #--- Downloading
   add("str_scanning_feeds", u"Csatornák keresése")

   # Feed right-click menu
   add("str_remove", u"Eltávolítás")
   add("str_open_in_browser", u"Megnyitás böngészõben")

   # Downloads right-click menu
   add("str_play_episode", u"Adás lejátszása médiaplayerben.")
   add("str_clear_selected", u"Kiválasztott eleme törlése")
