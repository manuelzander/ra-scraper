import logging
import os

import scrapy
from scraper.utils.file_io import get_artists
from scraper.utils.logger import get_logger
from scraper.items import ScraperItem

log = get_logger(__name__)


class RaArtistSpider(scrapy.Spider):
    name = "ra_artist_spider"
    allowed_domains = ["residentadvisor.net"]

    def __init__(self):
        if os.environ.get("SCRAPY_CHECK"):
            log.setLevel(logging.WARNING)

    def parse(self, response):
        # """ Default callback used by Scrapy to process downloaded responses
        # Spiders Contracts: https://docs.scrapy.org/en/latest/topics/contracts.html
        #
        # @url https://www.residentadvisor.net/dj/Solomun
        # @returns items 0
        # @scrapes date artist title venue city
        # """
        # TODO: Get Spiders Contracts working

        log.info("Parse function called on %s", response.url)

        EVENT_SELECTOR = "#items .bbox"

        for event in response.css(EVENT_SELECTOR):

            DATE_SELECTOR = ".flag+ h1 ::text"
            TITLE_SELECTOR = ".title .title ::text"
            LINK_SELECTOR = ".title a::attr(href)"
            VENUE_CITY_SELECTOR = "a+ span ::text"

            date = event.css(DATE_SELECTOR).extract_first()
            title = event.css(TITLE_SELECTOR).extract_first()
            link = "https://www.residentadvisor.net" + event.css(LINK_SELECTOR).extract_first()
            venue_and_city = event.css(VENUE_CITY_SELECTOR).getall()

            # TODO: Improve parsing of venue and city
            try:
                if len(venue_and_city) == 2:
                    venue = venue_and_city[0][2:]
                    city = venue_and_city[1]
                else:
                    venue = venue_and_city[1]
                    city = venue_and_city[3]
            except Exception as e:
                log.error("Unexpected ERROR: %s", e)
                raise

            # TODO: Follow links to events to automatically get full line-up and prices, if available

            log.info("Successfully parsed %s", response.url)
            yield ScraperItem(
                artist=response.meta["artist"],
                date=date,
                title=title,
                link=link,
                venue=venue,
                city=city,
            )

    def start_requests(self):
        artists = get_artists("artists.txt")
        for artist in artists:
            url = f"https://www.residentadvisor.net/dj/{artist}"
            yield scrapy.Request(url=url, callback=self.parse, meta={"artist": artist})
