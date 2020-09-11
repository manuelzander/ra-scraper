# ra-scraper: Resident Advisor event scraper

![status](https://img.shields.io/github/workflow/status/manuelzander/ra-scraper/ra-scraper/master?label=actions&logo=github&style=for-the-badge) ![last-commit](https://img.shields.io/github/last-commit/manuelzander/ra-scraper/master?logo=github&style=for-the-badge) ![issues-pr-raw](https://img.shields.io/github/issues-pr-raw/manuelzander/ra-scraper?label=open%20prs&logo=github&style=for-the-badge) ![release](https://img.shields.io/github/v/release/manuelzander/ra-scraper?&style=for-the-badge) [![license](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Scrape [Resident Advisor](https://residentadvisor.net) (RA) to find out where and when your favourite (techno) artists are playing.

## Prerequisites

![python](https://img.shields.io/badge/python-3.7-blue?style=for-the-badge&logo=python&logoColor=white)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The code is run and tested with Python 3.7.5 on macOS 10.14.6 and Ubuntu 18.04.5.

### Environment

Clone the repo to your local machine.
Create a virtual environment for Python 3 with:

```
virtualenv -p python3 env
```

Activate the virtual environment with:

```
source env/bin/activate
```

Install the required Python packages with:

```
pip3 install -r requirements.txt
```

### Artists

Within the `scraper/artists.txt` file specify all artists you want to scrape events for (one per line).

Artist names should be in a format such that a valid RA url `https://www.residentadvisor.net/dj/ARTIST_NAME` exists.

## Running the scraper (spider)

This project uses the [scrapy](https://scrapy.org/) Python library (tutorial [here](https://docs.scrapy.org/en/latest/intro/tutorial.html)).

You can find the spider with the name `ra_artist_spider` in the file `scraper/scraper/spiders/ra_artist_spider.py`.

To start the spider and save results locally please run:

```
make build
```

If you want to recursively scrape events of artists mentioned in the lineup section on the event pages scraped for the initially given artists, set the following value in `scraper/scraper/settings.py`:

```
RECURSIVE = True
```

This setting can result in a very large number of requests, which can be controlled by `CLOSESPIDER_ITEMCOUNT` or `CLOSESPIDER_PAGECOUNT`.

## Example output

Every run of `make build` produces three JSON Line files (data models in `scraper/scraper/items.py`).
The first one contains general event information for the given artists, the second and third ones contain the lineup and price information for these events, if available.

For example (one artist only, no recursive scraping):

1. `EventItem.jsonl` (four events on artist page [Solomun](https://www.residentadvisor.net/dj/solomun))

```
{"id": "1319532", "artist": "Solomun", "date": "Tue, 31 Dec 2019", "title": "NYE with Solomun & Jamie Jones by Link Miami Rebels", "link": "https://www.residentadvisor.net/events/1319532", "venue": "Space", "city": "Miami"}
{"id": "1363163", "artist": "Solomun", "date": "Sat, 04 Jan 2020", "title": "Solomun 1 Maceo Plex Tulum", "link": "https://www.residentadvisor.net/events/1363163", "venue": "Templo Xunanha Tulum", "city": "South"}
{"id": "1363420", "artist": "Solomun", "date": "Sat, 25 Apr 2020", "title": "Solomun Paris 2020", "link": "https://www.residentadvisor.net/events/1363420", "venue": "La Seine Musicale / Seguin", "city": "Paris"}
{"id": "1352870", "artist": "Solomun", "date": "Sat, 20 Jun 2020", "title": "Diynamic - Off Week Festival", "link": "https://www.residentadvisor.net/events/1352870", "venue": "Parc Del Forum", "city": "Barcelona"}
```

2. `EventLineupItem.jsonl` (four events with lineup section available)

```
{"id": "1319532", "lineup": ["Solomun", "Jamie Jones", "Danyelino", "Thunderpony"]}
{"id": "1363163", "lineup": ["Solomun", "Maceo Plex"]}
{"id": "1363420", "lineup": ["Solomun"]}
{"id": "1352870", "lineup": ["Solomun"]}
```

3. `EventPriceItem.jsonl` (three events with price section available, both sold-out and on-sale event prices)

```
{"id": "1319532", "closed_prices": [["$20.00", "1st release (entry before 12AM)"], ["$50.00", "2nd release (entry before 12AM)"], ["$80.00", "3rd release (entry before 12AM)"], ["$150.00", "4th release (entry before 12AM)"], ["$80.00", "1st release (entry before 3 AM)"], ["$100.00", "2nd release (entry before 3 AM)"], ["$120.00", "3rd release (entry before 3 AM)"], ["$100.00", "1st release (entry ANYTIME)"], ["$120.00", "2nd release (entry ANYTIME)"], ["$150.00", "3rd release (entry ANYTIME)"], ["$250.00", "4th release (entry ANYTIME)"], ["$80.00", "1st release (entry AFTER 10 AM)"], ["$100.00", "2nd release (entry AFTER 10 AM)"], ["$120.00", "3rd release (entry AFTER 10 AM)"], ["$70.00", "1st release (entry AFTER 12 PM)"], ["$60.00", "1st release (entry AFTER 2 PM)"], ["$80.00", "2nd release (entry AFTER 2 PM)"]], "onsale_prices": [["$100.00 + $12.50", "2nd release (entry AFTER 12 PM)"]]}
{"id": "1363420", "closed_prices": [], "onsale_prices": [["35,00 € + 4,40 €", "1st release"], ["100,00 € + 12,50 €", "Backstage - VIP"]]}
{"id": "1352870", "closed_prices": [["19,50 €", "Early bird "], ["29,50 €", "1st release"]], "onsale_prices": [["39,50 € + 4,95 €", "2nd release"], ["150,00 € + 18,75 €", "Backstage experience"], ["49,00 € + 6,10 €", "FRIDAY ALL PARK TICKET (Afterlife+Arpiar+Solid Grooves)"], ["49,00 € + 6,10 €", "SATURDAY ALL PARK TICKET (Diynamic+FRRC+Secretsundaze)"], ["99,00 € + 12,40 €", "WEEKEND ALL PARK TICKET (All Events)"], ["300,00 € + 37,50 €", "Weekend backstage experience "]]}
```

In order to additionally create a JSONL or CSV file with all results, set the following values in `scraper/scraper/settings.py`:

```
FEED_EXPORTERS = {"jsonlines": "scrapy.exporters.JsonLinesItemExporter"}
FEED_FORMAT = "jsonlines"
FEED_URI = "results.jsonl"
```

```
FEED_EXPORTERS = {"csv": "scrapy.exporters.CsvItemExporter"}
FEED_FORMAT = "csv"
FEED_URI = "results.csv"
```

## Email notifications

To send the content in `EventItem.jsonl` via eMail to your Google mail account run:

```
make notify
```

You need to set the environment variables `ACCOUNT` (eMail address) and `SECRET` (password) before.

Further settings are available in `scraper/notifications.py`.

For daily notifications, you can use GitHub Actions and deploy the workflow with the `.github/workflows/app.yml` file.

## To-do list

- [x] Event lineup and price collection
- [x] Email notifications
- [ ] Visualizations/stats (Dash front-end?)
- [ ] Database connection
- [ ] Resident Advisor API

## Authors

- Manuel Zander

## License

See [LICENSE](./LICENSE)
