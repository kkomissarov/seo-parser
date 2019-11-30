import requests
from bs4 import BeautifulSoup as bs
from utils import clean_link
from db_config import db_session
from models import QueueItem, CrawlerItem
from time import sleep


def get_page_info(response):
    soup = bs(response.text, 'lxml')
    response_code = response.status_code
    page_url = response.url
    title_tag = soup.find('title')
    title_text = title_tag.text if title_tag else None
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description_text = description_tag.get('content') if description_tag else None
    page_info_dict = {
        'url': page_url,
        'response_code': response_code,
        'title': title_text,
        'description': description_text
    }
    return page_info_dict


def get_page_links(response):
    soup = bs(response.text, 'lxml')
    base_url_tag = soup.find('base', href=True)
    base_url = base_url_tag['href'] if base_url_tag else response.url
    all_links = [a.get('href') for a in soup.find_all('a', href=True) if a.get('href')]
    cleaned_links = list(set([clean_link(link, base_url) for link in all_links]) - {None})
    return cleaned_links


def write_page_info(response, source=None):
    similar_crawler_item = db_session.query(CrawlerItem).filter(CrawlerItem.url == response.url).first()
    if not similar_crawler_item:
        new_crawler_item = CrawlerItem(**get_page_info(response), source=source)
        db_session.add(new_crawler_item)
        db_session.commit()
        print(new_crawler_item)
    else:
        print(f'Warning! Результат для страницы {response.url} уже собран.')


def write_redirect_in_queue(response):
    redirect_url = response.headers['Location']
    similar_queue_item = db_session.query(QueueItem).filter(QueueItem.url == redirect_url).first()
    if not similar_queue_item:
        redirect_queue_item = QueueItem(url=response.headers['Location'], source=response.url)
        db_session.add(redirect_queue_item)
        db_session.commit()


def write_page_links_in_queue(response):
    for link in get_page_links(response):
        similar_in_queue = db_session.query(QueueItem).filter(QueueItem.url == link).first()
        similar_in_crawler = db_session.query(CrawlerItem).filter(CrawlerItem.url == link).first()
        if not similar_in_crawler and not similar_in_queue:
            queue_item = QueueItem(url=link, source=response.url)
            db_session.add(queue_item)
            db_session.commit()


def run_crawler(domain, speed=0.1, verify_ssl=True):
    db_session.query(CrawlerItem).delete()
    db_session.query(QueueItem).delete()
    first_queue_item = QueueItem(domain)
    db_session.add(first_queue_item)
    db_session.commit()

    while db_session.query(QueueItem).first():
        sleep(speed)
        current_queue_item = db_session.query(QueueItem).first()
        response = requests.get(
            current_queue_item.url,
            headers={'User-Agent': 'MrnrBot/1.0'},
            allow_redirects=False,
            verify=verify_ssl
        )
        write_page_info(response, current_queue_item.source)

        if response.is_redirect:
            write_redirect_in_queue(response)

        if response.ok:
            write_page_links_in_queue(response)

        db_session.delete(current_queue_item)
        db_session.commit()

