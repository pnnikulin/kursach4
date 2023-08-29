from src.api_connectors import HhApiConnector, SjApiConnector, Platform


# print(superjob_vacancies)
# print(hh_vacancies)


def filter_vacancies(hh_vacancies, superjob_vacancies, filter_words):
    result = []
    for vacancy in hh_vacancies + superjob_vacancies:
        for word in filter_words:
            if word in vacancy.description:
                result.append(vacancy)
                break
    return result


def sort_vacancies():
    pass


def get_top_vacancies():
    pass


def user_interaction():
    print(f"Программа для поиска вакансий с платформ HeadHunter или SuperJob")

    try:
        platform = Platform(input())
    except ValueError:
        print('Error input')
        exit(1)

    if platform == Platform.SuperJob:
        api = SjApiConnector()

    elif platform == Platform.HeadHunter:
        api = HhApiConnector()
    else:
        print('Unsupported platform')
        exit(1)

    search_query = str(input("Введите поисковый запрос: "))
    vacancies = api.get_vacancies(search_query)
    #print(vacancies)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    #filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    # print(len(filtered_vacancies))
    # #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # # print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
