import scrapy
class BookscraperItem(scrapy.Item):
# define the fields for your item here like:
# name = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
