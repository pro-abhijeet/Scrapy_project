import scrapy
import json
from dateutil.parser import parse
import datetime
import re

class PMA(scrapy.Spider):
    name = 'pma'
    start_urls = [
        'https://projectmanagementacademy.net/training-courses'
    ]
    def parse(self, response):
        for ele in response.xpath("//div[@class='col-12 col-lg-5 card px-0 mb-5 bg-muted']//p[@class='font-weight-bold font-s']"):
            link = ele.xpath("./a/@href").get()
            if ('www.') not in link:
                link = "https://projectmanagementacademy.net" + link
            title = ele.xpath("./a/text()").getall()
            title = " ".join(title)
            yield scrapy.Request(link, callback=self.parser_content, cb_kwargs={'title':title})
    def parser_content(self,response, title):
        link = response.request.url
        if response.xpath("//div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through']/text() | //div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through text-muted']/text()"):
            offer_price = response.xpath("//div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through']/text() | //div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through text-muted']/text()").get()
        else:
            offer_price = response.xpath("//div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']/text() | //div[@class='scheduleCard card my-2 onlineColor']//div[@class='text-right']/text()").get()
        if offer_price is not None:
            offer_price = offer_price.strip()
            if "$" in offer_price:
                currency = 'USD'
            offer_price = offer_price.replace('$', '').replace(' USD', '')
        else:
            offer_price = ""
            currency = ""
        regular_price = response.xpath("//div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through text-muted']/following-sibling::text() | //div[@class='d-lg-none col-6 my-auto text-right']//div[@class='my-1']//*[@class='line-through']/../../div[2]/text()").get()
        if regular_price is None:
            regular_price = offer_price
        else:
            regular_price = regular_price.replace("$", "").replace(" USD", "")
        
        if response.xpath("//*[contains(text(), 'Online - India (IST)')]"):
            Batches = []
            for i in response.xpath("//div[@class='card bg-muted my-3 p-2'][1]//script[@type='application/ld+json']"):
                batch_time = i.xpath("./preceding-sibling::div[@class='scheduleCard card my-2 virtualBorder'][1]//div[@class='col-6 pt-1']/div[2]/text()").get()
                start_time , end_time= batch_time.split("-")
                start_time = datetime.datetime.strptime(start_time, "%I:%M%p")
                start_time = datetime.datetime.strftime(start_time, "%H:%M")
                end_time = datetime.datetime.strptime(end_time, "%I:%M%p")
                end_time = datetime.datetime.strftime(end_time, "%H:%M")
                data = i.xpath("./text()").get()
                data = json.loads(data)
                start_date = data['startDate']
                end_date = data['endDate']
                offer_price = data['offers']['price']
                regular_price = i.xpath("./..//div[@class='scheduleCard card my-2 virtualBorder']//span[@class='line-through text-muted text-nowrap']/text()").get()
                regular_price = regular_price.replace("$", "").replace(" USD", "")
                currency = data['offers']['priceCurrency']
                instructor_based_offer_price = offer_price
                instructor_based_offer_price = instructor_based_offer_price.replace("$", "").replace(" USD", "")
                instructor_based_regular_price = regular_price
                instructor_based_regular_price = instructor_based_regular_price.replace("$", "").replace(" USD", "")
                Batches.append(  {
                        'batch_start_date':start_date,
                        'batch_end_date':end_date,
                        #'batch_time_zone': {'id': time_zone_id},
                        #'batch_type': {'id': batch_type},
                        'batch_start_time': start_time,
                        'batch_end_time': end_time,
                        'currency': currency,
                        'regular_price': regular_price,
                        'offer_price': offer_price
                    }   )
            
            
        else:
            Batches = ''
            instructor_based_regular_price = response.xpath("//span[@class='line-through text-muted text-nowrap']/text() | //span[@class='line-through text-muted']/text()").get()
            if instructor_based_regular_price is not None:
                instructor_based_regular_price = instructor_based_regular_price.replace("$", "").replace(" USD", "")
            else:
                instructor_based_regular_price = ""
            instructor_based_offer_price = response.xpath("//span[@class='text-nowrap']/text() | //span[@class='line-through text-muted']/../text()[2]").get()
            if instructor_based_offer_price is not None:
                instructor_based_offer_price = re.sub(r'\r\n', '', instructor_based_offer_price)
                instructor_based_offer_price = re.sub(r'\t', '', instructor_based_offer_price)
                instructor_based_offer_price = instructor_based_offer_price.replace("$", "").replace(" USD", "")
            else:
                instructor_based_offer_price = ""
        yield{
            'Title': title,
            'Link': link,
            'Batches': Batches,
            #'Instructor Based Regular Price': instructor_based_regular_price,
            #'Instructor Based Offer PRice': instructor_based_offer_price,
            'Currency': currency,
            'Regular Price':regular_price,
            'Offer Price': offer_price
        }