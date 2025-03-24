from parsers.base_parser import BaseParser
from repositories.vacancy_repository import VacancyRepository


class VacancyService:
    def __init__(self, repository: VacancyRepository, parser: BaseParser):  # Используем абстракцию BaseParser
        self.repository = repository
        self.parser = parser


    def fetch_and_store_vacancies(self):
        vacancies = self.parser.parse_vacancies()
        for vacancy_data in vacancies:
            self.repository.create_vacancy(vacancy_data)