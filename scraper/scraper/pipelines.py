from scraper.items import EventItem, EventLineupItem
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter


class DuplicatesPipeline(object):
    """Removes duplicates, using the 'id' field (per item category)"""

    def __init__(self):
        self.EventItem_seen = set()
        self.EventLineupItem_seen = set()
        self.EventPriceItemItem_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, EventItem):
            if item["id"] in self.EventItem_seen:
                raise DropItem("Duplicate item found: %s", item)
            else:
                self.EventItem_seen.add(item["id"])
                return item
        elif isinstance(item, EventLineupItem):
            if item["id"] in self.EventLineupItem_seen:
                raise DropItem("Duplicate item found: %s", item)
            else:
                self.EventLineupItem_seen.add(item["id"])
                return item
        else:
            if item["id"] in self.EventPriceItemItem_seen:
                raise DropItem("Duplicate item found: %s", item)
            else:
                self.EventPriceItemItem_seen.add(item["id"])
                return item


# class CustomDuplicatesPipeline(object):
#     """Removes duplicates, using the 'artist', 'date' and 'title' fields as composite key"""
#
#     def __init__(self):
#         self.events_seen = set()
#
#     def process_item(self, item, spider):
#
#         # Only use DuplicatesPipeline for EventItem instances
#         if not isinstance(item, EventItem):
#             return item
#
#         combined_key = f'{item["artist"]}-{item["date"]}-{item["title"]}'
#
#         if combined_key in self.events_seen:
#             raise DropItem("Duplicate item found: %s", item)
#         else:
#             self.events_seen.add(combined_key)
#             return item


class DatesPipeline(object):
    """Reformat the 'date' field, removing the last 3 chars"""

    def process_item(self, item, spider):

        # Only use DuplicatesPipeline for EventItem instances
        if not isinstance(item, EventItem):
            return item

        if item.get("date"):
            item["date"] = item["date"][:-3]
            return item
        else:
            raise DropItem("Missing date in %s", item)


class MyJsonLinesItemExporter(object):
    """Distribute items across multiple JSONL files according to item types (type(item).__name__)"""

    def open_spider(self, spider):
        self.item_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.item_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        type_name = str(type(item).__name__)
        if type_name not in self.item_to_exporter:
            f = open("{}.jsonl".format(type_name), "wb")
            exporter = JsonLinesItemExporter(f, encoding="utf-8", ensure_ascii=False)
            exporter.start_exporting()
            self.item_to_exporter[type_name] = exporter
        return self.item_to_exporter[type_name]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
