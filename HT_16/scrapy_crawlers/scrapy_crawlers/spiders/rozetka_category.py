import json
from urllib.parse import urljoin
from urllib.parse import urlencode

import scrapy

from scrapy_crawlers.items import RozetkaItem


class RozetkaCategorySpider(scrapy.Spider):
    name = 'rozetka_category_spider'
    allowed_domains = ['rozetka.com.ua']
    BASE_URL = 'http://rozetka.com.ua/'
    BASE_URL_API_GOOD = ('https://rozetka.com.ua/api/product-api/v4/'
                         'goods/get-main')

    def __init__(self, relative_url=None, *args, **kwargs):
        super(RozetkaCategorySpider, self).__init__(*args, **kwargs)
        self.start_url = f'{urljoin(self.BASE_URL, relative_url)}'
        self.last_number_page = None

    def start_requests(self):
        yield scrapy.Request(self.start_url)

    def parse(self, response, n_page=1):
        for idx, good_id in enumerate(
                response.css('div.goods-tile__inner::attr(data-goods-id)')
                .getall()):
            yield scrapy.Request(
                self.BASE_URL_API_GOOD + "?" + urlencode(
                    {"lang": "ua", "goodsId": good_id}), 
                callback=self.parse_good, 
                cb_kwargs={"n_page": n_page, "n_good_on_page": idx})

        # find possible next page
        if self.last_number_page is None:
            # this is first page
            last_page_href = response.css(
                'ul.pagination__list li.pagination__item a::attr(href)'
                ).getall()[-1]
            self.last_number_page = int(
                last_page_href.split('/')[-2].replace("page=", ""))

        if self.last_number_page == n_page:
            # break process crawling
            return
        cb_kwargs = {"n_page": n_page + 1}
        href_target = f'page={cb_kwargs["n_page"]}'
        yield scrapy.Request(
            urljoin(self.start_url, href_target), 
            callback=self.parse, cb_kwargs=cb_kwargs)

    def parse_good(self, response, n_page, n_good_on_page):
        data_json = json.loads(response.text)["data"]

        item = RozetkaItem(
            id_item=data_json["id"],
            title=data_json["title"],
            price=data_json["price"],
            old_price=data_json["old_price"],
            href=data_json["href"],
            name=data_json["name"],
            docket=data_json["docket"],
            state=data_json["state"],
            brand=data_json["brand"],
            category_id=data_json["last_category"]["id"],
            category_title=data_json["last_category"]["title"],
            article=data_json["article"]
            )

        yield item
