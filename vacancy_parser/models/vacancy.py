from sqlalchemy import Column, Integer, String, Text
from database.db import Base


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer, unique=True, nullable=False)  # ID вакансии из API
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)


    def __repr__(self):
        return f"<Vacancy(vacancy_id={self.vacancy_id}, title='{self.title}', company='{self.company}', location='{self.location}')>"