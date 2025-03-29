# Main entry point for the application
from parsers.finder_parser import FinderParser
from services.vacancy_service import VacancyService
from services.company_service import CompanyService
from database.db import Base, engine

API_URL = "https://api.finder.work/api/v2/vacancies/"
LIMIT = 50

params = {
    'location': 'all',
    # 'ordering': 'relevance',
    'ordering': '-publicated_at',
    'limit': LIMIT,
    'offset': 0,
}

# ENUM

# params = {
#     'employment_type': [
#         'full_time',
#         'part_time',
#         'non_standard',
#         'project',
#         'internship',
#     ],
#     'location': 'moskva',
#     'limit': '35',
#     'offset': '35',
# }

def parse():
    # Создание таблиц (если они еще не созданы)
    Base.metadata.create_all(bind=engine)

    parser = FinderParser(API_URL, params)
    raw_vacancies = parser.parse()
    vacancies, companies = zip(*[parser.extract_data(item) for item in raw_vacancies])

    # Save vacancies
    vacancy_service = VacancyService()
    vacancy_service.save_vacancies(vacancies)

    # Save companies
    company_service = CompanyService()
    company_service.save_company(companies)

def main():
    parse()

if __name__ == "__main__":
    main()
