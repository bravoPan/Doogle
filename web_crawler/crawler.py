# from .models import
import requests
from bs4 import BeautifulSoup
from search_engine.models import PageInfo, Href, WordList
import re
from multiprocessing import pool
import jieba
from pprint import pprint

ignores_words = ["+", "=", "|", "{", "}", "-", "_", ";", ")", "(", ":", "]", "[", "<", ">", "\\",
                 "&", "#", "�"]


class splitter:
    def get_one_line_text(self, text, preview_size=30):
        pure_one = re.sub("\\t+\\n+", "", text)
        if len(pure_one) > preview_size:
            return pure_one[0:preview_size]
        else:
            return pure_one

    def get_text_only(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            result_text = ''
            for t in c:
                sub_text = self.get_text_only(t)
                result_text += sub_text + " "
            return result_text
        else:
            return v.strip()

    def convert_chinese_list(self, text):
        text = text.encode("utf-8").decode("utf-8")
        # get rid of chinese symbols
        text = re.sub("[\.\!\/_,$《》？?%^*(+\"\']+|[+——！，。、~@#￥%……&*（）:：]；、+·".encode("utf-8").decode("utf-8"),
                      "".encode("utf-8").decode("utf-8"),
                      text)
        # get rid of english symbols
        splitter = re.compile(
            '\\s+')
        text = ' '.join([i for i in jieba.cut_for_search(text)])
        return [s.lower() for s in splitter.split(text) if s != ""]


class WebCrawler(splitter):
    def insert_word(self, word_location, father, word):
        if word not in ignores_words:
            w = WordList(word=word, word_location=word_location, url_location_id=father)
            w.save()

    def crawl(self, url):
        crawl_info = {}
        crawl_info.setdefault("current_page", {"title": '', "text": '', "url": ''})
        crawl_info.setdefault("next_urls", [])
        # try:
        if PageInfo.objects.filter(url=url).count() == 0:
            web_data = requests.get(url)
            web_data.encoding = "utf-8"
            soup = BeautifulSoup(web_data.text, "lxml")
            crawl_info["next_urls"].append(url)
            title = soup.select("title")[0].text
            crawl_info["title"] = title
            text = self.get_text_only(soup)
            crawl_info["text"] = text
            crawl_info["url"] = url
            p = PageInfo(title=title, text=text, url=url)
            p.save()
            crawl_info["next_urls"] = self.get_all_hrefs(soup, p)
            # insert into word
            chinese = self.convert_chinese_list(text)
            [self.insert_word(word=chinese[i], word_location=i, father=p) for i in range(len(chinese))]
            return crawl_info
            # p.save()
            # except:
            #     print("This page could not open " + url)
            #     return None

    def get_all_hrefs(self, soup, url_location_id):
        all_links = []
        links = soup.select("a")
        for link in links:
            if "href" in dict(link.attrs):
                next_href = link.get("href")
                if next_href.startswith("http"):
                    next_href = next_href.split("#")[0]
                    if Href.objects.filter(url=next_href).count() == 0:
                        h = Href(url=next_href, url_location_id=url_location_id)
                        h.save()
                        all_links.append(next_href)
        return all_links

    def multi_crawl(self, urls, depth=2):
        for i in range(depth):
            pool_map = pool.Pool(processes=4)
            try:
                crawl_info = pool_map.map(self.crawl, urls)
                pool_map.close()
                if crawl_info:
                    urls = [i["next_urls"] for i in crawl_info]
                    # pprint(crawl_info)
                    new_urls = []
                    [[new_urls.append(i) for i in j] for j in urls]
                    urls = new_urls
            except:
                pass

# test = Crawler()
# test.crawl(["https://www.douban.com"])
