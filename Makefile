all: build notify

.PHONY: all clean process notify

module = scraper
object = jsonl

clean:
	# Removing results file
	rm -rf $(module)/*.$(object)

build: clean
	# Checking bot
	#cd $(module) && scrapy check ra_artist_spider
	# Producing results file
	cd $(module) && scrapy crawl ra_artist_spider
	#@echo "Data written to .$(object)-files in $(PWD)/$(module)"

process: build
	# Processing data

notify: process
	# Sending notifications
	cd $(module) && python3 notifications.py


