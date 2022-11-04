from datetime import datetime
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "amity_prices" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://amityonline.com/'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        data = response.xpath("//a[@onclick='hrefClick(this.id)']/@href").extract()

        for link in data:

            if 'Home' in link:
                link = response.url + link
            
            yield scrapy.Request(url=link, callback=self.prices)



    def prices(self, response):

        regular_price = response.xpath('//h2[@id="pfees"]/following::h3[1]/text() | //div[@id="dvOneTimeG-one"]//span/span[2]/text()').get()
        
        regular_price = re.sub('[^0-9]', '',  regular_price)
        regular_price = float(regular_price)

        currency = 'INR'

        sale_price = regular_price

        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }