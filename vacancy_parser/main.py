from database.db import get_db, Base, engine
from parsers.finder_api_parser import FinderApiParser
from parsers.finder_web_parser import FinderWebParser  # Новый парсер
from repositories.vacancy_repository import VacancyRepository
from services.vacancy_service import VacancyService


def main():
    # Создание таблиц в базе данных
    Base.metadata.create_all(bind=engine)

    # Параметры для API
    LIMIT = 100
    api_params = {
        'location': 'all',
        'ordering': 'relevance',
        'limit': LIMIT,
        'offset': 0,
    }

    # Инициализация компонентов
    db = next(get_db())

    # Используем API парсер
    api_parser = FinderApiParser(base_url="https://api.finder.work/api/v2/vacancies/", params=api_params)

    repository = VacancyRepository(db)

    service = VacancyService(repository, api_parser)
    # Запуск парсера и сохранение данных в базу
    service.fetch_and_store_vacancies()

    # Используем веб-парсер (пример)
    # web_parser = FinderWebParser(base_url="https://finder.work/vacancies")
    # web_service = VacancyService(repository, web_parser)
    # web_service.fetch_and_store_vacancies()


if __name__ == "__main__":
    main()