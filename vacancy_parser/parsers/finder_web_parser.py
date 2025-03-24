from bs4 import BeautifulSoup
import requests
from parsers.base_parser import BaseParser

class FinderWebParser(BaseParser):
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_vacancies(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancies = []

        # Пример парсинга (зависит от структуры сайта)
        for item in soup.find_all('div', class_='vacancy-item'):
            title = item.find('h2').text.strip()
            company = item.find('div', class_='company').text.strip()
            location = item.find('div', class_='location').text.strip()
            description = item.find('div', class_='description').text.strip()

            vacancies.append({
                'vacancy_id': int(item.get('data-id', 0)),  # Пример получения ID
                'title': title,
                'company': company,
                'location': location,
                'description': description
            })

        return vacancies