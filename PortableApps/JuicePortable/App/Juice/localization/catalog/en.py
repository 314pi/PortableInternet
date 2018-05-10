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
    ##    u"Should we set iPodder to launch from one-click subscription links?" % PRODUCT_NAME)

    
    ##_________________________________________________________
    ##
    ##     New strings
    ##_________________________________________________________

    add("str_sort_cleanup_by_size", u"Sort cleanup tab by size.")
    add("str_copy_location", u"Copy Location")
    add("str_set_file_types", u"Set file types")
    add("str_set_file_types_warn", \
        u"%s is not currently set to handle some file types. \n" \
        u"Would you like to set them now?" % PRODUCT_NAME)
    add("str_subscription_options", u"One-click Subscription options:")
    add("str_enforce_settings", u"Enforce these settings at startup")
    add("str_file_types", u"File Types")
    add("str_play_button_enqueues", u"Play button enqueues selected track")
    add("str_authentication", u"Authentication")
    add("str_dl_state_skipped", u"Skipped")
    add("str_dl_state_removed", u"Removed")
    
    add("str_username", u"Username")
    add("str_password", u"Password")
    add("str_missing_proxy_password", u"A proxy username was set but no proxy password. \n" \
        u"Please either clear the username or enter a password.")

    add("str_goto_background_on_close_title", u"Set close behavior")
    add("str_goto_background_on_close_warn", \
        u"%s can continue running in the background after its main window \n" \
        u"is closed.  Or %s can quit.  Would you like %s to continue \n" \
        u"running?" % (PRODUCT_NAME,PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"Continue running in the background when I close the main window")
    add("str_yes", u"Yes")
    add("str_no", u"No")
    add("str_dont_ask", u"Don't ask me again")
    add("str_ok", u"OK")
    add("str_hide_window", u"Hide window")
    add("str_hide_tray_icon", u"Hide Tray Icon")
    add("str_show_window", u"Show window")

    add("str_catchup_pref", u"Catchup skips older episodes permanently")
    add("str_set_catchup_title", u"Set catchup behavior")
    add("str_set_catchup_description", \
        u"When checking in Catchup mode, %s will skip all but the top \n" \
        u"item in each feed.  Please specify how %s should treat the \n" \
        u"skipped items." % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"Skip permanently")
    add("str_skip_temporarily", u"Skip this time only")
    
    add("str_txt_feedmanager", u"Compatible feedmanagers:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Search or browse podcasts, single click subscribing")

    add("str_open_downloads_folder", u"Open downloads folder")
    add("str_chkupdate_on_startup", u"Check for new versions of the application at startup.")
    add("str_bad_feedmanager_url", u"Please enter a valid URL for the feed manager.")
    add("str_feed_manager", u"Feed manager")
    add("str_feedmanager_enable", u"Synchronize my subscriptions from a remote service")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"Set track genre to")
    add("str_auto_delete", u"Automatically delete episodes more than")
    add("str_days_old", u"days old")
    
    add("str_show_notes", u"Show Notes")
    add("str_close", u"Close")
    
    add("str_critical_error_minspace_exceeded", \
        u"Download skipped; free space %dMB less " \
        u"than min %dMB.  Please free up space on " \
        u"your disk using Cleanup or adjust the storage " \
        u"management settings in Preferences")
    add("str_critical_error_unknown", u"Unknown critical error while downloading.")
    
    add("str_error_checking_new_version", u"We're sorry, but there was an error checking for a new version.  Please try again later.")
    add("str_hours", u"hours")
    add("str_minutes", u"minutes")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Scanning")
    add("str_scanned", u"Scanned")
    add("str_feed", u"feed")
    add("str_feeds", u"feeds")
    
    add("str_downloading_new_episodes", u"Downloading new episodes")
    add("str_sched_specific", u"Check at specific times")
    add("str_sched_reg", u"Check at regular intervals")
    add("str_repeat_every", u"Repeat every")
    add("str_next_run_label", u"Next run:")
    
    add("str_license", u"This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.")

    add("str_donate", u"Donate to Juice")
    add("str_donate_expl", u"It's important to keep community-owned Juice applications online and keep this new way of consuming media free as in speech. Any amount of money will make the team happy and encourage them to work on new features and services!")
    add("str_donate_yes", u"Yes, take me to the donations page now!")
    add("str_donate_two_weeks", u"I still have to check it a bit more, show this again in two weeks")
    add("str_donate_already", u"I allready made a donation, don't show this dialog again")
    add("str_donate_no", u"No, I don't want to donate, never show this dialog again")
    add("str_donate_one_day", u"Not now, notify me again in 1 day")
    add("str_donate_proceed", u"Proceed")

    add("str_scheduler_dialog", u"Scheduler")
    add("str_scheduler_tab", u"Settings")

    add("str_select_import_file", u"Select import file")    
    add("str_add_feed_dialog", u"Add a Feed")
    add("str_edit_feed", u"Feed properties")

    add("str_really_delete", u"Really delete")

    add("str_license_caption", u"License")

    add("str_ep_downloaded", u"Downloaded")
    add("str_ep_skipped_removed_other", u"Skipped/Removed/OtherFeed")
    add("str_dl_state_to_download", u"To Download")

    add("str_select_none_cleanup", u"Select none")
    add("str_submit_lang", u"Submit a language")
    
    add("str_dltab_live", u"Live downloads: ")
    add("str_dltab_ul_speed", u"Upload speed: ")
    add("str_dltab_dl_speed", u"Download speed: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"File")
    add("str_import_opml", u"Import feeds from opml...")
    add("str_export_opml", u"Export feeds as opml...")
    add("str_preferences_menubar", u"Preferences...")
    add("str_close_window", u"Close window")
    add("str_quit", u"Quit")

    add("str_edit", u"Edit")
    add("str_select_all", u"Select all")

    add("str_tools", u"Tools")
    add("str_check_all", u"Check all")
    add("str_catch_up", u"Catch-up")
    add("str_check_selected", u"Check selected")
    add("str_add_feed", u"Add a Feed...")
    add("str_remove_selected", u"Remove Feed")
    add("str_feed_properties", u"Feed properties...")
    add("str_scheduler_menubar", u"Scheduler...")
    
    add("str_select_language", u"Select language")

    ## these are also used for the tabs
    add("str_view", u"View")
    add("str_downloads", u"Downloads")
    add("str_subscriptions", u"Subscriptions")
    add("str_podcast_directory", u"Podcast directory")
    add("str_cleanup", u"Cleanup")

    add("str_help", u"Help")
    add("str_online_help", u"Online Help")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Check for Update...")
    add("str_report_a_problem", u"Report a Problem")
    add("str_goto_website", u"Go to the Website")
    add("str_make_donation", u"Make a Donation")
    add("str_menu_license", u"License...")
    add("str_about", u"About...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Remove selected items")
    add("str_cancel_selected_download", u"Cancel selected download")
    add("str_pause_selected", u"Pause selected")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"New")
    add("str_dl_state_queued", u"Queued")
    add("str_dl_state_downloading", u"Downloading")
    add("str_dl_state_downloaded", u"Downloaded")
    add("str_dl_state_cancelled", u"Cancelled")
    add("str_dl_state_finished", u"Finished")
    add("str_dl_state_partial", u"Partially downloaded")
    add("str_dl_state_clearing", u"Clearing")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Check for new podcasts")
    add("str_catch_up_mode", u"Catch-up - Only download the last new subscriptions")

    add("str_add_new_feed", u"Add new feed");
    add("str_remove_selected_feed", u"Remove selected feed")
    add("str_properties", u"Feed Properties")
    add("str_check_selected_feed", u"Check/Download selected feed")

    add("str_scheduler_on", u"Scheduler - On")
    add("str_scheduler_off", u"Scheduler - Off")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Next run:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Downloading episode info...")
    add("str_no_episodes_found", u"No episodes found.")


    ## Directorytab Toolbar
    add("str_refresh", u"Refresh")
    add("str_open_all_folders", u"Open all folders")
    add("str_close_all_folders", u"Close all folders")
    add("str_add", u"Add")

    ## Directorytab Other items
    add("str_directory_description", u"Click on a feed in the tree or type/paste in the space above then click add.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Select a feed")
    add("str_refresh_cleanup", u"Refresh")
    
    add("str_look_in", u"Look for episodes in")        
    add("str_player_library", u"Player library")
    add("str_downloads_folder", u"Downloads folder")
    add("str_delete_library_entries", u"Delete library entries")
    add("str_delete_files", u"Delete downloaded files")
    add("str_select_all_cleanup", u"Select all")
    add("str_delete", u"Delete")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Clear")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Name")
    add("str_lst_date", u"Date")        
    add("str_lst_progress", u"Progress")
    add("str_lst_state", u"State")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Location")
    add("str_lst_episode", u"Episode")
    add("str_lst_playlist", u"Playlist")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Subscribed")
    add("str_disabled", u"Disabled")
    add("str_newly-subscribed", u"Newly Subscribed")
    add("str_unsubscribed", u"Unsubscribed")
    add("str_preview", u"Preview")
    add("str_force", u"Force")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Choose a name for the export file")
    add("str_subs_exported", u"Subscriptions exported.")
    
    ## Preferences Dialog
    add("str_preferences", u"Preferences")
    
    add("str_save", u"Save")
    add("str_cancel", u"Cancel")
    
    # General
    add("str_general", u"General")
    add("str_gen_options_expl", u"Set the general options for the %s application" % PRODUCT_NAME)
    add("str_hide_on_startup", u"At startup only show %s in the system tray" % PRODUCT_NAME)

    add("str_run_check_startup", u"Run a check for new podcasts when the application is started")
    add("str_play_after_download", u"Play downloads right after they're downloaded")
    add("str_location_and_storage", u"Location and storage management")
    add("str_stop_downloading", u"Stop downloading if harddisk reaches a minimal of")
    add("str_bad_megabyte_limit_1", u"Sorry, the megabyte limit doesn't look like an integer")
    add("str_bad_megabyte_limit_2", u"Please try again.")

    add("str_download_folder", u"Download podcasts into this folder")
    add("str_browse", u"Browse")
    add("str_bad_directory_pref_1", u"Sorry, we couldn't find the directory you entered")
    add("str_bad_directory_pref_2", u"Please create it and try again.")

    
    # Threading
    add("str_threads", u"Threading")
    add("str_multiple_download", u"Multiple download settings")
    add("str_max_feedscans", u"maximal threads for feedscanning per session")
    add("str_max_downloads", u"maximal downloads per session")
   
    # Network settings
    add("str_networking", u"Network settings")
    add("str_coralize_urls", u"Coralize URLs (experimental)")
    add("str_proxy_server", u"Use a proxyserver")
    add("str_proxy_address", u"Address")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Username")
    add("str_proxy_password", u"Password")
    add("str_bad_proxy_pref", u"You enabled proxy support but didn't provide a proxy host and port.  Please return to the Network settings tab and set the proxy host and port.")

    # Player
    add("str_player", u"Player")
    add("str_choose_a_player", u"Choose a player")
    add("str_no_player", u"No player")
    
    # Advanced
    add("str_advanced", u"Advanced")
    add("str_options_power_users", u"These options can be used by Power Users")
    add("str_run_command_download", u"Run this command after each download")
    add("str_rcmd_full_path", u"%f = Full path to downloaded file")
    add("str_rcmd_podcast_name", u"%n = Podcast name")
    add("str_other_advanced_options", u"Other advanced options")
    add("str_show_log", u"Show log tab in application")



    ## Feed Dialog (add/properties)
    add("str_title", u"Title")
    add("str_url", u"URL")
    add("str_goto_subs", u"Go to subscriptions tab to see this feed's episodes")
    add("str_feed_save", u"Save")
    add("str_feed_cancel", u"Cancel")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Enable scheduler")
    add("str_sched_select_type", u"Select radio buttons below to check at specific times or at regular intervals:")
    add("str_check_at_specific_times", u"Check at these specific times")
    add("str_check_at_regular_intervals", u"Check at regular intervals")
    add("str_repeat_every:", u"Repeat every:")
    add("str_latest_run", u"Latest run:")
    add("str_next_run", u"Next run:")
    add("str_not_yet", u"Not yet")
    #--- Cancel
    add("str_save_and_close", u"Save and close")
    #--- Save

    add("str_time_error", u"One of the scheduled times doesn't look right. Valid times look like this: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Check for new podcasts by pressing the button green check button")
    add("str_last_check", u"Last check completed at")
    add("str_of", u"of")
    add("str_item", u"item")
    add("str_items", u"items")
    add("str_downloading", u"downloading")
    add("str_downloaded", u"downloaded")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"Loading your media player...")
    add("str_loaded_mediaplayer", u"Loaded your media player...")        
    add("str_initialized", u"%s ready" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"To localize all controls of %s a restart is required. Click Ok to shutdown cleanly, cancel to continue." % PRODUCT_NAME)
    add("str_really_quit", u"A download is in progress.  Really quit?");
    add("str_double_check", u"It looks like a download is already in progress.");
    
    # check for update
    add("str_new_version_ipodder", u"A new version of %s is available, press Ok to go to the download site." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"This version of %s is up to date" % PRODUCT_NAME)
    add("str_other_copy_running", u"Another copy of %s is running. Please raise it, wait for it to complete, or kill it." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Check Now")        
    add("str_open_ipodder", u"Open %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Scanning feeds")

    # Feed right-click menu
    add("str_remove", u"Remove")        
    add("str_open_in_browser", u"Open in browser")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Play episode in mediaplayer")
    add("str_clear_selected", u"Clear selected items")
    



