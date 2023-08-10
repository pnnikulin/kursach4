from abc import abstractmethod, ABC
from src.api_connectors import Vacancy
import json

from src.api_connectors import SjApiConnector, HhApiConnector

from pathlib import Path

PATH = Path(Path(__file__).parent.parent, 'data', 'vacancy.json')


class AbstractSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractSaver):
    """Class для сохранения, чтения, удаления вакансий"""

    def __init__(self):
        self.path_json = PATH

    def _read_vacancies(self):
        with open(self.path_json, 'r', encoding='utf8') as json_file:
            json_vacancies = json.loads(json_file.read())
        # print(json_vacancies)
        self.vacancies = [Vacancy.from_dict(data) for data in json_vacancies]
        # print(self.vacancies)

    def _save_vacancies(self):
        json_vacancies = [vacancy.to_dict() for vacancy in self.vacancies]
        #print(json_vacancies)

        with open(self.path_json, 'w', encoding='utf8') as json_file:
            json.dump(json_vacancies, json_file, indent=2, ensure_ascii=False)

    def get_vacancies(self):
        pass
        # get_sj_data_temp = self.get_vacancies.
        # get_hh_data_temp = self.get_vacancies().HhApiConnector
        # get_sj_data = json.dumps(get_sj_data_temp, indent=2, ensure_ascii=False)
        # get_hh_data = json.dumps(get_hh_data_temp, indent=2, ensure_ascii=False)
        # print(get_sj_data)
        # return get_sj_data, get_hh_data

    def add_vacancy(self, vacancy_list):
        #print(vacancy)
        self._read_vacancies()
        # print(self.vacancies)
        for vacancy in vacancy_list:
            print(vacancy)
            if vacancy not in self.vacancies:
                self.vacancies.append(vacancy)
                self._save_vacancies()

    def get_top_vacancies_by_salary(self):
        pass

    def delete_vacancy(self):
        pass


# sjapi = SjApiConnector()
# test = JSONSaver()
#
# new_vacancy = sjapi.get_vacancies('Python')
# test2 = test.add_vacancy(new_vacancy)
