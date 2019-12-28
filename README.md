# ra-scraper
Scrape www.residentadvisor.net to find out where and when your favourite (techno) artists are playing.

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

The artist name should be in a format such that a valid url, i.e. https://www.residentadvisor.net/dj/{artist} exists.

## Running the spider

This project uses the [scrapy](https://scrapy.org/) Python library (tutorial [here](https://docs.scrapy.org/en/latest/intro/tutorial.html)).

You can find the spider with the name `ra_artist_spider` in the file `scraper/scraper/spiders`.

To produce a file ```results.json``` containing the results in JSON format simply run:

```
make
```

Every run of `make` will produce an updated ```results.json``` file (not appending).