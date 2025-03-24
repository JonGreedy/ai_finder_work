import requests
from parsers.base_parser import BaseParser


class FinderApiParser(BaseParser):
    def __init__(self, base_url, params):
        self.base_url = base_url
        self.params = params


    def parse_vacancies(self):
        response = requests.get(self.base_url, params=self.params)
        if response.status_code != 200:
            raise Exception(f"Ошибка при запросе к API: {response.status_code}")

        data = response.json()
        vacancies = []

        for item in data.get('items', []):
            vacancies.append({
                'vacancy_id': item['id'],
                'title': item.get('title', ''),
                'company': item.get('company', {}).get('title', ''),
                # 'location': item['locations'][0]['name'],
                'location': "item.get('locations',[])[0].get('name','')",
                'description': item.get('description', '')
            })

        return vacancies