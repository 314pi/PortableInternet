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

    ## REMOVED strings
    ##
    ## add("str_ensure_oneclick_handler", u"Always use %s for one-click subscription" % PRODUCT_NAME)
    ## add("str_set_oneclick_handler", u"Set one-click handler")
    ## add("str_set_oneclick_handler_warn",\
    ##    u"%s is not currently your one-click subscription handler for podcasts. \n" \
    ##    u"Should we set %s to launch from one-click subscription links?" % (PRODUCT_NAME,PRODUCT_NAME))

    
    ##_________________________________________________________
    ##
    ##     New strings
    ##_________________________________________________________

    add("str_copy_location", u"העתק מיקום")
    add("str_set_file_types", u"קבע סוגי קבצים")
    add("str_set_file_types_warn", \
        u"%s אינו מוגדר כרגע לעבודה עם מספר סוגי קבצים. \n" \
        u"האם ברצונך לקבוע אותם כעת?" % PRODUCT_NAME)
    add("str_subscription_options", u"אפשרויות מינוי בלחיצת כפתור:")
    add("str_enforce_settings", u"הכרח מאפיינים אלו בזמן הטעינה")
    add("str_file_types", u"סוגי קבצים")
    add("str_play_button_enqueues", u"כפתור הניגון מוסיף את הפרקים הנבחרים לתור")
    add("str_authentication", u"אימות")
    add("str_dl_state_skipped", u"דולג")
    add("str_dl_state_removed", u"הוסר")
    
    add("str_username", u"שם משתמש")
    add("str_password", u"סיסמא")
    add("str_missing_proxy_password", u"נקבע שם משתמש ל proxy ללא סיסמא. \n" \
        u"אנא מחק את שם המשתמש או הססמא.")

    add("str_goto_background_on_close_title", u"קבע התנהגות בסגירה")
    add("str_goto_background_on_close_warn", \
        u"%s יכול להמשיך לרוץ ברקע לאחר סגירת \n" \
        u"החלון הראשי.  לחילופין %s יכול לצאת.  האם ברצונך ש \n" \
        u"ימשיך לרוץ?" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"המשך ריצה ברקע לאחר סגירת החלון הראשי")
    add("str_yes", u"כן")
    add("str_no", u"לא")
    add("str_dont_ask", u"אל תשאל אותי פעם נוספת")
    add("str_ok", u"אישור")
    add("str_hide_window", u"הסתר חלון")
    add("str_hide_tray_icon", u"הסתר צלמית של ה Tray")
    add("str_show_window", u"הצג חלון")

    add("str_catchup_pref", u"השלמת חוסרים מדלגת על פרקים ישנים באופן קבוע")
    add("str_set_catchup_title", u"הגדר התנהגות 'השלמת חוסרים'")
    add("str_set_catchup_description", \
        u"בזמן השלמת חוסרים, %s ידלג על כולם מלבד הפרק האחרון \n" \
        u"בכל feed.  אנא הגדר כיצד על %s להתייחס לפרקים שדולגו \n" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"דלג באופן קבוע")
    add("str_skip_temporarily", u"דלג בפעם זו בלבד")
    
    add("str_txt_feedmanager", u"מנהלי feeds תואמים:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - חפש או סרוק פודקאסטים, מינוי בלחיצת כפתור")

    add("str_open_downloads_folder", u"פתח תיקיית הורדות")
    add("str_chkupdate_on_startup", u"בדוק לגרסאות חדשות של התוכנה בזמן העליה.")
    add("str_bad_feedmanager_url", u"אנא הכנס URL חוקי למנהל ה feeds.")
    add("str_feed_manager", u"Feeds מנהל")
    add("str_feedmanager_enable", u"סנכרן את המינויים שלי עם שירות מרוחק")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"Set track genre to")
    add("str_auto_delete", u"מחק בצורה אוטומאטית קבצים בני למעלה מ")
    add("str_days_old", u"ימים")
    
    add("str_show_notes", u"רשימות התוכנית")
    add("str_close", u"סגור")
    
    add("str_critical_error_minspace_exceeded", \
        u"הורדה דולגה; פנוי %dMB פחות " \
        u"מהמינימום %dMB.  אנא נקה מקום בכונן " \
        u"שלך באמצעות חלון הניקוי או עדכן את גבולות" \
        u"האחסון ב'הגדרות'")
    add("str_critical_error_unknown", u"חלה בעיה כלשהי בזמן ההורדה.")
    
    add("str_error_checking_new_version", u"חלה תקלה בזמן הבדיקה לגרסה חדשה של התוכנה, אנא נסה שנית מאוחר יותר")
    add("str_hours", u"שעות")
    add("str_minutes", u"דקות")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"סורק")
    add("str_scanned", u"סרוק")
    add("str_feed", u"feed")
    add("str_feeds", u"feeds")
    
    add("str_downloading_new_episodes", u"מוריד פרקים חדשים")
    add("str_sched_specific", u"בדוק בזמנים קבועים")
    add("str_sched_reg", u"בדוק במרווחי זמן קבועים")
    add("str_repeat_every", u"חזור בכל")
    add("str_next_run_label", u"ריצה הבאה:")
    
    add("str_license", u"זוהי תוכנה חופשית; אתה יכול להפיץ אותה מחדש ו/או לשנות אותה תחת התנאים של רשיון GNU General Public License כפי שמפורסם על-ידי ה Free Software Foundation; לפי גרסה 2 או כל גרסה מתקדמת יותר, כרצונך. תוכנה זו מופצת מתוך תקווה שהיא תהיה שימושית, אך ללא אחריות כלשהי; אפילו ללא האפשרות המרומזת של תאימות למסחר או לשימוש כלשהו. \n\nראה GNU General Public License לפרטים נוספים.")

    add("str_donate", u"תרום ל %s" % PRODUCT_NAME)
    add("str_donate_expl", u"ישנה חשיבות גדולה לשמירה של תוכנות מסוג זה חופשיות, ככלי תומך לחופש הביטוי. כל סכום של כסף יתרום למוטיבציה של המפתחים להוסיף שירותים ותכונות נוספים לתוכנה!")
    add("str_donate_yes", u"קח אותי לדף התרומות עכשיו!")
    add("str_donate_two_weeks", u"אני צריך לבדוק זאת, הצג לי חלון זה בעוד שבועיים")
    add("str_donate_already", u"כבר תרמתי, אל תציג בקשה זו פעם נוספת")
    add("str_donate_no", u"אינני מעוניין לתרום, אל תציג בקשה זו פעם נוספת")
    add("str_donate_one_day", u"לא עכשיו, בקש מחר פעם נוספת")
    add("str_donate_proceed", u"המשך")

    add("str_scheduler_dialog", u"מתאם זמנים")
    add("str_scheduler_tab", u"הגדרות")

    add("str_select_import_file", u"בחר קובץ לייבוא")    
    add("str_add_feed_dialog", u"הוסף Feed")
    add("str_edit_feed", u"תכונות Feed")

    add("str_really_delete", u"מחק באמת")

    add("str_license_caption", u"רשיון")

    add("str_ep_downloaded", u"ירד")
    add("str_ep_skipped_removed_other", u"דולג/הוסר/אחר")
    add("str_ep_to_download", u"להורדה")
    add("str_dl_state_to_download", u"להורדה")

    add("str_select_none_cleanup", u"נקה בחירה")
    add("str_submit_lang", u"שלח שפה")
    
    add("str_dltab_live", u"הורדות פעילות: ")
    add("str_dltab_ul_speed", u"קצב העלאה: ")
    add("str_dltab_dl_speed", u"קצב הורדה: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"קובץ")
    add("str_import_opml", u"יבא feeds מ opml...")
    add("str_export_opml", u"יצא feeds כ opml...")
    add("str_preferences_menubar", u"העדפות...")
    add("str_close_window", u"סגור חלון")
    add("str_quit", u"צא")

    add("str_edit", u"ערוך")
    add("str_select_all", u"בחר הכל")

    add("str_tools", u"כלים")
    add("str_check_all", u"בחר הכל")
    add("str_catch_up", u"השלם חוסרים")
    add("str_check_selected", u"בדוק את הבחורים")
    add("str_add_feed", u"הוסף Feed...")
    add("str_remove_selected", u"הסר Feed")
    add("str_feed_properties", u"תכונות Feed...")
    add("str_scheduler_menubar", u"מתאם זמנים...")
    
    add("str_select_language", u"בחר שפה")

    ## these are also used for the tabs
    add("str_view", u"תצוגה")
    add("str_downloads", u"הורדות")
    add("str_subscriptions", u"מינויים")
    add("str_podcast_directory", u"תיקיית פודקאסטים")
    add("str_cleanup", u"מחיקות")

    add("str_help", u"עזרה")
    add("str_online_help", u"עזרה מקוונת")
    add("str_faq", u"שאלות נפוצות")
    add("str_check_for_update", u"בדוק לעדכון...")
    add("str_report_a_problem", u"דווח על תקלה")
    add("str_goto_website", u"גלוש לאתר")
    add("str_make_donation", u"תרום לפרוייקט")
    add("str_menu_license", u"רשיון...")
    add("str_about", u"אודות...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"הסר עצמים שנבחרו")
    add("str_cancel_selected_download", u"בטל הורדות שנבחרו")
    add("str_pause_selected", u"הפסק זמנית הורדה של הפרקים")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"חדש")
    add("str_dl_state_queued", u"בתור")
    add("str_dl_state_downloading", u"מוריד")
    add("str_dl_state_downloaded", u"ירד")
    add("str_dl_state_cancelled", u"בוטל")
    add("str_dl_state_finished", u"הסתיים")
    add("str_dl_state_partial", u"ירד חלקית")
    add("str_dl_state_clearing", u"מנקה")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"בדוק לפרקים חדשים")
    add("str_catch_up_mode", u"השלם חוסרים - הורד את המינויים החדשים בלבד")

    add("str_add_new_feed", u"הוסף feed");
    add("str_remove_selected_feed", u"הסר feed שנבחר")
    add("str_properties", u"אפשרויות Feed")
    add("str_check_selected_feed", u"בדוק/הורד feed שנבחר")

    add("str_scheduler_on", u"מתאם זמנים - פעיל")
    add("str_scheduler_off", u"מתאם זמנים - מופסק")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"ריצה הבאה:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"מוריד מידע על הפרקים...")
    add("str_no_episodes_found", u"לא נמצאו פרקים.")


    ## Directorytab Toolbar
    add("str_refresh", u"רענן")
    add("str_open_all_folders", u"פתח את כל התיקיות")
    add("str_close_all_folders", u"סגור את כל התיקיות")
    add("str_add", u"הוסף")

    ## Directorytab Other items
    add("str_directory_description", u"בחר ב feed או הזן במקום המיועד לכך מעלה, והוסף.")




    ## Cleanuptab items
    add("str_select_a_feed", u"בחר ב feed")
    add("str_refresh_cleanup", u"רענן")
    
    add("str_look_in", u"בדוק לפרקים ב")        
    add("str_player_library", u"ספריית הנגן")
    add("str_downloads_folder", u"סיפריית הורדות")
    add("str_delete_library_entries", u"Delete library entries")
    add("str_delete_files", u"מחק קבצים שירדו")
    add("str_select_all_cleanup", u"בחר הכל")
    add("str_delete", u"מחק")




    ## Logtab items
    add("str_log", u"רישום")
    add("str_clear", u"מחק")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"שם")
    add("str_lst_date", u"תאריך")        
    add("str_lst_progress", u"התקדמות")
    add("str_lst_state", u"מצב")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"כתובת")
    add("str_lst_episode", u"פרק")
    add("str_lst_playlist", u"פודקאסט")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"מנוי")
    add("str_disabled", u"מנוטרל")
    add("str_newly-subscribed", u"מנוי חדש")
    add("str_unsubscribed", u"לא מנוי")
    add("str_preview", u"תצוגה מקדימה")
    add("str_force", u"הכרח")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"בחר שם לקובץ היצוא")
    add("str_subs_exported", u"מינויים יוצאו.")
    
    ## Preferences Dialog
    add("str_preferences", u"העדפות")
    
    add("str_save", u"שמור")
    add("str_cancel", u"בטל")
    
    # General
    add("str_general", u"כללי")
    add("str_gen_options_expl", u"קבע אפשרויות כלליות לתוכנה")
    add("str_hide_on_startup", u"בעליה, הצג את התוכנה ב ‎Tray בלבד")

    add("str_run_check_startup", u"בדוק בטעינת התוכנה אם יש פרקים חדשים")
    add("str_play_after_download", u"נגן פרק מייד לאחר הורדתו")
    add("str_location_and_storage", u"ניהול מיקום ואחסון")
    add("str_stop_downloading", u"הפסק הורדה אם המקום בכונן ירד מתחת לגבול")
    add("str_bad_megabyte_limit_1", u"גבול הגודל אינו נראה כמו מספר")
    add("str_bad_megabyte_limit_2", u"אנא נסה פעם נוספת.")

    add("str_download_folder", u"הורד פודקאסטים לתיקיה זו")
    add("str_browse", u"Browse")
    add("str_bad_directory_pref_1", u"לא נמצאה התיקייה שהוכנסה")
    add("str_bad_directory_pref_2", u"אנא צור אותה ונסה פעם נוספת")

    
    # Threading
    add("str_threads", u"מקביליות")
    add("str_multiple_download", u"הגדרות להורדה במקביל")
    add("str_max_feedscans", u"מספר feeds שיסרקו בהתחברות")
    add("str_max_downloads", u"מספר הורדות במקביל")
   
    # Network settings
    add("str_networking", u"הגדרות רשת")
    add("str_coralize_urls", u"צבע URLs (ניסיוני)")
    add("str_proxy_server", u"השתמש ב proxyserver")
    add("str_proxy_address", u"כתובת")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"שם משתמש")
    add("str_proxy_password", u"סיסמא")
    add("str_bad_proxy_pref", u"אפשרת תמיכה ב proxy אך לא קבעת כתובת ו port. אנא חזור להגדרות הרשת כדי לקבוע ערכים אלו.")

    # Player
    add("str_player", u"נגן")
    add("str_choose_a_player", u"בחר נגן")
    add("str_no_player", u"ללא נגן")
    
    # Advanced
    add("str_advanced", u"מתקדם")
    add("str_options_power_users", u"אפשרויות אלו נועדו למשתמש מתקדם")
    add("str_run_command_download", u"הרץ פקודה זו לאחר כל הורדה")
    add("str_rcmd_full_path", u"%f = נתיב מלא לקובץ המורד")
    add("str_rcmd_podcast_name", u"%n = שם הפודקאסט")
    add("str_other_advanced_options", u"אפשרויות מתקדמות נוספות")
    add("str_show_log", u"הצג לשונית רישום ביישום")



    ## Feed Dialog (add/properties)
    add("str_title", u"כותרת")
    add("str_url", u"URL")
    add("str_goto_subs", u"גש ללשונית המינויים כדי לצפות בפרקים של פודקאסט זה")
    add("str_feed_save", u"שמור")
    add("str_feed_cancel", u"בטל")

    ## Scheduler Dialog
    add("str_enable_scheduler", u"אפשר תיאום זמנים")
    add("str_sched_select_type", u"בחר למטה אם לבדוק בזמנים קבועים ביום, או במרווח זמן קבוע:")
    add("str_check_at_specific_times", u"בדוק בזמנים אלו")
    add("str_check_at_regular_intervals", u"בדוק במרווחי זמן קבועים")
    add("str_repeat_every:", u"חזור בכל:")
    add("str_latest_run", u"ריצה אחרונה:")
    add("str_next_run", u"ריצה הבאה:")
    add("str_not_yet", u"עדיין לא")
    #--- Cancel
    add("str_save_and_close", u"שמור וסגור")
    #--- Save

    add("str_time_error", u"נראה שאחד מתיאומי הזמנים אינו תקין. זמנים תקינים נראים כך: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"בדוק לפודקאסטים חדשים על-ידי לחיצה על הכפתור הירוק")
    add("str_last_check", u"בדיקה אחרונה הושלמה ב")
    add("str_of", u"מתוך")
    add("str_item", u"עצם")
    add("str_items", u"עצמים")
    add("str_downloading", u"מוריד")
    add("str_downloaded", u"ירד")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"טוען את נגן המדיה...")
    add("str_loaded_mediaplayer", u"נטען נגן המדיה...")        
    add("str_initialized", u"התוכנה מוכנה")




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"כדי לשנות שפה יש להתחיל מחדש את התוכנה. לחץ על אישור כדי להתחיל מחדש בצורה מסודרת, או על ביטול כדי להמשיך.")
    add("str_really_quit", u"ישנו קובץ בהורדה, באמת לצאת?");
    add("str_double_check", u"נראה שקובץ נמצא בהורדה.");
    
    # check for update
    add("str_new_version_ipodder", u"ישנה גרסה חדשה של התוכנה, בחר באישור כדי לגלוש לאתר ההורדה")
    add("str_no_new_version_ipodder", u"גרסה זו של התוכנה היא העדכנית")
    add("str_other_copy_running", u"התוכנה כבר רצה. אנא צא מהריצה הקיימת כדי להריץ את התוכנה שנית")

    # Windows taskbar right-click menu
    add("str_check_now", u"בדוק כעת")        
    add("str_open_ipodder", u"פתח %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"סורק feeds")

    # Feed right-click menu
    add("str_remove", u"הסר")        
    add("str_open_in_browser", u"פתח בדפדפן")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"נגן פרק בנגן המדיה")
    add("str_clear_selected", u"נקה פרקים שנבחרו")
    









