import os
import requests
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
        self.salary = salary or 0
        self.description = description

    def __repr__(self):
        return f'{self.name} ({self.salary}) {self.description}'

    def __eq__(self, other):
        return self.url == other.url

    def to_dict(self):
        return {
            'platform': self.platform,
            'name': self.name,
            'url': self.url,
            'salary': self.salary,
            'description': self.description,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            platform=data['platform'],
            name=data['name'],
            url=data['url'],
            salary=data['salary'],
            description=data['description']
        )


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

        super_job_vacancies_list = []
        superjob_data = requests.get(self.URL, headers=self.HEADERS, params=payload).json()
        for vacancy in superjob_data['objects']:
            # print(vacancy)
            super_job_vacancies_list.append(
                Vacancy(
                    platform=Platform.SuperJob,
                    name=vacancy.get('profession'),
                    url=vacancy.get('link'),
                    salary=vacancy.get('payment_from'),
                    description=vacancy.get('candidat')
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
            hh_vacancies_list.append(
                Vacancy(
                    platform=Platform.HeadHunter,
                    name=vacancy.get('name'),
                    url=vacancy.get('alternate_url'),
                    salary=vacancy["salary"].get("from", 0) if vacancy.get("salary") else 0,
                    description=vacancy.get('snippet', {}).get('requirement')
                )
            )
        return hh_vacancies_list

#
# sjapi = SjApiConnector()
# result = sjapi.get_vacancies('Python')
# # #print(result[0] == result[3])
# # #print(id(result[0]))
# # #print(id(result[3]))
# #
# hhapi = HhApiConnector()
# result_hh = hhapi.get_vacancies('Python')
# #print(result_hh)
# print(result)
# # print(testhh2)
