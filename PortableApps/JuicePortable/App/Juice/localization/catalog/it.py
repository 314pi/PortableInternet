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

    add("str_username", u"Username")
    add("str_password", u"Password")
    add("str_missing_proxy_password", u"E' stato impostato un username per il proxy ma non una password. \n" \
        u"Resettare entrambi i valori o inserire una password.")

    add("str_goto_background_on_close_title", u"Set close behavior")
    add("str_goto_background_on_close_warn", \
        u"%s può continuare a lavorare in background dopo la chiusura \n" \
        u"della finestra principale. In alternativa %s può essere chiuso. \n" \
        u"Desideri mantenere attivo %s?" % (PRODUCT_NAME,PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"Continua l'esecuzione in background alla chiusura della finestra principale")
    add("str_yes", u"Si")
    add("str_no", u"No")
    add("str_dont_ask", u"Non chiedere nuovamente")
    add("str_ok", u"OK")
    add("str_hide_window", u"Nascondi finestra")
    add("str_hide_tray_icon", u"Nascondi icona nella System Tray")
    add("str_show_window", u"Mostra finestra")

    add("str_catchup_pref", u"Catchup skips older episodes permanently")
    add("str_set_catchup_title", u"Set catchup behavior")
    add("str_set_catchup_description", \
        u"When checking in Catchup mode, %s will skip all but the top \n" \
        u"item in each feed. Please specify how %s should treat the \n" \
        u"skipped items." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"Salta permanentemente")
    add("str_skip_temporarily", u"Salta solo questa volta")
    
    add("str_set_oneclick_handler", u"Set one-click handler")
    add("str_set_oneclick_handler_warn",\
        u"%s is not currently your one-click subscription handler for podcasts. \n" \
        u"Should we set %s to launch from one-click subscription links?" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"Always use %s for one-click subscription" % PRODUCT_NAME)
    
    add("str_txt_feedmanager", u"Gestori di feed compatibili:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Cerca o visualizza i podcast, iscrizione mediante un solo click")

    add("str_open_downloads_folder", u"Apri la cartella dei download")
    add("str_chkupdate_on_startup", u"Controlla nuove versioni all'avvio del programma.")
    add("str_bad_feedmanager_url", u"Impostare un URL valido per il gestore dei feed.")
    add("str_feed_manager", u"Gestore dei Feed")
    add("str_feedmanager_enable", u"Sincronizza le sottoscrizioni con un servizio remoto")
    add("str_opml_url", u"URL OPML")
    add("str_set_track_genre", u"Imposta il genere della traccia a")
    add("str_auto_delete", u"Cancella automaticamente episodi più vecchi di")
    add("str_days_old", u"giorni")
    
    add("str_show_notes", u"Mostra note")
    add("str_close", u"Chiudi")
    
    add("str_critical_error_minspace_exceeded", \
        u"Download saltato; spazio libero %dMB minore " \
        u"dei %dMB richiesti. Liberare spazio " \
        u"sul computer utilizzando il comando Pulizia o cambiare le impostazioni " \
        u"di salvataggio nelle Preferenze")
    add("str_critical_error_unknown", u"Errore critico sconosciuto durante il download.")
    
    add("str_error_checking_new_version", u"Si è verificato un errore durante il controllo delle nuove versioni. Riprovare più tardi.")
    add("str_hours", u"ore")
    add("str_minutes", u"minuti")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Scansione in corso")
    add("str_scanned", u"Scansione completata")
    add("str_feed", u"feed")
    add("str_feeds", u"feed")
    
    add("str_downloading_new_episodes", u"Scaricamento di nuovi episodi in corso")
    add("str_sched_specific", u"Controlla ad orari specifici")
    add("str_sched_reg", u"Controlla ad intervalli regolari")
    add("str_repeat_every", u"Ripeti ogni")
    add("str_next_run_label", u"Prossimo avvio:")
    
    add("str_license", u"Questo è un programma gratuito; è possibile ridistribuire e/o modificare il programma secondo i termini della  General Public License come pubblicato dalla Free Software Foundation; è possibile utilizzare la versione 2 della Licenza, o (a propria discrezione) una qualsiasi versione successiva. Il programma è distribuito nella speranza che possa essere utile, ma senza alcuna garanzia; in particolare, ma non esclusivamente, nessuna garanzia implicita sulla commerciabilità o l'idoneità a uno scopo particolare. \n\nPer maggiori informazioni consultare la GNU General Public License.")

    add("str_donate", u"Fai una donazione a %s" % PRODUCT_NAME)
    add("str_donate_expl", u"E' importante mantenere in vita la comunità di %s e continuare a fornire questo nuovo modo di consumare file multimediali libero. Qualsiasi somma di denaro è ben gradita dal team di sviluppo ed incoraggerà la realizzazione di nuove funzioni e servizi!" % PRODUCT_NAME)
    add("str_donate_yes", u"Sì, apri ora la pagina per eseguire la donazione!")
    add("str_donate_two_weeks", u"Devo ancora pensarci su, mostra questa finestra tra due settimane")
    add("str_donate_already", u"Ho già eseguito una donazione, non mostrare nuovamente questa finestra")
    add("str_donate_no", u"No, non desidero eseguire una donazione, non mostrare nuovamente questa finestra")
    add("str_donate_one_day", u"Non ora, mostra questa notifica tra 1 giorno")
    add("str_donate_proceed", u"Procedi")

    add("str_scheduler_dialog", u"Scheduler")
    add("str_scheduler_tab", u"Impostazioni")

    add("str_select_import_file", u"Seleziona file da importare")    
    add("str_add_feed_dialog", u"Aggiungi Feed")
    add("str_edit_feed", u"Proprietà Feed")

    add("str_really_delete", u"Confermi eliminazione?")

    add("str_license_caption", u"Licenza")

    add("str_ep_downloaded", u"Scaricati")
    add("str_ep_skipped_removed_other", u"Saltati/Rimossi/Altri Feed")
    add("str_dl_state_to_download", u"Da scaricare")

    add("str_select_none_cleanup", u"Nessuna selezione")
    add("str_submit_lang", u"Invia una traduzione")
    
    add("str_dltab_live", u"Download live: ")
    add("str_dltab_ul_speed", u"Velocità upload: ")
    add("str_dltab_dl_speed", u"Velocità download: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"File")
    add("str_import_opml", u"Importa feed da file opml...")
    add("str_export_opml", u"Esporta feed in un file opml...")
    add("str_preferences_menubar", u"Preferenze...")
    add("str_close_window", u"Chiudi finestra")
    add("str_quit", u"Esci")

    add("str_edit", u"Modifica")
    add("str_select_all", u"Seleziona tutto")

    add("str_tools", u"Strumenti")
    add("str_check_all", u"Controlla tutti")
    add("str_catch_up", u"Catch-up")
    add("str_check_selected", u"Controlla selezionati")
    add("str_add_feed", u"Aggiungi feed...")
    add("str_remove_selected", u"Rimuovi feed")
    add("str_feed_properties", u"Proprietà feed...")
    add("str_scheduler_menubar", u"Scheduler...")
    
    add("str_select_language", u"Scegli lingua")

    ## these are also used for the tabs
    add("str_view", u"Visualizza")
    add("str_downloads", u"Download")
    add("str_subscriptions", u"Sottoscrizioni")
    add("str_podcast_directory", u"Directory podcast")
    add("str_cleanup", u"Pulizia")

    add("str_help", u"Help")
    add("str_online_help", u"Help Online")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Controlla aggiornamenti...")
    add("str_report_a_problem", u"Segnala un problema")
    add("str_goto_website", u"Vai al sito")
    add("str_make_donation", u"Fai una donazione")
    add("str_menu_license", u"Licenza...")
    add("str_about", u"Informazioni...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Rimuovi elementi selezionati")
    add("str_cancel_selected_download", u"Cancella download selezionati")
    add("str_pause_selected", u"Metti in pausa")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Nuovo")
    add("str_dl_state_queued", u"In coda")
    add("str_dl_state_downloading", u"Scaricamento in corso")
    add("str_dl_state_downloaded", u"Scaricamento completato")
    add("str_dl_state_cancelled", u"Cancellato")
    add("str_dl_state_finished", u"Completato")
    add("str_dl_state_partial", u"Parzialmente completato")
    add("str_dl_state_clearing", u"Cancellazione in corso")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Controlla nuovi podcast")
    add("str_catch_up_mode", u"Catch-up - Scarica solo l'ultima sottoscrizione")

    add("str_add_new_feed", u"Aggiungi feed");
    add("str_remove_selected_feed", u"Rimuovi feed selezionati")
    add("str_properties", u"Proprietà feed")
    add("str_check_selected_feed", u"Controlla/Scarica feed selezionati")

    add("str_scheduler_on", u"Scheduler - Attivato")
    add("str_scheduler_off", u"Scheduler - Disattivato")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Prossimo avvio:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Scaricamento informazioni episodio in corso...")
    add("str_no_episodes_found", u"Nessun episodio trovato.")


    ## Directorytab Toolbar
    add("str_refresh", u"Aggiorna")
    add("str_open_all_folders", u"Apri tutte le cartelle")
    add("str_close_all_folders", u"Chiudi tutte le cartelle")
    add("str_add", u"Aggiungi")

    ## Directorytab Other items
    add("str_directory_description", u"Seleziona un feed nell'elenco o digita/incolla l'indirizzo nello spazio sottostante e scegli aggiungi.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Seleziona feed")
    add("str_refresh_cleanup", u"Aggiorna")
    
    add("str_look_in", u"Cerca episodi in")        
    add("str_player_library", u"Libreria di esecuzione")
    add("str_downloads_folder", u"Cartella di scaricamento")
    add("str_delete_library_entries", u"Elimina elementi nella libreria")
    add("str_delete_files", u"Elimina file scaricati")
    add("str_select_all_cleanup", u"Seleziona tutto")
    add("str_delete", u"Elimina")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Cancella")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nome")
    add("str_lst_date", u"Data")        
    add("str_lst_progress", u"Progresso")
    add("str_lst_state", u"Stato")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Collocazione")
    add("str_lst_episode", u"Episodio")
    add("str_lst_playlist", u"Playlist")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Sottoscritto")
    add("str_disabled", u"Disabilitato")
    add("str_newly-subscribed", u"Nuova sottoscrizione")
    add("str_unsubscribed", u"Non sottoscritto")
    add("str_preview", u"Anteprima")
    add("str_force", u"Force")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Scegliere un nome per il file")
    add("str_subs_exported", u"Sottoscrizioni esportate.")
    
    ## Preferences Dialog
    add("str_preferences", u"Preferenze")
    
    add("str_save", u"Salva")
    add("str_cancel", u"Cancella")
    
    # General
    add("str_general", u"Generale")
    add("str_gen_options_expl", u"Imposta le opzioni generali per il programma %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Mostra %s nella system tray all'avvio" % PRODUCT_NAME)

    add("str_run_check_startup", u"Esegui un controllo per nuovi podcast all'avvio del programma")
    add("str_play_after_download", u"Riproduci immediatamente i file a scaricamento completato")
    add("str_location_and_storage", u"Gestione collocazione e salvataggio contenuti")
    add("str_stop_downloading", u"Interrompi lo scaricamento se l'harddisk raggiunge lo spazio di")
    add("str_bad_megabyte_limit_1", u"Il limite di megabyte impostato non sembra essere un valore intero")
    add("str_bad_megabyte_limit_2", u"Si prega di riprovare.")

    add("str_download_folder", u"Scarica i podcast in questa cartella")
    add("str_browse", u"Seleziona")
    add("str_bad_directory_pref_1", u"Impossibile trovare la cartella specificata.")
    add("str_bad_directory_pref_2", u"Creare la cartella e riprovare.")

    
    # Threading
    add("str_threads", u"Processi")
    add("str_multiple_download", u"Impostazioni di scaricamento multiplo")
    add("str_max_feedscans", u"numero massimo di processi di scansione feed per sessione")
    add("str_max_downloads", u"numero massimo di download per sessione")
   
    # Network settings
    add("str_networking", u"Impostazioni di rete")
    add("str_coralize_urls", u"Coralize URLs (experimental)")
    add("str_proxy_server", u"Usa server proxy")
    add("str_proxy_address", u"Indirizzo")
    add("str_proxy_port", u"Porta")
    add("str_proxy_username", u"Username")
    add("str_proxy_password", u"Password")
    add("str_bad_proxy_pref", u"E' stato abilitato il supporto proxy senza specificare un host o una porta. Ritornare alle impostazioni di rete ed impostare l'host e la porta per il proxy.")

    # Player
    add("str_player", u"Player")
    add("str_choose_a_player", u"Scegli un player")
    add("str_no_player", u"Nessun player")
    
    # Advanced
    add("str_advanced", u"Avanzate")
    add("str_options_power_users", u"L'utilizzo di queste opzioni è consigliato ad Utenti Esperti")
    add("str_run_command_download", u"Esegui questo comando dopo ogni download")
    add("str_rcmd_full_path", u"%f = Percorso completo al file scaricato")
    add("str_rcmd_podcast_name", u"%n = Nome podcast")
    add("str_other_advanced_options", u"Altre opzioni avanzate")
    add("str_show_log", u"Mostra la tab dei log nel programma")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titolo")
    add("str_url", u"URL")
    add("str_goto_subs", u"Vai alla tab delle sottoscrizioni per visualizzare questo episodio")
    add("str_feed_save", u"Salva")
    add("str_feed_cancel", u"Cancella")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Abilita scheduler")
    add("str_sched_select_type", u"Seleziona i bottoni sottostanti per controllare ad un orario specifico o ad intervalli regolari:")
    add("str_check_at_specific_times", u"Controlla ad orari specifici")
    add("str_check_at_regular_intervals", u"Controlla ad intervalli regolari")
    add("str_repeat_every:", u"Ripeti ogni:")
    add("str_latest_run", u"Ultimo avvio:")
    add("str_next_run", u"Prossimo avvio:")
    add("str_not_yet", u"Non ancora")
    #--- Cancel
    add("str_save_and_close", u"Salva e chiudi")
    #--- Save

    add("str_time_error", u"Uno degli orari pianificati non risulta corretto. esempio di formato corretto: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Controlla nuovi podcast premendo il bottone verde")
    add("str_last_check", u"Ultimo controllo completato il")
    add("str_of", u"di")
    add("str_item", u"elemento")
    add("str_items", u"elementi")
    add("str_downloading", u"in fase di scaricamento")
    add("str_downloaded", u"scaricati")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosure")
    add("str_fetched", u"letto")
    add("str_loading_mediaplayer", u"Caricamento media player in corso...")
    add("str_loaded_mediaplayer", u"Caricamento media player completato...")        
    add("str_initialized", u"%s pronto" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"E' necessario riavviare il programma per aggiornare la localizzazione. Clicca OK per procedere, cancella per continuare.")
    add("str_really_quit", u"Scaricamento in corso. Confermi l'uscita?");
    add("str_double_check", u"Sembra che uno scaricamento sia in corso.");
    
    # check for update
    add("str_new_version_ipodder", u"E' disponibile una nuova versione di %s, premi Ok per aprire la pagina di download." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"La versione di %s in uso è la più recente" % PRODUCT_NAME)
    add("str_other_copy_running", u"Un'altra istanza di %s è in esecuzione. Attendere il completamento o chiudere l'istanza." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Controlla Ora")        
    add("str_open_ipodder", u"Apri %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Scansione feed in corso")

    # Feed right-click menu
    add("str_remove", u"Rimuovi")        
    add("str_open_in_browser", u"Apri nel browser")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Riproduci episodio in mediaplayer")
    add("str_clear_selected", u"Rimuovi elementi selezionati")
    




