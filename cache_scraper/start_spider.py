#!/usr/bin/env python3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from useragentscraper.spiders.useragent import (
    UserAgentSpider,
)

# Start crawl right away
process = CrawlerProcess(get_project_settings())
process.crawl(UserAgentSpider)
process.start()
