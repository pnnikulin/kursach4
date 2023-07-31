import json
import os
import requests
import datetime
import time
from abc import abstractmethod, ABC
from enum import StrEnum


class Platform(StrEnum):
    SuperJob = 'SuperJob'
    HeadHunter = 'HeadHunter'


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
            # }
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

    API_URL = f'https://api.hh.ru/vacancies/'
    HEADER = {"User_Agent": "HH-User-Agent"}

    def __init__(self):
        pass

    def get_vacancies(self, keyword):
        payload = {
            "text": keyword,
            "per_page": 20,
            "page": 0,
            "archived": False
        }

        hh_vacancies_list = []
        hh_data = requests.get(self.API_URL, headers=self.HEADER, params=payload).json()
        for vacancy in hh_data['items']:
            try:
                hh_vacancies_list.append(
                    Vacancy(
                        platform=Platform.HeadHunter,
                        name=vacancy.get('name'),
                        url=vacancy.get('alternate_url'),
                        salary=vacancy.get('salary', 99).get('from', 0),
                    )
                )
            except AttributeError:
                hh_vacancies_list.append(
                    Vacancy(
                        platform=Platform.HeadHunter,
                        name=vacancy.get('name'),
                        url=vacancy.get('alternate_url'),
                        salary=0,
                    )
                )

        return hh_vacancies_list


sjapi = SjApiConnector()
result = sjapi.get_vacancies('Python')
#print(result[0] == result[3])
#print(id(result[0]))
#print(id(result[3]))

hhapi = HhApiConnector()
result_hh = hhapi.get_vacancies('Python')
print(result_hh)
print(result)
# print(testhh2)
