# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Join


def del_line_feed(value):
    return value.replace('\n', '')


def del_carriage_return(value):
    return value.replace('\r', '')


class ExtentionItem(scrapy.Item):
    id_item = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(
            del_line_feed,
            del_carriage_return,
            str.strip),
        output_processor=Join()
        )


class RozetkaItem(scrapy.Item):
    id_item = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    href = scrapy.Field()
    name = scrapy.Field()
    category_id = scrapy.Field()
    docket = scrapy.Field()
    state = scrapy.Field()
    brand = scrapy.Field()
    category_id = scrapy.Field()
    category_title = scrapy.Field()
    article = scrapy.Field()

    # description = scrapy.Field(
    #     input_processor=MapCompose(
    #         del_line_feed,
    #         del_carriage_return,
    #         str.strip),
    #     output_processor=Join()
    # )

 #    "id":340365525,
 #    "title":"Мобільний телефон Samsung Galaxy A73 5G 6/128Gb White (SM-A736BZWDSEK)",
 #    "price":"19299",
 #    "old_price":"20699",
 #    "href":"https://rozetka.com.ua/ua/samsung-sm-a736bzwdsek/p340365525/",
 #    "name":"samsung-sm-a736bzwdsek",
 #    "category_id":80003,
 #    "docket":"Екран (6.7\", Super AMOLED Plus, 2400x1080) / Qualcomm Snapdragon 778G (4 x 2.4 ГГц + 4 x 1.8 ГГц) / основная квадрокамера: 108 Мп + 12 Мп + 5 Мп + 5 Мп, фронтальна 32 Мп / RAM 6 ГБ / 128 ГБ вбудованої пам'яті + microSD (до 1 ТБ) / 3G / LTE / 5G / GPS / A-GPS / ГЛОНАСС / BDS / підтримка 2х SIM-карт (Nano-SIM) / Android 12 / 5000 мА*год",
 #    "state":"new",
 #    "brand":"Samsung",
 #    "last_category":{
 #      "id":80003,
 #      "title":"Мобільні телефони",}
 #    "article":"SM-A736BZWDSEK",

 # * бренд,
 # * категорія,
 # * модель,
 # * ціна,
 # * рейтинг

