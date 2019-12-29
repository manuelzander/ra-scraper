.PHONY: clean

module = scraper
object = results.jsonl

build: clean
	#@echo "Check bot"
	#cd $(module) && scrapy check ra_artist_spider
	@echo "Producing results file"
	cd $(module) && scrapy crawl ra_artist_spider
	@echo "Printing results file"
	cat $(module)/$(object)
	@echo "Data written to $(PWD)/$(module)"

clean:
	@echo "Removing results file"
	rm -rf $(module)/$(object)
