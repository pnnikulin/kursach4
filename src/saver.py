from abc import abstractmethod, ABC
from src import api_connectors


class AbstractSaver(ABC):
    @abstractmethod
    def __init__(self):
        pass


class JSONSaver(AbstractSaver):

    def get_vacancies(self):
        get_sj_data = api_connectors.SjApiConnector
        get_hh_data = api_connectors.HhApiConnector



    def add_vacancy(self):
        pass


    def get_vacancies_by_salary(self):
        pass


    def delete_vacancy(self):
        pass

