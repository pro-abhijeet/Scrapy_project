from datetime import datetime
from locale import currency
import scrapy



class MyprojectSpider(scrapy.Spider):

    name = "cfi" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://corporatefinanceinstitute.com/pricing/'

        yield scrapy.Request(url=link, callback=self.subscription)



    def subscription(self, response):

        monthly_pricing = response.xpath("//div[@class='card-price-value']/text()").extract()
        pricing_decimal = response.xpath("//div[@class='card-price-value-decimal']/text()").extract()
        monthly_currency = response.xpath("//div[@class='card-price-currency']/text()").extract()

        subscription_type = response.xpath("//h3[@class='card-name']/text()[1]").extract()

        for price, decimal, currency, sub_type in zip(monthly_pricing, pricing_decimal, monthly_currency, subscription_type):

            regular_price = price+decimal

            if currency == '$': 
                currency = 'USD'

            sub_type = sub_type.strip()

            price = regular_price

            yield {
                'regular_price': regular_price,
                'price': price,
                'currency': currency,
                'subscription_type': sub_type
            }