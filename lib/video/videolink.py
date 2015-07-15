
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from HTMLParser import HTMLParser

home_url = "http://www.dpstream.net/"


# SEARCH PUREVID
class search_purevid(HTMLParser):
    purevid_urls = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if "href" in attr:
                if "purevid.com/" in attr[1]:
                    print("preuvid link found on page : "+attr[1])
                    self.purevid_urls.append(attr[1])


# CHOICE VIDEO LINK
class choice_link(HTMLParser):
    urls = []
    nextWillBeOk = False

    def handle_starttag(self, tag, attrs):
        if 'img' in tag and 'purevid':
             for attr in attrs:
                if "src" in attr:
                    if "purevid" in attr[1]:
                        print('yeah find purevid in many videos'+attr[1]+" "+tag)
                        self.nextWillBeOk = True

        if self.nextWillBeOk is False:
            return

        self.findhref = False
        for attr in attrs:
            if "href" in attr and self.nextWillBeOk is True:
                self.nextWillBeOk = False
                if "film-" in attr[1] and "en-streaming" in attr[1] and "facebook" not in attr[1]:
                    print("find any film : "+home_url+attr[1])
                    self.findhref = True
                    self.urls.append(home_url+attr[1])
                else:
                    self.findhref = False
            else:
                self.findhref = False