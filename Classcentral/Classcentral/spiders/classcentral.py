import scrapy
from ..items import ClasscentralItem
from scrapy.loader import ItemLoader


class ClasscentralSpider(scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']

    def __init__(self, subject=None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject
        self.base_url = 'https://www.classcentral.com/'
        self.short_subjects = {'Computer Science': 'cs', 'Business': 'business', 'Humanities': 'humanities',
                               'Data Science': 'data-science', 'Personal Development': 'personal-development',
                               'Art & Design': 'art-and-design', 'Programming': 'programming-and-software-development',
                               'Engineering': 'engineering', 'Health & Medicine': 'health', 'Mathematics': 'maths',
                               'Science': 'science', 'Social Sciences': 'social-sciences',
                               'Education & Teaching': 'education', 'Information Security (InfoSec)': 'infosec'}

    def start_requests(self):
        if self.subject and self.subject in self.short_subjects:
            absolute_url = self.base_url + f'subject/{self.short_subjects[self.subject]}'
            yield scrapy.Request(absolute_url, callback=self.parse_subject)
        elif self.subject and self.subject not in self.short_subjects:
            self.logger.info(f'"{self.subject}" NOT EXIST SUBJECT. PLEASE ENTER CORRECT SUBJECT')
        else:
            for subject in self.short_subjects:
                absolute_url = self.base_url + f'subject/{subject}'
                yield scrapy.Request(absolute_url, callback=self.parse_subject)

    def parse_subject(self, response):
        courses = response.xpath('//li[@itemprop="itemListElement"]')

        for course in courses:
            l = ItemLoader(item=ClasscentralItem(), selector=course)
            l.add_xpath('title', './/h2[@itemprop="name"]/text()')
            l.add_xpath('description', './/p/a/text()')
            l.add_xpath('rating', './/*[@class="cmpt-rating-medium "]/@aria-label')
            l.add_xpath('views', './/span[@class="text-3 color-gray margin-left-xxsmall"]/text()')
            advantages = course.xpath('.//span[@class="text-3 margin-left-small line-tight"]/text()').getall()
            l.add_xpath('provider', './/a[@aria-label="Provider"]/text()')
            l.add_value('advantages', [advantage.strip() for advantage in advantages])

            yield l.load_item()

        next_page_url = response.xpath('//link[@rel="next"]/@href').get()

        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url, callback=self.parse_subject)
