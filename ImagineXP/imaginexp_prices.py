from datetime import datetime
from locale import currency
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "imaginexp_price" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://imaginxp.com/courses/ui-design-course/'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        try:
            regular_price = response.xpath("//div[@class='priceBlock']//del/text()").get()
        except:
            regular_price = ''

        sale_price = response.xpath("//div[@class='priceBlock']//ins/text()").get()

        if regular_price == '':
            regular_price = sale_price


        if '₹' in regular_price:
            currency = 'INR'

        regular_price = re.sub('[^0-9]', '', regular_price)
        sale_price = re.sub('[^0-9]', '', sale_price)

        print(regular_price)
        print(sale_price)

        
