import requests
from bs4 import BeautifulSoup
import json
import time
import random

url = 'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

data_dict = {} # словарь для информации о всех людях

count = 0
for i in range(0, 741, 20):
    url_ = f'{url}{i}'
    
    req = requests.get(url=url_, headers=headers)
    src = req.content
    soup = BeautifulSoup(src, 'lxml')
    all_links = soup.find_all('a')

    hrefs = []
    for link in all_links:
        hrefs.append(link.get('href'))
    
    for href in hrefs:
        req = requests.get(url=href, headers=headers)
        src = req.content

        soup = BeautifulSoup(src, 'lxml')
        
        username = soup.find(class_='bt-biografie-name').find('h3').text
        username = username.strip()
        job = soup.find(class_='bt-biografie-beruf').find('p').text

        contacts_ul = soup.find('ul', {'class': 'bt-linkliste'}).find_all('li')
        contacts_dict = {}
        for contact in contacts_ul:
            contact_title = contact.find('a').get('title')
            contact_href = contact.find('a').get('href')
            contacts_dict[contact_title] = contact_href

        data_dict[username] = {'Должность': job, 'Контакты': {}}

        for title, href in contacts_dict.items():
            data_dict[username]['Контакты'][title] = href

        count += 1
        print(f'#{count} Пользователь {username} добавлен!')

    break

print('ВСЕ ПОЛЬЗОВАТЕЛИ ДОБАВЛЕНЫ.')

# сохранение в json
with open('data.json', 'a', encoding='utf-8') as file:
    json.dump(data_dict, file, ensure_ascii=False, indent=4)

print('Файл сохранен.')