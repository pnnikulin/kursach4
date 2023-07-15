import json
import os
import requests
import datetime
import time
from abc import abstractmethod, ABC


class API_connector(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancy(self):
        pass


class SJ_API_Connector(API_connector):
    """класс для подключения к API SuperJob и парсер вакансий"""

    api_key_superjob = os.getenv('SJ_API_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api_key_superjob}

    def __init__(self, keyword):
        self.keyword: str = keyword
        self.payload = {
            'keyword': self.keyword,
            'count': 20,
            'page': 0,
            'archive': False
        }

    def get_vacancy(self):
        superjob_data = requests.get(self.url, headers=self.headers, params=self.payload).json()
        super_job_vacancies_list = []
        for vacancy in superjob_data['objects']:
            keys_vacancy = {
                'platform': "SuperJob",
                'profession': vacancy.get('profession'),
                'salary': vacancy.get('payment_from'),
                'link': vacancy.get('link'),
                'currency': vacancy.get("currency")
            }
            super_job_vacancies_list.append(keys_vacancy)
        return super_job_vacancies_list

class HH_API_Connector(API_connector):
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

    def get_vacancy(self):
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


testsj = SJ_API_Connector('python')
testsj2 = SJ_API_Connector.get_vacancy(testsj)

testhh = HH_API_Connector('python')
testhh2 = HH_API_Connector.get_vacancy(testhh)


print(testsj2)
print(testhh2)
