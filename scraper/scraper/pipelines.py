from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    """Removes duplicates, using an items 'title' field as key"""

    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        if item["title"] in self.titles_seen:
            raise DropItem("Duplicate item found: %s", item)
        else:
            self.titles_seen.add(item["title"])
            return item
