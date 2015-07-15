
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from HTMLParser import HTMLParser

home_url = "http://www.dpstream.net/"

class MovieFolder():
    url = ""
    title = ""

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

