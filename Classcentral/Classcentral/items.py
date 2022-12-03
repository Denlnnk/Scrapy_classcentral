# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


def receive_rating(value):
    return value.split('out')[0]


def remove_spaces(value):
    return value.strip()


class ClasscentralItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field(input_processor=MapCompose(receive_rating), output_processor=TakeFirst())
    views = scrapy.Field()
    provider = scrapy.Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    advantages = scrapy.Field()
