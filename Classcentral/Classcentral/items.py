import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def receive_rating(value):
    return value.split('out')[0]


def correct(value):
    return value.strip().replace('\u00ed', 'i').replace('\u00e1', 'a').replace('\u00fa', 'u')


class ClasscentralItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(correct), output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(correct), output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(receive_rating), output_processor=TakeFirst())
    views = scrapy.Field()
    provider = scrapy.Field(input_processor=MapCompose(correct), output_processor=TakeFirst())
    advantages = scrapy.Field()
