import json
from urllib.parse import urljoin
from urllib.parse import urlencode

import scrapy
# from scrapy.loader import ItemLoader

from scrapy_crawlers.items import RozetkaItem


class RozetkaCategorySpider(scrapy.Spider):
    name = 'rozetka_category_spider'
    allowed_domains = ['rozetka.com.ua']
    BASE_URL = 'http://rozetka.com.ua/'
    BASE_URL_API_GOOD = ('https://rozetka.com.ua/api/product-api/v4/'
                         'goods/get-main')

    def __init__(self, relative_url=None, *args, **kwargs):
        super(RozetkaCategorySpider, self).__init__(*args, **kwargs)
        # self.log(f'===>{self.BASE_URL=}')
        # self.log(f'===>{relative_url=}')
        # self.log(f'===>{urljoin(self.BASE_URL, relative_url)}')
        self.start_url = f'{urljoin(self.BASE_URL, relative_url)}'
        self.last_number_page = None

    def start_requests(self):
        # self.log(f"start_requests: {self.start_url}")
        yield scrapy.Request(self.start_url)

    def parse(self, response, n_page=1):
        self.log(f"parse: {response.url} page:{n_page}")
        # todo debug 
        # with open(f"page_{n_page}.html", "wb") as file:
        #     file.write(response.body)

        # # todo stub restriction only 2 pages in pagination
        # if n_page > 2:
        #     return

        for idx, good_id in enumerate(response.css('div.goods-tile__inner::attr(data-goods-id)').getall()):
            # todo debug case
            # self.log(f'{n_page}-{idx}-{self.BASE_URL_API_GOOD + "?" + urlencode({"lang":"ua", "goodsId": good_id})}')

            # todo debug case get first idx goods of first page
            # if idx > 2:
            #     return
            yield scrapy.Request(self.BASE_URL_API_GOOD + "?" + urlencode({"lang": "ua", "goodsId": good_id}), callback=self.parse_good, cb_kwargs={"n_page": n_page, "n_good_on_page": idx})

        # find possible next page
        if self.last_number_page is None:
            # this is first page
            last_page_href = response.css('ul.pagination__list li.pagination__item a::attr(href)').getall()[-1]
            self.last_number_page = int(last_page_href.split('/')[-2].replace("page=", ""))
            self.log(f"~~~~~~~~~~~>last avail url:{last_page_href}, last_n_page:{self.last_number_page}")

        # href_target = response.css('ul.pagination__list li.pagination__item + li  a::attr(href)').get()
        # self.log(f"______>:{n_page=} next-url:{href_target=}")
        # self.log(f"______>:{n_page=} {urljoin(self.BASE_URL, href_target)}")
        if self.last_number_page == n_page:
            # break process crawling
            self.log(f"__~~~~~~~~____>:{self.last_number_page} == {n_page=} BREAK")
            return
        cb_kwargs = {"n_page": n_page + 1}
        href_target = f'page={cb_kwargs["n_page"]}'
        yield scrapy.Request(urljoin(self.start_url, href_target), callback=self.parse, cb_kwargs=cb_kwargs)

    def parse_good(self, response, n_page, n_good_on_page):
        # todo debug case
        # self.log(f"parse_good: {n_page}-{n_good_on_page}")

        # # todo debug 
        # with open(f"good_{n_page}_{n_good_on_page}.json", "wb") as file:
        #     file.write(response.body)

        data_json = json.loads(response.text)["data"]

        # self.log(f"{data_json=}")

        # item_loader = ItemLoader(item=RozetkaItem(), response=response)
        # self.log(f"{str(item_loader)=}")
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
        # self.log(f"{item.keys()=}")

        yield item

        # item_loader.add_value(id_item, data_json["id"])
        # item_loader.add_value(title, data_json["title"])
        # item_loader.add_value(price, data_json["price"])
        # item_loader.add_value(old_price, data_json["old_price"])
        # item_loader.add_value(href, data_json["href"])
        # item_loader.add_value(name, data_json["name"])
        # item_loader.add_value(docket, data_json["docket"])
        # item_loader.add_value(state, data_json["state"])
        # item_loader.add_value(brand, data_json["brand"])
        # item_loader.add_value(category_id, data_json["last_category"]["id"])
        # item_loader.add_value(category_title, data_json["last_category"]["title"])
        # item_loader.add_value(article, data_json["article"])

        # return item_loader.load_item()
