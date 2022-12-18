# run_spider_chrome_webstore.py
# task_1.py
import scrapy
from scrapy.crawler import CrawlerProcess

from scrapy_crawlers.spiders.chrome_webstore import ChromeWebstoreSpider
# class MySpider(scrapy.Spider):
#     # Your spider definition
#     ...

# proc = CrawlerProcess(s)

# s = proc.get_project_settings()
# s['FEED_FORMAT'] = 'csv'
# s['LOG_LEVEL'] = 'INFO'
# s['FEED_URI'] = 'result.csv'
# s['LOG_FILE'] = 'result.log'
def run_spider():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "result.csv": {"format": "csv"},
        },
    })

    process.crawl(ChromeWebstoreSpider)
    process.start()
    

if __name__ == "__main__":
    run_spider()