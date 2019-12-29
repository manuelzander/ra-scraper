# ra-scraper: Resident Advisor event scraper
Scrape [Resident Advisor](https://residentadvisor.net) (RA) to find out where and when your favourite (techno) artists are playing.

## Prerequisites

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The code is run and tested with Python 3.7.5 on macOS 10.14.6.

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

You may need to set your PYTHONPATH as:

```
export PYTHONPATH=.
```

### Artists

Within the `scraper/artists.txt` file specify all artists you want to scrape events for (one per line).

Artist names should be in a format such that a valid RA url `https://www.residentadvisor.net/dj/ARTIST_NAME` exists.

## Running the scraper (spider)

This project uses the [scrapy](https://scrapy.org/) Python library (tutorial [here](https://docs.scrapy.org/en/latest/intro/tutorial.html)).

You can find the spider with the name `ra_artist_spider` in the file `scraper/scraper/spiders/ra_artist_spider.py`.

To produce a file `results.json` in the `scraper` folder containing the resulting data in JSON format run:

```
make
```

## Example output

Every run of `make` produces an updated (not appended) `results.json` file with data for all specified artists.

An example `results.json` for only one artist ([Ben Böhmer](https://www.residentadvisor.net/dj/benbohmer)) looks like this:

```
{"artist": "benbohmer", "date": "Tue, 31 Dec 2019", "title": "Every End Is A New Beginning - NYE", "link": "https://www.residentadvisor.net/events/1354509", "venue": "Watergate", "city": "Berlin"}
{"artist": "benbohmer", "date": "Fri, 21 Feb 2020", "title": "Afterglow: Ben Böhmer (Live)", "link": "https://www.residentadvisor.net/events/1333629", "venue": "Soundcheck", "city": "Washington DC"}
{"artist": "benbohmer", "date": "Sat, 22 Feb 2020", "title": "Ben Böhmer at Quantum Brooklyn (Formerly Known as Analog Brooklyn) - Made Event & Gray Area", "link": "https://www.residentadvisor.net/events/1334023", "venue": "Quantum", "city": "New York"}
{"artist": "benbohmer", "date": "Fri, 28 Feb 2020", "title": "Ben Böhmer [live]", "link": "https://www.residentadvisor.net/events/1333482", "venue": "Coda", "city": "Toronto"}
{"artist": "benbohmer", "date": "Sat, 29 Feb 2020", "title": "Ben Böhmer (Live) au Théâtre Fairmount", "link": "https://www.residentadvisor.net/events/1350509", "venue": "Théâtre Fairmount", "city": "Quebec"}
{"artist": "benbohmer", "date": "Sat, 07 Mar 2020", "title": "Crssd Festival Spring '20 presented by FNGRS CRSSD", "link": "https://www.residentadvisor.net/events/1356911", "venue": "Waterfront Park in San Diego", "city": "San Diego"}
{"artist": "benbohmer", "date": "Fri, 03 Apr 2020", "title": "Ben Böhmer (Live)", "link": "https://www.residentadvisor.net/events/1345882", "venue": "Audio SF", "city": "San Francisco"}
{"artist": "benbohmer", "date": "Fri, 17 Apr 2020", "title": "Ben Böhmer Live", "link": "https://www.residentadvisor.net/events/1356219", "venue": "Orange Yard", "city": "London"}
{"artist": "benbohmer", "date": "Fri, 01 May 2020", "title": "Ben Böhmer Live - Breathing Tour", "link": "https://www.residentadvisor.net/events/1365670", "venue": "Roxy", "city": "Prague"}
```

In order to create a CSV file, set the following values in `scraper/scraper/settings.py`:
```
FEED_EXPORTERS = {"csv": "scrapy.exporters.CsvItemExporter"}
FEED_FORMAT = "csv"
FEED_URI = "results.csv"
```


## Authors

* Manuel Zander

## License

See [LICENSE](./LICENSE)
