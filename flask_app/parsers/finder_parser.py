import requests
from typing import Dict, List, Tuple
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
            'employment_type': item['employment_type'],
            'distant_work': item['distant_work'],
            'experience': item['experience'],
            'created_at': item['created_at'],
            'publication_at': item['publication_at'],
            'company_id': item['company']['id'],
            'locations': [{
                'id': loc['id'],
                'name': loc['name'],
                'name_prepositional': loc['name_prepositional'],
                'slug': loc['slug']
            } for loc in item['locations']],
        }

    def extract_company_data(self, item: Dict) -> Dict:
        return {
            'company_id': item['company']['id'],
            'title': item['company']['title'],
            'tax_id': item['company'].get('tax_id'),
            'site_url': item['company'].get('site_url'),
            'description': item['company']['description'],
            'logo': item['company']['logo'],
            'type': item['company']['type'],
            'has_paid_vacancies': item['company'].get('has_paid_vacancies'),
            'contacts': item['contacts'],
        }

    def extract_data(self, item: Dict) -> Tuple[Dict, Dict]:
        vacancy_data = self.extract_vacancy_data(item)
        company_data = self.extract_company_data(item)
        return vacancy_data, company_data
