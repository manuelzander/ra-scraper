from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    """Removes duplicates, using the 'artist', 'date' and 'title' fields as composite key"""

    def __init__(self):
        self.events_seen = set()

    def process_item(self, item, spider):

        combined_key = f'{item["artist"]}-{item["date"]}-{item["title"]}'

        if combined_key in self.events_seen:
            raise DropItem("Duplicate item found: %s", item)
        else:
            self.events_seen.add(combined_key)
            return item


class DatesPipeline(object):
    """Reformat the 'date' field, removing the last 3 chars"""

    def process_item(self, item, spider):
        if item.get("date"):
            item["date"] = item["date"][:-3]
            return item
        else:
            raise DropItem("Missing date in %s", item)
