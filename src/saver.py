from abc import abstractmethod, ABC
from src.api_connectors import Vacancy
import json


from pathlib import Path

PATH = Path(Path(__file__).parent.parent, 'data', 'vacancy.json')


class AbstractSaver(ABC):
    @abstractmethod
    def add_vacancies(self, vacancies):
        pass


class JSONSaver(AbstractSaver):
    """Class для сохранения, чтения, удаления вакансий"""

    def __init__(self):
        self.path_json = PATH
        self.vacancies = None

    def _read_vacancies(self):
        with open(self.path_json, 'r', encoding='utf8') as json_file:
            json_vacancies = json.loads(json_file.read())
        # print(json_vacancies)
        self.vacancies = [Vacancy.from_dict(data) for data in json_vacancies]
        # print(self.vacancies)
        return self.vacancies

    def _save_vacancies(self):
        json_vacancies = [vacancy.to_dict() for vacancy in self.vacancies]
        # print(json_vacancies)
        with open(self.path_json, 'w', encoding='utf8') as json_file:
            json.dump(json_vacancies, json_file, indent=2, ensure_ascii=False)

    def clear_vacancies(self):
        json_vacancies = []
        with open(self.path_json, 'w', encoding='utf8') as json_file:
            json.dump(json_vacancies, json_file, indent=2, ensure_ascii=False)

    def get_vacancies(self):
        with open(self.path_json, 'r', encoding='utf8') as json_file:
            json_vacancies = json.loads(json_file.read())
        return json_vacancies

    def add_vacancies(self, vacancy_list):
        # print(vacancy)
        self._read_vacancies()
        # print(self.vacancies)
        for vacancy in vacancy_list:
            # print(vacancy)
            if vacancy not in self.vacancies:
                self.vacancies.append(vacancy)
        self._save_vacancies()

    def delete_vacancy(self, url):
        self._read_vacancies()
        self.vacancies = list(filter(lambda i: i.url != url, self.vacancies))
        self._save_vacancies()

# sjapi = SjApiConnector()
# test = JSONSaver()
# #
# new_vacancy = sjapi.get_vacancies('Python')
# test2 = test.add_vacancy(new_vacancy)
