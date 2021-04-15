# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllCodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    data=scrapy.Field()
    history=scrapy.Field()
    #for k,v in data.items():
    #    print

class AllCodsList(scrapy.Item):
    word=scrapy.Field()
    url = scrapy.Field()
    type_word = scrapy.Field()

