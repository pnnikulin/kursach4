from src.api_connectors import HhApiConnector, SjApiConnector



hh_api = HhApiConnector()
superjob_api = SjApiConnector()

hh_vacancies = hh_api.get_vacancies("Python")
superjob_vacancies = superjob_api.get_vacancies("Python")

def filter_vacancies(hh_vacancies, superjob_vacancies, filter_words):
    result = []
    for vacancy in hh_vacancies + superjob_vacancies:
        for word in filter_words:
            if word in vacancy.description:
                result.append(vacancy)
                break
    return result


def user_interaction():
    ##platforms = ["HeadHunter", "SuperJob"]
    #search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return
    print(filtered_vacancies)

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()