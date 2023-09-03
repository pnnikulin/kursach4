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
