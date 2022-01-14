import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem

#11
class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://kirov.superjob.ru/vakansii/stroitel.html',
                   'https://kirov.superjob.ru/vakansii/stroitel.html'
                  ]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath('//span[@class="_1BOkc"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//span[@class="_3a-0Y _3DjcL _3sM6i"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//span[@class='_2Wp8I _3a-0Y _3DjcL _1tCB5 _3fXVo']//text()")
        if salary:
            salary = salary.getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
