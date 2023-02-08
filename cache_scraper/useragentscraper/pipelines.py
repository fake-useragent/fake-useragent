# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import logging

logger = logging.getLogger(__name__)

# from scrapy.pipelines.files import FilesPipeline

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from scrapy.exceptions import DropItem


# Template:
class ScraperPipeline:
    def process_item(self, item, spider):
        return item
