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

    #######################################################
    ## MV: 03 mar 2005 22:00
    ## A LIRE AVANT D'EDITER / AJOUTER !!
    ## Si vous ajoutez de nouvelles entrées,
    ## ajoutez les dans la partie "Nouvelles chaines'.
    ## On pourra facilement les transmettre aux traducteurs.
    #######################################################

    ##_________________________________________________________
    ##
    ##     Nouvelles chaines
    ##_________________________________________________________

    add("str_error_checking_new_version", u"Nous sommes désolé, il y a eu une erreur lors de la vérification de mise à jour. Essayer de nouveau plus tard.")
    add("str_hours", u"heures")
    add("str_minutes", u"minutes")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Recherche en cours")
    add("str_scanned", u"Recherche terminée")
    add("str_feed", u"source")
    add("str_feeds", u"sources")

    add("str_downloading_new_episodes", u"Téléchargement de nouveaux épisodes")

    add("str_select_none_cleanup", u"Aucun")
    add("str_submit_lang", u"Soumettre une traduction")
    
    add("str_dltab_live", u"Téléchargement en cours : ")
    add("str_dltab_ul_speed", u"Vitesse d'envoi : ")
    add("str_dltab_dl_speed", u"Vitesse de réception : ")
    


    add("str_sched_specific", u"Vérifier à heure régulière")
    add("str_sched_reg", u"Vérifier à intervals réguliers")
    add("str_repeat_every", u"Répéter tous les")
    add("str_next_run_label", u"Prochaine vérification :")
    
    add("str_menu_license", u"Licence")
    add("str_license", u"Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous). Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique.\n\nReportez-vous à la Licence Publique Générale GNU pour plus de détails.")
    add("str_donate", u"Faites un don pour %s" % PRODUCT_NAME)
    add("str_donate_expl", u"Il est important de garder les applications %s communautaire en ligne et de garder cette nouvelle façon de consommer les médias, libre. Quelque soit la somme, l'équipe de développement sera contente et sera encouragée à développer de nouvelles fonctionnalités et de nouveaux services !" % PRODUCT_NAME)
    add("str_donate_yes", u"Oui, envoyez-moi sur la page de contributions !")
    add("str_donate_two_weeks", u"Je dois encore y jeter un oeil, montre moi ça de nouveau dans 2 semaines.")
    add("str_donate_already", u"J'ai déjà fait un don. Ne me montre plus cette fenêtre.")
    add("str_donate_no", u"Non, je ne veux pas faire de don, ne me montre plus cette fenêtre.")
    add("str_donate_one_day", u"Pas maintenant, rappelez-moi demain")
    add("str_donate_proceed", u"Allez, on y va :o)")

    add("str_preferences", u"Préférences")
    add("str_preferences_menubar", u"Préférences...")

    add("str_scheduler_dialog", u"Programmateur")
    add("str_scheduler_tab", u"Préférences")
    add("str_scheduler_menubar", u"Programmateur...")

    add("str_select_import_file", u"Choisir un fichier à importer")    
    add("str_add_feed_dialog", u"Ajouter une source")
    add("str_edit_feed", u"Propriétés de la source")

    add("str_really_delete", u"Vraiment effacer")

    add("str_license_caption", u"Licence")

    add("str_ep_downloaded", u"téléchargé")
    add("str_ep_skipped_removed_other", u"Sauté/Enlevé/AutreSource")
    add("str_dl_state_to_download", u"A télécharger")


    
    ##_________________________________________________________
    ##
    ##     Fenêtre principale (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Fichier")
    add("str_import_opml", u"Importer depuis un fichier OPML...")
    add("str_export_opml", u"Exporter vers un fichier OPML...")
    add("str_preferences_menubar", u"Préférences...")
    add("str_close_window", u"Fermer la fenêtre")
    add("str_quit", u"Quitter")

    add("str_edit", u"Edition")
    add("str_select_all", u"Tout sélectionner")

    add("str_tools", u"Outils")
    add("str_check_all", u"Tout vérifier")
    add("str_catch_up", u"Marquer 'à jour'")
    add("str_check_selected", u"Vérifier les sélections")
    add("str_add_feed", u"Ajouter une source...")
    add("str_remove_selected", u"Enlever une source")
    add("str_feed_properties", u"Propriétés de la source...")
    add("str_scheduler_menubar", u"Programmateur...")
    

    add("str_select_language", u"Langue")

    ## Ils sont aussi utilisés pour les onglets
    add("str_view", u"Affichage")
    add("str_downloads", u"Téléchargements")
    add("str_subscriptions", u"Abonnement")
    add("str_podcast_directory", u"Bibliothèque de podcasts")
    add("str_cleanup", u"Nettoyer")

    add("str_help", u"Aide")
    add("str_online_help", u"Aide en ligne")
    add("str_faq", u"FAQ")
    add("str_check_for_update", u"Vérifier les mises à jour...")
    add("str_report_a_problem", u"Rapporter un problème")
    add("str_goto_website", u"Aller sur le site")
    add("str_make_donation", u"Faire un don")
    add("str_menu_license", u"Licence...")
    add("str_about", u"A propos...")


    ## Barre d'outils  : Téléchargement
    add("str_remove_selected_items", u"Enlever les items sélectionnés")
    add("str_cancel_selected_download", u"Annuler les téléchargements sélectionnés")
    add("str_pause_selected", u"Pause")

    ## Etat onglet de téléchargement (dans les colonnes)
    ## Etats de l'Enclosure. Utiliser le préfixe str_dl_state_ afin d'éviter
    ## les collisions avec d'autres chaines, e.g. str_downloading ci-dessus
    ## qui ne sont pas en majuscule.
    add("str_dl_state_new", u"Nouveau")
    add("str_dl_state_queued", u"A la queue")
    add("str_dl_state_downloading", u"En téléchargement")
    add("str_dl_state_downloaded", u"Téléchargé")
    add("str_dl_state_cancelled", u"Annulé")
    add("str_dl_state_finished", u"Terminé")
    add("str_dl_state_partial", u"Téléchargé partiellement")
    add("str_dl_state_clearing", u"Nettoyage")


    ## Barre d'outil : Abonnement
    add("str_check_for_new_podcasts", u"Recherche de nouveaux podcasts")
    add("str_catch_up_mode", u"Catch-up - Seulement les derniers abonnements")

    add("str_add_new_feed", u"Ajouter de nouvelles sources");
    add("str_remove_selected_feed", u"Enlever les sources sélectionnées")
    add("str_properties", u"Propriétés")
    add("str_check_selected_feed", u"Vérifier les sources sélectionnées")

    add("str_scheduler_on", u"Programmateur en marche")
    add("str_scheduler_off", u"Programmateur arrêté")        

    ## Onglet Souscription : Info Programmateur
    add("str_next_run:", u"Prochaine vérification :")

    ## Onglet Souscription : cadre épisode
    add("str_downloading_episode_info", u"Téléchargement des infos de l'épisode...")
    add("str_no_episodes_found", u"Aucun épisode.")


    ## Onglet Répertoire
    add("str_refresh", u"Rafraîchir")
    add("str_open_all_folders", u"Ouvrir tous les dossiers")
    add("str_close_all_folders", u"Fermer tous les dossiers")
    add("str_add", u"Ajouter")

    ## Onglet Répertoire : Autres entrées
    add("str_directory_description", u"Cliquez sur une source ou entrez / collez dans le champ ci-dessus, puis cliquer Ajouter.")


    ## Onglet Nettoyage
    add("str_select_a_feed", u"Sélectionner une source")
    add("str_refresh_cleanup", u"Rafraîchir")
    
    add("str_look_in", u"Chercher un épisode dans")        
    add("str_player_library", u"Bibliothèque du lecteur")
    add("str_downloads_folder", u"Dossier de téléchargement")
    add("str_delete_library_entries", u"Effacer les entrées de la bibliothèque")
    add("str_delete_files", u"Effacer les fichiers")
    add("str_select_all_cleanup", u"Tout sélectionner")
    add("str_delete", u"Nettoyer")




    ## Onglet journal
    add("str_log", u"Journal")
    add("str_clear", u"Vider")


    ## Colonnes (dans téléchargements et souscriptions)
    add("str_lst_name", u"Nom")
    add("str_lst_date", u"Date")        
    add("str_lst_progress", u"Progression")
    add("str_lst_state", u"Etat")
    add("str_lst_mb", u"Mo")
    add("str_lst_location", u"Lieu")
    add("str_lst_episode", u"Episode")
    add("str_lst_playlist", u"Playlist")

    ## Etat des abonnements -- voir les variables ipodder/feeds.py SUB_STATES
    add("str_subscribed", u"Abonné")
    add("str_disabled", u"Désactivé")
    add("str_newly-subscribed", u"Nouveau abonnement")
    add("str_unsubscribed", u"Désabonné")
    add("str_preview", u"Prévisualisation")
    add("str_force", u"Forcer")
    





    ##_________________________________________________________
    ##
    ##   Fenêtre de dialogue
    ##_________________________________________________________



    ## Fenêtre d'import OPML
    #--- Selection fichier import

    ## Fenêtre d'esport OPML
    add("str_choose_name_export_file", u"Sélectionner un nom de fichier d'export")
    add("str_subs_exported", u"Abonnements exportés.")
    
    ## Fenetre Préférences
    add("str_preferences", u"Préférences")
    
    add("str_save", u"Sauver")
    add("str_cancel", u"Annuler")
    
    # Général
    add("str_general", u"Général")
    add("str_gen_options_expl", u"Définis les options générales de %s" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Au lancement, ne montrer que l'icone du system tray")

    add("str_run_check_startup", u"Vérifier l'arrivée de nouveaux podcasts au démarrage de l'application")
    add("str_play_after_download", u"Jouer les podcasts juste après leur téléchargement")
    add("str_location_and_storage", u"Gestion des lieux de stockage")
    add("str_stop_downloading", u"Arrêter les téléchargements si le disque dur atteint une taille minimum de")
    add("str_bad_megabyte_limit_1", u"Désolé, la limite en MegaOctet ne semble pas être un entier")
    add("str_bad_megabyte_limit_2", u"Essayez encore une fois.")

    add("str_download_folder", u"Télécharger les podcasts dans ce dossier")
    add("str_browse", u"Naviguer")
    add("str_bad_directory_pref_1", u"Désolé, nous ne pouvons pas trouver les dossiers que vous avez entré")
    add("str_bad_directory_pref_2", u"Créé le dossier et essayez de nouveau. Merci.")

    
    # Fil (threads)
    add("str_threads", u"Téléchargement simultané")
    add("str_multiple_download", u"Préférences de téléchargement simultané")
    add("str_max_feedscans", u"Nombre maximal de recherche par session")
    add("str_max_downloads", u"Nombre maximal de téléchargement par session")
   
    # Préférences réseau
    add("str_networking", u"Préférences réseau")
    add("str_coralize_urls", u"URL sur Coral CDN (experimental)")
    add("str_proxy_server", u"Utiliser un serveur proxy")
    add("str_proxy_address", u"Adresse")
    add("str_proxy_port", u"Port")
    add("str_proxy_username", u"Identifiant")
    add("str_proxy_password", u"Mot de passe")
    add("str_bad_proxy_pref", u"Vous avez activé le support proxy, mais vous n'avez pas donné ni d'hôte, ni de port. Revenez dans les préférences réseau et entrez le nom d'hôte et le port.")

    # Lecteur
    add("str_player", u"Lecteur")
    add("str_choose_a_player", u"Sélectionner un lecteur")
    add("str_no_player", u"Aucun lecteur")
    
    # Advancé
    add("str_advanced", u"Avancé")
    add("str_options_power_users", u"Ces options peuvent être utilisées par les utilisateurs avancés")
    add("str_run_command_download", u"Lancer cette commande après chaque téléchargement")
    add("str_rcmd_full_path", u"%f = chemin complet du fichier téléchargé")
    add("str_rcmd_podcast_name", u"%n = nom du podcast")
    add("str_other_advanced_options", u"Autres options avancées")
    add("str_show_log", u"Montrer l'onglet journal")



    ## Fenêtre de feeds (ajout/propriétés)
    add("str_title", u"Titre")
    add("str_url", u"URL")
    add("str_goto_subs", u"Aller à l'onglet Abonnement pour voir les épisodes de cette source")
    add("str_feed_save", u"Sauver")
    add("str_feed_cancel", u"Annuler")




    ## Fenêtre programmateur
    add("str_enable_scheduler", u"Activer le programmateur")
    add("str_sched_select_type", u"Sélectionnez le type de programmateur ci-dessous :")
    add("str_check_at_specific_times", u"Vérifier à heure régulière")
    add("str_check_at_regular_intervals", u"Vérifier à intervals réguliers")
    add("str_repeat_every:", u"Répéter toutes les :")
    add("str_latest_run", u"Dernière vérification :")
    add("str_next_run", u"Prochaine vérification :")
    add("str_not_yet", u"pas encore")
    #--- Annuler
    add("str_save_and_close", u"Sauver et fermer")
    #--- Sauver

    add("str_time_error", u"Une des heures programmées ne semble pas correcte. Exemple valide : 10:02am, 16:43.")


    ## Fenêtre A propos
    #--- Version:
    #--- Programmation : Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nDesign: Martijn Venrooy\nStratège de contenu : Mark Alexander Posth\nConcept: Adam Curry, Dave Winer\nMerci à tous les traducteurs pour leur apports !\n\nBasé sur Feedparser et la technologie BitTorrent.\nCe programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous). Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.


    ## Entrée de la barre de Status
    add("str_check_for_new_podcast_button", u"Vérifier l'arrivée de nouveaux podcasts en cliquant le bouton vert")
    add("str_last_check", u"Dernière vérification :")
    add("str_of", u"de")
    add("str_item", u"item")
    add("str_items", u"items")
    add("str_downloading", u"en téléchargement")
    add("str_downloaded", u"téléchargé")
    add("str_enclosure", u"enclosure")
    add("str_enclosures", u"enclosures")
    add("str_fetched", u"récupéré")
    add("str_loading_mediaplayer", u"Lancement de votre lecteur de média...")
    add("str_loaded_mediaplayer", u"Lecteur de média lancé...")        
    add("str_initialized", u"%s prêt" % PRODUCT_NAME)




    ## Chaine pour d'autres applications
    add("str_ipodder_title", u"%s - Récepteur de podcast v" % PRODUCT_NAME + __version__)
    add("str_localization_restart", u"Pour changer la langue, %s doit être redémarré. Cliquez sur OK pour quitter proprement, ou Annuler pour continuer." % PRODUCT_NAME)
    add("str_really_quit", u"Un téléchargement est en cours. Vraiment quitter ?");
    add("str_double_check", u"Apparemment un téléchargement est en cours.");
    
    # Mise à jour
    add("str_new_version_ipodder", u"Une nouvelle version de %s est disponible, cliquez sur OK pour aller sur le site." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Cette version de %s est à jour" % PRODUCT_NAME)
    add("str_other_copy_running", u"Une autre copie de %s est déja lancée. Mettez-la en avant, et attendez qu'elle se termine ou tuez le processus." % PRODUCT_NAME)

    # Menu contextuel (bouton droit de la souris, Windows)
    add("str_check_now", u"Vérifier maintenant")        
    add("str_open_ipodder", u"Ouvrir %s" % PRODUCT_NAME)
    #--- Téléchargement
    add("str_scanning_feeds", u"Vérifications des sources")

    # Menu contextuel (Feed)
    add("str_remove", u"Enlever")        
    add("str_open_in_browser", u"Ouvrir dans un navigateur")
    
    

    # Menu contectuel (T2léchargements)
    add("str_play_episode", u"Jouer l'épisode")
    add("str_clear_selected", u"Nettoyer les entrées sélectionnées")
    




