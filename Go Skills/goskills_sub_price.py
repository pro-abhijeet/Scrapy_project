from datetime import datetime
from locale import currency
import scrapy



class MyprojectSpider(scrapy.Spider):

    name = "goskills" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.goskills.com/Bundle/Unlimited/Pricing'

        yield scrapy.Request(url=link, callback=self.subscription)



    def subscription(self, response):

        annual_price_per_month = response.xpath("//span[@class='price annual']/span[@class='before-decimal-point']/text()").extract_first()
        annual_currency = response.xpath("//span[@class='price annual']/span[@class='currency-symbol']/text()").extract_first()

        monthly_price = response.xpath("//span[@class='price monthly']/span[@class='before-decimal-point']/text()").extract_first()
        monthly_currency = response.xpath("//span[@class='price monthly']/span[@class='currency-symbol']/text()").extract_first()


        free_trial_price = response.xpath("//span[@class='price']/span[@class='before-decimal-point']/text()").extract_first()
        free_trial_text = response.xpath("//span[@class='price']/following-sibling::span[@class='h5 d-block m-top-sm']/text()").extract_first()

        course_page = "https://www.goskills.com/Courses"
        
        yield scrapy.Request(url=course_page, callback=self.courses, cb_kwargs={'monthly': monthly_price, 'yearly': annual_price_per_month, 'monthly_currency': monthly_currency, "annual_currency": annual_currency, 'free_trial_price': free_trial_price})

    def courses(self, response, monthly, yearly, monthly_currency, annual_currency, free_trial_price):

        prefix = "https://www.goskills.com"

        for url in response.xpath("//a[@class='bag-card-link wrapping-link']"):

            link = url.xpath("./@href").extract_first()
            course_url = prefix + link

            yearly_total = float(yearly)*12

            yield {
                    "course": {
                        "url": course_url,
                        "regular_price": "",
                        "sale_price": "",
                        "subscription": {
                            "Free Trial": {
                                "price_details": {
                                    "currency": monthly_currency,
                                    "type": "Free",
                                    "regular_price_monthly": free_trial_price,
                                    "sale_price_monthly": free_trial_price
                                    }
                            },
                            "Annual Plan": {
                                "price_details": {
                                    "currency": annual_currency,
                                    "type": "Self Study",
                                    "regular_price_monthly": yearly,
                                    "sale_price_monthly": yearly,
                                    "total_price": yearly_total,
                                    "coupon": ""
                                    },
                                    "price_details": {
                                    "currency": annual_currency,
                                    "type": "Immersion",
                                    "regular_price_monthly": yearly,
                                    "sale_price_monthly": yearly,
                                    "total_price": yearly_total,
                                    "coupon": ""
                                    }
                            },
                            "Monthly PLan": {
                                "price_details": {
                                    "currency": monthly_currency,
                                    "type": "",
                                    "regular_price_monthly": monthly,
                                    "sale_price_monthly": monthly,
                                    "coupon": ""
                                    }
                            }
                        }
                    }
                }