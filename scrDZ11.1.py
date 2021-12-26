# 1
# import requests
# import json
# url = 'https://api.github.com'
# user='den90man'
# r = requests.get(f'{url}/users/{user}/repos')
# with open('data.json', 'w') as f:
#     json.dump(r.json(), f)
#     for i in r.json():
#         print(i['name'])

# import requests
# import time
# import json
# def get_data(service, appid,city):
#     while True:
#         time.sleep(1)
#         url = f'{service}?q={city}&appid={appid}'
#         response = requests.get(url)
#         if response.status_code == 200:
#             print(url)
#             break
#     return response.json()
#
# appid = '1fb529a1d2f6add03daafc120746a4d2'
# service = 'https://api.openweathermap.org/data/2.5/weather'
# city = 'Kirov'
# # city ='Manchester,uk'
# response = get_data(service, appid, city)
#
# print('Получен результат')
# print(response)

##################################
#############################
# 2 (первый вариант)
#import requests
#import time
#import json
# appid = 'BA6vgssBa5PuLcaB6QsdoOqm7ed1ddO1158gsm3a'
# service = 'https://api.nasa.gov'
# def get_data(service, appid):
#     while True:
#         time.sleep(1)
#         url = "https://api.nasa.gov/techport"
#         response = requests.get(url)
#         if response.status_code == 200:
#             print(url)
#             break
#     return response.json()


# response = get_data(service, appid)

# print('Получен результат')
# print(response)
#2 (второй вариант)
url = "https://api.nasa.gov/techport/apod"
headers = {
    'x-rapidapi-host': "https://api.nasa.gov",
    'x-rapidapi-key': "3m010LfT92A9zBPGjqARgXsrbhl2nRwQbbz28XGT"
       }
que = {"q":"apod", "region" : "US"}
response = requests.request("Get", url, headers=headers, params=que)
print (response.text)