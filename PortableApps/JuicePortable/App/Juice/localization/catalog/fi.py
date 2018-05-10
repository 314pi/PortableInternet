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
        u"Lataus ohitettu; vapaata tilaa %dMt vähemmän " \
        u"kuin tarvittava %dMt.  Vapauta levytilaa " \
        u"käyttämällä siivoustoimintoa tai muuttamalla arkistointi- " \
        u"asetuksia Asetuksista")
    add("str_critical_error_unknown", u"Tuntematon kriittinen virhe latauksessa.")
    
    add("str_error_checking_new_version", u"Pahoittelemme häiriötä version tarkistamisessa. Yritä uudelleen myöhemmin.")
    add("str_hours", u"tuntia")
    add("str_minutes", u"minuuttia")

    # The next 4 are for the status bar updates during the initial scan.
    add("str_scanning", u"Etsii")
    add("str_scanned", u"Etsiminen valmis")
    add("str_feed", u"virta")
    add("str_feeds", u"virtaa")
    
    add("str_downloading_new_episodes", u"Lataa uusia jaksoja")
    add("str_sched_specific", u"Tarkista määrättyinä aikoina")
    add("str_sched_reg", u"Tarkista säännöllisesti")
    add("str_repeat_every", u"Toista joka")
    add("str_next_run_label", u"Seuraava suoritus:")
    
    add("str_license", u"Tämä ohjelma on ilmainen ja vapaa; voit levittää ja/tai muokata sitä GNU General Public License:ssä määrätyllä tavalla, jonka on julkaissut Free Software Foundation; joko lisensiin version 2, tai (valintasi mukaan) uudemman version mukaan. Tätä ohjelmaa levitetään siinä toivossa, että se olisi hyödyllinen, mutta ilman minkäänlaista takuuta; ei edes takuuta sen sopivuudesta tiettyyn tarkoitukseen. \n\nLue GNU General Public License jos haluat lisätietoja.")

    add("str_donate", u"Lahjoita rahaa %sille" % PRODUCT_NAME)
    add("str_donate_expl", u"On tärkeää pitää yhteisön omistamia %s-ohjelmia verkossa ja pitää yllä sananvapautta tässä uudessa tavassa kuluttaa mediaa . Mikä tahansa rahasumma tekee työryhmän onnelliseksi ja rohkaisee heitä työskentelemään uusien ominaisuuksien ja palvelujen parissa!" % PRODUCT_NAME)
    add("str_donate_yes", u"Kyllä, siirry lahjoitussivulle!")
    add("str_donate_two_weeks", u"Minun pitää vielä tutustua paremmin, näytä tämä ilmoitus uudestaan kahden viikon kuluttua")
    add("str_donate_already", u"Olen jo lahjoittanut, älä näytä tätä enää")
    add("str_donate_no", u"Ei, en halua lahjoittaa, älä koskaan näytä tätä ilmoitusta enää")
    add("str_donate_one_day", u"Ei nyt, ilmoita uudestaan päivän kuluttua")
    add("str_donate_proceed", u"Jatka")

    add("str_scheduler_dialog", u"Ajastin")
    add("str_scheduler_tab", u"Asetukset")

    add("str_select_import_file", u"Valitse tuotava tiedosto")    
    add("str_add_feed_dialog", u"Lisää virta")
    add("str_edit_feed", u"Virran ominaisuudet")

    add("str_really_delete", u"Tuhoa oikeasti")

    add("str_license_caption", u"Lisenssi")

    add("str_ep_downloaded", u"Ladttu")
    add("str_ep_skipped_removed_other", u"Hypätty/Poistettu/MuuVirta")
    add("str_dl_state_to_download", u"Latausjonossa")

    add("str_select_none_cleanup", u"Älä valitse mitään")
    add("str_submit_lang", u"Lähetä kieli")
    
    add("str_dltab_live", u"Aktiivisia latauksia: ")
    add("str_dltab_ul_speed", u"Lähetysnopeus: ")
    add("str_dltab_dl_speed", u"Latausnopeus: ")


    ##_________________________________________________________
    ##
    ##     Main window (iPodder.xrc)
    ##_________________________________________________________


    
    ## File menu
    add("str_file", u"Tiedosto")
    add("str_import_opml", u"Tuo virtoja opml:nä...")
    add("str_export_opml", u"Vie virtoja opml:nä...")
    add("str_preferences_menubar", u"Asetukset...")
    add("str_close_window", u"Sulje ikkuna")
    add("str_quit", u"Lopeta")

    add("str_edit", u"Muokkaa")
    add("str_select_all", u"Valitse kaikki")

    add("str_tools", u"Työkalut")
    add("str_check_all", u"Tarkista kaikki")
    add("str_catch_up", u"Ota kiinni")
    add("str_check_selected", u"Tarkista valitut")
    add("str_add_feed", u"Lisää virta...")
    add("str_remove_selected", u"Poista virta")
    add("str_feed_properties", u"Virran ominaisuudet...")
    add("str_scheduler_menubar", u"Ajastin...")
    
    add("str_select_language", u"Valitse kieli")

    ## these are also used for the tabs
    add("str_view", u"Näkymä")
    add("str_downloads", u"Lataukset")
    add("str_subscriptions", u"Tilatut virrat")
    add("str_podcast_directory", u"Podcast-hakemisto")
    add("str_cleanup", u"Siivoa")

    add("str_help", u"Ohje")
    add("str_online_help", u"Online-ohje")
    add("str_faq", u"UKK")
    add("str_check_for_update", u"Tarkista päivitystarve...")
    add("str_report_a_problem", u"Raportoi ongelma")
    add("str_goto_website", u"Siirry kotisivulle")
    add("str_make_donation", u"Tee lahjoitus")
    add("str_menu_license", u"Lisenssi...")
    add("str_about", u"Tietoja...")


    ## Downloadstab Toolbar
    add("str_remove_selected_items", u"Poista valitut")
    add("str_cancel_selected_download", u"Keskeytä valittu lataus")
    add("str_pause_selected", u"Pidä tauko valituissa")

    ## Downloadstab States (in columns)
    ## Enclosure states. Use str_dl_state_ prefix to avoid collisions with
    ## other strings, e.g. str_downloading above which isn't capitalized.
    add("str_dl_state_new", u"Uusi")
    add("str_dl_state_queued", u"Jonossa")
    add("str_dl_state_downloading", u"Lataa")
    add("str_dl_state_downloaded", u"Ladattu")
    add("str_dl_state_cancelled", u"Keskeytetty")
    add("str_dl_state_finished", u"Valmis")
    add("str_dl_state_partial", u"Osittain ladattu")
    add("str_dl_state_clearing", u"Poistaa")


    ## Subscriptionstab Toolbar
    add("str_check_for_new_podcasts", u"Tarkista podcastit")
    add("str_catch_up_mode", u"Ota kiinni - Lataa vain viimeisimmät uudet tilaukset")

    add("str_add_new_feed", u"Lisää uusi virta");
    add("str_remove_selected_feed", u"Poista valittu virta")
    add("str_properties", u"Ominaisuudet")
    add("str_check_selected_feed", u"Tarkista valittu virta")

    add("str_scheduler_on", u"Ajastin - päällä")
    add("str_scheduler_off", u"Ajastin - poissa päältä")        

    ## Subscriptionstab Scheduler information
    add("str_next_run:", u"Seuraava tarkistus:")

    ## Subscriptionstab episode frame
    add("str_downloading_episode_info", u"Lataa tietoa jaksosta...")
    add("str_no_episodes_found", u"Jaksoja ei löytynyt.")


    ## Directorytab Toolbar
    add("str_refresh", u"Päivitä")
    add("str_open_all_folders", u"Avaa kaikki kansiot")
    add("str_close_all_folders", u"Sulje kaikki kansiot")
    add("str_add", u"Lisää")

    ## Directorytab Other items
    add("str_directory_description", u"Klikkaa virtaa puukuvaimessa tai kirjoita/liitä virta yllä olevaan laatikkoon ja paina Lisää.")




    ## Cleanuptab items
    add("str_select_a_feed", u"Valitse virta")
    add("str_refresh_cleanup", u"Päivitä")
    
    add("str_look_in", u"Etsi jaksoja:")        
    add("str_player_library", u"Soittimen kirjastosta")
    add("str_downloads_folder", u"Latauskansiosta")
    add("str_delete_library_entries", u"Poista kirjastomerkinnät")
    add("str_delete_files", u"Poista tiedostot")
    add("str_select_all_cleanup", u"Valitse kaikki")
    add("str_delete", u"Poista")




    ## Logtab items
    add("str_log", u"Loki")
    add("str_clear", u"Tyhjennä")


    ## Columns (in downloads- and subscriptionstab)
    add("str_lst_name", u"Nimi")
    add("str_lst_date", u"Päivämäärä")        
    add("str_lst_progress", u"Edistys")
    add("str_lst_state", u"Tila")
    add("str_lst_mb", u"Mt")
    add("str_lst_location", u"Sijainti")
    add("str_lst_episode", u"Jakso")
    add("str_lst_playlist", u"Soittolista")

    ## Feed subscription states -- see ipodder/feeds.py SUB_STATES variable
    add("str_subscribed", u"Tilattu")
    add("str_disabled", u"Estetty")
    add("str_newly-subscribed", u"Viime aikoina tilattu")
    add("str_unsubscribed", u"Tilaus peruutettu")
    add("str_preview", u"Esikatsele")
    add("str_force", u"Pakota")
    





    ##_________________________________________________________
    ##
    ##   Dialog Windows
    ##_________________________________________________________



    ## OPML Import Dialog
    #--- Valitse tuotava tiedosto

    ## OPML Export Dialog
    add("str_choose_name_export_file", u"Valitse nimi vientitiedostolle")
    add("str_subs_exported", u"Tilatut virrat viety.")
    
    ## Preferences Dialog
    add("str_preferences", u"Asetukset")
    
    add("str_save", u"Tallenna")
    add("str_cancel", u"Keskeytä")
    
    # General
    add("str_general", u"Yleistä")
    add("str_gen_options_expl", u"%s:in yleiset asetukset" % PRODUCT_NAME)
    add("str_hide_on_startup", u"Näytä %s vain tehtäväpalkissa käynnistyttyä" % PRODUCT_NAME)

    add("str_run_check_startup", u"Tarkista uudet podcastit käynnistyksen yhteydessä")
    add("str_play_after_download", u"Toista lataukset heti lataamisen jälkeen")
    add("str_location_and_storage", u"Sijainnin ja arkistoinnin määritykset")
    add("str_stop_downloading", u"Lopeta lataaminen kun levyllä on enää tilaa:")
    add("str_bad_megabyte_limit_1", u"Megatavurajaa ei voi lukea")
    add("str_bad_megabyte_limit_2", u"Yritä uudestaan.")

    add("str_download_folder", u"Lataa podcastit tähän kansioon")
    add("str_browse", u"Selaa...")
    add("str_bad_directory_pref_1", u"Kirjoittamaasi kansiota ei löydy")
    add("str_bad_directory_pref_2", u"Luo se ja yritä uudestaan.")

    
    # Threading
    add("str_threads", u"Säikeistys")
    add("str_multiple_download", u"Usean päällekkäisen latauksen asetukset")
    add("str_max_feedscans", u"maksimimäärä säikeitä virtojen etsimiseen sessiota kohden")
    add("str_max_downloads", u"maksimimäärä latauksia sessiota kohden")
   
    # Network settings
    add("str_networking", u"Verkkoasetukset")
    add("str_coralize_urls", u"Koralisoi URL:it (kokeilu)")
    add("str_proxy_server", u"Käytä välityspalvelinta")
    add("str_proxy_address", u"Osoite")
    add("str_proxy_port", u"Portte")
    add("str_proxy_username", u"Käyttäjänimi")
    add("str_proxy_password", u"Salasana")
    add("str_bad_proxy_pref", u"Sallit välityspalvelintuen, mutta et antanut palvelimen osoitetta ja porttia.  Palaa Verkkoasetuksiin ja anna proxyn osoite sekä portti.")

    # Player
    add("str_player", u"Soitin")
    add("str_choose_a_player", u"Valitse soitin")
    add("str_no_player", u"Ei soitinta")
    
    # Advanced
    add("str_advanced", u"Erityisasetukset")
    add("str_options_power_users", u"Nämä asetukset on tarkoitettu tehokäyttäjille")
    add("str_run_command_download", u"Suorita tämä komento jokaisen latauksen jälkeen")
    add("str_rcmd_full_path", u"%f = Ladatun tiedoston koko polku")
    add("str_rcmd_podcast_name", u"%n = Podcastin nimi")
    add("str_other_advanced_options", u"Muita erityisasetuksia")
    add("str_show_log", u"Näytä lokipalkki ohjelmassa")



    ## Feed Dialog (add/properties)
    add("str_title", u"Otsikko")
    add("str_url", u"Osoite")
    add("str_goto_subs", u"Mene Tilausikkunaan nähdäksesi tämän virran jaksot")
    add("str_feed_save", u"Tallenna")
    add("str_feed_cancel", u"Peruuta")




    ## Scheduler Dialog
    add("str_enable_scheduler", u"Salli ajastin")
    add("str_sched_select_type", u"Valitse alla olevista painikkeista, haluatko ohjelman tekevän tarkistuksen asetettuna aikana, vai säännöllisesti:")
    add("str_check_at_specific_times", u"Tarkista asetettuina aikoina")
    add("str_check_at_regular_intervals", u"Tarkista säännöllisin väliajoin")
    add("str_repeat_every:", u"Toista joka:")
    add("str_latest_run", u"Viimeisin suoritus:")
    add("str_next_run", u"Seuraava suoritus:")
    add("str_not_yet", u"Ei vielä")
    #--- Cancel
    add("str_save_and_close", u"Tallenna ja sulje")
    #--- Save

    add("str_time_error", u"Yksi annetuista ajoista ei ole luettavissa. Ohjelma ymmärtää kellonaikoja muodossa: 10:02am tai 16:43.")


    ## Donations Dialog
    #--- Lahjoita iPodderille
    #--- On tärkeää pitää yhteisön omistamia iPodder-ohjelmia verkossa ja pitää yllä sananvapautta tässä uudessa tavassa kuluttaa mediaa . Mikä tahansa rahasumma tekee työryhmän onnelliseksi ja rohkaisee heitä työskentelemään uusien ominaisuuksien ja palvelujen parissa!
    #--- Kyllä, siirry lahjoitussivulle!
    #--- Minun pitää vielä tutustua paremmin, näytä tämä ilmoitus uudestaan kahden viikon kuluttua
    #--- Olen jo lahjoittanut, älä näytä tätä enää
    #--- Ei, en halua lahjoittaa, älä koskaan näytä tätä ilmoitusta enää
    #--- Ei nyt, ilmoita uudestaan päivän kuluttua
    #--- OK




    ## About Dialog
    #--- Versio:
    #--- Ohjelmointi: Erik de Jonge, Andrew Grumet, Garth Kidd, Perica Zivkovic\nSuunnittelu: Martijn Venrooy\nSisältöstrategisti: Mark Alexander Posth\nKonsepti: Adam Curry, Dave Winer\nKiitoksia kaikille kääntäjille!\n\nPerustuu Feedparser- ja BitTorrent-teknologiaan.\nTämä ohjelma on ilmainen ja vapaa; voit levittää ja/tai muokata sitä GNU General Public License:ssä määrätyllä tavalla, jonka on julkaissut Free Software Foundation; joko lisensiin version 2, tai (valintasi mukaan) uudemman version mukaan. Tätä ohjelmaa levitetään siinä toivossa, että se olisi hyödyllinen, mutta ilman minkäänlaista takuuta; ei edes takuuta sen sopivuudesta tiettyyn tarkoitukseen. \n\nLue GNU General Public License jos haluat lisätietoja.




    ## Statusbar items
    add("str_check_for_new_podcast_button", u"Tarkista uudet podcastit painamalla vihreää tarkistuspainiketta")
    add("str_last_check", u"Viimeisin tarkistus suoritettu aikaan")
    add("str_of", u":sta")
    add("str_item", u"kohde")
    add("str_items", u"kohdetta")
    add("str_downloading", u"lataa")
    add("str_downloaded", u"ladattu")
    add("str_enclosure", u"sisälytettyä")
    add("str_enclosures", u"sisällytetyt")
    add("str_fetched", u"haetut")
    add("str_loading_mediaplayer", u"Lataa mediasoitinta...")
    add("str_loaded_mediaplayer", u"Mediasoitin ladattu...")        
    add("str_initialized", u"%s valmis" % PRODUCT_NAME)




    ## Other application strings
    add("str_ipodder_title", PRODUCT_NAME + u" - Podcast-vastaanotin v" + __version__)
    add("str_localization_restart", u"Kaikkien toimintojen kääntymiseen tarvitaan ohjelman uudelleenkäynnistys. Paina OK sammuttaaksesi ohjelman, paina Peruuta keskeyttääksesi.")
    add("str_really_quit", u"Lataus on kesken.  Poistutaanko silti?");
    add("str_double_check", u"Näyttää kuin lataus olisi jo käynnissä.");
    
    # check for update
    add("str_new_version_ipodder", u"Uusi versio %s:ista on saatavilla, paina Ok siirtyäksesi lataussivulle." % PRODUCT_NAME)
    add("str_no_new_version_ipodder", u"Tämä versio %sista on ajan tasalla." % PRODUCT_NAME)
    add("str_other_copy_running", u"Toinen kopio %sista on auki. Valitse se, odota sen valmistumista, tai lopeta se." % PRODUCT_NAME)

    # Windows taskbar right-click menu
    add("str_check_now", u"Tarkista nyt")        
    add("str_open_ipodder", u"Avaa %s" % PRODUCT_NAME)
    #--- Downloading
    add("str_scanning_feeds", u"Tarkistaa virtoja")

    # Feed right-click menu
    add("str_remove", u"Poista")        
    add("str_open_in_browser", u"Avaa selaimessa")
    
    

    # Downloads right-click menu
    add("str_play_episode", u"Toista jakso mediasoittimessa")
    add("str_clear_selected", u"Poista valitut")
    
