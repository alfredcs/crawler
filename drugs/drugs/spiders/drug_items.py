import scrapy
class DrugScraperItem(scrapy.Item):
# define the fields for your item here like:
# name = scrapy.Field()
    href = scrapy.Field()
    names = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
