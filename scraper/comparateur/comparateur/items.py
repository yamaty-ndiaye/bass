import scrapy


import scrapy

class ProductItem(scrapy.Item):
    title = scrapy.Field() # ou 'name' selon ce que tu choisis
    price = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
