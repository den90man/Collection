import requests
from bs4 import BeautifulSoup
from pprint import pprint

list = 0
id = 0
running = True
while running:

    url = 'https://hh.ru'
    params = {'text': 'python', 'page': list}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    try:
        next = dom.find('div', {'class': ['pager']}).find('a', {'class': ['bloko-button']}).get('href')
    except:
        # running = False
        break

    vacancies = dom.find_all('div', {'vacancy-serp-item'})

    list_of_vacancies = []

    for cv in vacancies:
        cv_data = {}
        name = cv.find('a').text
        link = cv.find('a', {'class': ['bloko-link']}).get('href')
        try:
            price = cv.find('div', {'class': 'vacancy-serp-item__sidebar'}).find('span').text.replace('\u202f', ' ')
            price_str = price[-1:]
            price = price[:-1]
            if ' - ' in price:
                price_list = price.split('')
                price_min = price_list[0]
                price_max = price_list[1]
            else:
                price_min = price
                price_max = None
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
        list_of_vacancies.append(cv_data)
    pprint(list_of_vacancies)
    list += 1
