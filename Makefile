all: build notify

.PHONY: all clean process notify

module = scraper
object = jsonl

clean:
	#@echo "Removing results file"
	rm -rf $(module)/*.$(object)

build: clean
	#@echo "Checking bot"
	#cd $(module) && scrapy check ra_artist_spider
	#@echo "Producing results file"
	cd $(module) && scrapy crawl ra_artist_spider
	#@echo "Data written to .$(object)-files in $(PWD)/$(module)"

process: build
	#@echo "Processing data"

notify: process
	#@echo "Sending notifications"
	cd $(module) && python3 notifications.py


