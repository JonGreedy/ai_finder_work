from datetime import datetime
import json

from database.db import Base

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    salary_from = Column(Integer, nullable=True, default=0)
    salary_to = Column(Integer, nullable=True, default=0)
    currency_symbol = Column(String, nullable=True)
    employment_type = Column(String(50), nullable=True)
    distant_work = Column(Boolean, default=False)
    experience = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    publication_at = Column(DateTime, default=datetime.now)
    locations = Column(Text, nullable=True)  # Хранение местоположений в формате JSON
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    company = relationship("Company", back_populates="vacancies")

    @property
    def locations_list(self):
        return json.loads(self.locations) if self.locations else []

    def __repr__(self):
        return f"<Vacancy(id={self.id}, title={self.title}, salary_from={self.salary_from}, salary_to={self.salary_to})>"
