# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Join


class ExtentionItem(scrapy.Item):
    id_item = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(str.strip), 
        output_processor=Join())
