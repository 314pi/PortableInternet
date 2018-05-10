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

    add("str_donate", u"Donate to %s" % PRODUCT_NAME)
    add("str_donate_expl", u"It's important to keep community-owned %s applications online and keep this new way of consuming media free as in speech. Any amount of money will make the team happy and encourage them to work on new features and services!" % PRODUCT_NAME)
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
    add("str_file", u"ファイル")
    add("str_import_opml", u"opml からのフィードをインポート")
    add("str_export_opml", u"opml としてフィードをエキスポート")
    add("str_preferences", u"個人設定")
    add("str_close_window", u"ウィンドウを閉じる")
    add("str_quit", u"終了")

    add("str_edit", u"編集")
    add("str_select_all", u"すべてを選択")

    add("str_tools", u"ツール")
    add("str_check_all", u"すべての新着を確認")
    add("str_catch_up", u"新着のポッドキャストをダウンロード")
    add("str_check_selected", u"選択項目の新着を確認")
    add("str_add_feed", u"フィードを追加する")
    add("str_remove_selected", u"フィードを削除する")
    add("str_feed_properties", u"フィードのプロパティ")
    add("str_scheduler", u"スケジューラ")

    add("str_select_language", u"言語")

    ## these are also used for the tabs
    add("str_view", u"表示")
    add("str_downloads", u"ダウンロード")
    add("str_subscriptions", u"購読")
    add("str_podcast_directory", u"ポッドキャストディレクトリ")
    add("str_cleanup", u"クリーンアップ")

    add("str_help", u"ヘルプ")
    add("str_online_help", u"オンラインヘルプ")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"更新を確認")
    add("str_report_a_problem", u"問題を報告する")
    add("str_goto_website", u"ホームページに行く")
    add("str_make_donation", u"寄付する")
    add("str_about", u"%s について" % PRODUCT_NAME)


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"選択された項目を削除")
    add("str_cancel_selected_download", u"選択されたダウンロードをキャンセル")
    add("str_pause_selected", u"選択されたダウンロードを一時停止")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"新規")
    add("str_dl_state_queued", u"順番待ち")
    add("str_dl_state_downloading",u"ダウンロード中")
    add("str_dl_state_downloaded",u"ダウンロード完了")
    add("str_dl_state_cancelled", u"キャンセル")
    add("str_dl_state_finished", u"終了")
    add("str_dl_state_partial", u"部分的にダウンロード終了")

    add("str_dl_state_clearing", u"クリア中")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"新しいポッドキャストを確認")
    add("str_catch_up_mode", u"最後に購読したポッドキャストを最新に")

    add("str_add_new_feed", u"新しいフィードを追加");
    add("str_remove_selected_feed", u"選択されたフィードを削除")
    add("str_properties", u"プロパティ")
    add("str_check_selected_feed", u"選択されたフィードを確認")

    add("str_scheduler_on", u"スケジューラ - オン")
    add("str_scheduler_off", u"スケジューラ - オフ")

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"次の実行:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"ダウンロード中のエピソードの情報は...")
    add("str_no_episodes_found", u"エピソードが見つかりませんでした。")


    ## Directorytab Toolbar
    add("str_refresh", u"更新")
    add("str_open_all_folders", u"すべてのフォルダを開く")
    add("str_close_all_folders", u"すべてのフォルダを閉じる")
    add("str_add", u"追加")

    ## Directorytab Other items
    add("str_directory_description", u"ツリー中のフィードをクリックするか、上のテキストボックスに入力して、追加をクリックしてください。")




    ## Cleanuptab items
    add("str_select_a_feed", u"フィードを選択")
    add("str_refresh_cleanup", u"更新")
    
    add("str_look_in", u"エピソードを探す場所は ... ")        
    add("str_player_library", u"プレイヤライブラリ")
    add("str_downloads_folder", u"ダウンロードフォルダ")
    add("str_delete_library_entries", u"ライブラリの項目を削除")
    add("str_delete_files", u"ファイルを削除")
    add("str_select_all_cleanup", u"すべてを選択")
    add("str_delete", u"削除")




    ## Logtab items
    add("str_log", u"ログ")
    add("str_clear", u"クリア")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"名前")
    add("str_lst_date", u"日付")        
    add("str_lst_progress", u"進捗")
    add("str_lst_state", u"状態")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"場所")
    add("str_lst_episode", u"エピソード")
    add("str_lst_playlist", u"プレイリスト")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"購読済み")
    add("str_disabled", u"無効化")
    add("str_newly-subscribed", u"最近の購読")
    add("str_unsubscribed", u"未購読")
    add("str_preview", u"プレビュー")
    add("str_force", u"強制")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog


    ## OPML Export Dialog
    add("str_choose_name_export_file", u"エキスポートするファイルの名前を選択")
    add("str_subs_exported", u"エキスポートする購読")
    
    ## Preferences Dialog
    add("str_save", u"保存")
    add("str_cancel", u"キャンセル")
    
    # General
    add("str_general", u"全般")
    add("str_gen_options_expl", u"%s の全般的なオプションを設定" % PRODUCT_NAME)
    add("str_hide_on_startup", u"スタートアップ時に %s をシステムトレイに置く" % PRODUCT_NAME)

    add("str_run_check_startup", u"スタートアップ時に新着のポッドキャストを確認")
    add("str_play_after_download", u"ダウンロード完了後すぐに再生")
    add("str_location_and_storage", u"ロケーションと場所の管理")
    add("str_stop_downloading", u"ダウンロードを続けてもいいハードディスク残量は最低")

    add("str_bad_megabyte_limit_1", u"メガバイトの制限が 整数 ではありませんでした。")
    add("str_bad_megabyte_limit_2", u"整数で指定してください。")

    add("str_download_folder", u"このフォルダにポッドキャストをダウンロードする")
    add("str_browse", u"ブラウズ")

    add("str_bad_directory_pref_1", u"入力したディレクトリが見つかりませんでした。")
    add("str_bad_directory_pref_2", u"ディレクトリを作ってから、もう一度行ってください。")

    
    # Threading
    add("str_threads", u"スレッディング")
    add("str_multiple_download", u"複数ダウンロードの設定")
    add("str_max_feedscans", u"セッションごとのフィードスキャニングの最大スレッド数")
    add("str_max_downloads", u"セッションごとの最大ダウンロード数")
   
    # Network settings
    add("str_networking", u"ネットワーク設定")
    add("str_coralize_urls", u"URL を coralize (experimental)")
    add("str_proxy_server", u"プロキシサーバの使用")
    add("str_proxy_address", u"プロキシのアドレス")
    add("str_proxy_port", u"ポート")
    add("str_proxy_username", u"ユーザ名")
    add("str_proxy_password", u"パスワード")
    add("str_bad_proxy_pref", u"プロキシサポートを有効にした場合は、プロキシホストとポートを設定してください。")

    # Player
    add("str_player", u"プレイヤ")
    add("str_choose_a_player", u"プレイヤを選択してください")

    add("str_no_player", u"プレイヤがありません。")
    
    # Advanced
    add("str_advanced", u"高度な機能")
    add("str_options_power_users", u"これらのオプションはパワーユーザ用です。")
    add("str_run_command_download", u"ダウンロードする度にこのコマンドを実行")
    add("str_rcmd_full_path", u"%f = ダウンロードされたファイルのフルパス")
    add("str_rcmd_podcast_name", u"%n = ポッドキャストの名前")
    add("str_other_advanced_options", u"他の高度なオプション")
    add("str_show_log", u"ログのタブを表示")



    ## Feed Dialog (add/properties)
    add("str_title", u"タイトル")
    add("str_url", u"URL")
    add("str_goto_subs", u"このフィードのエピソードを表示するには、購読タブを開いてください。")
    add("str_feed_save", u"保存")
    add("str_feed_cancel", u"キャンセル")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"スケジューラを有効に")
    add("str_sched_select_type", u"下のラジオボタンを選択することで、新着の確認を指定した時刻または間隔で行えます。")
    add("str_check_at_specific_times", u"これらの時刻に新着の確認を行います。")
    add("str_check_at_regular_intervals", u"この間隔で新着の確認を行います")
    add("str_repeat_every:", u"次の回数繰り返します : ")
    add("str_latest_run", u"最後に実行したのは :")
    add("str_next_run", u"次の実行は :")
    add("str_not_yet", u"まだ ")
    #--- Cancel
    add("str_save_and_close", u"保存して終了")
    #--- Save

    add("str_time_error",u"時刻の形式が誤っています。次の形式で指定してください : 10:02am, 16:43.")



    ## Statusbar items
    add("str_check_for_new_podcast_button", u"Check for new podcasts by pressing the button green check button")
    add("str_last_check", u"最後に新着の確認をしたのは、")
    add("str_of", u"の")
    add("str_item", u"項目")
    add("str_items", u"項目")
    add("str_downloading", u"ダウンロード中")
    add("str_downloaded", u"ダウンロード完了")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"取得済み")
    add("str_loading_mediaplayer", u"メディアプレイヤをロード中")
    add("str_loaded_mediaplayer", u"メディアプレーヤのロード完了")        
    add("str_initialized", u"%s は準備ができました" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", u"%s - Podcast receiver v" % PRODUCT_NAME + __version__)
    add("str_localization_restart", u"%s の言語設定の変更には再起動が必要です。%s を終了してもよいときは、Ok をクリックしてください。続けるには Cancel をクリックしてください。" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_really_quit", u"ダウンロード中です。本当に %s を終了しますか？" % PRODUCT_NAME);
    add("str_double_check", u"ダウンロードが始まっているようです。終了しますか？");
    
    # check for update
    add("str_new_version_ipodder", u"%s の新しいバージョンが利用可能です。ダウンロードサイトに行くには Ok をクリックしてください。" % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"今お使いの %s は最新です。" % PRODUCT_NAME)
    add("str_other_copy_running", u"%s が別に実行中です。そちらを終了もしくは強制終了させてください" % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"今すぐ新着の確認をする")
    add("str_open_ipodder", u"%s を開く" % PRODUCT_NAME)

    #--- Downloading

    add("str_scanning_feeds", u"フィードのスキャン中")

    # Feed right-click menu
    add("str_remove", u"削除")        
    add("str_open_in_browser", u"ブラウザーの中で開く")

    # Downloads right-click menu
    add("str_play_episode", u"エピソードの再生")
    add("str_clear_selected", u"選択された項目のクリア")
    
