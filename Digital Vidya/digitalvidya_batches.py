from datetime import datetime
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "digitalv" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.digitalvidya.com'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        courseurls = response.xpath("//div[@id='university_programs']//h4/a/@href | //div[@id='dp-carouselccourses']//h4/a/@href").extract()
        
        for link in courseurls:

            yield scrapy.Request(url=link, callback=self.batches)

    def batches(self, response):

        batch_date = response.xpath('//table[@style="border-collapse: collapse; width: 100%;"]//tbody//tr//td[1]/text() | //span[text()="Dates"]/following::div[@class="et_pb_blurb_description"][1]/p/text() | //div[@class="lp-element lp-pom-box detailbox"][1]//p[1]/span/text()').extract()
        timings = response.xpath('//table[@style="border-collapse: collapse; width: 100%;"]//tbody//tr//td[2]/text() | //span[text()="Timings"]/following::div[@class="et_pb_blurb_description"][1]/p/text() | //div[@id="discount"]/div[2]/div[2]//div[@class="et_pb_blurb_description"]//p/text()').extract()
        if timings == []:
            timings.append('')
        batch_price = response.xpath('//span[text()="Course Fee"]/following::div[@class="et_pb_blurb_description"][1]/p/text() | //div//h4/span[contains(text(), "INR")]//text() | //h4/span[text()="Course Fee"]//following::div[1]/text() | //h4[text()="Course Fee"]/following::h3[1]').extract()

        additional_batches = list()

        for batch, time, price in zip(batch_date, timings, batch_price):

            if response.url == "https://course.digitalvidya.com/digital-marketing-leadership-program/":
                print(batch, time, price)


            batch = batch.replace("\xa0", '')
            batch = batch.replace("–", '-')

            year = re.findall("\d\d\d\d", batch)[0]
            dates = batch.split('-')
            
            start_date = dates[0].split(',')[0].strip()
            start_date = start_date+f",{year}"
            try:
                end_date = dates[1].split(',')[0].strip()
                end_date = end_date+f",{year}"
            except:
                end_date = ''

            # batch start date and end date
            try:
                try:
                    start_date = datetime.strptime(start_date, '%b %d,%Y')
                    start_date = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
                except:
                    try:
                        start_date = datetime.strptime(start_date, '%B %d,%Y')
                        start_date = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    except:
                        start_date = datetime.strptime(start_date, '%d %b,%Y')
                        start_date = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
            except:
                start_date = ''
            
            try:
                try:
                    end_date = datetime.strptime(end_date, '%b %d,%Y')
                    end_date = end_date.strftime('%Y-%m-%dT00:00:00.000Z')
                except:
                    try:
                        end_date = datetime.strptime(end_date, '%B %d,%Y')
                        end_date = end_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    except:
                        end_date = datetime.strptime(end_date, '%d %b,%Y')
                        end_date = end_date.strftime('%Y-%m-%dT00:00:00.000Z')
            except:
                end_date = ''

            time = time.replace('–', 'to')
            time = time.replace('-', 'to')
            time = time.split('to')


            # Batch (Start Time , Time Zone ID & End Time)

            # batch start time
            try:
                start_time = time[0]
                start_time = start_time.strip()
                start_time = re.sub("\s\[.*\]", "", start_time)
                try:
                    start_time = datetime.strptime(start_time, "%I:%M %p")
                except:
                        start_time = datetime.strptime(start_time, "%I:%M %P")
                start_time = datetime.strftime(start_time, "%H:%M")
                start_time = start_time+":00"
            except:
                start_time = ''

            # batch time zone
            try:
                end_time = time[1]
                time_zone = re.findall('\((.*)\)', end_time)[0]
            except:
                time_zone = 'IST'
            if time_zone == 'IST':
                time_zone_id = '90'

            # batch end time
            try:
                end_time = re.sub('\((.*)\)', '', end_time)
                end_time = end_time.strip()
                end_time = re.sub("\s\[.*\]", "", end_time)
                try:
                    end_time = datetime.strptime(end_time, "%I:%M %p")
                except:
                        end_time = datetime.strptime(end_time, "%I:%M %P")
                end_time = datetime.strftime(end_time, "%H:%M")
                end_time = end_time+":00"
            except:
                end_time = ''

            # print(price)
            regular_price = price.replace('\xa0', '')
            regular_price = re.findall("\d+,\d+", price)[0]
            

            additional_batches.append(  {
                        'batch_start_date':start_date,
                        'batch_end_date':end_date,
                        'batch_time_zone': {'id': time_zone_id},
                        'batch_start_time': start_time,
                        'batch_end_time': end_time
                    }   )

            

            yield {"additional_batches": additional_batches}
