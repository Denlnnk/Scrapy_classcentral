import scrapy


class ClasscentralSpider(scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/']

    def parse(self, response, **kwargs):
        pass
