import scrapy
from datetime import datetime

class CareerSpider(scrapy.Spider):
    name = "brainsensei"
    allowed_domains = ['brainsensei.com']
    start_urls = ['https://brainsensei.com']

    def parse(self,response):
        uxls = response.xpath('//div[@class="wpb_wrapper"]/a[@class="nectar-button jumbo regular accent-color  regular-button"]//@href').getall()
        for i in uxls:
            if i.endswith('live-virtual-instructor/'):
                yield scrapy.Request(i,callback= self.parse_virtual)
            yield scrapy.Request(i, callback=self.parse_url)

    def parse_virtual(self,response):
        title = response.xpath('//div[@class="summary entry-summary"]/h1/text()').get()
        
        # #Formatted Dates
        dates  = response.xpath('//div[@class="simple-col simple-data-date"]/text()').getall() #2022-11-26
        batch_date = []
        for date in dates:
            now = date.replace(",","").strip()
            now = datetime.strptime(f'{now}','%A %B %d %Y').strftime('%d/%m/%Y')
            batch_date.append(now)
        
        #Formatted Timings
        timing_xpath = response.xpath('//div[@class="simple-col simple-data-time"]/text()[1]').getall()
        timings = []
        for time in timing_xpath:
            start_time = datetime.strptime(time.split('to')[0].strip(),'%I:%M%p').strftime("%H:%M %p")
            end_time = datetime.strptime(time.split('to')[1].strip(),'%I:%M%p').strftime("%H:%M %p")
            timings.append(f"{start_time} to {end_time}")
        
        #Formatted Price
        prices = []
        count_y = 1
        for i in range(1,len(batch_date)+1):
            try:
                x = response.xpath(f'(//div[@class="simple-row simple-row-content"]//div[@class="simple-col"][2])[{i}]/text()').get()
                if x != None: # better: if item is not None
                    prices.append(x)
                else:        
                    raise TypeError 
            except TypeError:
                y = response.xpath(f'(//div[@class="simple-row simple-row-content"]//div[@class="simple-price-big"])[{count_y}]/text()').get()
                prices.append(y)
                count_y+=1

        #additional_batches
        additional_batches = list()
        for batch, time, price in zip(batch_date, timings, prices):
            additional_batches.append(  {
                'batch_start_date':{batch},
                'batch_time_zone': {time},
                'batch_price':{price}
            }   )

        yield{
            'title':title,
            'additional_batches' : additional_batches
        }

    def parse_url(self,response):
        title = response.xpath('//div[@class="summary entry-summary"]/h1/text()').get()
        currency = response.xpath('//p[@class="price nectar-inherit-default"]//bdi/span/text()').get()
        monthly_price = response.xpath('//div[@class="main-head"]/p[@class="enroll-price-p"]/span/text()').get()

        #yearly regular price
        yearly_price = response.xpath('//span[@class="woocommerce-Price-amount amount"]/bdi/text()').extract_first()
        if yearly_price==None:
            yearly_price="Na"
        else:
            yearly_regular_price = yearly_price.replace('\xa0USD', '')

        #yearly sale price
        yearly_sale_price = response.xpath('//div[@class="main-head"]//span[@class="enroll-price"]/text()').getall()
        if yearly_sale_price==None:
            yearly_sale_price = yearly_regular_price
        for price in yearly_sale_price:
            if price==monthly_price:
                continue
            yearly_sale_price = price

        yield{
            'title':title,
            'currency':currency,
            'monthly_price':monthly_price,
            'yearly_regular_price':yearly_regular_price,
            'yearly_sale_price':yearly_sale_price
        }

