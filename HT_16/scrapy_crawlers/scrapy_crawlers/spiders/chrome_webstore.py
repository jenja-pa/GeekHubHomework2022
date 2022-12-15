import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_crawlers.items import ExtentionItem


class ChromeWebstoreSpider(scrapy.Spider):
    name = 'chrome_webstore_spider'
    allowed_domains = ['chrome.google.com']

    def start_requests(self):
        start_url = 'https://chrome.google.com/webstore/sitemap'
        yield scrapy.Request(url=start_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        self.log("parse_sitemap = 1")

        # filename = "2_response_loc.txt"
        lst = response.xpath("//*[name()='loc']/text()").getall()
        # self.log(f'{lst=}')
        # self.log(f'2:{response.xpath("//loc/text()").get()}')
        # with open(filename, "w") as file:
        #     for loc in lst:
        #         file.write(f"{loc}\n")
        # self.log(f'Saved file {filename}')
        for idx, url_next_page in enumerate(lst):
            # todo - debug exit
            if idx > 2:
                return
            yield scrapy.Request(url_next_page, callback=self.parse_shard, cb_kwargs={"n_page": idx})

    def parse_shard(self, response, n_page):
        # self.log("parse_shard = 2")
        # filename = f"3_shard_loc_{n_page}.txt"
        # with open(filename, "w") as file:
        #     file.write(response.text)
        # self.log(f'Saved file {filename}')
        pass

