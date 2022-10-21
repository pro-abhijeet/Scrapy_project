from datetime import datetime
from locale import currency
import scrapy


class MyprojectSpider(scrapy.Spider):

    name = "blockchain" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://101blockchains.com/membership/'

        yield scrapy.Request(url=link, callback=self.subscription)

    def subscription(self, response):

        prices = response.xpath("//div[@class='pho-price-time']/h3/ins/bdi/text()").extract()
        yearly_regular_price = response.xpath('//div[@class="pho-price-time"]/h3/del[@aria-hidden="true"]/bdi/text()').extract_first()

        monthly_regular_price = prices[0]
        yearly_sale_price = prices[1]

        if '$' in monthly_regular_price:
            currency = 'USD'

        courses_url = "https://101blockchains.com/academy/"

        print(monthly_regular_price)
        print(yearly_sale_price)

        yield scrapy.Request(url=courses_url, callback=self.price, cb_kwargs={'monthly': monthly_regular_price, 'yearly_sale': yearly_sale_price, 'currency': currency, 'yearly_regular': yearly_regular_price})


    def price(self, response, currency, monthly, yearly_sale, yearly_regular):

        for course in response.xpath('//div[@class="t-couse-wrapper"]'):

            course_url = course.xpath('./a/@href').extract_first()

            regular_price = course.xpath('./h5/text()').extract_first()

            if regular_price == None:
                regular_price = ''

            if '$' in regular_price:
                regular_price = regular_price.replace('$', '')
                regular_price = float(regular_price)
                currency = 'USD'
            
            

            yield {"Annual Plan": {"price_details": {"url": course_url,"currency": currency, "type": "", "regular_price_monthly": yearly_regular, "sale_price_monthly": yearly_sale, "total_price": float(yearly_regular)*12, "coupon": "ABC"}}}