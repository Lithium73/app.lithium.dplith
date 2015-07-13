import sys
import urllib
import urlparse
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net




base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
addon = Addon('plugin.video.dpstreamparser', sys.argv)

args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
net = Net()
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

home_url = "http://www.dpstream.net/"

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

class MovieFolder():
    url = ""
    title = ""

class SaisonFolder():
    url = ""
    number = ""

# ############################################  PARSER ###########################################

# WEEKLY MOVIE
class weeklymovie_parser(HTMLParser):
    homeMovieUrl = []
    findhref = False

    def handle_starttag(self, tag, attrs):
        self.findhref = False
        for attr in attrs:
            if "href" in attr:
                if "films-" in attr[1]:
                    self.findhref = True
                    objecttopush = MovieFolder()
                    objecttopush.url = home_url+attr[1];
                    self.homeMovieUrl.append(objecttopush)
                else:
                    self.findhref = False
            else:
                self.findhref = False

    def handle_data(self, data):
        if self.findhref:
            if len(self.homeMovieUrl[len(self.homeMovieUrl)-1].title) == 0:
                self.homeMovieUrl[len(self.homeMovieUrl)-1].title = data

# WEEKLY SERIE
class weeklyserie_parser(HTMLParser):
    homeSerieUrl = []
    findhref = False

    def handle_starttag(self, tag, attrs):
        self.findhref = False
        for attr in attrs:
            if "href" in attr:
                if "serie-" in attr[1]:
                    self.findhref = True
                    objecttopush = MovieFolder()
                    objecttopush.url = home_url+attr[1];
                    self.homeSerieUrl.append(objecttopush)
                else:
                    self.findhref = False
            else:
                self.findhref = False

    def handle_data(self, data):
        if self.findhref:
            if len(self.homeSerieUrl[len(self.homeSerieUrl)-1].title) == 0:
                self.homeSerieUrl[len(self.homeSerieUrl)-1].title = data


# Parse saison
class serie_saison_parser(HTMLParser):
    saisons = []
    findh3 = False

    def handle_starttag(self, tag, attrs):
        self.findh3 = False
        if tag == 'h3':
            self.findh3 = True

    def handle_data(self, data):
        if self.findh3:
            if "Saison " in data:
                self.saisons.append(data)


# Parse episode
class serie_episode_parser(HTMLParser):
    episodes = []
    findhref = False

    def __init__(self, saison):
        HTMLParser.__init__(self)
        self.saison = saison

    def handle_starttag(self, tag, attrs):
        sais = self.saison
        sais = sais.replace(" ", "-")
        sais = sais.lower()
        for attr in attrs:
            if "href" in attr:
                if "serie-" in attr[1] and sais in attr[1]:
                    self.findhref = True
                    objecttopush = MovieFolder()
                    objecttopush.url = home_url+attr[1];
                    self.episodes.append(objecttopush)
                else:
                    self.findhref = False
            else:
                self.findhref = False

    def handle_data(self, data):
         if self.findhref:
            if len(self.episodes[len(self.episodes)-1].title) == 0:
                self.episodes[len(self.episodes)-1].title = data
                self.makePurevidUrl(len(self.episodes)-1)

    def makePurevidUrl(self, index):

        # example http://www.dpstream.net/fichiers/includes/inc_afficher_serie/
        # changer_episode.php?changer_episod=1&id_serie=101&saison=2&episode=04&version=FR

        url = self.episodes[index].url
        # find saison
        saisonIndex = url.find("saison-")+7
        lastSaisonIndex = url.find("-episode")
        saison = url[saisonIndex:lastSaisonIndex]

        #find episode
        episodeIndex = url.find("-episode")+8
        tmpurl = url[episodeIndex+1:]
        lastEpisodeIndex = tmpurl.find("-")
        episode = tmpurl[:lastEpisodeIndex]

        # find id
        idIndex = url.find("serie-")+5
        tmpurl = url[idIndex+1:]
        lastIdIndex = tmpurl.find("-")
        id = tmpurl[:lastIdIndex]

        # find lang
        langIndex = url.find(episode+"-")+len(episode)
        tmpurl = url[langIndex+1:]
        lastLangIndex = tmpurl.find(".")
        lang = tmpurl[:lastLangIndex]

        finalUrl = home_url+"fichiers/includes/inc_afficher_serie/changer_episode.php?changer_episod="+episode+"&id_serie="+id+"&saison="+saison+"&episode="+episode+"&version="+lang
        self.episodes[index].url = finalUrl

class searchymovie_parser(HTMLParser):
    homeMovieUrl = []
    findhref = False

    def handle_starttag(self, tag, attrs):
        self.findhref = False
        for attr in attrs:
            if "href" in attr:
                if "films-" in attr[1]:
                    self.findhref = True
                    objecttopush = MovieFolder()
                    objecttopush.url = home_url+attr[1];
                    self.homeMovieUrl.append(objecttopush)
                else:
                    self.findhref = False
            else:
                self.findhref = False

    def handle_data(self, data):
        if self.findhref:
            if len(self.homeMovieUrl[len(self.homeMovieUrl)-1].title) == 0:
                self.homeMovieUrl[len(self.homeMovieUrl)-1].title = data


class searchserie_parser(HTMLParser):
    homeSerieUrl = []
    findhref = False

    def handle_starttag(self, tag, attrs):
        self.findhref = False
        for attr in attrs:
            if "href" in attr:
                if "serie-" in attr[1] and "serie-lettre" not in attr[1]:
                    self.findhref = True
                    objecttopush = MovieFolder()
                    objecttopush.url = home_url+attr[1];
                    self.homeSerieUrl.append(objecttopush)
                else:
                    self.findhref = False
            else:
                self.findhref = False

    def handle_data(self, data):
        if len(self.homeSerieUrl) > 0 and len(self.homeSerieUrl[len(self.homeSerieUrl)-1].title) == 0:
            self.homeSerieUrl[len(self.homeSerieUrl)-1].title = data

# ############################################  PARSER ###########################################
# ############################################  PARSER UTILS ###########################################




# SEARCH PUREVID
class search_purevid(HTMLParser):
    purevid_url = ""

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if "href" in attr:
                if "purevid.com" in attr[1]:
                    print("preuvid link found on page : "+attr[1])
                    self.purevid_url = attr[1]


# CHOICE VIDEO LINK
class choice_link(HTMLParser):
    urls = []

    def handle_starttag(self, tag, attrs):
        self.findhref = False
        for attr in attrs:
            if "href" in attr:
                if "film-" in attr[1] and "en-streaming" in attr[1] and "facebook" not in attr[1]:
                    print("find any film : "+home_url+attr[1])
                    self.findhref = True
                    self.urls.append(home_url+attr[1])
                else:
                    self.findhref = False
            else:
                self.findhref = False

# ############################################  PARSER UTILS ###########################################
# ############################################  GET VIDEO URL ###########################################

def get_video_item(url2):
    if "films" in url2:
        print("have to make a purevid choice")
        multifilmparser = choice_link()
        source = net.http_GET(url2).content.encode('utf-8').strip()
        multifilmparser.feed(source)
        if len(multifilmparser.urls) > 0 and "film-" in multifilmparser.urls[0]:
            url2 = multifilmparser.urls[0]

    source = net.http_GET(url2).content.encode('utf-8').strip()
    parser = search_purevid()
    parser.feed(source)
    url2 = parser.purevid_url
    if len(url2) < 1:
       xbmc.executebuiltin("Notification(DPLith,Purevid link not found)")
       return ''
    print("read this stream : "+url2)
    stream_url = urlresolver.HostedMediaFile(url2).resolve()
    return stream_url
    #  return url2

    # xbmcgui.Dialog().ok('log', stream_url)
    # addon.resolve_url(stream_url);

# ############################################  GET VIDEO URL ###########################################

# ############################################  CREATE LIST ITEM ###########################################

def create_video_item(url):
     print("find purevid for :"+url)
     li = xbmcgui.ListItem('PureVid', iconImage='DefaultVideo.png')
     li.setProperty('isplayable', 'true')
     li.setProperty('Video', 'true')
     xbmcplugin.addDirectoryItem(handle=addon_handle, url=get_video_item(url), listitem=li, isFolder=False)
     xbmcplugin.endOfDirectory(addon_handle)


def create_list_item_video(array):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'folder', 'foldername': 'Folder Two', 'url': array[i].url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle);

def create_list_serie(array):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'saison', 'foldername': 'Folder Two', 'url': array[i].url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle);

def create_list_saison(array, urlDp):
    for i in range(0, len(array)):
        li = xbmcgui.ListItem(array[i], iconImage='DefaultFolder.png')
        url = build_url({'mode': 'episode', 'foldername': 'Folder Two', 'saison': array[i], 'url': urlDp})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle);


def create_list_episode(saison):
    for i in range(0, len(saison)):
        li = xbmcgui.ListItem(saison[i].title, iconImage='DefaultFolder.png')
        url = build_url({'mode': 'folder', 'foldername': 'Folder Two', 'url': ""})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
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
