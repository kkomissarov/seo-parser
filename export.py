import csv
from models import CrawlerItem
from db_config import db_session


def export_csv():
    qs = db_session.query(CrawlerItem).all()
    with open('export.csv', 'w', encoding='windows-1251') as export_file:
        writer = csv.writer(export_file)
        writer.writerow(['code', 'url', 'source', 'title', 'description'])
        for item in qs:
            writer.writerow([item.response_code, item.url, item.source, item.title, item.description])
