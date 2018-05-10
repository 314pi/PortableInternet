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
       u"Descarga cancelada; espazo ceibe %dMB menor " \
       u"do mínimo %dMB.  Libera espazo no " \
       u"teu disco usando Limpeza ou axustando as opcións " \
       u"de almacenamento en Preferenzas")
   add("str_critical_error_unknown", u"Erro crítico descoñecido mentres descargaba.")

   add("str_error_checking_new_version", u"Lamentámolo, aconteceu un erro cando comprobaba se existe unha nova versión. Por favor, téntao máis tarde.")
   add("str_hours", u"horas")
   add("str_minutes", u"minutos")

   # The next 4 are for the status bar updates during the initial scan.
   add("str_scanning", u"Revisando")
   add("str_scanned", u"Revisado")
   add("str_feed", u"orixe")
   add("str_feeds", u"orixes")

   add("str_downloading_new_episodes", u"Descargando novos episodios")
   add("str_sched_specific", u"Revisar a horas estabelecidas")
   add("str_sched_reg", u"Revisar a intervalos regulares")
   add("str_repeat_every", u"Repetir cada")
   add("str_next_run_label", u"Seguinte revisión:")

   add("str_license", u"Este programa é software ceibe; podes redistribuilo e/ou modificalo baixo os termos da licenza GNU (General Public License) publicada pola Free Software Foundation; aplícase a versión 2 da Licenza, ou calquera versión posterior. Este programa distribuese coa intención de que resulte útil, mais sin ningunha garantía; incluso sin garantía implícita de comerciabilidade ou adecuación a un propósito determinado. \n\nOlla a GNU General Public License para máis detalles.")

   add("str_donate", u"Donativo a %s" % PRODUCT_NAME)
   add("str_donate_expl", u"É importante preservar o esprito comunitario, aberto e público de %s e mante-lo xeito de acceso a este novo medio de comunicación ceibe. Calquera cantidade de diñeiro aledará á equipa de desenrolo e animaraos a traballar en novas prestacións e servizos!" % PRODUCT_NAME)
   add("str_donate_yes", u"Sí, lévame á páxina de donacións agora!")
   add("str_donate_two_weeks", u"Teño que cavilar un chisco máis, lémbramo outra volta dentro dun par de semanas")
   add("str_donate_already", u"Xa fixen a miña donación, non amoses este aviso outra vez")
   add("str_donate_no", u"Non, non desexo donar nada e tampouco quero que me avises máis")
   add("str_donate_one_day", u"Agora non, lémbramo mañá")
   add("str_donate_proceed", u"Proceder")

   add("str_scheduler_dialog", u"Programador")
   add("str_scheduler_tab", u"Preferenzas")

   add("str_select_import_file", u"Selecionar arquivo a importar")
   add("str_add_feed_dialog", u"Engadir unha Orixe")
   add("str_edit_feed", u"Propiedades da Orixe")

   add("str_really_delete", u"Eliminar definitivamente")

   add("str_license_caption", u"Licenza")

   add("str_ep_downloaded", u"Descargados")
   add("str_ep_skipped_removed_other", u"Cancelado/Eliminado/OutraOrixe")
   add("str_dl_state_to_download", u"Para descargar")

   add("str_select_none_cleanup", u"Cancelar seleción")
   add("str_submit_lang", u"Enviar unha linguaxe")

   add("str_dltab_live", u"Descargas activas: ")
   add("str_dltab_ul_speed", u"Velocidade de subida: ")
   add("str_dltab_dl_speed", u"Velocidade de descarga: ")

   ##_________________________________________________________
   ##
   ##     Main window (iPodder.xrc)
   ##_________________________________________________________

   ## File menu
   add("str_file", u"Arquivo")
   add("str_import_opml", u"Importar Orixes dende opml...")
   add("str_export_opml", u"Exportar Orixes como opml...")
   add("str_preferences_menubar", u"Preferenzas...")
   add("str_close_window", u"Pechar xanela")
   add("str_quit", u"Saír")

   add("str_edit", u"Edición")
   add("str_select_all", u"Selecionar todos")

   add("str_tools", u"Ferramentas")
   add("str_check_all", u"Revisar todos")
   add("str_catch_up", u"Capturar")
   add("str_check_selected", u"Revisar selecionados")
   add("str_add_feed", u"Engadir Orixe...")
   add("str_remove_selected", u"Eliminar Orixe")
   add("str_feed_properties", u"Propiedades da Orixe...")
   add("str_scheduler_menubar", u"Programador...")

   add("str_select_language", u"Trocar idioma")

   ## these are also used for the tabs
   add("str_view", u"Ver")
   add("str_downloads", u"Descargas")
   add("str_subscriptions", u"Subscripcións")
   add("str_podcast_directory", u"Directorio de Podcast")
   add("str_cleanup", u"Limpeza")

   add("str_help", u"Axuda")
   add("str_online_help", u"Axuda Online")
   add("str_faq", u"FAQ")
   add("str_check_for_update", u"Procurar Actualizacións...")
   add("str_report_a_problem", u"Informar dun problema")
   add("str_goto_website", u"Ir ao website")
   add("str_make_donation", u"Facer un donativo")
   add("str_menu_license", u"Licenza...")
   add("str_about", u"Acerca de...")

   ## Downloadstab Toolbar
   add("str_remove_selected_items", u"Eliminar elementos selecionados")
   add("str_cancel_selected_download", u"Cancelar descarga")
   add("str_pause_selected", u"Pausar selecionados")

   ## Downloadstab States (in columns)
   ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
   ## other strings, e.g. str_downloading above which isn't capitalized.
   add("str_dl_state_new", u"Novo")
   add("str_dl_state_queued", u"En cola")
   add("str_dl_state_downloading", u"Descargando...")
   add("str_dl_state_downloaded", u"Descargado")
   add("str_dl_state_cancelled", u"Cancelado")
   add("str_dl_state_finished", u"Rematado")
   add("str_dl_state_partial", u"Descargado parcialmente")
   add("str_dl_state_clearing", u"Limpado")

   ## Subscriptionstab Toolbar
   add("str_check_for_new_podcasts", u"Revisar novos podcasts")
   add("str_catch_up_mode", u"Capturar - Só descarga as últimas subscripcións")

   add("str_add_new_feed", u"Engadir nova orixe");
   add("str_remove_selected_feed", u"Eliminar orixe selecionada")
   add("str_properties", u"Propiedades")
   add("str_check_selected_feed", u"Revisar orixe")

   add("str_scheduler_on", u"Programador - On")
   add("str_scheduler_off", u"Programador - Off")

   ## Subscriptionstab Scheduler information
   add("str_next_run:", u"Seguinte revisión:")

   ## Subscriptionstab episode frame
   add("str_downloading_episode_info", u"Descargando info do episodio...")
   add("str_no_episodes_found", u"Non se atoparon episodios.")

   ## Directorytab Toolbar
   add("str_refresh", u"Actualizar")
   add("str_open_all_folders", u"Expandir cartafoles")
   add("str_close_all_folders", u"Contraer cartafoles")
   add("str_add", u"Engadir")

   ## Directorytab Other items
   add("str_directory_description", u"Preme nunha Orixe na árbore, ou teclea/pega na liña de arriba e dalle a Engadir.")

   ## Cleanuptab items
   add("str_select_a_feed", u"Seleciona unha Orixe")
   add("str_refresh_cleanup", u"Actualizar")

   add("str_look_in", u"Procurar episodios en")
   add("str_player_library", u"Biblioteca do Reproductor")
   add("str_downloads_folder", u"Cartafol de descargas")
   add("str_delete_library_entries", u"Eliminar entradas da Biblioteca")
   add("str_delete_files", u"Eliminar arquivos")
   add("str_select_all_cleanup", u"Selecionar todos")
   add("str_delete", u"Eliminar")

   ## Logtab items
   add("str_log", u"Rexistro")
   add("str_clear", u"Limpar")

   ## Columns (in downloads- and subscriptionstab)
   add("str_lst_name", u"Nome")
   add("str_lst_date", u"Data")
   add("str_lst_progress", u"Progreso")
   add("str_lst_state", u"Estado")
   add("str_lst_mb", u"MB")
   add("str_lst_location", u"Localización")
   add("str_lst_episode", u"Episodio")
   add("str_lst_playlist", u"Lista de reproducción")

   ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
   add("str_subscribed", u"Subscrito")
   add("str_disabled", u"Desactivado")
   add("str_newly-subscribed", u"Recén subscrito")
   add("str_unsubscribed", u"Subscripción anulada")
   add("str_preview", u"Previsualizar")
   add("str_force", u"Forzar")

   ##_________________________________________________________
   ##
   ##   Dialog Windows
   ##_________________________________________________________

   ## OPML Import Dialog
   #--- Select import file

   ## OPML Export Dialog
   add("str_choose_name_export_file", u"Elixe un nome para o arquivo a exportar")
   add("str_subs_exported", u"Subscripcións exportadas.")

   ## Preferences Dialog
   add("str_preferences", u"Preferenzas")

   add("str_save", u"Gardar")
   add("str_cancel", u"Cancelar")

   # General
   add("str_general", u"Xerais")
   add("str_gen_options_expl", u"Establece as opcións xerais de %s" % PRODUCT_NAME)
   add("str_hide_on_startup", u"Ao iniciar amosar %s unicamente na Bandexa do Sistema" % PRODUCT_NAME)

   add("str_run_check_startup", u"Revisar se hai novos podcasts cando se inicia a aplicación")
   add("str_play_after_download", u"Reproducir podcasts xusto ao rematar de descargar")
   add("str_location_and_storage", u"Opcións de ubicación e almacenamento")
   add("str_stop_downloading", u"Adiar as descargas se o espazo en disco diminúe por debaixo de")
   add("str_bad_megabyte_limit_1", u"Laméntoo, o límite de megas non semella ser un número enteiro")
   add("str_bad_megabyte_limit_2", u"Por favor, téntao de novo.")

   add("str_download_folder", u"Descargar podcasts neste cartafol")
   add("str_browse", u"Examinar")
   add("str_bad_directory_pref_1", u"Laméntoo, non son quen de atopar o cartafol introducido")
   add("str_bad_directory_pref_2", u"Por favor, crea o cartafol e téntao de novo.")

   # Threading
   add("str_threads", u"Multifíos")
   add("str_multiple_download", u"Opcións de descargas múltiples")
   add("str_max_feedscans", u"max. de fíos para revisión de orixes por sesión")
   add("str_max_downloads", u"max. de descargas por sesión")

   # Network settings
   add("str_networking", u"Opcións de Rede")
   add("str_coralize_urls", u"Coralizar URL's (experimental)")
   add("str_proxy_server", u"Usar un servidor proxy")
   add("str_proxy_address", u"Enderezo")
   add("str_proxy_port", u"Porto")
   add("str_proxy_username", u"Nome de usuario")
   add("str_proxy_password", u"Chave")
   add("str_bad_proxy_pref", u"Habilitaches o soporte proxy mais non definiches o servidor nin o porto. Por favor volta á pestana das opcións de Rede e introduce a IP e porto do proxy.")

   # Player
   add("str_player", u"Reproductor")
   add("str_choose_a_player", u"Elixe un reproductor")
   add("str_no_player", u"Sin reproductor")

   # Advanced
   add("str_advanced", u"Avanzado")
   add("str_options_power_users", u"Estas opcións deben ser modificadas por usuarios avanzados")
   add("str_run_command_download", u"Executar este comando após cada descarga")
   add("str_rcmd_full_path", u"%f = Roteiro completo ao ficheiro descargado")
   add("str_rcmd_podcast_name", u"%n = nome do podcast")
   add("str_other_advanced_options", u"Outras opcións avanzadas")
   add("str_show_log", u"Amosar pestana de Rexistro")

   ## Feed Dialog (add/properties)
   add("str_title", u"Título")
   add("str_url", u"URL")
   add("str_goto_subs", u"Ir á pestana de subscripcións para ve-los episodios desta Orixe")
   add("str_feed_save", u"Gardar")
   add("str_feed_cancel", u"Cancelar")

   ## Scheduler Dialog
   add("str_enable_scheduler", u"Activar Programador")
   add("str_sched_select_type", u"Seleciona os botóns para revisar a horas estabelecidas ou a intervalos regulares:")
   add("str_check_at_specific_times", u"Revisar a horas estabelecidas")
   add("str_check_at_regular_intervals", u"Revisar a intervalos regulares")
   add("str_repeat_every:", u"Repetir cada:")
   add("str_latest_run", u"Última revisión:")
   add("str_next_run", u"Seguinte revisión:")
   add("str_not_yet", u"Aínda non")
   #--- Cancel
   add("str_save_and_close", u"Gardar e pechar")
   #--- Save

   add("str_time_error", u"Unha das horas programadas semella non ser correcta. As horas válidas son do seguinte xeito: 10:02am, 16:43.")

   ## Donations Dialog
   #--- Donativo a iPodder
   #--- É importante preservar o esprito comunitario, aberto e público de iPodder e mante-lo xeito de acceso a este novo medio de comunicación ceibe. Calquera cantidade de diñeiro aledará á equipa de desenrolo e animaraos a traballar en novas prestacións e servizos!
   #--- Sí, lévame á páxina de donacións agora!
   #--- Teño que cavilar un chisco máis, lémbramo outra volta dentro dun par de semanas
   #--- Xa fixen a miña donación, non amoses este aviso outra vez
   #--- Non, non desexo donar nada e tampouco quero que me avises máis
   #--- Agora non, lémbramo mañá
   #--- Proceder

   ## About Dialog
   #--- Versión:
   #--- Programación: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDeseño: Martijn Venrooy\nAnalista de contidos: Mark Alexander Posth\nConcepto: Adam Curry, Dave Winer\nVersión en Galego: Ramiro Rodríguez Suárez\nGrazas a tódolos traductores polas súas comisións!\n\nBaseado nas tecnoloxías Feedparser e BitTorrent.\nEste programa é software ceibe; podes redistribuilo e/ou modificalo baixo os termos da licenza GNU (General Public License) publicada pola Free Software Foundation; aplícase a versión 2 da Licenza, ou calquera versión posterior. Este programa distribuese coa intención de que resulte útil, mais sin ningunha garantía; incluso sin garantía implícita de comerciabilidade ou adecuación a un propósito determinado. \n\nOlla a GNU General Public License para máis detalles.

   ## Statusbar items
   add("str_check_for_new_podcast_button", u"Procurar novos podcasts premendo no botón verde")
   add("str_last_check", u"Última revisión completada ás")
   add("str_of", u"de")
   add("str_item", u"elemento")
   add("str_items", u"elementos")
   add("str_downloading", u"descargando")
   add("str_downloaded", u"descargado")
   add("str_enclosure", u"ámbito")
   add("str_enclosures", u"ámbitos")
   add("str_fetched", u"adequiridos")
   add("str_loading_mediaplayer", u"Cargando o reproductor...")
   add("str_loaded_mediaplayer", u"Cargado o reproductor...")
   add("str_initialized", u"%s listo" % PRODUCT_NAME)

   ## Other application strings
   add("str_ipodder_title", PRODUCT_NAME + u" - Receptor Podcast v" + __version__)
   add("str_localization_restart", u"Para localizar tódolos controis de %s é preciso que reinicies. Preme Ok para reiniciar ou Cancelar para continuar." % PRODUCT_NAME)
   add("str_really_quit", u"Descarga en marcha. Queres saír?");
   add("str_double_check", u"Semella que aínda hai unha descarga en marcha.");

   # check for update
   add("str_new_version_ipodder", u"Está dispoñible unha nova versión de %s, preme Ok para visitar a páxina de descargas." % PRODUCT_NAME)
   add("str_no_new_version_ipodder", u"Esta versión de %s está ao día" % PRODUCT_NAME)
   add("str_other_copy_running", u"Outra copia de %s está en execución. Por favor, actívaa, agarda a que remate ou péchaa." % PRODUCT_NAME)

   # Windows taskbar right-click menu
   add("str_check_now", u"Revisar agora")
   add("str_open_ipodder", u"Abrir %s" % PRODUCT_NAME)
   #--- Downloading
   add("str_scanning_feeds", u"Revisando orixes")

   # Feed right-click menu
   add("str_remove", u"Eliminar")
   add("str_open_in_browser", u"Abrir no navegador")

   # Downloads right-click menu
   add("str_play_episode", u"Reproducir episodio")
   add("str_clear_selected", u"Eliminar elementos selecionados")

