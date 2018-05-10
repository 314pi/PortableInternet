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
        u"Descarga cancelada; espacio libre %dMB menos " \
        u"que el minimo de %dMB.  Por favor, libere espacio en" \
        u"su disco usando la herramienta limpieza o ajustando los parámetros de administrador" \
        u"de almacenamiento en Preferencias")
    add("str_critical_error_unknown", u"Error critico desconocido en la descarga")
    
    add("str_error_checking_new_version", u"Error comprobando nueva versión.  Por favor, intentelo más tarde.")
    add("str_hours", u"horas")
    add("str_minutes", u"minutos")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Revisando")
    add("str_scanned", u"Revisado")
    add("str_feed", u"fuente")
    add("str_feeds", u"fuentes")
    
    add("str_downloading_new_episodes", u"Descargando nuevos episodios")
    add("str_sched_specific", u"Comprobar en instantes determinados")
    add("str_sched_reg", u"Comprobar en intervalos regulares")
    add("str_repeat_every", u"Repetir cada")
    add("str_next_run_label", u"Próxima ejecución:")
    
    add("str_license", u"Este programa es de codigo libre; puedes distribuirlo y/o modificarlo bajo los términos de la licencia GNU General Public License publicada por la Free Software Foundation, tanto en la versión 2 de la Licencia como en cualquier version posterior. Este programa se distribuye con la finalidad de ser útil, pero sin ninguna garantía; incluso sin la garantia implicita en la comercialidad o el proposito particular de un programa. \n\nMira la GNU General Public License para más detalles.")

	

    add("str_donate", u"Donar a %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Es importante mantener las aplicaciones de la comunidad %s online y mantener esta nueva forma de transmitir contenidos multimedia. Cualquier aporte de dinero sera bien recibido por el equipo y los animara a trabajar en nuevas características y servicios!" % PRODUCT_NAME)


    add("str_donate_yes", u"Si, llevame a la pagina de donaciones ahora!")
    add("str_donate_two_weeks", u"Todavia me lo tengo que pensar un poco más, vuelve a consultarme en dos semanas")
    add("str_donate_already", u"Ya he hecho una donación, no vuelvas a consultarme")
    add("str_donate_no", u"No, no quiero hacer ninguna donación, no vuelvas a consultarme")
    add("str_donate_one_day", u"Ahora no, consultame otra vez mañana")
    add("str_donate_proceed", u"Procede")

    add("str_scheduler_dialog", u"Planificador")
    add("str_scheduler_tab", u"Opciones")

    add("str_select_import_file", u"Selecciona el fichero a importar")    
    add("str_add_feed_dialog", u"Añadir una fuente")
    add("str_edit_feed", u"Propiedades de la fuente")

    add("str_really_delete", u"Definitivamente borralo")

    add("str_license_caption", u"Licencia")

    add("str_ep_downloaded", u"Descargado")
    add("str_ep_skipped_removed_other", u"Omitido/Eliminado/Otra fuente")
    add("str_dl_state_to_download", u"Para descargar")

    add("str_select_none_cleanup", u"No seleccionar ninguno")
    add("str_submit_lang", u"Enviar un idioma")
    
    add("str_dltab_live", u"Descargas actuales:")
    add("str_dltab_ul_speed", u"Velocidad de subida: ")
    add("str_dltab_dl_speed", u"Velocidad de descarga: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Archivo")
    add("str_import_opml", u"Importar fuentes de ompl...")
    add("str_export_opml", u"Exportar fuentes a opml...")
    add("str_preferences_menubar", u"Preferencias...")
    add("str_close_window", u"Cerrar ventana")
    add("str_quit", u"Salir")

    add("str_edit", u"Editar")
    add("str_select_all", u"Seleccionar todo")

    add("str_tools", u"Herramientas")
    add("str_check_all", u"Comprobar todos")
    add("str_catch_up", u"Ponerse al dia")
    add("str_check_selected", u"Comprobar seleccionados")
    add("str_add_feed", u"Añadir una fuente...")
    add("str_remove_selected", u"Eliminar fuente")
    add("str_feed_properties", u"Propiedades de la fuente...")
    add("str_scheduler_menubar", u"Planificador...")
    
    add("str_select_language", u"Seleccionar idioma")

    ## these are also used for the tabs
    add("str_view", u"Ver")
    add("str_downloads", u"Descargas")
    add("str_subscriptions", u"Suscripciones")
    add("str_podcast_directory", u"Directorio de Podcast")
    add("str_cleanup", u"Limpiar")

    add("str_help", u"Ayuda")
    add("str_online_help", u"Ayuda online")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Comprobar actualizaciones...")
    add("str_report_a_problem", u"Notificar un problema")
    add("str_goto_website", u"Ir al sitio web")
    add("str_make_donation", u"Hacer una donación")
    add("str_menu_license", u"Licencia...")
    add("str_about", u"Sobre...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Eliminar elementos seleccionados")
    add("str_cancel_selected_download", u"Cancelar la descarga seleccionada")
    add("str_pause_selected", u"Interrumpir los elementos seleccionados")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Nuevo")
    add("str_dl_state_queued", u"En cola")
    add("str_dl_state_downloading", u"Descargando")
    add("str_dl_state_downloaded", u"Descargado")
    add("str_dl_state_cancelled", u"Cancelado")
    add("str_dl_state_finished", u"Terminado")
    add("str_dl_state_partial", u"Descargado parcialmente")
    add("str_dl_state_clearing", u"Limpiando")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Comprobar nuevos podcasts")
    add("str_catch_up_mode", u"Ponerse al dia - Descargar solo las ultimas suscripciones")

    add("str_add_new_feed", u"Añadir nueva fuente");
    add("str_remove_selected_feed", u"Eliminar fuente seleccionada")
    add("str_properties", u"Propiedades")
    add("str_check_selected_feed", u"Comprobar fuente seleccionada")

    add("str_scheduler_on", u"Planificador - Activado")
    add("str_scheduler_off", u"Planificador - Desactivado")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Proxima tarea planificada:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Descargando información del episodio...")
    add("str_no_episodes_found", u"Ningun episodio encontrado.")


    ## Directorytab Toolbar
    add("str_refresh", u"Actualizar")
    add("str_open_all_folders", u"Abrir todoas las carpetas")
    add("str_close_all_folders", u"Cerrar todas las carpetas")
    add("str_add", u"Añadir")

    ## Directorytab Other items
    add("str_directory_description", u"Haz click en una fuente o escribe/pega en el espacio disponible y haz click en añadir")




    ## Cleanuptab items
    add("str_select_a_feed", u"Selecciona una fuente")
    add("str_refresh_cleanup", u"Actualizar")
    
    add("str_look_in", u"Buscar episodios en")        
    add("str_player_library", u"Libreria de reproducción")
    add("str_downloads_folder", u"Directorio de descargas")
    add("str_delete_library_entries", u"Eliminar entradas de la biblioteca")
    add("str_delete_files", u"Eliminar ficheros")
    add("str_select_all_cleanup", u"Seleccionar todo")
    add("str_delete", u"Eliminar")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Limpiar")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nombre")
    add("str_lst_date", u"Fecha")        
    add("str_lst_progress", u"Progreso")
    add("str_lst_state", u"Estado")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Localización")
    add("str_lst_episode", u"Episodio")
    add("str_lst_playlist", u"Lista de reproducción")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Suscrito")
    add("str_disabled", u"Desactivado")
    add("str_newly-subscribed", u"Nueva suscripción")
    add("str_unsubscribed", u"No suscrito")
    add("str_preview", u"Previsualizar")
    add("str_force", u"Forzar")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Escoge un nombre para el archivo a exportar")
    add("str_subs_exported", u"Suscripciones exportadas.")
    
    ## Preferences Dialog
    add("str_preferences", u"Preferencias")
    
    add("str_save", u"Guardar")
    add("str_cancel", u"Cancelar")
    
    # General
    add("str_general", u"General")
    add("str_gen_options_expl", u"Establecer las opciones generales para la aplicacion %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Mostrar %s en la barra de herramientas al inicio" % PRODUCT_NAME)

    add("str_run_check_startup", u"Comprobar nuevos podcasts al iniciar la aplicación ")
    add("str_play_after_download", u"Reproducir las descargas al terminar de bajarse")
    add("str_location_and_storage", u"Administración de localización y almacenamiento")
    add("str_stop_downloading", u"Parar de descargar si el disco duro alcanza un minimo de ")
    add("str_bad_megabyte_limit_1", u"El límite de megabytes no es un numero entero")
    add("str_bad_megabyte_limit_2", u"Prueba otra vez.")

    add("str_download_folder", u"Descargar podcasts en este directorio")
    add("str_browse", u"Navegar")
    add("str_bad_directory_pref_1", u"No se ha podido encontrar el directorio solicitado")
    add("str_bad_directory_pref_2", u"Por favor, vuelve a crearlo y prueba otra vez.")

    
    # Threading
    add("str_threads", u"Hilos concurrentes")
    add("str_multiple_download", u"Opciones de descarga múltiple")
    add("str_max_feedscans", u"Máximos hilos concurrentes de revisión de fuentes por sesión")
    add("str_max_downloads", u"Máximas descargas por sesión")
   
    # Network settings
    add("str_networking", u"Opciones de red")
    add("str_coralize_urls", u"Coralize URLs (experimental)")
    add("str_proxy_server", u"Utilizar servidor proxy")
    add("str_proxy_address", u"Dirección")
    add("str_proxy_port", u"Puerto")
    add("str_proxy_username", u"Nombre de usuario")
    add("str_proxy_password", u"Contraseña")
    add("str_bad_proxy_pref", u"Has activado el soporte para servidor proxy pero no has introducido el servidor proxy y el puerto. Vuelve a la pestaña de opciones de red e introduce un servidor proxy y un puerto válidos.")



    # Player
    add("str_player", u"Reproductor")
    add("str_choose_a_player", u"Elegir un reproductor")
    add("str_no_player", u"Ningun reproductor")
    
    # Advanced
    add("str_advanced", u"Avanzado")
    add("str_options_power_users", u"Estas opciones pueden ser usadas por usuarios avanzados")
    add("str_run_command_download", u"Ejecuta este comando después de cada descarga")
    add("str_rcmd_full_path", u"%f = Ruta entera al archivo descargado")
    add("str_rcmd_podcast_name", u"%n = nombre del Podcast")
    add("str_other_advanced_options", u"Otras opciones avanzadas")
    add("str_show_log", u"Mostrar pestaña de log en la aplicación")



    ## Feed Dialog (add/properties)
    add("str_title", u"Titulo")
    add("str_url", u"Dirección URL")
    add("str_goto_subs", u"Ir a la pestaña de suscripciones para ver los episodios de esta fuente")
    add("str_feed_save", u"Guardar")
    add("str_feed_cancel", u"Cancelar")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Activar planificador")
    add("str_sched_select_type", u"Selecciona los botones debajo para comprobar en instantes especificos o en intervalos regulares:")
    add("str_check_at_specific_times", u"Comprobar en instantes determinados")
    add("str_check_at_regular_intervals", u"Comprobar en intervalos regulares")
    add("str_repeat_every:", u"Repetir cada:")
    add("str_latest_run", u"Última ejecución:")
    add("str_next_run", u"Próxima ejecución:")
    add("str_not_yet", u"Todavia no")
    #--- Cancel
    add("str_save_and_close", u"Guardar y cerrar")
    #--- Save

    add("str_time_error", u"Alguna de las horas planificadas no parece ser correcta. Valores válidos son de la forma:  10:02am, 16:43.")


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
    add("str_check_for_new_podcast_button", u"Comprobar nuevos podcasts pulsando el boton verde de comprobar")
    add("str_last_check", u"Ultima comprobación llevada a cabo a las")
    add("str_of", u"de")
    add("str_item", u"elemento")
    add("str_items", u"elementos")
    add("str_downloading", u"descargando")
    add("str_downloaded", u"descargado")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"fetched")
    add("str_loading_mediaplayer", u"Cargando tu reproductor multimedia...")
    add("str_loaded_mediaplayer", u"Reproductor multimedia cargado...")        
    add("str_initialized", u"%s listo" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"Para localizar todos los controles de %s es necesario reiniciar. Haz click en ok para reiniciar, o en cancelar para continuar." % PRODUCT_NAME)
    add("str_really_quit", u"Hay descargas en curso, seguro que deseas salir?");
    add("str_double_check", u"Parece que algun archivo esta descargandose");
    
    # check for update
    add("str_new_version_ipodder", u"Existe una nueva version de %s disponible, haz click en Ok para ir a la pagina de descargas." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"This version of %s is up to date" % PRODUCT_NAME)
    add("str_other_copy_running", u"%s ya esta ejecutandose. Por favor, apagalo o espera a que acabe." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Comprobar ahora")        
    add("str_open_ipodder", u"Abrir %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Escanear fuentes")

    # Feed right-click menu
    add("str_remove", u"Eliminar")        
    add("str_open_in_browser", u"Abrir en el navegador")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Reproducir episodio en el reproductor multimedia.")
    add("str_clear_selected", u"Eliminar elementos seleccionados")
    



