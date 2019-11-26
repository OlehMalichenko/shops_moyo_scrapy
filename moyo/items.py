import scrapy


class MoyoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    prod_id = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    available = scrapy.Field()

