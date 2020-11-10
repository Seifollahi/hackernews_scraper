from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, SmallInteger)
from scrapy.utils.project import get_project_settings


Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """

    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class News(Base):
    __tablename__ = "News"

    id = Column(Integer, primary_key = True)
    post_id = Column('post_id', String(20))
    title = Column('title', Text())
    source = Column('source', Text())
    url = Column('url', Text())
    ponits = Column('points', SmallInteger)
    date = Column('date', DateTime)
    comments = Column('comments', Integer)
    user = Column('user', String(150))
