from parsers.base_parser import BaseParser
from typing import Dict, List


class NewSiteParser(BaseParser):
    def __init__(self, api_url: str, params: Dict):
        self.api_url = api_url
        self.params = params


    def parse(self) -> List[Dict]:
        # Реализация парсера для нового сайта
        pass