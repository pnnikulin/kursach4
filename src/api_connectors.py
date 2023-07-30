import json
import os
import requests
import datetime
import time
from abc import abstractmethod, ABC
from enum import StrEnum

class Platform(StrEnum):
    SuperJob ='SuperJob'
    HeadHunter ='HeadHunter'

class Vacancy:
    def __init__(self, platform: Platform, name: str, url: str, salary: int, description: str = ''):
        self.platform = platform
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    def __repr__(self):
        return f'{self.name} ({self.salary})'

    def __eq__(self, other):
        return self.salary == other.salary


class ApiConnector(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class SjApiConnector(ApiConnector):
    """класс для подключения к API SuperJob и парсер вакансий"""

    API_KEY = os.getenv('SJ_API_KEY')
    URL = 'https://api.superjob.ru/2.0/vacancies/'
    HEADERS = {'X-Api-App-Id': API_KEY}

    def __init__(self):
        pass

    def get_vacancies(self, keyword):
        payload = {
            'keyword': keyword,
            'count': 20,
            'page': 0,
            'archive': False
        }
        superjob_data = requests.get(self.URL, headers=self.HEADERS, params=payload).json()
        super_job_vacancies_list = []
        for vacancy in superjob_data['objects']:
            # keys_vacancy = {
            #     'platform': "SuperJob",
            #     'profession': vacancy.get('profession'),
            #     'salary': vacancy.get('payment_from'),
            #     'link': vacancy.get('link'),
            #     'currency': vacancy.get("currency")
            #}
            super_job_vacancies_list.append(
                Vacancy(
                    platform=Platform.SuperJob,
                    name=vacancy.get('profession'),
                    url=vacancy.get('link'),
                    salary=vacancy.get('payment_from'),
                )
            )
        return super_job_vacancies_list


class HhApiConnector(ApiConnector):
    """класс для подключения к API HH и парсер вакансий"""
    def __init__(self, keyword):
        self.keyword: str = keyword
        self.api_url_hh = f'https://api.hh.ru/vacancies/'
        self.header = {"User_Agent": "HH-User-Agent"}
        self.payload = {
            "text": self.keyword,
            "per_page": 20,
            "page": 0,
            "archived": False
        }

    def get_vacancies(self, keyword):
        hh_vacancies_list = []
        hh_data = requests.get(self.api_url_hh, headers=self.header, params=self.payload).json()
        for vacancy in hh_data['items']:
            try:
                keys_vacancy = {
                    'platform': "HeadHunter",
                    'profession': vacancy.get('name'),
                    'salary': vacancy.get('salary', 99).get('from', 0),
                    'link': vacancy.get('alternate_url'),
                    'currency': vacancy.get('salary').get("currency")
                }
            except AttributeError:
                keys_vacancy = {
                    'platform': "HeadHunter",
                    'profession': vacancy.get('name'),
                    'salary': 0,
                    'link': vacancy.get('alternate_url'),
                    'currency': "RUB"
                }
            hh_vacancies_list.append(keys_vacancy)
        return hh_vacancies_list


sjapi = SjApiConnector()
result = sjapi.get_vacancies('Python')
print(result[0] == result[3])
print(id(result[0]))
print(id(result[3]))

# testhh = HH_API_Connector('python')
# testhh2 = HH_API_Connector.get_vacancy(testhh)


print(result)
#print(testhh2)
