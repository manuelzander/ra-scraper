import scrapy


class EventItem(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    artist = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    venue = scrapy.Field()
    city = scrapy.Field()


