from src.api_connectors import HhApiConnector, SjApiConnector, Platform
from src.saver import JSONSaver
import click
from operator import itemgetter, attrgetter, methodcaller


@click.group()
def cli():
    pass


@cli.command()
@click.option('--platform', help='Select platform', required=True)
@click.option('--keyword', help='Keyword for search', required=True)
def download(platform, keyword):
    try:
        Platform(platform)
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
    vacancies = api.get_vacancies(keyword)
    JSONSaver().add_vacancies(vacancies)
    #print_result = JSONSaver()._read_vacancies()
    for result in vacancies:
        print(result)
    # логика получения api по платформе
    # получение вакансий по кейворд
    # сохранение в файл
    # print("Saved 5 new vacancies")


@cli.command()
@click.option('--search', help='Select platform', required=True)
# @click.option('--top_n', type=int, help='....')
def find(search):
    vacancies = JSONSaver().get_vacancies()
    for result in vacancies:
        if search in result['description']:
            print(f"Платформа: {result['platform']}, Прямая ссылка: {result['url']}, "
                  f"Зарпалата: {result['salary']}, Описание: {result['description']}\n\n")


#     # вычитать из json вакансии
#     # отфильтровать
# if top_n:
#         # sort по зарплате + [:n]

@cli.command()
@click.option('--top_n', type=int, help='....')
def top(top_n):
    try:
        vacancies = JSONSaver().get_vacancies()
        sorted_result = sorted(vacancies, key=lambda x: x['salary'], reverse=True)
        for result in sorted_result[:top_n]:
            print(f"Зарплата: {result['salary']}, Платформа: {result['platform']}, "
                  f"Прямая ссылка: {result['url']}, Описание: {result['description']}\n\n")
    except TypeError:
        pass


@cli.command()
def count():
    print_result = JSONSaver().get_vacancies()
    print(f'Всего вакасий: {len(print_result)}')
    result_hh = []
    result_sj = []
    for result in print_result:
        if result['platform'] == 'SuperJob':
            result_sj.append(result)
        if result['platform'] == 'HeadHunter':
            result_hh.append(result)
    print(f'Вакансий Super Job: {len(result_sj)}')
    print(f'Вакансий Head Hunter: {len(result_hh)}')


@cli.command()
# @click.pass_context
@click.option('--url', help='Select platform', required=True)
def delete(url):
    """Delete vacancy by url"""
    #print('Вакансии до удаления')
    #count()

    JSONSaver().delete_vacancy(url=url)
    # проверка удаления
    #result_of_delete = JSONSaver().get_vacancies()
    print('Удалено. Для проверки удаления используйте функцию count')
    #count()


@cli.command()
# @click.pass_context
def clear():
    """Delete vacancy by url"""
    JSONSaver().clear_vacancies()


if __name__ == '__main__':
    cli()

# ./program.py download --platform=SuperJob --keyword=Python -> сохраниться в файл
# ./program.py download --platform=HeadHunter --keyword=Java -> сохраниться в файл
#
# ./program.py find --searhc_words=Java [top_n=N] -> результат фильтра
# ./program.py count -> общее количество ваканси по платформам
# ./program.py delete --url=url
