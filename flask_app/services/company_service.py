import json
from typing import List, Dict
from models.company import Company
from database.db import get_db

class CompanyService:
    def __init__(self):
        self.db = next(get_db())

    def save_company(self, companies: List[Dict]):
        for item in companies:
            # Проверяем, существует ли компания с таким company_id
            existing_company = self.db.query(Company).filter(Company.company_id == item['company_id']).first()
            if existing_company:
               continue
            # Убедимся, что contacts правильно сериализованы в JSON-строку
            contacts_json = json.dumps(item['contacts'], ensure_ascii=False)

            # Если компания не существует, добавляем её
            company = Company(
                company_id=item['company_id'],
                title=item['title'],
                tax_id=item['tax_id'],
                site_url=item['site_url'],
                description=item['description'],
                logo=item['logo'],
                type=item['type'],
                has_paid_vacancies=item['has_paid_vacancies'],
                contacts=contacts_json
            )
            self.db.add(company)
            # print(f"Компания с ID {item['company_id']} добавлена.")

            self.db.commit()  # Commit after each operation to ensure the session is properly managed
