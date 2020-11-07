import scrapy
from hckrnewsproject.items import HckrnewsprojectItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from datetime import datetime, timedelta

class hckrnewsSpider(CrawlSpider):
    name = "hckrnews"
    allowed_domains = ["ycombinator.com"]
    start_urls = [
        "https://news.ycombinator.com/"
    ]

    rules = [
        Rule(LinkExtractor(allow=r'news\?p=[0-3]'), callback='parse', follow=True),
    ]

    
    def parse(self,response):
        titles = response.xpath("//table[@class= 'itemlist']").xpath(".//tr[@class= 'athing']")
        item = HckrnewsprojectItem()

        for title in titles:
            id = title.xpath("./@id").get()
            points = response.xpath("//tr/td[@class='subtext']/span[@id='score_{id}']/text()".format(id=id)).extract_first()
            time = response.xpath("//tr/td[@class='subtext']/span[@class= 'age']/a[@href='item?id={id}']/text()".format(id=id)).get().split(' ', 1)[0]

            item['id']= id
            item['title']= title.xpath(".//a[@class='storylink']/text()").get()
            item['source']= title.xpath(".//span[@class= 'sitestr']/text()").get()
            item['url']= title.xpath(".//a[@class='storylink']/@href").get()
            item['points']= points
            item['date'] = datetime.now() - timedelta(hours=int(time))

            yield item

            


