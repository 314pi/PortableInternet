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
        u"Закачка прекращена; Свободного места на диске " \
        u"менее %dMB. Обеспечьте место под подкаст.")
    add("str_critical_error_unknown", u"Неизвестная ошибка при закачке.")
    
    add("str_error_checking_new_version", u"Возникла ошибка при проверки программы на новую версию")
    add("str_hours", u"час.")
    add("str_minutes", u"мин.")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Проверка")
    add("str_scanned", u"Проверка завершена")
    add("str_feed", u"подкаст-директория")
    add("str_feeds", u"подкаст-директорий")
    
    add("str_downloading_new_episodes", u"Закачка новых подкастов")
    add("str_sched_specific", u"Проверка в определённое время")
    add("str_sched_reg", u"Проверка в определённые интервалы")
    add("str_repeat_every", u"Повторять каждые")
    add("str_next_run_label", u"Следующая проверка:")
    
    add("str_license", u"Эта программа свободно распространяется; Вы можете пересобирать и/или модифицировать её под условиями лицензии GNU General Public License, опубликованной Free Software Foundation. Эта программа распространяется с надеждой, что может быть полезна, но без всяких гарантий. \n\nСмотрите GNU General Public License для большей информации.")

    add("str_donate", u"Внести пожертвование %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Очень важно сохранить ПО %s-сообщества и поддерживать его дальнейшее развитие. Небольшое денежное пожертвование сможет сделать разработчиков счастливыми и дать стимул для дальнейшей разработки и введению новых сервисов!" % PRODUCT_NAME)
    add("str_donate_yes", u"Да, открыть страницу пожертвований сейчас!")
    add("str_donate_two_weeks", u"Я ещё потестирую программу. Напомнить через 2 недели")
    add("str_donate_already", u"Я уже сделал пожертвование. Не показывать больше окно")
    add("str_donate_no", u"Нет, я не сделал пожертвование. Не показывать больше окно")
    add("str_donate_one_day", u"Не сейчас. Напомнить завтра")
    add("str_donate_proceed", u"Продолжить")

    add("str_scheduler_dialog", u"Планировщик")
    add("str_scheduler_tab", u"Параметры")

    add("str_select_import_file", u"Выберите импортируемый файл")    
    add("str_add_feed_dialog", u"Добавить подкаст-директорию")
    add("str_edit_feed", u"Установки подкаст-директории")

    add("str_really_delete", u"Действительно удалить")

    add("str_license_caption", u"Лицензия")

    add("str_ep_downloaded", u"Закачано")
    add("str_ep_skipped_removed_other", u"Пропущено/Удалено/Другое")
    add("str_dl_state_to_download", u"Закачать")

    add("str_select_none_cleanup", u"Выделение снято")
    add("str_submit_lang", u"Найти языки")
    
    add("str_dltab_live", u"Закачивается: ")
    add("str_dltab_ul_speed", u"Скорость закачки: ")
    add("str_dltab_dl_speed", u"Скорость скачивания: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Файл")
    add("str_import_opml", u"Импортировать подкаст-директории из opml...")
    add("str_export_opml", u"Экспортировать подкаст-директории в opml...")
    add("str_preferences_menubar", u"Установки...")
    add("str_close_window", u"Закрыть окно")
    add("str_quit", u"Выход")

    add("str_edit", u"Редактировать")
    add("str_select_all", u"Выбрать всё")

    add("str_tools", u"Инструменты")
    add("str_check_all", u"Проверить всё")
    add("str_catch_up", u"Скачать новое")
    add("str_check_selected", u"Проверить выбранное")
    add("str_add_feed", u"Добавить подкаст-директорию...")
    add("str_remove_selected", u"Удалить подкаст-директорию")
    add("str_feed_properties", u"Свойства подкаст-директории...")
    add("str_scheduler_menubar", u"Планировщик...")
    
    add("str_select_language", u"Выбрать язык")

    ## these are also used for the tabs
    add("str_view", u"Вид")
    add("str_downloads", u"Закачки")
    add("str_subscriptions", u"Описания")
    add("str_podcast_directory", u"База Подкаст-директорий")
    add("str_cleanup", u"Очистить")

    add("str_help", u"Помощь")
    add("str_online_help", u"Online помощь")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Проверить обновления...")
    add("str_report_a_problem", u"Послать отчёт об ошибке")
    add("str_goto_website", u"Посетить WEB-страницу")
    add("str_make_donation", u"Сделать пожертвование")
    add("str_menu_license", u"Лицензия...")
    add("str_about", u"О программе...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Удалить выбранное")
    add("str_cancel_selected_download", u"Отменить выбранные закачки")
    add("str_pause_selected", u"Пауза")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Новое")
    add("str_dl_state_queued", u"Очередь")
    add("str_dl_state_downloading", u"Скачивается")
    add("str_dl_state_downloaded", u"Скачано")
    add("str_dl_state_cancelled", u"Отменено")
    add("str_dl_state_finished", u"Закончено")
    add("str_dl_state_partial", u"Частично закачано")
    add("str_dl_state_clearing", u"Очистка")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Проверить на новые подкасты")
    add("str_catch_up_mode", u"Скачать новое - Только скачать новые описания")

    add("str_add_new_feed", u"Добавить подкаст-директорию");
    add("str_remove_selected_feed", u"Удалить выбранные подкаст-директории")
    add("str_properties", u"Установки")
    add("str_check_selected_feed", u"Проверить выбранные подкаст-директории")

    add("str_scheduler_on", u"Планировщик - Вкл")
    add("str_scheduler_off", u"Планировщик - Выкл")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Следующая проверка:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Скачивание информации об эпизоде...")
    add("str_no_episodes_found", u"Эпизодов не найдено.")


    ## Directorytab Toolbar
    add("str_refresh", u"Refresh")
    add("str_open_all_folders", u"Открыть все папки")
    add("str_close_all_folders", u"Закрыть все папки")
    add("str_add", u"Add")

    ## Directorytab Other items
    add("str_directory_description", u"Выберите подкаст-директорию в списке или введине название в поле выше.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Выберите подкаст-директорию")
    add("str_refresh_cleanup", u"Обновить")
    
    add("str_look_in", u"Искать эпизоды")        
    add("str_player_library", u"Библиотека")
    add("str_downloads_folder", u"Директории закачки")
    add("str_delete_library_entries", u"Удалить содержимое библиотеки")
    add("str_delete_files", u"Удалить файлы")
    add("str_select_all_cleanup", u"Выбрать всё")
    add("str_delete", u"Удалить")




    ## Logtab items
    add("str_log", u"Лог")
    add("str_clear", u"Очистить")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Название")
    add("str_lst_date", u"Дата")        
    add("str_lst_progress", u"Прогресс")
    add("str_lst_state", u"Состояние")
    add("str_lst_mb", u"Мб")
    add("str_lst_location", u"Местоположение")
    add("str_lst_episode", u"Эпизод")
    add("str_lst_playlist", u"Список воспроизведения")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Подписано")
    add("str_disabled", u"Отключено")
    add("str_newly-subscribed", u"Вновь подписано")
    add("str_unsubscribed", u"Отписано")
    add("str_preview", u"Предпросмотр")
    add("str_force", u"Заставлять")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Выберите имя экспортируемого файла")
    add("str_subs_exported", u"Описания экспортированы.")
    
    ## Preferences Dialog
    add("str_preferences", u"Установки")
    
    add("str_save", u"Сохранить")
    add("str_cancel", u"Отмена")
    
    # General
    add("str_general", u"Главные")
    add("str_gen_options_expl", u"Установите главные настройки %s'а" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Прятать %s в трей при старте" % PRODUCT_NAME)

    add("str_run_check_startup", u"Запускать проверку на новые версии при старте")
    add("str_play_after_download", u"Проигрывать скачанное")
    add("str_location_and_storage", u"Управление хранилищем")
    add("str_stop_downloading", u"Остановить закачку, если на диске места меньше, чем ")
    add("str_bad_megabyte_limit_1", u"Извините, но число не корректно")
    add("str_bad_megabyte_limit_2", u"Попробуйте ещё.")

    add("str_download_folder", u"Закачивать подкасты в папку")
    add("str_browse", u"Обзор")
    add("str_bad_directory_pref_1", u"Извините, директория не найдена")
    add("str_bad_directory_pref_2", u"Пожалуйста, создайте директорию и выберите её.")

    
    # Threading
    add("str_threads", u"Потоки")
    add("str_multiple_download", u"Установки многопотоковой закачки")
    add("str_max_feedscans", u"максимальное количество потоков при проверке")
    add("str_max_downloads", u"максимальное количество потоков при скачке")
   
    # Network settings
    add("str_networking", u"Установки сети")
    add("str_coralize_urls", u"Подсвечивать URL'ы (экспериментально)")
    add("str_proxy_server", u"Использовать proxy")
    add("str_proxy_address", u"Адрес")
    add("str_proxy_port", u"Порт")
    add("str_proxy_username", u"Логин")
    add("str_proxy_password", u"Пароль")
    add("str_bad_proxy_pref", u"Вы определили работу через прокси, но не определили адрес и порт.  Пожалуйста, вернитесь к этим настройкам и заполните их.")

    # Player
    add("str_player", u"Проигрыватель")
    add("str_choose_a_player", u"Выберите проигрыватель")
    add("str_no_player", u"Нет проигрывателя")
    
    # Advanced
    add("str_advanced", u"Расширенные")
    add("str_options_power_users", u"Эти настройки могут быть изменены продвинутыми пользователями")
    add("str_run_command_download", u"Запускать эту команду после каждой закачки")
    add("str_rcmd_full_path", u"%f = Полный путь к закачанному файлу")
    add("str_rcmd_podcast_name", u"%n = Название подкаста")
    add("str_other_advanced_options", u"Другие расширенные настройки")
    add("str_show_log", u"Показывать лог в отдельной вкладке")



    ## Feed Dialog (add/properties)
    add("str_title", u"Заголовок")
    add("str_url", u"URL")
    add("str_goto_subs", u"Перейти на вкладку описаний, чтобы поглядеть эпизоды")
    add("str_feed_save", u"Сохранить")
    add("str_feed_cancel", u"Отмена")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Включить Планировщик")
    add("str_sched_select_type", u"Выберите переключатели ниже. чтобы определить режим проверки:")
    add("str_check_at_specific_times", u"Проверка в определённое время")
    add("str_check_at_regular_intervals", u"Проверка через интервалы")
    add("str_repeat_every:", u"Повторять каждые:")
    add("str_latest_run", u"Последняя проверка:")
    add("str_next_run", u"Следующая проверка:")
    add("str_not_yet", u"Не сейчас")
    #--- Cancel
    add("str_save_and_close", u"Сохранить и выйти")
    #--- Save

    add("str_time_error", u"Одно из запланированных событий некорретно составлено. Правильный синтаксис: 10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Проверить на новые подкасты путём нажатия зелёной кнопки")
    add("str_last_check", u"Последняя проверка завершена в ")
    add("str_of", u"из")
    add("str_item", u"элем.")
    add("str_items", u"элем.")
    add("str_downloading", u"скачивается")
    add("str_downloaded", u"скачано")
    add("str_enclosure", u"вложить")
    add("str_enclosures", u"вложено")
    add("str_fetched", u"выбрано")
    add("str_loading_mediaplayer", u"Загружается Ваш медиапроигрыватель...")
    add("str_loaded_mediaplayer", u"Загружен Ваш медиапроигрыватель...")        
    add("str_initialized", u"%s готов" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Подкаст-менеджер v" + __version__)
    add("str_localization_restart", u"Чтобы применить установки, необходимо перегрузить программу. Нажмите Ok, чтобы завершить работу, Cancel Для продолжения работы.")
    add("str_really_quit", u"Закачка в процессе.  Прекратить и выйти?");
    add("str_double_check", u"Скачка уже в процессе.");
    
    # check for update
    add("str_new_version_ipodder", u"Доступна новая версия %s, нажмите Ok для перехода на сайт." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Эта версия %s - последняя" % PRODUCT_NAME)
    add("str_other_copy_running", u"Другая копия %s уже запущена. Пожалуйста, дождитесь её закрытия или прервите её выполнение." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Проверить сейчас")        
    add("str_open_ipodder", u"Открыть %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Проверка подкаст-директорий")

    # Feed right-click menu
    add("str_remove", u"Удалить")        
    add("str_open_in_browser", u"Открыть в браузере")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Проиграть эпизод в медиапроигрывателе")
    add("str_clear_selected", u"Очистить выбранные элементы")
