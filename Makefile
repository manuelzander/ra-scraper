.PHONY: clean

module = scraper
object = results.json

build: clean
	@echo "Producing results file"
	cd $(module) && scrapy crawl ra_artist_spider -o results.json
	@echo "Printing results file"
	cat $(module)/$(object)

clean:
	@echo "Removing results file"
	rm -rf $(module)/$(object)
