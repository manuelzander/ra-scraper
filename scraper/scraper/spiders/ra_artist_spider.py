import logging
import os

import scrapy

from scrapy.utils.project import get_project_settings

from scraper.items import EventItem, EventLineupItem, EventPriceItem
from scraper.utils.file_io import get_artists
from scraper.utils.logger import get_logger

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

        log.info("Parse artist event data; called on %s", response.url)

        EVENT_SELECTOR = "#items .bbox"

        for event in response.css(EVENT_SELECTOR):

            DATE_SELECTOR = ".flag+ h1 ::text"
            TITLE_SELECTOR = ".title .title ::text"
            LINK_SELECTOR = ".title a::attr(href)"
            VENUE_CITY_SELECTOR = "a+ span ::text"

            date = event.css(DATE_SELECTOR).extract_first()
            title = event.css(TITLE_SELECTOR).extract_first()
            link = response.urljoin(event.css(LINK_SELECTOR).extract_first())
            id = link.split("/")[-1]
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

            yield EventItem(
                id=id,
                artist=response.meta["artist"],
                date=date,
                title=title,
                link=link,
                venue=venue,
                city=city,
            )

            if link is not None:
                yield response.follow(
                    link, callback=self.parse_other_lineup_artists, meta={"id": id}
                )

    def parse_other_lineup_artists(self, response):

        log.info("Parse further artist event data; called on %s", response.url)

        links = []
        artists = []

        for size in ["small", "medium", "large"]:
            if not links and not artists:
                # Note: Currently only LINKED artists included in lineup
                links = response.css(f"#event-item .{size} a ::attr(href)").getall()
                artists = response.css(f"#event-item .{size} a ::text").getall()

        if links and artists:
            yield EventLineupItem(
                id=response.meta["id"], lineup=artists,
            )

        closed_prices = response.css("#tickets ul li.closed p ::text").getall()
        onsale_prices = response.css("#tickets ul li.onsale.but p ::text").getall()

        if closed_prices or onsale_prices:
            closed_prices_paired = [
                (closed_prices[i], closed_prices[i + 1])
                for i in range(0, len(closed_prices), 2)
            ]
            onsale_prices_paired = [
                (onsale_prices[i], onsale_prices[i + 1])
                for i in range(0, len(onsale_prices), 2)
            ]

            yield EventPriceItem(
                id=response.meta["id"],
                closed_prices=closed_prices_paired,
                onsale_prices=onsale_prices_paired,
            )

        # TODO: Consider use of scrapy-rotating-proxies and scrapy-useragents due to recursive calls
        if get_project_settings().get("RECURSIVE"):
            if (links and artists) and (len(links) == len(artists)):
                for link, artist in zip(links, artists):
                    yield response.follow(
                        link, callback=self.parse, meta={"artist": artist}
                    )

    def start_requests(self):
        artists = get_artists("artists.txt")
        for artist in artists:
            url = f"https://www.residentadvisor.net/dj/{artist}"
            yield scrapy.Request(url=url, callback=self.parse, meta={"artist": artist})
