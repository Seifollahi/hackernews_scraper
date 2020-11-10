# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from sqlalchemy import update
from hckrnewsproject.models import *
import scrapy
import postgresql


class HckrnewsprojectPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        news = News()

        news.post_id = item["post_id"]
        news.title = item["title"]
        news.source = item["source"]
        news.url = item["url"]
        news.points = item["points"]
        news.date = item["date"]
        news.comments = item["comments"]
        news.user = item["user"]


        # Check whether the id exists, then update the comments and points
        session_query = session.query(News).filter_by(post_id=news.post_id)
        exists_id = session_query.first()
        if exists_id is not None:
            # stmt = update(News).where(News.post_id==news.post_id).values(News.ponits = news.ponits)
            # stmt = update(News).where(News.post_id==news.post_id).values(News.ponits = news.ponits)
            session_query.update({News.ponits:news.points}, synchronize_session = False)
            session_query.update({News.comments:news.comments}, synchronize_session = False)
            session.commit()

            raise DropItem("Duplicate item found: %s" % item)


        try:
            session.add(news)
            session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

        