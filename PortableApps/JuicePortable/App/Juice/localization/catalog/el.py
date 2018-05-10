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

    add("str_username", u"Όνομα Χρήστη")
    add("str_password", u"Κωδικός")
    add("str_missing_proxy_password", u"Ένα όνομα χρήστη για διακομιστή μεσολάβησης (proxy) ορίστηκε, αλλά όχι και ένας κωδικός. \n" \
        u"Παρακαλώ σβήστε το όνομα χρήστη, ή δώστε ένα κωδικό.")

    add("str_goto_background_on_close_title", u"Ορισμός τρόπου τερματισμού")
    add("str_goto_background_on_close_warn", \
        u"Το %s μπορεί να συνεχίσει διακριτικά την λειτουργία του μετά το κλείσιμο. \n" \
        u"Διαφορετικά μπορεί να τερματίσει την λειτουργία του.  Θα θέλατε το %s \n" \
        u"να εξακολουθήσει να λειτουργεί;" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"Διακριτική λειτουργία με το κλείσιμο του κυρίως παραθύρου.")
    add("str_yes", u"Ναι")
    add("str_no", u"Όχι")
    add("str_dont_ask", u"Να μην ερωτηθώ ξανά")
    add("str_ok", u"Επιβεβαίωση")
    add("str_hide_window", u"Απόκρυψη Παραθύρου")
    add("str_hide_tray_icon", u"Απόκρυψη Εικονιδίου στη Γραμμή Εργασίας")
    add("str_show_window", u"Εμφάνιση Παραθύρου")

    add("str_catchup_pref", u"Η Αναπλήρωση (catch-up) προσπερνά τα παλιότερα επεισόδια, οριστικά.")
    add("str_set_catchup_title", u"Ορισμός τρόπου Αναπλήρωσης")
    add("str_set_catchup_description", \
        u"Όταν ελέγχει σε κατάσταση Αναπλήρωσης, το %s προσπερνά όλα εκτός από τα πιο πρόσφατα \n" \
        u"στοιχεία σε κάθε Feed. Παρακαλώ, διαλέξτε τι να κάνει το %s με τα \n" \
        u"προσπερασμένα στοιχεία." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"Προσπέρασμα Οριστικά")
    add("str_skip_temporarily", u"Προσπέρασμα μόνο αυτή τη φορά")
    
    add("str_set_oneclick_handler", u"Ορισμός ανάληψης με ένα κλίκ")
    add("str_set_oneclick_handler_warn",\
        u"Το %s αυτή την στιγμή δεν έχει ρυθμιστεί να αναλαμβάνει Άμεσες Συνδρομές (με ένα κλίκ) σε Podcasts. \n" \
        u"Θέλετε να ρυθμιστεί το %s να ξεκινά όταν κάνετε κλίκ σε Άμεσες Συνδρομές (με ένα κλίκ);" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"Πάντα να χρησιμοποιείται το %s για άμεση (με ένα κλίκ) συνδρομή" % PRODUCT_NAME)
    
    add("str_txt_feedmanager", u"Συμβατοί Διαχειριστές Feed:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Εύρεση Podcasts, Άμεση Συνδρομή (με ένα κλίκ)")

    add("str_open_downloads_folder", u"Άνοιγμα Φακέλου κατεβασμένων αρχείων")
    add("str_chkupdate_on_startup", u"Έλεγχος για νέα έκδοση του προγράμματος με το ξεκίνημα.")
    add("str_bad_feedmanager_url", u"Παρακαλώ δώστε μία έγκυρη διεύθυνση (URL) για τον Διαχειριστή Feed.")
    add("str_feed_manager", u"Διαχειριστής Feed")
    add("str_feedmanager_enable", u"Συγχρονισμός των συνδρομών μου μέσω μίας απομακρυσμένης υπηρεσίας")
    add("str_opml_url", u"Διεύθυνση (URL) OPML")
    add("str_set_track_genre", u"Ορισμός του είδους του κομματιού ως")
    add("str_auto_delete", u"Αυτόματη διαγραφή Επεισοδίων παλιότερων από")
    add("str_days_old", u"ημέρες")
    
    add("str_show_notes", u"Εμφάνιση Σημειώσεων")
    add("str_close", u"Κλείσιμο")
    
    add("str_critical_error_minspace_exceeded", \
        u"Το Κατέβασμα προσπεράστηκε; ο ελεύθερος χώρος είναι %dMB λιγότερος " \
        u"από τα ελάχιστα %dMB.  Παρακαλώ, ελευθερώστε χώρο " \
        u"στο δίσκο σας με την Εκκαθάριση ή προσαρμόστε τις ρυθμίσεις Διαχείρισης " \
        u"Αποθήκευσης στις Επιλογές")
    add("str_critical_error_unknown", u"Άγνωστο σφάλμα κατά το κατέβασμα αρχείων.")
    
    add("str_error_checking_new_version", u"Υπήρξε ένα σφάλμα κατά τον έλεγχο για νέα έκδοση. Παρακαλώ προσπαθήστε ξανά αργότερα.")
    add("str_hours", u"ώρες")
    add("str_minutes", u"λεπτά")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Διερεύνηση")
    add("str_scanned", u"Διερευνήθηκαν")
    add("str_feed", u"Feed")
    add("str_feeds", u"Feeds")
    
    add("str_downloading_new_episodes", u"Κατέβασμα νέων Επεισοδίων")
    add("str_sched_specific", u"Έλεγχος σε συγκεκριμένες χρονικές στιγμές")
    add("str_sched_reg", u"Έλεγχος ανά τακτά διαστήματα")
    add("str_repeat_every", u"Επανάληψη κάθε")
    add("str_next_run_label", u"Επόμενη εκτέλεση:")
    
    add("str_license", u"Αυτό το πρόγραμμα είναι ελεύθερο λογισμικό, μπορείτε να το επαναδιανέμετε και/ή να το τροποποιήσετε σύμφωνα με τους όρους της Άδειας Χρήσης GNU General Public License όπως αυτή εκδίδεται από το Free Software Foundation στην Δεύτερη (2) εκδοσή της ή κατ'επιλογή σας όποια μεταγενέστερη άδεια. Αυτό το πρόγραμμα διανέμεται με την ελπίδα πως θα είναι χρήσιμο, αλλά χωρίς καμία εγγύηση, χωρίς καν την υπονοούμενη εγγύηση εμπορικής διαθεσιμότητας ή καταλληλότητας για συγκεκριμένο σκοπό. \n\nΔείτε την GNU General Public License Άδεια Χρήσης για περισσότερες πληροφορίες.")

    add("str_donate", u"Δωρίστε στο %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Το %s είναι ιδιοκτησία της παγκόσμιας κοινότητας των χρηστών του. Είναι σημαντικό να διατηρηθεί αυτός ο νέος τρόπος πρόσβασης σε μέσα επικοινωνίας ελεύθερος. Οποιοδήποτε χρηματικό ποσό θα έδινε χαρά και ενθάρρυνση στην ομάδα του %s για την ανάπτυξη νέων λειτουργιών και υπηρεσιών." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_donate_yes", u"Ναι, επίσκεψη στην ιστοσελίδα δωρεών τώρα!")
    add("str_donate_two_weeks", u"Θέλω να το δοκιμάσω λίγο ακόμα, εμφάνιση αυτού του μηνύματος ξανά μετά από δύο εβδομάδες.")
    add("str_donate_already", u"Έχω ήδη δωρήσει, μην εμφανιστεί ξανά αυτό το μήνυμα.")
    add("str_donate_no", u"Όχι, δεν θέλω να κάνω οποιαδήποτε δωρεά ποτέ, να μην εμφανιστεί ξανά αυτό το μήνυμα.")
    add("str_donate_one_day", u"Όχι τώρα, υπενθυμίστε μου πάλι αύριο.")
    add("str_donate_proceed", u"Συνέχεια")

    add("str_scheduler_dialog", u"Προγραμματιστής")
    add("str_scheduler_tab", u"Ρυθμίσεις")

    add("str_select_import_file", u"Επιλογή αρχείου προς εισαγωγή")    
    add("str_add_feed_dialog", u"Προσθήκη ενός Feed")
    add("str_edit_feed", u"Ιδιότητες Feed")

    add("str_really_delete", u"Επιβεβαίωση διαγραφής")

    add("str_license_caption", u"Άδεια Χρήσης")

    add("str_ep_downloaded", u"Κατεβασμένο")
    add("str_ep_skipped_removed_other", u"Προσπερασμένο/Διαγραμμένο/Άλλο")
    add("str_ep_to_download", u"Προς Κατέβασμα")

    add("str_select_none_cleanup", u"Select none")
    add("str_submit_lang", u"Υποβολή Γλώσσας")
    
    add("str_dltab_live", u"Ενεργά κατεβάσματα αρχείων: ")
    add("str_dltab_ul_speed", u"Ταχύτητα ανεβάσματος: ")
    add("str_dltab_dl_speed", u"Ταχύτητα κατεβάσματος: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Αρχείο")
    add("str_import_opml", u"Εισαγωγή Feed από opml...")
    add("str_export_opml", u"Εξαγωγή των Feed ως opml...")
    add("str_preferences_menubar", u"Επιλογές...")
    add("str_close_window", u"Κλείσιμο παραθύρου")
    add("str_quit", u"Εγκατάλειψη")

    add("str_edit", u"Επεξεργασία")
    add("str_select_all", u"Επιλογή όλων")

    add("str_tools", u"Εργαλεία")
    add("str_check_all", u"Έλεγχος όλων")
    add("str_catch_up", u"Αναπλήρωση")
    add("str_check_selected", u"Έλεγχος επιλεγμένων")
    add("str_add_feed", u"Προσθήκη ενός Feed...")
    add("str_remove_selected", u"Αφαίρεση ενός Feed")
    add("str_feed_properties", u"Ιδιότητες Feed...")
    add("str_scheduler_menubar", u"Προγραμματιστής...")
    
    add("str_select_language", u"Επιλογή γλώσσας")

    ## these are also used for the tabs
    add("str_view", u"Προβολή")
    add("str_downloads", u"Κατέβασμα Αρχείων")
    add("str_subscriptions", u"Συνδρομές")
    add("str_podcast_directory", u"Ευρετήριο Podcast")
    add("str_cleanup", u"Εκκαθάριση")

    add("str_help", u"Βοήθεια")
    add("str_online_help", u"Online Βοήθεια")
    add("str_faq", u"Συχνές Ερωτήσεις")
    add("str_check_for_update", u"Έλεγχος νέας έκδοσης...")
    add("str_report_a_problem", u"Αναφορές Προβλημάτων")
    add("str_goto_website", u"Επίσκεψη στο Website")
    add("str_make_donation", u"Δωρεές")
    add("str_menu_license", u"Άδεια Χρήσης...")
    add("str_about", u"Αναφορικά...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Απομάκρυνση επιλεγμένων αντικειμένων")
    add("str_cancel_selected_download", u"Ακύρωση επιλεγμένου κατεβάσματος αρχείου")
    add("str_pause_selected", u"Παύση επιλεγμένων")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Νέο")
    add("str_dl_state_queued", u"Στη σειρά")
    add("str_dl_state_downloading", u"Κατεβαίνει")
    add("str_dl_state_downloaded", u"Κατεβασμένο")
    add("str_dl_state_cancelled", u"Ακυρώθηκε")
    add("str_dl_state_finished", u"Ολοκλήρωσε")
    add("str_dl_state_partial", u"Τμηματικά κατεβασμένο")
    add("str_dl_state_clearing", u"Clearing")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Έλεγχος για νέα Podcasts")
    add("str_catch_up_mode", u"Catch-up - Κατέβασμα μόνο των τελευταίων νέων συνδρομών")

    add("str_add_new_feed", u"Προσθήκη νέου feed");
    add("str_remove_selected_feed", u"Αφαίρεση επιλεγμένου Feed")
    add("str_properties", u"Ιδιότητες Feed")
    add("str_check_selected_feed", u"Έλεγχος/Κατέβασμα επιλεγμένου Feed")

    add("str_scheduler_on", u"Προγραμματιστής - Ενεργός")
    add("str_scheduler_off", u"Προγραμματιστής - Ανενεργός")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Επόμενη εκτέλεση:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Κατέβασμα πληροφοριών Επεισοδίων...")
    add("str_no_episodes_found", u"Δεν βρέθηκαν επεισόδια.")


    ## Directorytab Toolbar
    add("str_refresh", u"Ανανέωση")
    add("str_open_all_folders", u"Άνοιγμα όλων των φακέλων")
    add("str_close_all_folders", u"Κλείσιμο όλων των φακέλων")
    add("str_add", u"Προσθήκη")

    ## Directorytab Other items
    add("str_directory_description", u"Κάντε κλίκ σε ένα Feed του καταλόγου ή εισάγετε ένα στη φόρμα και κάντε κλίκ Προσθήκη")




    ## Cleanuptab items
    add("str_select_a_feed", u"Επιλέξτε ένα Feed")
    add("str_refresh_cleanup", u"Ανανέωση")
    
    add("str_look_in", u"Αναζήτηση Επεισοδίων σε")        
    add("str_player_library", u"Βιβλιοθήκη Προγράμματος Αναπαραγωγής")
    add("str_downloads_folder", u"Φάκελος Κατεβασμένων αρχείων")
    add("str_delete_library_entries", u"Διαγραφή εισαγωγών βιβλιοθήκης")
    add("str_delete_files", u"Διαγραφή κατεβασμένων αρχείων")
    add("str_select_all_cleanup", u"Επιλογή όλων")
    add("str_delete", u"Διαγραφή")




    ## Logtab items
    add("str_log", u"Καταγραφή")
    add("str_clear", u"Εκκαθάριση")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Όνομα")
    add("str_lst_date", u"Ημερομηνία")        
    add("str_lst_progress", u"Πρόοδος")
    add("str_lst_state", u"Κατάσταση")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Τοποθεσία")
    add("str_lst_episode", u"Επεισόδιο")
    add("str_lst_playlist", u"Λίστα Αναπαραγωγής")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Συνδρομή")
    add("str_disabled", u"Απενεργοποιημένο")
    add("str_newly-subscribed", u"Νέα Συνδρομή")
    add("str_unsubscribed", u"Ακυρωμένη Συνδρομή")
    add("str_preview", u"Προεσκόπηση")
    add("str_force", u"Εξαναγκασμός")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Επιλέξτε όνομα για το αρχείο προς εξαγωγή")
    add("str_subs_exported", u"Οι Συνδρομές έχουν εξαχθεί.")
    
    ## Preferences Dialog
    add("str_preferences", u"Επιλογές")
    
    add("str_save", u"Αποθήκευση")
    add("str_cancel", u"Άκυρο")
    
    # General
    add("str_general", u"Γενικά")
    add("str_gen_options_expl", u"Καθορισμός γενικών επιλογών για την εφαρμογή %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Στην εκκίνηση να εμφανίζεται το %s στο Πλαίσιο Συστήματος" % PRODUCT_NAME)

    add("str_run_check_startup", u"Έλεγχος για νέα Podcasts με την εκκίνηση του προγράμματος")
    add("str_play_after_download", u"Αναπαραγωγή κατεβασμένων αρχείων αμέσως μετά την λήψη τους")
    add("str_location_and_storage", u"Ρυθμίσεις Διαχείρισης Αποθήκευσης")
    add("str_stop_downloading", u"Τερματισμός κατεβάσματος αρχείων σε περίπτωση που ο ελεύθερος χώρος του Σκληρού Δίσκου φτάσει τα")
    add("str_bad_megabyte_limit_1", u"Λυπάμαι, το ελάχιστο όριο ΜΒ πρέπει να είναι ακέραιος αριθμός")
    add("str_bad_megabyte_limit_2", u"Παρακαλώ προσπαθήστε ξανά.")

    add("str_download_folder", u"Κατέβασμα Podcasts σε αυτόν τον φάκελο")
    add("str_browse", u"Αναζήτηση")
    add("str_bad_directory_pref_1", u"Λυπάμαι, δεν μπορεί να εντοπιστεί ο φάκελος που επιλέξατε")
    add("str_bad_directory_pref_2", u"Παρακαλώ δημιουργήστε τον και προσπαθήστε ξανά.")

    
    # Threading
    add("str_threads", u"Threading")
    add("str_multiple_download", u"Multiple download settings")
    add("str_max_feedscans", u"maximal threads for feedscanning per session")
    add("str_max_downloads", u"maximal downloads per session")
   
    # Network settings
    add("str_networking", u"Ρυθμίσεις Δικτύου")
    add("str_coralize_urls", u"Coralize URLs (πειραματικό)")
    add("str_proxy_server", u"Χρήση ενός διακομιστή μεσολάβησης (proxy server)")
    add("str_proxy_address", u"Διεύθυνση")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Όνομα Χρήστη")
    add("str_proxy_password", u"Κωδικός")
    add("str_bad_proxy_pref", u"Έχετε ενεργοποιήσει την υποστήριξη για διακομιστή μεσολάβησης (proxy) αλλά δεν δώσατε Διεύθυνση και port.  Παρακαλώ επιστρέψτε στις Ρυθμίσεις Δικτύου και ορίστε Διεύθυνση και port.")

    # Player
    add("str_player", u"Πρόγραμμα Αναπαραγωγής")
    add("str_choose_a_player", u"Επιλογή προγράμματος αναπαραγωγής")
    add("str_no_player", u"Κανένα πρόγραμμα αναπαραγωγής")
    
    # Advanced
    add("str_advanced", u"Για Προχωρημένους")
    add("str_options_power_users", u"Αυτές οι επιλογές μπορούν να χρησιμοποιηθούν από Προχωρημένους Χρήστες")
    add("str_run_command_download", u"Εκτέλεση αυτής της εντολής μετά από κάθε κατέβασμα αρχείου")
    add("str_rcmd_full_path", u"%f = Πλήρης τοποθεσία δίσκου για το κατεβασμένο αρχείο")
    add("str_rcmd_podcast_name", u"%n = Όνομα Podcast")
    add("str_other_advanced_options", u"Άλλες προχωρημένες επιλογές")
    add("str_show_log", u"Εμφάνιση καρτέλας Καταγραφής")



    ## Feed Dialog (add/properties)
    add("str_title", u"Τίτλος")
    add("str_url", u"Διεύθυνση URL")
    add("str_goto_subs", u"Πηγαίνετε στην καρτέλα Συνδρομές για να δείτε τα επεισόδια αυτού του Feed")
    add("str_feed_save", u"Αποθήκευση")
    add("str_feed_cancel", u"Άκυρο")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Ενεργοποίηση Προγραμματιστή")
    add("str_sched_select_type", u"Επιλέξτε έλεγχο σε συγκεκριμένες χρονικές στιγμές ή ανά τακτά χρονικά διαστήματα:")
    add("str_check_at_specific_times", u"Έλεγχος στις παρακάτω συγκεκριμένες χρονικές στιγμές")
    add("str_check_at_regular_intervals", u"Έλεγχος ανά τακτά διαστήματα")
    add("str_repeat_every:", u"Επανάληψη κάθε:")
    add("str_latest_run", u"Πιο πρόσφατη εκτέλεση:")
    add("str_next_run", u"Επόμενη εκτέλεση:")
    add("str_not_yet", u"Όχι ακόμα")
    #--- Cancel
    add("str_save_and_close", u"Αποθήκευση και Κλείσιμο")
    #--- Save

    add("str_time_error", u"Κάποια από τις προγραμματισμένες στιγμές δεν είναι σωστή. Οι έγκυρες χρονικές στιγμές έχουν την μορφή:  10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Ελέγξτε για νέα Podcasts πατώντας το πράσινο κουμπί ελέγχου.")
    add("str_last_check", u"Ο τελευταίος έλεγχος ολοκληρώθηκε στις")
    add("str_of", u"of")
    add("str_item", u"αντικείμενο")
    add("str_items", u"αντικείμενα")
    add("str_downloading", u"κατεβαίνει")
    add("str_downloaded", u"κατεβασμένο")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"Άνοιγμα προγράμματος αναπαραγωγής...")
    add("str_loaded_mediaplayer", u"Το πρόγραμμα αναπαραγωγής ενεργοποιήθηκε...")        
    add("str_initialized", u"%s έτοιμο" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"Για να μεταφραστούν όλα τα κουμπιά ελέγχου του %s χρειάζεται επανεκκίνηση. Πατήστε Επιβεβαίωση για κλείσιμο, ή Άκυρο για συνέχεια." % PRODUCT_NAME)
    add("str_really_quit", u"Ένα κατέβασμα αρχείου είναι σε εξέλιξη. Σίγουρα να τερματίσει;");
    add("str_double_check", u"Φαίνεται πως κάποιο κατέβασμα αρχείου βρίσκεται σε εξέλιξη.");
    
    # check for update
    add("str_new_version_ipodder", u"Υπάρχει μία νέα έκδοση του %s, πατήστε Επιβεβαίωση για επίσκεψη στον ιστοχώρο κατεβάσματος." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Αυτή η έκδοση του %s είναι ενήμερη." % PRODUCT_NAME)
    add("str_other_copy_running", u"Ένα άλλο αντίγραφο του %s είναι ανοικτό. Παρακαλώ ανοίξτε το, περιμένετε να ολοκληρώσει, ή κλείστε το." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Έλεγχος Τώρα")        
    add("str_open_ipodder", u"Άνοιγμα %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Έλεγχος Feeds")

    # Feed right-click menu
    add("str_remove", u"Αφαίρεση")
    add("str_open_in_browser", u"Άνοιγμα στον Φυλλομετρητή")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Αναπαραγωγή επεισοδίου στο πρόγραμμα αναπαραγωγής ήχου")
    add("str_clear_selected", u"Εκκαθάριση επιλεγμένων αντικειμένων")
    



