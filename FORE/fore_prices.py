from datetime import datetime
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "fore" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.fsm.ac.in/enhancing-assertiveness-and-positive-attitude'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        data = response.xpath("//b[contains(text(),'Fees:')]/following-sibling::text()").extract()

        for i in data:
            price = i.strip()
            if 'Online' in price:
                regular_price = re.findall('Rs\.(.*?)\s', price)[0]
            if 'Classroom' in price:
                class_regular_price = re.findall('Rs\.(.*?)\s', price)[0]
            if 'Residential' in price:
                resi_regular_price = re.findall('Rs\.(.*?)\s', price)[0]

        currency = 'INR'

        sale_price = regular_price

        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }