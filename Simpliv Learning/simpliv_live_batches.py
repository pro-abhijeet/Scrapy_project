import json
import scrapy
from dateutil.parser import parse
import datetime


class SimplivLearnSp1(scrapy.Spider):
    name = 'svlsp1'
    start_urls = [
        'https://www.simplivlearning.com/virtual-classroom'
    ]
    def parse(self, response):
        for i in range(1,13):
            url = f'https://www.simplivlearning.com/virtual-classroom/?page={i}&expand=courses,+subCategory,category'
            payload = f'page={i}&expand=courses,+subCategory,category'
            header = {
                'referer': 'https://www.simplivlearning.com/virtual-classroom',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'accept': 'application/json, text/plain, */*'
            }
            yield scrapy.Request(url,body=payload,headers=header,callback=self.parser_content)
    def parser_content(self, response):
        print(response)
        data =json.loads(response.body)
        data = data['data']['data']
        currency = 'USD'
        time_zone_id = '62' #Eastern Time
        for i in data:
            link = i['course_url']
            title = i['course_title_en']
            offer_price = str(i['price'])
            regular_price = str(i['increased_price'])
            if offer_price != 'USD 0':
                pricingtype = 'Paid'
            else:
                pricingtype = 'Free'
            if i['batches'] != []:
                batches = []

                batchlist = i['batches'][0]
                for i in batchlist:
                    sdate = i['date']
                    sdate = str(parse(sdate))
                    batch_days= i['days']
                    if "Sat-Sun" in batch_days:
                        batch_type = "1"
                    elif "Mon-Fri" in batch_days:
                        batch_type = "2"
                    else:
                        batch_type = ""
                    start_time= i['start_time'].replace(" ", "")
                    end_time= i['end_time'].replace(" (Eastern Time)", "").replace(" (Eastern Time", "").replace(" (Eastern TIme)", "").replace(" ", "")
                    try:
                        start_time = datetime.datetime.strptime(start_time, "%I:%M%p")   
                        start_time = datetime.datetime.strftime(start_time, "%H:%M")      
                        start_time = start_time + ":00"                
                    except:
                        start_time = datetime.datetime.strptime(start_time, "%I:%M%P")   
                        start_time = datetime.datetime.strftime(start_time, "%H:%M")  
                        start_time = start_time + ":00"               
                    try:
                        end_time = datetime.datetime.strptime(end_time, "%I:%M%p")    
                        end_time = datetime.datetime.strftime(end_time, "%H:%M")
                        end_time = end_time + ":00"
                    except:
                        end_time = datetime.datetime.strptime(end_time, "%I:%M%P")    
                        end_time = datetime.datetime.strftime(end_time, "%H:%M") 
                        end_time = end_time + ":00"
                    regular_price= regular_price
                    sale_price = offer_price
                    
                    batches.append(  {
                        'batch_start_date':sdate,
                        #'batch_end_date':edate,
                        'batch_time_zone': {'id': time_zone_id},
                        'batch_type': {'id': batch_type},
                        'batch_start_time': start_time,
                        'batch_end_time': end_time,
                        'pricing_type': pricingtype,
                        'regular_price': regular_price,
                        'sale_price': sale_price
                    }   )
            else:
                batches = ""
            
            yield{
                'course url': link,
                'title': title,
                'regular_price': regular_price,
                'price': offer_price,
                'batch':batches
            }