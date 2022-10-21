from datetime import datetime
from subprocess import call
from bs4 import BeautifulSoup
import scrapy
import json
import re
import time
import ast

class MyprojectSpider(scrapy.Spider):

    name = "hh" 
    # download_delay = 3

    def start_requests(self):

            link = 'https://www.henryharvin.com/our-courses'

            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        # print(len(response.xpath('//li[@id="wp-megamenu-item-7692"]//a').extract()))
          
        for link in response.xpath('//li[@id="wp-megamenu-item-7692"]//a'):
            url = link.xpath('./@href').extract_first()
            if 'tefl' in url:
                continue


            if 'https' not in  url:

                url = 'https://www.henryharvin.com/schedule/' + url

            
            yield scrapy.Request(url=url, callback=self.batchdetails)

    
    def batchdetails(self, response):

        # title = response.xpath('//h1/text()').extract_first()
        details = response.xpath("//script[@src='/js/axios.js']/following-sibling::script/text()").extract()
        details = str(details)

        # print(details)
        schedules = re.findall('"data":\[(.*?)\]', details)
        # print(schedules)

        regular_price = ''
        sale_price = ''
        regular_price_usd = ''
        add_regular_price = ''
        add_regular_price_usd = ''
        add_sale_price = ''
        batch_start_date = ''
        batch_end_date = ''
        batch_start_time = ''
        batch_end_time = ''
        pricing_type = ''
        batch_type = ''

        price_type = list()
        btype = list()
        add_regprice = list()
        add_regprice_usd = list()
        add_sprice = list()
        batch_sdate = list()
        batch_edate = list()
        batch_stime = list()
        batch_etime = list()
        

        for batch in schedules:

            batch = ast.literal_eval(batch)



            if type(batch) == tuple:
                
                for item in batch:

                    if item['batch_timing'] == 'Timing': 
                        regular_price = item['batch_price']
                        regular_price_usd = item['batch_price_option']
                        continue

                    add_regular_price = item['batch_price']
                    add_regprice.append(str(add_regular_price))

                    add_regular_price_usd = item['batch_price_option']
                    add_regprice_usd.append(str(add_regular_price_usd))

                    add_sale_price = add_regular_price
                    add_sprice.append(str(add_sale_price))


                    if int(regular_price) <= 0 or regular_price == '':
                        pricing_type = ''
                    else:
                        pricing_type = 'Paid'

                    price_type.append(pricing_type)


                    batch_start_date = item['batchDate']
                    batch_start_date = datetime.strptime(batch_start_date, '%d %B %Y')
                    batch_type_check = batch_start_date
                    batch_start_date = batch_start_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    batch_sdate.append(batch_start_date)


                    weeknum = batch_type_check.weekday()
                    if weeknum >= 0 and weeknum <= 4:
                        batch_type = 'Weekday (Mon - Fri)'
                        btype.append(batch_type)
                    elif weeknum == 5 or weeknum == 6:
                        batch_type = 'Weekend (Sat - Sun)'
                        btype.append(batch_type)


                    batch_end_date = item['batchEndDate']
                    batch_end_date = datetime.strptime(batch_end_date, '%Y-%m-%d')
                    batch_end_date = batch_end_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    batch_edate.append(batch_end_date)



                    timings = item['batch_timing']
                    timings = timings.split('-')

                    try:
                        batch_start_time = timings[0]
                        batch_start_time = datetime.strptime(batch_start_time, "%I:%M%p")
                        batch_start_time = datetime.strftime(batch_start_time, "%H:%M")
                        batch_start_time = batch_start_time+":00"
                    except:
                        batch_start_time = ''
                    batch_stime.append(batch_start_time)
                    

                    try:
                        batch_end_time = timings[1]
                        batch_end_time = datetime.strptime(batch_end_time, "%I:%M%p")
                        batch_end_time = datetime.strftime(batch_end_time, "%H:%M")
                        batch_end_time = batch_end_time+":00"
                    except:
                        batch_end_time = ''
                    batch_etime.append(batch_end_time)

            else:

                regular_price = batch['batch_price']
                regular_price_usd = batch['batch_price_option']



        sale_price = regular_price


        batch_start_date = '|'.join(batch_sdate)
        batch_end_date = '|'.join(batch_edate)
        batch_start_time = '|'.join(batch_stime)
        batch_end_time = '|'.join(batch_etime)
        pricing_type = '|'.join(price_type)
        add_regular_price = '|'.join(add_regprice)
        batch_type = '|'.join(btype)
        add_sale_price = '|'.join(add_sprice)

        add_regular_price_usd = '|'.join(add_regprice_usd)

        # print({'regprice': regular_price, 'saleprice': sale_price, 'regusd': regular_price_usd, 'bsdate': batch_start_date,
        # 'bedate': batch_end_date, 'bstime': batch_start_time, 'betime': batch_end_time, 'ptype': pricing_type, 'addreg': add_regular_price,
        # 'addsale': add_sale_price, 'btype': batch_type})

        yield {'regular_price': regular_price, 'sale_price': sale_price, 'regular_price_usd': regular_price_usd,
        'batch_start_date': batch_start_date, 'batch_end_date': batch_end_date, 'batch_start_time': batch_end_time,
        'pricing_type': pricing_type, 'additional_batch_regular_price': add_regular_price, 'batch_type': batch_type, 
        'additional_batch_sale_price': add_sale_price}