import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def collect_user_rates(user_login):
    page_num = 1
    data = []
    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/{page_num}/'
        try:
            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            print(f"Error fetching data for page {page_num}: {e}")
            break

        items = soup.find_all('div', class_='item')
        print(f'Page {page_num}: Found {len(items)} items')

        if len(items) == 0:
            break

        for item in items:
            nameRus = item.find('div', class_='nameRus')
            film_name = nameRus.find('a').text if nameRus else None
            release_date = item.find('div', class_='date').text if item.find('div', class_='date') else None
            vote = item.find('div', class_='vote')  # Поменяйте на актуальный класс для рейтинга
            rating = vote.text.strip() if vote else None

        data.append({'film_name': film_name, 'release_date': release_date, 'rating': rating})

        page_num += 1
        time.sleep(2)  # Задержка между запросами

    return data

user_rates = collect_user_rates(user_login='193988995')
print(len(user_rates))
df = pd.DataFrame(user_rates)
df.to_excel('user_rates.xlsx')
