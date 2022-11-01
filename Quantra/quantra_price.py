import scrapy
import json
import re

class MyprojectSpider(scrapy.Spider):

    name = "quantsi_price" 

    def start_requests(self):

        link = 'https://quantra.quantinsti.com/course/python-trading-basic'

        yield scrapy.Request(url=link, callback=self.parse)


    def parse(self, response):

        link = response.url
        cname = link.split('/')[-1]

        course_url = f'https://quantra-api-elb.quantinsti.com/getCourseDetailsById/{cname}'

        yield scrapy.Request(url=course_url, callback=self.price)

    def price(self, response):

        data = response.text
        data = json.loads(data)

        sale_price = float(data['result']['Amount'])
        regular_price = float(data['result']['amount_actual'])

        usa_sale_price = float(data['result']['amount_usd'])
        usa_regular_price = float(data['result']['amount_actual_usd'])

        other_sale_price = float(data['result']['amount_usd_developing_nations'])
        other_regular_price = float(data['result']['amount_actual_usd_developing_nations'])


        yield {
                'regular_price': regular_price,
                'price': sale_price
        }