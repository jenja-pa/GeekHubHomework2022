import re

import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from scrapy_crawlers.items import ExtentionItem


class ChromeWebstoreSpider(scrapy.Spider):
    name = 'chrome_webstore_spider'
    allowed_domains = ['chrome.google.com']

    def start_requests(self):
        start_url = 'https://chrome.google.com/webstore/sitemap'
        yield scrapy.Request(url=start_url, callback=self.parse_sitemap)

    @staticmethod
    def get_namespaces(response):
        """
        Добування наявних просторів імен із текстового представлення відповіді
        виду:
          xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
          xmlns:xhtml="http://www.w3.org/1999/xhtml"
        return [(name_namespace, url_namespace), ...]
        """
        begin_response_text = response.text[:1024]
        return re.findall(r'xmlns[\:]*(\w*)="([^"]*)"', begin_response_text)

    def parse_sitemap(self, response):
        self.log("parse_sitemap = 1")

        lst_ns = ChromeWebstoreSpider.get_namespaces(response)
        self.log(f"Response namespaces: {lst_ns=}")
        for name_ns, url_ns in lst_ns:
            response.selector.register_namespace('d' if name_ns == "" else name_ns, url_ns)
        # lst = response.xpath("//*[name()='loc']/text()").getall()
        # self.log(f'{lst=}')
        lst_locs = response.xpath("//d:loc/text()").getall()
        # self.log(f'{lst=}')
        # todo debug feature - save response
        # filename = "2_response_loc.txt"
        # with open(filename, "w") as file:
        #     for loc in lst:
        #         file.write(f"{loc}\n")
        # self.log(f'Saved file {filename}')
        for idx, url_next_page in enumerate(lst_locs):
            # todo - debug exit
            if idx > 2:
                return
            yield scrapy.Request(url_next_page, callback=self.parse_shard, cb_kwargs={"n_page": idx})

    def parse_shard(self, response, n_page):
        self.log(f"parse_shard: {n_page}")
    
        # todo debug feature - save response
        # filename = f"3_shard_loc_{n_page}.txt"
        # with open(filename, "w") as file:
        #     file.write(response.text)
        # self.log(f'Saved file {filename}')

        lst_ns = ChromeWebstoreSpider.get_namespaces(response)
        for name_ns, url_ns in lst_ns:
            response.selector.register_namespace('d' if name_ns == "" else name_ns, url_ns)
    
        lst_locs_webstore = response.xpath("//d:loc/text()").getall()
        for idx, url_target_page in enumerate(lst_locs_webstore):
            # todo - debug exit
            if idx > 1:
                return
            yield scrapy.Request(url_target_page, callback=self.parse_page_webstore, cb_kwargs={"n_page": n_page, "idx_in_page": idx})
    
    def parse_page_webstore(self, response, n_page, idx_in_page):
        item_loader = ItemLoader(item=ExtentionItem(), response=response)
        item_loader.add_value('id_item', response.url.split('/')[-1])
        item_loader.add_css('name', 'h1.e-f-w::text')
        item_loader.add_xpath('description', '//div[@itemprop="description"]/text()')

        return item_loader.load_item()
        