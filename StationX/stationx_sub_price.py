import scrapy
import json
import re


class MyprojectSpider(scrapy.Spider):

    name = "stationx" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://courses.stationx.net/courses/369378/coupon_and_product_data?coupon_code=VIPREGULAR'

        yield scrapy.Request(url=link, callback=self.subscription)



    def subscription(self, response):

        data = json.loads(response.text)
        print(data)

        coupon_code = data['coupon_code']
        discount_percent = data['discount_percent']

        regular_price = data['discounted_products'][0]['original_price']

        if '$' in regular_price:
            currency = 'USD '

        regular_price = float(re.sub('\$|,', '', regular_price))

        discounted_price = data['discounted_products'][0]['formatted_discount']
        discounted_price = float(re.sub('\$|,', '', discounted_price))


        # after using coupon_code only price is discounted
        sale_price = regular_price - discounted_price

        # if discount percentage is required (to be added in dictionary)
        # 'discount_percent': discount_percent

        # 'subscription_type': 'Annual'
        yield {
            'regular_price': regular_price,
            'sale_price': sale_price,
            'coupon_code': coupon_code,
            'currency': currency
        }