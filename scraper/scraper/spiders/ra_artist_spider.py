import scrapy
from scraper.utils.file_io import get_artists
from scraper.utils.logger import get_logger

log = get_logger(__name__)


class RaArtistSpider(scrapy.Spider):
    name = "ra_artist_spider"

    def parse(self, response):
        log.info("Parse function called on %s", response.url)

        EVENT_SELECTOR = "#items .bbox"

        for event in response.css(EVENT_SELECTOR):

            DATE_SELECTOR = ".flag+ h1 ::text"
            TITLE_SELECTOR = ".title .title ::text"
            VENUE_CITY_SELECTOR = "a+ span ::text"

            date = event.css(DATE_SELECTOR).extract_first()
            title = event.css(TITLE_SELECTOR).extract_first()
            venue_and_city = event.css(VENUE_CITY_SELECTOR).getall()

            # TODO: Improve parsing of venue and city
            if len(venue_and_city) == 2:
                venue = venue_and_city[0][2:]
                city = venue_and_city[1]
            else:
                venue = venue_and_city[1]
                city = venue_and_city[3]

            log.info("Successfully parsed %s", response.url)
            yield {"date": date, "title": title, "venue": venue, "city": city}

    def start_requests(self):
        artists = get_artists("artists.txt")
        urls = [f"https://www.residentadvisor.net/dj/{name}" for name in artists]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
