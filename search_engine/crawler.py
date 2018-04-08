# from .models import
import requests
from bs4 import BeautifulSoup
from .models import UrlList, WordLocation, WordList, Link, LinkWords
import re


# from sqlite3 import

# def create_index_tables():


class Crawler:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def db_commit(self):
        pass

    def add_to_index(self, url):
        if self.is_indexed(url):
            return
        print("Indexing %s " % url)

        text = self.get_entry_id('urllist')
        c = UrlList(url=url)
        c.save()

    def get_entry_id(self, field, value, create_new=True):
        return None

    def get_text_only(self, soup):
        v = soup.string
        if not v:
            c = soup.contents
            result_text = ''
            for t in c:
                sub_text = self.get_text_only(t)
                result_text += sub_text + '\n'
            return result_text
        else:
            return v.strip()

    def separate_words(self, text):
        splitter = re.compile('\\W*')
        return [s.lower for s in splitter.split(text) if s != '']

    def is_indexed(self, url):
        return UrlList.objects.filter(url).exists()

    def add_link_href(self, url_from, url_to, link_text):

        return None

    def crawl(self, pages, depth=2):
        for i in range(depth):
            new_pages = set()
            for page in pages:
                try:
                    wb_data = requests.get(page)
                except:
                    print("It could not be opened %s" % page)
                    continue
                soup = BeautifulSoup(wb_data.text, "lxml")
                self.add_to_index(page)

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = link.get("href").split("#")[0]
                        if url[0:4] == 'http' and not self.is_indexed(url):
                            new_pages.add(url)
                        link_text = self.get_text_only(link)
                        self.add_link_href(page, url, link_text)

            pages = new_pages


test = Crawler()
test.crawl(["https://www.douban.com"])
