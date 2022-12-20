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
    docket = scrapy.Field()
    state = scrapy.Field()
    brand = scrapy.Field()
    category_id = scrapy.Field()
    category_title = scrapy.Field()
    article = scrapy.Field()
