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
    ## Traducao realizada Colaborativamente por podcasters brasileiros
    #############################################

    ##_________________________________________________________
    ##
    ##     New strings
    ##_________________________________________________________

    add("str_critical_error_minspace_exceeded", \
        u"Download parado; espaço livre (%dMB) " \
        u"é menor que o min de %dMB.  Libere espaço em disco " \
        u"Utilizando a ferramenta Limpeza ou ajustando " \
        u"os valores de gerenciamento nas Preferências")
    add("str_critical_error_unknown", u"Erro crítico desconhecido no download.")

    add("str_error_checking_new_version", u"Lamentamos, mas houve um erro ao verificar por novas versões. Tente novamente mais tarde.")
    add("str_hours", u"horas")
    add("str_minutes", u"minutos")

   # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Examinando")
    add("str_scanned", u"Examinado")
    add("str_feed", u"feed")
    add("str_feeds", u"feeds")

    add("str_downloading_new_episodes", u"Baixar novos episódios")
    add("str_sched_specific", u"Checar por um horário específico")
    add("str_sched_reg", u"Checar por um intervalo regular")
    add("str_repeat_every", u"Repetir sempre")
    add("str_next_run_label", u"Próxima ação:")

    add("str_license", u"Este programa é um programa desenvolvido em Software Livre; você pode redistribuir e/ou modifica-lo conforme os termos da licença GNU Public License publicada pela Free Software Foundation; também pela versão 2 da Licença, ou (em sua opção) qualquer versão posterior. Este programa é distribuído na esperança que será útil, mas sem nenhuma garantia; também sem a garantia imposta de mercadabilidade ou de encaixe em algum propósito específico. \n\nPor favor, leia a licença GNU General Public License para maiores detalhes.")

    add("str_donate", u"Doações para %s" % PRODUCT_NAME)
    add("str_donate_expl", u"É importante para manter os programas e aplicações %s mantido pela comunidade e online e também para manter esse novo modo de consumo de informação livre como no discurso. Qualquer quantia de dinheiro irá fazer a equipe mais feliz além de encorajá-los para continuar trabalhando em novos serviços e melhorias!" % PRODUCT_NAME)
    add("str_donate_yes", u"Sim, leve-me a página de doações agora!")
    add("str_donate_two_weeks", u"Ainda quero dar mais uma olhada, mostre-me isso em 2 semanas")
    add("str_donate_already", u"Eu já fiz minha parte, não mostre este diálogo novamente")
    add("str_donate_no", u"Não, eu não quero doar, nunca mais me mostre essa mensagem denovo")
    add("str_donate_one_day", u"Não agora, tente novamente amanhã")
    add("str_donate_proceed", u"Proceda")

    add("str_scheduler_dialog", u"Agendamento")
    add("str_scheduler_tab", u"Configurações")

    add("str_select_import_file", u"Selecionar arquivo para importar")
    add("str_add_feed_dialog", u"Adicionar um Feed")
    add("str_edit_feed", u"Feed propriedades")

    add("str_really_delete", u"Apagar realmente")

    add("str_license_caption", u"Licença")

    add("str_ep_downloaded", u"Baixado")
    add("str_ep_skipped_removed_other", u"Pulado/Removido/OutroFeed")
    add("str_dl_state_to_download", u"Para baixar")

    add("str_select_none_cleanup", u"Selecionar nenhum")
    add("str_submit_lang", u"Enviar um Idioma")
    add("str_dltab_live", u"Baixando agora: ")
    add("str_dltab_ul_speed", u"Velocidade de envio: ")
    add("str_dltab_dl_speed", u"Velocidade de recebimento: ")



    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________



    ## File menu
    add("str_file", u"Arquivo")
    add("str_import_opml", u"Importar feeds de opml...")
    add("str_export_opml", u"Exportar feeds como opml...")
    add("str_preferences_menubar", u"Preferências...")
    add("str_close_window", u"Fechar Janela")
    add("str_quit", u"Sair")

    add("str_edit", u"Editar")
    add("str_select_all", u"Selecionar tudo")

    add("str_tools", u"Ferramentas")
    add("str_check_all", u"Verificar tudo")
    add("str_catch_up", u"Pegar tudo")
    add("str_check_selected", u"Verificar selecionado")
    add("str_add_feed", u"Adicionar um Feed...")
    add("str_remove_selected", u"Apagar Feed")
    add("str_feed_properties", u"Propriedades Feed...")
    add("str_scheduler_menubar", u"Agendamento...")

    add("str_select_language", u"Selecionar Idioma")

    ## these are also used for the tabs
    add("str_view", u"Visualizar")
    add("str_downloads", u"Downloads")
    add("str_subscriptions", u"Assinaturas")
    add("str_podcast_directory", u"Diretório Podcast")
    add("str_cleanup", u"Limpeza")

    add("str_help", u"Ajuda")
    add("str_online_help", u"Ajuda Online")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Verificar Atualização...")
    add("str_report_a_problem", u"Reportar um problema")
    add("str_goto_website", u"Ir para o Website")
    add("str_make_donation", u"Fazer uma Doação")
    add("str_menu_license", u"Licença...")
    add("str_about", u"Sobre...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Remover ítens selecionados")
    add("str_cancel_selected_download", u"Cancelar downloads selecionados")
    add("str_pause_selected", u"Pausar seleção")

    ## Downloadstab States (em colunas)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Novo")
    add("str_dl_state_queued", u"Na fila")
    add("str_dl_state_downloading", u"Baixando")
    add("str_dl_state_downloaded", u"Baixado")
    add("str_dl_state_cancelled", u"Cancelado")
    add("str_dl_state_finished", u"Finalizado")
    add("str_dl_state_partial", u"Parcialmente baixado")
    add("str_dl_state_clearing", u"Limpando")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Procurar por novos podcasts")
    add("str_catch_up_mode", u"Pegar - Baixar somente as novas assinaturas")

    add("str_add_new_feed", u"Adicionar novo feed");
    add("str_remove_selected_feed", u"Apagar feed selecionado")
    add("str_properties", u"Propriedades")
    add("str_check_selected_feed", u"Checar feed selecionado")

    add("str_scheduler_on", u"Agendamento - Ligado")
    add("str_scheduler_off", u"Agendamento - Desligado")

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Próxima ação:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Baixando informações sobre episódios...")
    add("str_no_episodes_found", u"Nenhum episódio encontrado.")


    ## Directorytab Toolbar
    add("str_refresh", u"Atualizar")
    add("str_open_all_folders", u"Abrir todos as pastas")
    add("str_close_all_folders", u"Fechar todas as pastas")
    add("str_add", u"Adicionar")

    ## Directorytab Other items
    add("str_directory_description", u"Clique em um feed na árvore ou digite/cole no espaço acima e clique em Adicionar.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Selecionar um feed")
    add("str_refresh_cleanup", u"Atualizar")

    add("str_look_in", u"Procurar por epísódios em")
    add("str_player_library", u"Biblioteca do Tocador")
    add("str_downloads_folder", u"Diretório de download")
    add("str_delete_library_entries", u"Apagar entradas da biblioteca")
    add("str_delete_files", u"Apagar arquivos")
    add("str_select_all_cleanup", u"Selecionar tudo")
    add("str_delete", u"Apagar")




    ## Logtab items
    add("str_log", u"Log")
    add("str_clear", u"Limpar")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nome")
    add("str_lst_date", u"Data")
    add("str_lst_progress", u"Progresso")
    add("str_lst_state", u"Estado")
    add("str_lst_mb", u"MB")
    add("str_lst_location", u"Localização")
    add("str_lst_episode", u"Episódio")
    add("str_lst_playlist", u"Playlist")

    ##Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Assinado")
    add("str_disabled", u"Desabilitado")
    add("str_newly-subscribed", u"Novas Postagens")
    add("str_unsubscribed", u"Assinatura Cancelada")
    add("str_preview", u"Prever")
    add("str_force", u"Forçar")






    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Select import file

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Escolha um nome para exportar o arquivo")
    add("str_subs_exported", u"Assinaturas exportadas")

    ## Preferences Dialog
    add("str_preferences", u"Preferências")

    add("str_save", u"Salvar")
    add("str_cancel", u"Cancelar")

    ## General
    add("str_general", u"Geral")
    add("str_gen_options_expl", u"Ajusta as opções gerais para o programa %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Ao íniciar mostre somente o %s no systray" % PRODUCT_NAME)

    add("str_run_check_startup", u"Verificar por novos podcasts quando iniciado")
    add("str_play_after_download", u"Tocar os podcasts assim que terminado o download")
    add("str_location_and_storage", u"Gerenciamento de local e armazanagem")
    add("str_stop_downloading", u"Parar downloads se o disco rígido alcançar um mínimo de")
    add("str_bad_megabyte_limit_1", u"O valor deve ser inteiro")
    add("str_bad_megabyte_limit_2", u"Por favor tente novamente.")

    add("str_download_folder", u"Salvar os podcasts nesta pasta")
    add("str_browse", u"Browse")
    add("str_bad_directory_pref_1", u"Não foi possível encontrar o diretório que específicou")
    add("str_bad_directory_pref_2", u"Crie-o e tente novamente.")


    ## Threading
    add("str_threads", u"Downloads Multplos")
    add("str_multiple_download", u"Configurações de downloads mltiplos")
    add("str_max_feedscans", u"threads maximos por sesso")
    add("str_max_downloads", u"Mximo de Downloads por sessão")

    ## Network settings
    add("str_networking", u"Configurações de Rede")
    add("str_coralize_urls", u"Coralizar URLs (experimental)")
    add("str_proxy_server", u"Usar um servidor proxy")
    add("str_proxy_address", u"Endereço")
    add("str_proxy_port", u"Porta")
    add("str_proxy_username", u"Nome de usuário")
    add("str_proxy_password", u"Senha")
    add("str_bad_proxy_pref", u"Você habilitou o suporte a proxy, mas não definiu um proxy e uma porta.  Volte as oprções de de Rede e defina um host de proxy e uma porta.")

    ## Player
    add("str_player", u"Player")
    add("str_choose_a_player", u"Escolha um player")
    add("str_no_player", u"Nenhum player")

   # Advanced
    add("str_advanced", u"Avançado")
    add("str_options_power_users", u"Estas opções podem ser utilizadas por usuários experientes")
    add("str_run_command_download", u"Rode este comando após cada download")
    add("str_rcmd_full_path", u"%f = Caminho completo para o arquivo baixado")
    add("str_rcmd_podcast_name", u"%n = Nome do Podcast")
    add("str_other_advanced_options", u"Outras opções avançadas")
    add("str_show_log", u"Mostra aba de log no programa")



    ## Feed Dialog (add/properties)
    add("str_title", u"Título")
    add("str_url", u"URL")
    add("str_goto_subs", u"Vá para a aba de assinaturas para ver os episódios")
    add("str_feed_save", u"Salvar")
    add("str_feed_cancel", u"Cancelar")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Habilitar agendamento")
    add("str_sched_select_type", u"Selecione os botões abaixo para checar em hora específica ou periodicamente:")
    add("str_check_at_specific_times", u"Checar nestes horários específicos")
    add("str_check_at_regular_intervals", u"Checar em intervalos regulares")
    add("str_repeat_every:", u"Repetir sempre:")
    add("str_latest_run", u"Ultima vez rodado:")
    add("str_next_run", u"Próxima vez:")
    add("str_not_yet", u"Ainda não")
    #--- Cancel
    add("str_save_and_close", u"Salvar e fechar")
    #--- Save

    add("str_time_error", u"Um dos horários definidos não parece correto. Horários válidos devem ser assim: 10:02am, 16:43.")


    ## Donations Dialog
    #--- Doar para o iPodder
    #--- É muito importante para manter o  iPodder e suas aplicações online e não-comerciais e para manter este novo modelo de consumo de media livre. Qualquer quantia de dinheiro irá tornar a equipe mais feliz e encorajá-los no trabalho e desenvolvimento de melhorias!
    #--- Sim, leve a página de doaçoes agora!
    #--- Quero dar mais uma olhada antes, me mostre isso em duas semanas
    #--- Eu ja fiz minha parte, não mostre este diálogo novamente
    #--- Não, eu não quero doar nada, e não mostre este diálogo novamente
    #--- Não agora, tente novamente amanhã
    #--- OK




    ## About Dialog
    #--- Versão:
    #--- Programação: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDesign: Martijn Venrooy\nEstrategista de Conteúdo: Mark Alexander Posth\nConceito: Adam Curry, Dave Winer\nAgradecemos a todos os tradutores por suas contribuíções!\n\nBaseado em um Feedparser e na tecnologia BitTorrent.\nEste programa é Software Livre; você pode re-distribuí-lo e/ou modificá-lo sob os termos da Licença GNU General Public License como publicada pela FSF - Free Software Foundation; também sob a licença 2, ou (em sua opção) qualquer versão posterior. Este programa é distribuído na esperança que será útil, mas sem nenhuma garantia; mesmo sem a garantia de mercadabilidade ou de encaixe em algum propósito específico. \n\nVeja a GNU General Public License para mais detalhes.




    ## Statusbar items
    add("str_check_for_new_podcast_button", u"Procure por novos podcasts clicando no botão verde")
    add("str_last_check", u"Ultima verificação feita em ")
    add("str_of", u"de")
    add("str_item", u"[ítem")
    add("str_items", u"ítens")
    add("str_downloading", u"baixando")
    add("str_downloaded", u"baixado")
    add("str_enclosure", u"embutido")
    add("str_enclosures", u"embutidos")
    add("str_fetched", u"pego")
    add("str_loading_mediaplayer", u"Carregando seu tocador...")
    add("str_loaded_mediaplayer", u"Tocador carregado...")
    add("str_initialized", u"%s aguardando" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast receiver v" + __version__)
    add("str_localization_restart", u"É necessário que o %s seja re-iniciado. Clique Ok para terminar de forma limpa, cancelar para continuar." % PRODUCT_NAME)
    add("str_really_quit", u"Um download está sendo realizado. Quer mesmo sair?");
    add("str_double_check", u"Um arquivo está sendo baixado.");

    ## check for update
    add("str_new_version_ipodder", u"Uma nova versão do %s esta disponível, clique em  Ok e acesso o site de download." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Esta versão é a mais recente")
    add("str_other_copy_running", u"Outra cópia do %s está rodando. Pare-a, espere até estar completo, ou mate-a." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Checar Agora")
    add("str_open_ipodder", u"Abrir %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Procurar feeds")

    # Feed right-click menu
    add("str_remove", u"Remover")
    add("str_open_in_browser", u"Abrir no navegador")



    ## Downloads right-click menu
    add("str_play_episode", u"Tocar episódio no seu tocador")
    add("str_clear_selected", u"Limpar ítems selecionados")
