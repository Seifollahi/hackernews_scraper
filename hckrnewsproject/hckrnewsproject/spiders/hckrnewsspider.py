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
        Rule(LinkExtractor(allow=r'news\?p=[0-9]'), callback='parse', follow=True),
    ]

    
    def parse(self,response):
        titles = response.xpath("//table[@class= 'itemlist']").xpath(".//tr[@class= 'athing']")
        item = HckrnewsprojectItem()

        for title in titles:
            post_id = title.xpath("./@id").get()
            points = response.xpath("//tr/td[@class='subtext']/span[@id='score_{id}']/text()".format(id=post_id)).extract_first().split()[0]
            time = response.xpath("//tr/td[@class='subtext']/span[@class= 'age']/a[@href='item?id={id}']/text()".format(id=post_id)).get().split()[0]
            comments = response.xpath("//tr/td[@class='subtext']/a[@href='item?id={id}']/text()".format(id=post_id)).get()

            if comments =='discuss':
                comments = 0

            else:
                comments = comments.split()[0]

            
            item['post_id']= post_id
            item['title']= title.xpath(".//a[@class='storylink']/text()").get()
            item['user'] = "NA"
            item['source']= title.xpath(".//span[@class= 'sitestr']/text()").get()
            item['url']= title.xpath(".//a[@class='storylink']/@href").get()
            item['points']= int(points)
            item['comments']= int(comments)
            item['date'] = datetime.now() - timedelta(hours=int(time))
            
            yield item

            


