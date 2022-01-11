
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html
import requests
import datetime
from pprint import pprint

def parse_from_email():

    url = 'https://news.mail.ru/'
    res = requests.get(url)
    dom = html.fromstring(res.text)
    news_links = dom.xpath('//a[contains(@class, "topnews__item")]/@href')

    client = MongoClient('127.0.0.1', 27017)
    db = client['dzzz_db']
    main_news_sr = db['dzzz']
    for link_url in news_links:
        response = requests.get(link_url)
        if response.status_code == 200:
            news_item = {}
            news_dom = html.fromstring(response.text)
            news_date_string = news_dom.xpath('//span[contains(@class, "note__text")]/@datetime')[0]
            news_date = datetime.datetime.strptime(news_date_string, '%Y-%m-%dT%H:%M:%S+03:00').strftime('%d.%m.%Y %H:%M')
            news_sourse = news_dom.xpath('//span[@class="link__text"]/text()')[0]
            news_title = news_dom.xpath('//h1[@class="hdr__inner"]/text()')[0]
            news_item["nlink"] = link_url
            news_item["date"] = news_date
            news_item["sours"] = news_sourse
            news_item["title"] = news_title


            try:
                main_news_sr.insert_one(news_item)
            except DuplicateKeyError:

                pass

    for news in main_news_sr.find({}):
        pprint(news)


parse_from_email()