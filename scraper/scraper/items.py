import scrapy


class EventItem(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    artist = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    venue = scrapy.Field()
    city = scrapy.Field()


class EventLineupItem(scrapy.Item):
    id = scrapy.Field()
    lineup = scrapy.Field()


class EventPriceItem(scrapy.Item):
    id = scrapy.Field()
    closed_prices = scrapy.Field()
    onsale_prices = scrapy.Field()
