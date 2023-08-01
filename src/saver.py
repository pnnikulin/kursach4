from abc import abstractmethod, ABC
from src import api_connectors
import json

from src.api_connectors import SjApiConnector, HhApiConnector

from pathlib import Path
PATH = Path(Path(__file__).parent.parent, 'data', 'vacancy.json')

class AbstractSaver(ABC):
    @abstractmethod
    def savefile(self, data):
        pass


class JSONSaver(AbstractSaver):
    """Class для сохранения, чтения, удаления вакансий"""

    def savefile(self, data, path_json=PATH):
        with open(path_json, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    def get_vacancies(self):
        pass
        # get_sj_data_temp = api_connectors.SjApiConnector
        # get_hh_data_temp = api_connectors.HhApiConnector
        # get_sj_data = json.dumps(get_sj_data_temp, indent=2, ensure_ascii=False)
        # get_hh_data = json.dumps(get_hh_data_temp, indent=2, ensure_ascii=False)
        # print(get_sj_data)
        # return get_sj_data, get_hh_data

    def add_vacancy(self):
        pass

    def get_vacancies_by_salary(self):
        pass

    def delete_vacancy(self):
        pass


sjapi = SjApiConnector()
test = JSONSaver()

test2 = test.savefile(data=sjapi.get_vacancies('Python'))
