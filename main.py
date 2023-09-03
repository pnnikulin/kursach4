from src.api_connectors import HhApiConnector, SjApiConnector, Platform
from src.saver import JSONSaver
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--platform', help='Select platform', required=True)
@click.option('--keyword', help='Keyword for search', required=True)
def download(platform, keyword):
    """Download and save vacancies to vacancies.json file"""
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
    for result in vacancies:
        print(result)


@cli.command()
def print_all():
    """Print all vacancies in the vacancies.json file"""
    vacancies = JSONSaver().get_vacancies()
    for result in vacancies:
        print(f"Платформа: {result['platform']}, Прямая ссылка: {result['url']}, "
              f"Зарпалата: {result['salary']}, Описание: {result['description']}\n\n")


@cli.command()
@click.option('--search', help='Input keyword', required=True)
def find(search):
    """Search in the 'Description' fild by keyword"""
    vacancies = JSONSaver().get_vacancies()
    for result in vacancies:
        if search in result['description']:
            print(f"Платформа: {result['platform']}, Прямая ссылка: {result['url']}, "
                  f"Зарпалата: {result['salary']}, Описание: {result['description']}\n\n")


@cli.command()
@click.option('--top_n', type=int, help='Input digit for Top_N output', required=True)
def top(top_n):
    """Output Top_N vacancies"""
    try:
        vacancies = JSONSaver().get_vacancies()
        sorted_vacancies = sorted(vacancies, key=lambda x: x['salary'], reverse=True)
        for result in sorted_vacancies[:top_n]:
            print(f"Зарплата: {result['salary']}, Платформа: {result['platform']}, "
                  f"Прямая ссылка: {result['url']}, Описание: {result['description']}\n\n")
    except TypeError:
        pass


@cli.command()
def count():
    """Vacancies counter"""
    print_result = JSONSaver().get_vacancies()
    print(f'Всего вакасий: {len(print_result)}')
    vacancies_hh = []
    vacancies_sj = []
    for result in print_result:
        if result['platform'] == 'SuperJob':
            vacancies_sj.append(result)
        if result['platform'] == 'HeadHunter':
            vacancies_hh.append(result)
    print(f'Вакансий Super Job: {len(vacancies_sj)}')
    print(f'Вакансий Head Hunter: {len(vacancies_hh)}')


@cli.command()
@click.option('--url', help='Input URL', required=True)
def delete(url):
    """Delete vacancy by url"""
    JSONSaver().delete_vacancy(url=url)
    print('Вакансия удалена. Для проверки удаления используйте функцию count')


@cli.command()
def clear():
    """Clear vacancies.json file"""
    JSONSaver().clear_vacancies()
    print('Вакансии удалены. Для проверки используйте функцию count')


if __name__ == '__main__':
    cli()
