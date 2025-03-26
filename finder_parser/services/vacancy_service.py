import json
from typing import List, Dict
from models.vacancy import Vacancy
from database.db import get_db
from datetime import datetime as dt

class VacancyService:
    def __init__(self):
        self.db = next(get_db())

    def save_vacancies(self, vacancies: List[Dict]):
        for item in vacancies:
            # Проверяем, существует ли вакансия с таким vacancy_id
            existing_vacancy = self.db.query(Vacancy).filter(Vacancy.vacancy_id == item['vacancy_id']).first()
            if existing_vacancy:
                print(f"Вакансия с ID {item['vacancy_id']} уже существует, пропускаем.")
                continue  # Пропускаем добавление, если вакансия уже существует

            # Убедимся, что locations правильно сериализованы в JSON-строку
            locations_json = json.dumps(item['locations'], ensure_ascii=False)

            # Если вакансия не существует, добавляем её
            vacancy = Vacancy(
                vacancy_id=item['vacancy_id'],
                title=item['title'],
                description=item['description'],
                salary_from=item['salary_from'],
                salary_to=item['salary_to'],
                currency_symbol=item['currency_symbol'],
                employment_type=item.get('employment_type'),
                distant_work=item.get('distant_work', False),
                experience=item.get('experience'),
                created_at=dt.fromisoformat(item['created_at'].replace('Z', '+00:00')),
                publication_at=dt.fromisoformat(item['publication_at'].replace('Z', '+00:00')),

                # pub_at = '2025-03-26T13:29:00.461Z'
                # created_at = '2025-02-27T13:14:29.461Z'

                # # Формат для разбора
                
                # pub_datetime = datetime.strptime(pub_at, iso_format)
                # created_datetime = datetime.strptime(created_at, iso_format)

                locations=locations_json,
                company_id=item['company_id']
            )
            self.db.add(vacancy)
            # print(f"Вакансия с ID {item['vacancy_id']} добавлена.")

        self.db.commit()