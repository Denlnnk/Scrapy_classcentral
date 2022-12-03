# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClasscentralItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    views = scrapy.Field()
    advantages = scrapy.Field()
