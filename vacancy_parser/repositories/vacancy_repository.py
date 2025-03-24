from sqlalchemy.orm import Session
from models.vacancy import Vacancy


class VacancyRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_vacancy(self, vacancy_data):
        # Проверяем, существует ли вакансия с таким vacancy_id
        existing_vacancy = self.db.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_data['vacancy_id']).first()
        if existing_vacancy:
            return None  # Если вакансия уже существует, пропускаем

        vacancy = Vacancy(**vacancy_data)
        # print(f"Adding vacancy to database: {vacancy_data}")
        self.db.add(vacancy)
        self.db.commit()
        self.db.refresh(vacancy)
        # print(f"Vacancy added to database: {vacancy}")
        return vacancy


    def get_vacancies(self):
        return self.db.query(Vacancy).all()
