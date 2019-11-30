from models import Base
from utils import get_url_from_terminal
from parsing import run_crawler
from export import export_csv


def main():
    Base.metadata.create_all()
    domain = get_url_from_terminal()
    run_crawler(domain)
    print('Парсинг завершен. Экспортируем результат')
    export_csv()
    print('Экспорт завершен!')


if __name__ == '__main__':
    main()