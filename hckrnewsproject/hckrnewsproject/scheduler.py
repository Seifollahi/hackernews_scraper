import datetime as dt
from twisted.internet import reactor
from twisted.internet import task

from spiders.hckrnewsspider import hckrnewsSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner

def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(hckrnewsSpider)

# def schedule_next_crawl(null, hour, minute):
#     tomorrow = (
#         dt.datetime.now() + dt.timedelta(seconds=45)
#         ).replace(hour=hour, minute=minute, second=0, microsecond=0)
#     sleep_time = (tomorrow - dt.datetime.now()).total_seconds()
#     reactor.callLater(45, crawl_job)
#     print("running")

def crawl():
    # d = crawl_job()
    # d.addCallback(schedule_next_crawl, hour = 18, minute= 39)
    l= task.LoopingCall(crawl_job)
    l.start(86400)



def catch_error(failure):
    print(failure.value)

if __name__=="__main__":
    crawl()
    reactor.run()