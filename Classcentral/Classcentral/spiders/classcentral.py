import scrapy
from ..items import ClasscentralItem


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
            self.logger.info(f'"{self.subject}" NOT IN SUBJECTS. PLEASE ENTER RIGHT SUBJECT')
        else:
            for subject in self.short_subjects:
                absolute_url = self.base_url + f'subject/{subject}'
                yield scrapy.Request(absolute_url, callback=self.parse_subject)

    def parse_subject(self, response):
        l = ClasscentralItem()

        courses = response.css(
            'li.bg-white.border-all.border-gray-light.padding-xsmall.radius-small.margin-bottom-small.medium-up-padding-horz-large.medium-up-padding-vert-medium.course-list-course')

        for course in courses:
            l['title'] = course.xpath('.//h2[@itemprop="name"]/text()').get()
            l['description'] = course.xpath('.//p/a/text()').get()
            l['rating'] = course.xpath('.//*[@class="cmpt-rating-medium "]/@aria-label').get().split('out')[0]
            l['views'] = course.xpath('.//span[@class="text-3 color-gray margin-left-xxsmall"]/text()').get()
            advantages = course.xpath('.//span[@class="text-3 margin-left-small line-tight"]/text()').getall()
            l['advantages'] = [advantage.strip() for advantage in advantages]

            yield l
