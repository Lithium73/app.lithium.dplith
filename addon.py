import sys
import urllib
import urlparse
import xbmcgui
import xbmc
import xbmcplugin
import os
import xbmcaddon
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


sys.path.append(xbmc.translatePath(os.path.join(xbmc.translatePath('special://home'), 'addons',
                                                xbmcaddon.Addon().getAddonInfo('id'), 'lib', )))
sys.path.append(xbmc.translatePath(os.path.join(xbmc.translatePath('special://home'), 'addons',
                                                xbmcaddon.Addon().getAddonInfo('id'), 'lib', 'parser')))
sys.path.append(xbmc.translatePath(os.path.join(xbmc.translatePath('special://home'), 'addons',
                                                xbmcaddon.Addon().getAddonInfo('id'), 'lib', 'video')))

from mainmenu import MainMenu

from movieparser import weeklymovie_parser
from movieparser import searchymovie_parser

from serieparser import weeklyserie_parser
from serieparser import serie_saison_parser
from serieparser import serie_episode_parser
from serieparser import searchserie_parser

from videolink import search_purevid
from videolink import choice_link


a = MainMenu()

view_mode_id=504


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
addon = Addon('plugin.video.dpstreamparser', sys.argv)

args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
net = Net()

home_url = "http://www.dpstream.net/"

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)


# ############################################  PARSER ###########################################
# ############################################  PARSER UTILS ###########################################






# ############################################  PARSER UTILS ###########################################
# ############################################  GET VIDEO URL ###########################################

def get_video_item(url2):
    urls = []
    link = 0
    if "films" in url2:
        print("have to make a purevid choice")
        multifilmparser = choice_link()
        source = net.http_GET(url2).content.encode('utf-8').strip()
        multifilmparser.feed(source)
        if len(multifilmparser.urls) >= 1 :
            for url in multifilmparser.urls:
                print("an url -> "+url)
                if "film-" in url:
                    link = link+1
                    source = net.http_GET(url).content.encode('utf-8').strip()
                    parser = search_purevid()
                    parser.feed(source)
                    urls.append(urlresolver.HostedMediaFile(url=parser.purevid_urls[0], title="Link "+str(link)))
    else:
        source = net.http_GET(url2).content.encode('utf-8').strip()
        parser = search_purevid()
        parser.feed(source)
        print('go else')
        for url in parser.purevid_urls:
            link = link+1
            print("url find for serie "+url)
            urls.append(urlresolver.HostedMediaFile(url=url, title="Link "+str(link)))

    source = urlresolver.choose_source(urls)
    if len(url2) == 0 or source is False:
       xbmc.executebuiltin("Notification(DPLith,Purevid link not found)")
       print('error on '+url2)
       return
    print("read this stream : "+url2)

    stream_url = source.resolve()
    # wherebegin = xbmcgui.Dialog().input("When begin ?")
    # return stream_url+"start="+(wherebegin*60*1000)
    return stream_url
    #  return url2

    # xbmcgui.Dialog().ok('log', stream_url)
    # addon.resolve_url(stream_url);

# ############################################  GET VIDEO URL ###########################################

# ############################################  CREATE LIST ITEM ###########################################

def create_video_item(url):
     xbmcplugin.setContent(int(sys.argv[1]),'movies')

     print("find purevid for :"+url)
     li = xbmcgui.ListItem('PureVid', iconImage='DefaultVideo.png')
     li.setProperty('isplayable', 'true')
     li.setProperty('Video', 'true')
     li.setInfo( type="Video", infoLabels={"Year":2003 ,"Title": "title","Plot":"description","rating":"rating"  } )
     xbmcplugin.addDirectoryItem(handle=addon_handle, url=get_video_item(url), listitem=li, isFolder=False)
     xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
     xbmcplugin.endOfDirectory(addon_handle)


def create_list_item_video(array):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'folder', 'foldername': 'Folder Two', 'url': array[i].url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    xbmcplugin.endOfDirectory(addon_handle);

def create_list_serie(array):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'saison', 'foldername': 'Folder Two', 'url': array[i].url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    xbmcplugin.endOfDirectory(addon_handle);

def create_list_saison(array, urlDp):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i], iconImage='DefaultFolder.png')
        url = build_url({'mode': 'episode', 'foldername': 'Folder Two', 'saison': array[i], 'url': urlDp})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    xbmcplugin.endOfDirectory(addon_handle);


def create_list_episode(saison):
    for i in range(0, len(saison)):
        li = xbmcgui.ListItem(saison[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'folder', 'foldername': 'Folder Two', 'url': ""})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    xbmcplugin.endOfDirectory(addon_handle);

# ############################################  CREATE LIST ITEM ###########################################
# ############################################  PARSING ###########################################

def parse_weeklymovie():
    URL = "http://www.dpstream.net/?action=cent&aff=tophebdo"
    source = net.http_GET(URL).content.encode('utf-8').strip()
    # print(source)
    parser = weeklymovie_parser()
    parser.feed(source)
    create_list_item_video(parser.homeMovieUrl)


def parse_weeklyserie():
    URL = "http://www.dpstream.net/?action=cent&aff=tophebdo"
    source = net.http_GET(URL).content.encode('utf-8').strip()
    # print(source)
    parser = weeklyserie_parser()
    parser.feed(source)
    create_list_serie(parser.homeSerieUrl)

def parse_saison(url):
    source = net.http_GET(url).content.encode('utf-8').strip()
    parser = serie_saison_parser()
    parser.feed(source)
    create_list_saison(parser.saisons,url)

def parse_episode(url,saison):
    source = net.http_GET(url).content.encode('utf-8').strip()
    parser = serie_episode_parser(saison)
    parser.feed(source)
    print("parse with :"+parser.episodes[0].url)
    create_list_item_video(parser.episodes)

def parse_searchmovie(movie_to_search):
    URL = "http://www.dpstream.net/fichiers/includes/inc_liste_film/fonction_liste_film2.php?p=chercher&titre="+movie_to_search
    source = net.http_GET(URL).content.encode('utf-8').strip()
    # print(source)
    parser = searchymovie_parser()
    parser.feed(source)
    create_list_item_video(parser.homeMovieUrl)

def parse_searchserie(serie_to_search):
    URL = "http://www.dpstream.net/liste-series-en-streaming.html"
    data = {'recherchem' : serie_to_search}
    source = net.http_POST(URL, data).content.encode('utf-8').strip()
    # print(source)
    parser = searchserie_parser()
    parser.feed(source)
    print(parser.homeSerieUrl)
    create_list_serie(parser.homeSerieUrl)

# ############################################  PARSING ###########################################

def get_app_home():
    # dailymovie
    li = xbmcgui.ListItem("Daily movies", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'dailymovie', 'foldername': 'Daily movies'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # dailyserie
    li = xbmcgui.ListItem("Daily Series", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'dailyserie', 'foldername': 'Daily series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # weeklymovie
    li = xbmcgui.ListItem("Weekly Movies", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'weeklymovie', 'foldername': 'Weekly Moviess'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # weeklyserie
    li = xbmcgui.ListItem("Weekly Series", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'weeklyserie', 'foldername': 'Weekly Series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # searchmovie
    li = xbmcgui.ListItem("Search Movies", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'searchmovie', 'foldername': 'Search Movies'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # searchserie
    li = xbmcgui.ListItem("Search Series", iconImage='DefaultFolder.png')
    url = build_url({'mode': 'searchserie', 'foldername': 'Search Series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle);


if mode is None:
    get_app_home()
    # parse_home()
    # create_list_item_video(["http://www.purevid.com/v/36101kilt42knusfl6323/","http://www.purevid.com/v/36101kilt42knusfl6323/","http://www.purevid.com/v/36101kilt42knusfl6323/","http://www.purevid.com/v/36101kilt42knusfl6323/","http://www.purevid.com/v/36101kilt42knusfl6323/"])
elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    url = args['url'][0]
    create_video_item(url)
elif mode[0] == 'weeklymovie':
    parse_weeklymovie()
elif mode[0] == 'weeklyserie':
    parse_weeklyserie()
elif mode[0] == 'saison':
    url = args['url'][0]
    parse_saison(url)
elif mode[0] == 'episode':
    print('episode mode')
    url = args['url'][0]
    saison = args['saison'][0]
    parse_episode(url, saison)
elif mode[0] == 'searchmovie':
    movie_to_search = xbmcgui.Dialog().input("Search a movie")
    parse_searchmovie(movie_to_search)
elif mode[0] == 'searchserie':
    serie_to_search = xbmcgui.Dialog().input("Search a movie")
    parse_searchserie(serie_to_search)
