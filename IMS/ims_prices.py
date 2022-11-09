import scrapy
import re


class ImsSpyder(scrapy.Spider):
    name = "ims"
    start_urls = ['https://www.internetmarketingschool.co.in/all-courses/']

    def parse(self, response):
        hrefs = response.xpath("//div[@class='elementor-image']/a/@href").extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.xpath("//h2[@class='elementor-heading-title elementor-size-default']/text()").get()
        currency = response.xpath("//p[@class='price']/del/span/bdi/span/text()").get()
        currency = currency.replace('\u20b9', '₹')
        if '₹' in currency:
            currency = 'INR '
        regular_price = response.xpath("//p[@class='price']/del/span/bdi/text()").get()
        sale_price = response.xpath("//p[@class='price']/ins/span/bdi/text()").get()
        link = response.request.url

        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }