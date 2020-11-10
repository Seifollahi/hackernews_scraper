# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HckrnewsprojectItem(scrapy.Item):
    
    post_id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    points = scrapy.Field()
    date = scrapy.Field()
    comments = scrapy.Field()
    user = scrapy.Field()
    pass
