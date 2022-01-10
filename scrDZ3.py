import requests
from bs4 import BeautifulSoup
from pprint import pprint

import pymongo
from pymongo import MongoClient
from pymongo.errors import *

client = MongoClient('127.0.0.1', 27017)

# try:
#     client['HH_base'].vacancy.drop()
# except:
#     pass

db = client['HH_base']
hh_vacancy = db.vacancy
# hh_vacancy.delete_many({})
hh_vacancy.create_index([('tag', pymongo.TEXT)], name='search_index', unique=True)

page = 0
id = 0

running = True
while running:

    url = 'https://hh.ru'
    params = {'text': 'python', 'page': page, 'items_on_page': 20}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    try:
        next = dom.find('div', {'class': ['pager']}).find('a', {'class': ['bloko-button']}).get('href')
    except:
        running = False

    vacancies = dom.find_all('div', {'vacancy-serp-item'})

    list_of_vacancies = []

    for cv in vacancies:
        cv_data = {}
        name = cv.find('a').text
        link = cv.find('a', {'class': ['bloko-link']}).get('href')
        tag = ''

        for word in link:
            if word.isnumeric():
                tag = tag + word

        try:
            price = cv.find('div', {'class': 'vacancy-serp-item__sidebar'}).find('span').text.replace('\u202f', ' ')
            price_str = price[-4:].replace(' ', '')
            price = price[:-4]
            if '–' in price:
                price_list = price.split('–')
                price_min = int(price_list[0].replace(' ', ''))
                price_max = int(price_list[1].replace(' ', ''))
            elif 'от' in price:
                price_min = int(price[2:].replace(' ', ''))
                price_max = None
            elif 'до' in price:
                price_min = None
                price_max = int(price[2:].replace(' ', ''))
        except:
            price = None
            price_str = None
            price_min = None
            price_max = None

        id += 1

        cv_data['name'] = name
        cv_data['price_min'] = price_min
        cv_data['price_max'] = price_max
        cv_data['price_str'] = price_str
        cv_data['link'] = link
        cv_data['base'] = url
        cv_data['id'] = id
        cv_data['tag'] = tag

        try:
            hh_vacancy.insert_one(cv_data)
        except DuplicateKeyError as double_error:
            print('Doublicate: ', double_error)
    page += 1
price = 15000

for doc in hh_vacancy.find({'$or': [{'price_min': {'$gt': price}}, {'price_max': {'$gt': price}}]}):
    pprint(doc)