from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse_vacancies(self):
        """Абстрактный метод для парсинга вакансий."""
        pass