import json
from typing import List, Dict
from models.vacancy import Vacancy
from database.db import get_db


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

            # Сериализуем сложные данные в JSON-строки
            contacts_json = json.dumps(item['contacts'], ensure_ascii=False)
            company_info_json = json.dumps(item['company_info'], ensure_ascii=False)
            locations_json = json.dumps(item['locations'], ensure_ascii=False)

            # Если вакансия не существует, добавляем её
            vacancy = Vacancy(
                vacancy_id=item['vacancy_id'],
                title=item['title'],
                description=item['description'],
                salary_from=item['salary_from'],
                salary_to=item['salary_to'],
                currency_symbol=item['currency_symbol'],
                contacts=contacts_json,
                company_info=company_info_json,
                locations=locations_json
            )
            self.db.add(vacancy)
            # print(f"Вакансия с ID {item['vacancy_id']} добавлена.")
        
        self.db.commit()