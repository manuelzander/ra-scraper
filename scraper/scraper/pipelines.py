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


class DatesPipeline(object):
    """Reformat the 'date' field, removing the last 3 chars"""

    def process_item(self, item, spider):
        if item.get('date'):
            item['date'] = item['date'][:-3]
            return item
        else:
            raise DropItem("Missing date in %s", item)
