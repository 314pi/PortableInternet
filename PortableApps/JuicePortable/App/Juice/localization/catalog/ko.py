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

    add("str_goto_background_on_close_title", u"Set close behavior")
    add("str_goto_background_on_close_warn", \
        u"%s는 창을 닫은 후에도 백그라운드에서 실행이 가능합니다. \n" \
        u" 백그라운드 실행을 사용하시겠습니까?" % PRODUCT_NAME)
    add("str_goto_background_on_close_pref", u"창을 닫은 후에도 계속 실행하겠습니다.")
    add("str_yes", u"예")
    add("str_no", u"아니오")
    add("str_dont_ask", u"다시 묻지 않기")
    add("str_ok", u"확인")
    add("str_hide_window", u"창 숨기기")
    add("str_show_window", u"창 보이기")

    add("str_catchup_pref", u"최신방송확인시 오래된 방송은 항상 건너뜁니다.")
    add("str_set_catchup_title", u"최신방송확인 설정")
    add("str_set_catchup_description", \
        u"최신방송확인을 사용하면 각 방송의 \n최신파일 이외의 모든 파일은 \n확인하지 않습니다. \n\n확인방법을 선택하여 주십시오.")
    add("str_skip_permanently", u"항상 확인하지 않기")
    add("str_skip_temporarily", u"이번만 확인하지 않기")
    
    add("str_set_oneclick_handler", u"원클릭 설정")
    add("str_set_oneclick_handler_warn",\
        u"%s는 현재 원클릭구독신청을 지원하지 않습니다. \n" \
        u"%s에서 원클릭구독신청을 사용하게 할까요?" % (PRODUCT_NAME,PRODUCT_NAME))
    add("str_ensure_oneclick_handler", u"언제나 원클릭구독신청을 사용합니다.")
    
    add("str_txt_feedmanager", u"호환가능(Compatible) 방송관리자:")
    add("str_feedmanager_btn_podnova", u"www.PodNova.com - Podcast를 원클릭구독신청 하세요.")

    add("str_open_downloads_folder", u"파일이 다운로드된 폴더를 엽니다.")
    add("str_chkupdate_on_startup", u"시작 시에 프로그램의 새 버전을 확인합니다.")
    add("str_bad_feedmanager_url", u"방송관리자에 올바른 URL을 입력하세요.")
    add("str_feed_manager", u"방송관리자")
    add("str_feedmanager_enable", u"구독중인 방송목록과 원격서비스를 동기화 합니다.")
    add("str_opml_url", u"opml URL")
    add("str_set_track_genre", u"아래를 트랙 장르로 설정합니다.")
    add("str_auto_delete", u"다운로드후 ")
    add("str_days_old", u"일이 지난 파일은 자동삭제합니다.")
    
    add("str_show_notes", u"주석 보기")
    add("str_close", u"Close")
    
    add("str_critical_error_minspace_exceeded", \
        u"다운로드가 중지되었습니다; 하드디스크 여유공간 %dMB 으로 " \
        u"최소요구 용량 %dMB 보다 적습니다. 파일정리나 환경설정의 저장공간설정의 조정으로 " \
        u"하드디스크 용량을 확보하여 주십시오.")
    add("str_critical_error_unknown", u"다운로드중 알려지지 않은 치명적인 에러가 있었습니다.")
    
    add("str_error_checking_new_version", u"죄송합니다. 새로운 버전 확인에 에러가 있었습니다. 다시 시도해 주십시오.")
    add("str_hours", u"시")
    add("str_minutes", u"분")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"확인중")
    add("str_scanned", u"확인완료")
    add("str_feed", u"방송")
    add("str_feeds", u"방송")
    
    add("str_downloading_new_episodes", u"새 방송 다운로드 중")
    add("str_sched_specific", u"지정된 시각에 확인")
    add("str_sched_reg", u"지정된 시간에 확인")
    add("str_repeat_every", u"항상 반복")
    add("str_next_run_label", u"다음 실행:")
    
    add("str_license", u"본 프로그램은 프리웨어입니다; 여러분들은 자유소프트웨어재단의 GNU Genereal Public Licence에 따라 재배포 또는 수정 및 재배포 할 수 있습니다; 버전2나 그 이후의 버전 역시 마찬가지입니다. 본 프로그램은 유용하게 사용하시길 바라면서 배포되었지만 사용상의 어떤 보증도 하지 않습니다; 판매용이나 특수목적으로 변형된 경우 역시 보증하지 않습니다. \n\nGNU General Public License에서 세부사항을 확인하십시오.")

    add("str_donate", u"%s에 기부하기" % PRODUCT_NAME)
    add("str_donate_expl", u"기부는 커뮤니티기반의 %s 프로그램을 계속 진행하고, 무료 미디어의 소비를 유지하는 데 중요한 일입니다. 크거나 작은 모든 도움들이 개발팀을 기쁘게하고 그들이 원하는 새로운 기능이나 서비스의 개발에 도움이 될것입니다!" % PRODUCT_NAME)
    add("str_donate_yes", u"예, 지금 기부페이지로 연결하겠습니다!")
    add("str_donate_two_weeks", u"좀 더 살펴보겠습니다. 이틀 뒤에 다시 알려주세요.")
    add("str_donate_already", u"이미 기부를 했습니다. 다시 보여주지 마세요.")
    add("str_donate_no", u"No, 기부하지 않겠습니다. 다시 보여주지 마세요.")
    add("str_donate_one_day", u"하루후에 다시 알려주세요.")
    add("str_donate_proceed", u"계속하겠습니다.")

    add("str_scheduler_dialog", u"예약실행")
    add("str_scheduler_tab", u"예약실행 옵션")

    add("str_select_import_file", u"가져올 파일 선택")    
    add("str_add_feed_dialog", u"방송 추가")
    add("str_edit_feed", u"방송 속성")

    add("str_really_delete", u"다음 방송을 정말 삭제하시겠습니까?")

    add("str_license_caption", u"라이센스")

    add("str_ep_downloaded", u"다운로드완료")
    add("str_ep_skipped_removed_other", u" ")
    add("str_dl_state_to_download", u"다운로드예정")

    add("str_select_none_cleanup", u"선택 해제")
    add("str_submit_lang", u"Submit a language")
    
    add("str_dltab_live", u"다운로드 파일: ")
    add("str_dltab_ul_speed", u"업로드 속도: ")
    add("str_dltab_dl_speed", u"다운로드 속도: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"파일")
    add("str_import_opml", u"구독중인 방송 opml파일에서 가져오기")
    add("str_export_opml", u"구독중인 방송 opml파일로 내보내기")
    add("str_preferences_menubar", u"환경설정")
    add("str_close_window", u"창 닫기")
    add("str_quit", u"종료")

    add("str_edit", u"수정")
    add("str_select_all", u"모두 선택")

    add("str_tools", u"도구")
    add("str_check_all", u"모두 확인")
    add("str_catch_up", u"최신방송확인")
    add("str_check_selected", u"선택된 방송확인")
    add("str_add_feed", u"방송 추가")
    add("str_remove_selected", u"방송 삭제")
    add("str_feed_properties", u"방송 정보")
    add("str_scheduler_menubar", u"예약실행")
    
    add("str_select_language", u"사용언어 선택")

    ## these are also used for the tabs
    add("str_view", u"보기")
    add("str_downloads", u"다운로드")
    add("str_subscriptions", u"구독중인 방송")
    add("str_podcast_directory", u"Podcast 디렉토리")
    add("str_cleanup", u"파일정리")

    add("str_help", u"도움말")
    add("str_online_help", u"온라인 도움말")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"업데이트 확인")
    add("str_report_a_problem", u"문제 알려주기")
    add("str_goto_website", u"공식 웹사이트")
    add("str_make_donation", u"개발팀에 기부하기 ")
    add("str_menu_license", u"라이센스")
    add("str_about", u"%s 정보" % PRODUCT_NAME)


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"선택된 방송을 삭제합니다")
    add("str_cancel_selected_download", u"선택된 방송의 다운로드를 취소합니다.")
    add("str_pause_selected", u"선택된 방송의 다운로드를 일시정지합니다.")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"새 방송")
    add("str_dl_state_queued", u"다운로드예정")
    add("str_dl_state_downloading", u"다운로드중")
    add("str_dl_state_downloaded", u"다운로드완료")
    add("str_dl_state_cancelled", u"취소됨")
    add("str_dl_state_finished", u"완료됨")
    add("str_dl_state_partial", u"일부 다운로드됨")
    add("str_dl_state_clearing", u"삭제중")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"새 방송 확인")
    add("str_catch_up_mode", u"최신방송확인 - 새로 추가된 목록 중 가장 최신 방송만 다운로드합니다.")

    add("str_add_new_feed", u"새 방송 추가");
    add("str_remove_selected_feed", u"선택된 방송 삭제")
    add("str_properties", u"속성")
    add("str_check_selected_feed", u"선택된 방송 확인")

    add("str_scheduler_on", u"예약실행(사용중)")
    add("str_scheduler_off", u"예약실행")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"다음 실행:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"세부방송내역 다운로드 중")
    add("str_no_episodes_found", u"세부방송내역이 없습니다.")


    ## Directorytab Toolbar
    add("str_refresh", u"새로고침")
    add("str_open_all_folders", u"해당폴더 모두 열기")
    add("str_close_all_folders", u"해당폴더 모두 닫기")
    add("str_add", u"추가")

    ## Directorytab Other items
    add("str_directory_description", u"디렉토리내의 방송을 선택하거나 주소를 직접입력 후 추가버튼을 누르세요.")




    ## Cleanuptab items
    add("str_select_a_feed", u"방송을 선택하세요")
    add("str_refresh_cleanup", u"새로고침")
    
    add("str_look_in", u"다음에서 방송 찾기")        
    add("str_player_library", u"재생프로그램 라이브러리")
    add("str_downloads_folder", u"다운로드파일 저장폴더")
    add("str_delete_library_entries", u"라이브러리 항목 삭제")
    add("str_delete_files", u"파일 삭제")
    add("str_select_all_cleanup", u"전체선택")
    add("str_delete", u"삭제")




    ## Logtab items
    add("str_log", u"로그")
    add("str_clear", u"초기화")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"이름")
    add("str_lst_date", u"다운로드 날짜")        
    add("str_lst_progress", u"진행상황")
    add("str_lst_state", u"상태")
    add("str_lst_mb", u"크기(MB)")
    add("str_lst_location", u"위치")
    add("str_lst_episode", u"세부방송명")
    add("str_lst_playlist", u"방송명")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"구독등록완료")
    add("str_disabled", u"사용할수없음")
    add("str_newly-subscribed", u"새로등록됨")
    add("str_unsubscribed", u"등록되지않음")
    add("str_preview", u"미리보기")
    add("str_force", u"Force")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"내보낼 파일 이름을 선택해 주십시오.")
    add("str_subs_exported", u"구독중인 방송을 내보냅니다.")
    
    ## Preferences Dialog
    add("str_preferences", u"환경설정")
    
    add("str_save", u"저장")
    add("str_cancel", u"취소")
    
    # General
    add("str_general", u"일반")
    add("str_gen_options_expl", u"일반 옵션")
    add("str_hide_on_startup", u"프로그램 시작 시 시스템트레이에만 표시")

    add("str_run_check_startup", u"프로그램 시작 시 새 방송 확인")
    add("str_play_after_download", u"다운로드 후 방송 바로듣기")
    add("str_location_and_storage", u"저장공간 설정")
    add("str_stop_downloading", u"하드디스크 공간이 다음 용량 미만일 때 다운로드 중지")
    add("str_bad_megabyte_limit_1", u"하드디스크 저장단위는 정수만 입력가능합니다.")
    add("str_bad_megabyte_limit_2", u"다시 입력해주십시오.")

    add("str_download_folder", u"다운로드된 파일의 저장 경로")
    add("str_browse", u"찾기")
    add("str_bad_directory_pref_1", u"입력한 폴더를 찾을 수 없습니다.")
    add("str_bad_directory_pref_2", u"다시 시도해 주십시오.")

    
    # Threading
    add("str_threads", u"쓰레드(Thread)")
    add("str_multiple_download", u"다중 다운로드 설정")
    add("str_max_feedscans", u"세션당 세부방송목록확인 최대 Thread 개수")
    add("str_max_downloads", u"세션당 최대 다운로드 개수")
   
    # Network settings
    add("str_networking", u"네트워크 설정")
    add("str_coralize_urls", u"Coralize URLs (시험용)")
    add("str_proxy_server", u"프록시서버 사용")
    add("str_proxy_address", u"주소")
    add("str_proxy_port", u"포트")
    add("str_proxy_username", u"사용자명")
    add("str_proxy_password", u"비밀번호")
    add("str_bad_proxy_pref", u"프록시서버정보가 정확하지 않습니다. 서버주소와 포트번호를 다시 확인해주십시오.")

    # Player
    add("str_player", u"재생프로그램")
    add("str_choose_a_player", u"재생프로그램 선택")
    add("str_no_player", u"지정안함")
    
    # Advanced
    add("str_advanced", u"고급")
    add("str_options_power_users", u"다음은 고급사용자들을 위한 항목입니다")
    add("str_run_command_download", u"각 다운로드 후 다음 명령을 실행합니다")
    add("str_rcmd_full_path", u"%f = 다운로드된 파일의 전체경로명")
    add("str_rcmd_podcast_name", u"%n = 방송명")
    add("str_other_advanced_options", u"기타 고급 옵션")
    add("str_show_log", u"로그 탭을 표시합니다")



    ## Feed Dialog (add/properties)
    add("str_title", u"방송명")
    add("str_url", u"URL")
    add("str_goto_subs", u"방송목록확인을 위해 '구독중인 방송목록'탭으로 이동합니다.")
    add("str_feed_save", u"저장")
    add("str_feed_cancel", u"취소")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"예약실행 사용")
    add("str_sched_select_type", u"업데이트할 시각 또는 시간을 선택하여 주십시오:")
    add("str_check_at_specific_times", u"지정된 시각에 업데이트를 실행합니다.")
    add("str_check_at_regular_intervals", u"다음의 시간마다 업데이트를 실행합니다.")
    add("str_repeat_every:", u"매일 반복:")
    add("str_latest_run", u"마지막 실행:")
    add("str_next_run", u"다음 실행:")
    add("str_not_yet", u"실행된 적 없음")
    #--- Cancel
    add("str_save_and_close", u"저장 후 닫기")
    #--- Save

    add("str_time_error", u"지정된 시각의 형식이 올바르지 않습니다. 다음의 형식에 맞게 입력해주십시오: 10:02am, 16:43.")


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
    #--- 프로그래밍: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\n디자인: Martijn Venrooy\n컨텐츠: Mark Alexander Posth\n기획: Adam Curry, Dave Winer\n참여해주신 모든 번역자들에게 감사드립니다!\n\nBased on Feedparser and BitTorrent technology.\n본 프로그램은 프리웨어입니다; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the  License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of  merchantability or fitness for a particular purpose. \n\nSee the GNU General Public License for more details.




    ## Statusbar items
    add("str_check_for_new_podcast_button", u"녹색 체크버튼을 눌러서 새로운 Podcast를 확인하세요")
    add("str_last_check", u"해당 시각에 마지막 확인을 완료하였습니다.")
    add("str_of", u"/")
    add("str_item", u" - ")
    add("str_items", u"개")
    add("str_downloading", u"다운로드중")
    add("str_downloaded", u"다운로드완료")
    add("str_enclosure", u"개 파일을")
    add("str_enclosures", u"개 파일을")
    add("str_fetched", u"가져왔습니다.")
    add("str_loading_mediaplayer", u"미디어플레이어를 부르는 중")
    add("str_loaded_mediaplayer", u"미디어플레이어 실행완료")        
    add("str_initialized", u"%s 준비완료" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"한국어를 사용하려면 프로그램을 다시 시작해야합니다. \n종료하시려면 확인, 계속 사용하시려면 취소를 선택하세요.")
    add("str_really_quit", u"다운로드가 진행중입니다. 종료하시겠습니까?");
    add("str_double_check", u"이미 다운받은 파일입니다.");
    
    # check for update
    add("str_new_version_ipodder", u"%s 새 버전이 나왔습니다. 확인을 선택하시면 다운로드 사이트로 이동합니다." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"업데이트버전이 없습니다.")
    add("str_other_copy_running", u"다른버전의 %s가 작동중입니다. 작업이 끝나기를 기다리거나, 종료시켜주십시오." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"새 방송 확인")        
    add("str_open_ipodder", u"%s 열기" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"방송 확인중")

    # Feed right-click menu
    add("str_remove", u"삭제")        
    add("str_open_in_browser", u"브라우저로 보기")

    # Downloads right-click menu
    add("str_play_episode", u"미디어플레이어로 듣기")
    add("str_clear_selected", u"선택된 항목 삭제")