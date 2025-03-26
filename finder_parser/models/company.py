import json

from finder_parser.database.db import Base

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    tax_id = Column(String, nullable=True)
    site_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo = Column(String, nullable=True)
    type = Column(String, nullable=True)
    has_paid_vacancies = Column(Boolean)
    contacts = Column(String, nullable=True)
    vacancies = relationship("Vacancy", back_populates="company")

    @property
    def contacts_dict(self):
        contacts = json.loads(self.contacts) if self.contacts else []
        phone = next((item['value'] for item in contacts if item['type'] == 'phone'), None)
        email = next((item['value'] for item in contacts if item['type'] == 'email'), None)
        other = next((item['value'] for item in contacts if item['type'] == 'other'), None)
        telegram = next((item['value'] for item in contacts if item['type'] == 'telegram'), None)
        return {'phone': phone, 'email': email, 'other': other, 'telegram': telegram}


    def __repr__(self):
        return f"<Company(id={self.id}, title={self.title})>"
