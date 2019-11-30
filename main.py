from models import Base
from utils import get_url_from_terminal
from parsing import run_crawler


def main():
    Base.metadata.create_all()
    domain = get_url_from_terminal()
    run_crawler(domain)


if __name__ == '__main__':
    main()