from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from HTMLParser import HTMLParser

home_url = "http://www.dpstream.net/"

class MovieFolder():
    url = ""
    title = ""

class SaisonFolder():
    url = ""
    number = ""

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

