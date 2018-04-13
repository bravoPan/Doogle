from django.db import models
# Create your models here.
from web_crawler import crawler
from search_engine.models import Href, PageInfo
from multiprocessing import pool


def multi_crawl(size=20, time=5):
    crawler_mode = crawler.WebCrawler()
    multi_pool = pool.Pool(processes=4)
    for i in range(time):
        all_links = Href.objects.all().order_by("date")[0:size]
        multi_pool.map(crawler_mode.crawl, all_links)
    multi_pool.close()


def start_crawl():
    test_crawl = crawler.WebCrawler()
    all_links = Href.objects.all().order_by("date")[0:5]
    # p = PageInfo(url="www.baidu.com", text="Here we are ", title="This is just a test")
    # p.save()
    # print(all_links)
    # links = [i.url for i in all_links]
    # print(links)
    # links = ["https://news.baidu.com", "https://news.baidu.com"]
    links = all_links
    # test_crawl.multi_crawl(urls=links, depth=5)
    # sleep(100)


# start_crawl()
# multi_crawl()
