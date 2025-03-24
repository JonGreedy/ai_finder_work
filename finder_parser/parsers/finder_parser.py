import requests
from typing import Dict, List
from parsers.base_parser import BaseParser

class FinderParser(BaseParser):
    def __init__(self, api_url: str, params: Dict):
        self.api_url = api_url
        self.params = params

    def parse(self) -> List[Dict]:
        response = requests.get(self.api_url, params=self.params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def extract_vacancy_data(self, item: Dict) -> Dict:
        return {
            'vacancy_id': item['id'],
            'title': item['title'],
            'description': item['description'],
            'salary_from': item['salary_from'],
            'salary_to': item['salary_to'],
            'currency_symbol': item['currency_symbol'],
            'contacts': item['contacts'],
            'company_info': {
                'id': item['company']['id'],
                'title': item['company']['title'],
                'description': item['company']['description'],
                'logo': item['company']['logo'],
                'type': item['company']['type']
            },
            'locations': [{
                'id': loc['id'],
                'name': loc['name'],
                'name_prepositional': loc['name_prepositional'],
                'slug': loc['slug']
            } for loc in item['locations']]
        }