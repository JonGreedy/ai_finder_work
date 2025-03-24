# Main entry point for the application
from parsers.finder_parser import FinderParser
from parsers.new_parser import NewSiteParser
from services.vacancy_service import VacancyService
from database.db import Base, engine

API_URL = "https://api.finder.work/api/v2/vacancies/"
LIMIT = 200

params = {
    'location': 'all',
    'ordering': 'relevance',
    'limit': LIMIT,
    'offset': 0,
}

def main():
    # Создание таблиц (если они еще не созданы)
    Base.metadata.create_all(bind=engine)
    parser = FinderParser(API_URL, params)
    raw_vacancies = parser.parse()
    # print(raw_vacancies)
    vacancies = [parser.extract_vacancy_data(item) for item in raw_vacancies]
    # print(vacancies)
    service = VacancyService()
    service.save_vacancies(vacancies)


    # Использование нового парсера
    # new_parser = NewSiteParser(API_URL, params)
    # raw_vacancies = new_parser.parse()
    # new_vacancies = [new_parser.extract_vacancy_data(item) for item in raw_vacancies]

    # service = VacancyService()
    # service.save_vacancies(new_vacancies)

if __name__ == "__main__":
    main()