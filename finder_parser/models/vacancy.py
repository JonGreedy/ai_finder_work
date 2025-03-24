from sqlalchemy import Column, Integer, String, Text, JSON
from ..database.db import Base
import json

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    salary_from = Column(Integer, nullable=True)
    salary_to = Column(Integer, nullable=True)
    currency_symbol = Column(String, nullable=True)
    contacts = Column(String, nullable=True)  # Хранение контактов в формате JSON
    @property
    def contacts_dict(self):
        contacts = json.loads(self.contacts) if self.contacts else []
        phone = next((item['value'] for item in contacts if item['type'] == 'phone'), None)
        email = next((item['value'] for item in contacts if item['type'] == 'email'), None)
        return {'phone': phone, 'email': email}
    company_info = Column(String, nullable=True)  # Хранение информации о компании в формате JSON
    @property
    def company_info_dict(self):
        return json.loads(self.company_info) if self.company_info else {}
    locations = Column(String, nullable=True)  # Хранение местоположений в формате JSON
    @property
    def locations_list(self):
        # locations = json.loads(self.locations) if self.locations else []
        # return [location['name'] for location in locations]
        return json.loads(self.locations) if self.locations else []

    def __repr__(self):
        return f"<Vacancy(id={self.id}, title={self.title}, salary_from={self.salary_from}, salary_to={self.salary_to})>"
