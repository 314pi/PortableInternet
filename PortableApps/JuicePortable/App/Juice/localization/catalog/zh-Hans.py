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

    add("str_goto_background_on_close_title", u"设置关闭行为")
    add("str_goto_background_on_close_warn", \
        u"当关闭主窗口时，%s可以在后台运行或退出，\n" \
        u"你希望%s继续运行？" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_goto_background_on_close_pref", u"当关闭主窗口时，继续后台运行")
    add("str_yes", u"是")
    add("str_no", u"否")
    add("str_dont_ask", u"别再问我")
    add("str_ok", u"OK")
    add("str_hide_window", u"隐藏窗口")
    add("str_show_window", u"显示窗口")

    add("str_catchup_pref", u"跟进动作将会永久地跳过旧的曲目")
    add("str_set_catchup_title", u"设置跟进行为")
    add("str_set_catchup_description", \
        u"当使用跟进动作时，%s只是处理每个Feed中最新的一个Podcast\n" \
        u"请选择%s应该怎样处理跳过的条目" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_skip_permanently", u"永久跳过")
    add("str_skip_temporarily", u"只是这次跳过")
    
    add("str_set_oneclick_handler", u"设置单击处理器")
    add("str_set_oneclick_handler_warn",\
        u"%s不是你当前的Podcast单击订阅处理器。\n" \
        u"当点击单击订阅链接时，启动%s吗？" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"总是使用%s进行单击订阅" % PRODUCT_NAME)
    
    add("str_txt_feedmanager", u" 兼容的Feed管理器")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - 搜索或浏览Podcast，单击订阅")

    add("str_open_downloads_folder", u"打开下载目录")
    add("str_chkupdate_on_startup", u"启动时检查新版本")
    add("str_bad_feedmanager_url", u"请为Feed管理输入一个合法的URL")
    add("str_feed_manager", u"Feed管理")
    add("str_feedmanager_enable", u"同步我的订阅到一个远程服务")
    add("str_opml_url", u"OPML URL")
    add("str_set_track_genre", u"设置音轨流派为")
    add("str_auto_delete", u"自动删除曲目，时间大于")
    add("str_days_old", u"天的")
    
    add("str_show_notes", u"显示注解")
    add("str_close", u"关闭")

    add("str_critical_error_minspace_exceeded", \
        u"跳过下载; 目前可用空间为%dMB, 小于 " \
        u"设定的最小值 %dMB.  请释放硬盘空间 " \
        u"用清除功能或在“参数选择”中调整“存储管理”选项")
    add("str_critical_error_unknown", u"下载过程中出现严重的未知错误")
    
    add("str_error_checking_new_version", u"很抱歉，检查新版本过程中出错，请稍后重试")
    add("str_hours", u"小时")
    add("str_minutes", u"分钟")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"扫描中")
    add("str_scanned", u"扫描完成")
    add("str_feed", u"Feed")
    add("str_feeds", u"Feeds")
    
    add("str_downloading_new_episodes", u"下载中的新曲目")
    add("str_sched_specific", u"在指定时间检查")
    add("str_sched_reg", u"在固定时间间隔内检查")
    add("str_repeat_every", u"重复每隔")
    add("str_next_run_label", u"下次运行")
    
    add("str_license", u"This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.")

    add("str_donate", u"捐助%s" % PRODUCT_NAME)
    add("str_donate_expl", u"It's important to keep community-owned %s applications online and keep this new way of consuming media free as in speech. Any amount of money will make the team happy and encourage them to work on new features and services!" % PRODUCT_NAME)
    add("str_donate_yes", u"是的，马上带我去捐助页面！")
    add("str_donate_two_weeks", u"我想再了解一下,两周后再显示")
    add("str_donate_already", u"我已经捐助了，别再显示对话窗")
    add("str_donate_no", u"我不想捐助，别再显示对话窗")
    add("str_donate_one_day", u"现在不想捐助，1天后再次提醒我")
    add("str_donate_proceed", u"继续")

    add("str_scheduler_dialog", u"定时器")
    add("str_scheduler_tab", u"设置")

    add("str_select_import_file", u"选择导入文件")    
    add("str_add_feed_dialog", u"添加新的Feed")
    add("str_edit_feed", u"Feed属性")

    add("str_really_delete", u"真的删除")

    add("str_license_caption", u"版权协议")

    add("str_ep_downloaded", u"已下载")
    add("str_ep_skipped_removed_other", u"跳过/删除/其他的Feed")
    add("str_dl_state_to_download", u"待下载")

    add("str_select_none_cleanup", u"全不选")
    add("str_submit_lang", u"提交一种语言")
    
    add("str_dltab_live", u"活动的下载进程: ")
    add("str_dltab_ul_speed", u"上传速度: ")
    add("str_dltab_dl_speed", u"下载速度: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"文件")
    add("str_import_opml", u"从OPML文件导入Feeds...")
    add("str_export_opml", u"导出Feeds到OPML文件...")
    add("str_preferences_menubar", u"个人设定...")
    add("str_close_window", u"关闭窗口")
    add("str_quit", u"退出")

    add("str_edit", u"编辑")
    add("str_select_all", u"全选")

    add("str_tools", u"工具")
    add("str_check_all", u"全部检查")
    add("str_catch_up", u"跟进")
    add("str_check_selected", u"检查选中的")
    add("str_add_feed", u"添加新的Feed...")
    add("str_remove_selected", u"删除Feed")
    add("str_feed_properties", u"Feed属性...")
    add("str_scheduler_menubar", u"定时器...")
    
    add("str_select_language", u"选择语言")

    ## these are also used for the tabs
    add("str_view", u"查看")
    add("str_downloads", u"下载")
    add("str_subscriptions", u"订阅")
    add("str_podcast_directory", u"Podcast目录")
    add("str_cleanup", u"清理")

    add("str_help", u"帮助")
    add("str_online_help", u"在线帮助")
    add("str_faq", u"常见问题解答")
    add("str_check_for_update", u"检查更新...")
    add("str_report_a_problem", u"问题报告")
    add("str_goto_website", u"访问网站")
    add("str_make_donation", u"捐助")
    add("str_menu_license", u"版权协议...")
    add("str_about", u"关于...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"删除选中的条目")
    add("str_cancel_selected_download", u"取消下载（选中的条目）")
    add("str_pause_selected", u"暂停下载（选中的条目）")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"新建")
    add("str_dl_state_queued", u"在队列中")
    add("str_dl_state_downloading", u"下载中")
    add("str_dl_state_downloaded", u"已下载")
    add("str_dl_state_cancelled", u"已取消")
    add("str_dl_state_finished", u"已完成")
    add("str_dl_state_partial", u"部分下载")
    add("str_dl_state_clearing", u"正在清理")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"全部检查 - 检查新的Podcast")
    add("str_catch_up_mode", u"跟进 - 仅下载最新的Podcast")

    add("str_add_new_feed", u"添加Feed");
    add("str_remove_selected_feed", u"删除选中的Feed")
    add("str_properties", u"属性")
    add("str_check_selected_feed", u"检查选中的Feed")

    add("str_scheduler_on", u"定时器 - 打开")
    add("str_scheduler_off", u"定时器 - 关闭")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"下次运行")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"下载中的曲目信息...")
    add("str_no_episodes_found", u"没有找到曲目。")


    ## Directorytab Toolbar
    add("str_refresh", u"刷新")
    add("str_open_all_folders", u"打开所有目录")
    add("str_close_all_folders", u"关闭所有目录")
    add("str_add", u"添加")

    ## Directorytab Other items
    add("str_directory_description", u"在目录中点击一个Feed，或在上面的空白处输入或粘贴，然后点击添加")




    ## Cleanuptab items
    add("str_select_a_feed", u"选择一个Feed")
    add("str_refresh_cleanup", u"刷新")
    
    add("str_look_in", u"查找曲目在...")        
    add("str_player_library", u"播放器媒体库")
    add("str_downloads_folder", u"下载目录")
    add("str_delete_library_entries", u"删除媒体库中的条目")
    add("str_delete_files", u"删除文件")
    add("str_select_all_cleanup", u"全选")
    add("str_delete", u"删除")



    ## Logtab items
    add("str_log", u"日志")
    add("str_clear", u"清理")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"名称")
    add("str_lst_date", u"日期")        
    add("str_lst_progress", u"进度")
    add("str_lst_state", u"状态")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"位置")
    add("str_lst_episode", u"曲目")
    add("str_lst_playlist", u"播放列表")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"已订阅")
    add("str_disabled", u"已失效")
    add("str_newly-subscribed", u"最近订阅")
    add("str_unsubscribed", u"已退订")
    add("str_preview", u"预览")
    add("str_force", u"强制")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"为导出文件选择一个名字")
    add("str_subs_exported", u"所有的订阅已经导出")
    
    ## Preferences Dialog
    add("str_preferences", u"配置")
    
    add("str_save", u"保存")
    add("str_cancel", u"取消")
    
    # General
    add("str_general", u"通用")
    add("str_gen_options_expl", u"为%s程序设置通用选项" % PRODUCT_NAME)
    add("str_hide_on_startup", u"启动后只在系统托盘中显示%s" % PRODUCT_NAME)

    add("str_run_check_startup", u"启动时自动检查新Podcast")
    add("str_play_after_download", u"所有曲目下载完就播放")
    add("str_location_and_storage", u"位置和存储管理")
    add("str_stop_downloading", u"停止下载，当硬盘空间剩余容量最小到")
    add("str_bad_megabyte_limit_1", u"请输入整数")
    add("str_bad_megabyte_limit_2", u"请重试")

    add("str_download_folder", u"下载Podcast到此目录")
    add("str_browse", u"浏览")
    add("str_bad_directory_pref_1", u"找不到指定的目录")
    add("str_bad_directory_pref_2", u"请先创建此目录然后重试")

    
    # Threading
    add("str_threads", u"线程")
    add("str_multiple_download", u"多线程下载设置")
    add("str_max_feedscans", u"为搜索Feed，每个会话最大线程")
    add("str_max_downloads", u"每个会话最大下载线程")
   
    # Network settings
    add("str_networking", u"网络设置")
    add("str_coralize_urls", u"Coralize URLs (实验的)")
    add("str_proxy_server", u"用代理服务器")
    add("str_proxy_address", u"地址")
    add("str_proxy_port", u"端口")
    add("str_proxy_username", u"用户名")
    add("str_proxy_password", u"密码")
    add("str_bad_proxy_pref", u"你选择使用代理服务器，但没有提供其地址和端口，请重新设置")

    # Player
    add("str_player", u"播放器")
    add("str_choose_a_player", u"选择一个播放器")
    add("str_no_player", u"没有播放器")
    
    # Advanced
    add("str_advanced", u"高级")
    add("str_options_power_users", u"这些选项适用于高级用户")
    add("str_run_command_download", u"在完成每个下载后运行这个命令")
    add("str_rcmd_full_path", u"%f = 下载文件的全路径")
    add("str_rcmd_podcast_name", u"%n = Podcast名称")
    add("str_other_advanced_options", u"其他高级选项")
    add("str_show_log", u"在程序中显示日志标签")



    ## Feed Dialog (add/properties)
    add("str_title", u"标题")
    add("str_url", u"URL")
    add("str_goto_subs", u"到订阅标签中查看这个Feed对应的曲目")
    add("str_feed_save", u"保存")
    add("str_feed_cancel", u"取消")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"打开定时器")
    add("str_sched_select_type", u"定时器运行方式:")
    add("str_check_at_specific_times", u"在指定时间检查")
    add("str_check_at_regular_intervals", u"在固定时间间隔检查")
    add("str_repeat_every:", u"重复每隔")
    add("str_latest_run", u"最后一次运行")
    add("str_next_run", u"下次运行")
    add("str_not_yet", u"还没有")
    #--- Cancel
    add("str_save_and_close", u"保存并关闭")
    #--- Save

    add("str_time_error", u"时间格式不正确，正确的时间格式应该像这样: 10:02am, 16:43")


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
    add("str_check_for_new_podcast_button", u"点击绿色按钮，检查新的Podcast")
    add("str_last_check", u"最后检查完成于")
    add("str_of", u"的")
    add("str_item", u"条目")
    add("str_items", u"条目")
    add("str_downloading", u"下载中")
    add("str_downloaded", u"下载完成")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"抓取完成")
    add("str_loading_mediaplayer", u"正在引导Media Player...")
    add("str_loaded_mediaplayer", u"Media Player引导完成...")        
    add("str_initialized", u"%s 准备完成" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast 接收机 v" + __version__)
    add("str_localization_restart", u"%s的语言切换需要重新启动，点击确定重新启动，点击取消继续" % PRODUCT_NAME)
    add("str_really_quit", u"一个下载进程在运行，真的退出？");
    add("str_double_check", u"已经有一个下载进程在运行");
    
    # check for update
    add("str_new_version_ipodder", u"已经有新版本的%s了，去下载页面" % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"这个版本的%s已经是最新的" % PRODUCT_NAME)
    add("str_other_copy_running", u"另一个%s正在运行中，你可以选择打开它或等它完成或中止它" % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"立刻检查")        
    add("str_open_ipodder", u"打开%s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"扫描的Feed")

    # Feed right-click menu
    add("str_remove", u"删除")        
    add("str_open_in_browser", u"在浏览器中打开")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"用Media Player播放曲目")
    add("str_clear_selected", u"清理选中的条目")
    



