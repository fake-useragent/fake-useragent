#!/usr/bin/env python3
from multiprocessing import Process

from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from useragentscraper.spiders.useragent import (
    UserAgentSpider,
)


# Create Process around the CrawlerRunner
class CrawlerRunnerProcess(Process):
    def __init__(self, spider):
        Process.__init__(self)
        self.runner = CrawlerRunner(get_project_settings())
        self.spider = spider

    def run(self):
        deferred = self.runner.crawl(self.spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)


# The wrapper to make it run multiple spiders, multiple times
def run_spider(spider):
    crawler = CrawlerRunnerProcess(spider)
    crawler.start()
    crawler.join()


configure_logging()

# Start the crawler in a scheduler
scheduler = BlockingScheduler(timezone="Europe/Amsterdam")
# Use cron job; runs the user-agent spider once a week (on sunday) at 6:10
scheduler.add_job(
    run_spider, "cron", args=[UserAgentSpider], day_of_week="sun", hour=6, minute=10
)
scheduler.start()
