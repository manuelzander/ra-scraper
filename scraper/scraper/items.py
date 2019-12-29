import scrapy


class ScraperItem(scrapy.Item):
    date = scrapy.Field()
    artist = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    venue = scrapy.Field()
    city = scrapy.Field()
