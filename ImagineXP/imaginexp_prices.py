
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "imaginexp_price" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://imaginxp.com/courses/supply-chain-management-course/'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        try:
            regular_price = response.xpath("//div[@class='priceBlock']//del/text()").get()
        except:
            regular_price = ''

        sale_price = response.xpath("//div[@class='priceBlock']//ins/text()").get()

        if regular_price == None:
            regular_price = sale_price


        if '₹' in regular_price:
            currency = 'INR'

        regular_price = re.sub('\..*|[^0-9]', '', regular_price)
        sale_price = re.sub('\..*|[^0-9]', '', sale_price)

        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }

        
