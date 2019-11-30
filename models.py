from db_config import Base
from sqlalchemy import Column, String, Integer


class QueueItem(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True)
    url = Column(String(500), unique=True)
    source = Column(String(500))

    def __init__(self, url, source=None):
        self.url = url
        self.source = source

    def __str__(self):
        return f'<QueueItem: {self.url}>'


class CrawlerItem(Base):
    __tablename__ = "crawler"

    id = Column(Integer, primary_key=True)
    url = Column(String(500), unique=True)
    response_code = Column(Integer)
    title = Column(String(500))
    description = Column(String(500))
    source = Column(String(500))

    def __init__(self, url, response_code, title=None, description=None, source=None):
        self.url = url
        self.response_code = response_code
        self.title = title
        self.description = description
        self.source = source

    def __str__(self):
        return f'<CrawlerItem: {self.response_code} {self.url}>'
