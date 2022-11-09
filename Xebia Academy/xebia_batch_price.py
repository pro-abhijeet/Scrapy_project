from bs4 import BeautifulSoup
import datetime
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "xebia" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.xebiaacademyglobal.com/sitemap'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        courseurls = response.xpath("//ul[@class='course-map-menu']//li/a/@href").extract()
        
        for link in courseurls:

            yield scrapy.Request(url=link, callback=self.batches)

    def batches(self, response):

        data = BeautifulSoup(response.text, "html.parser")

        batches = data.find_all("div", class_="course-schedule")
        additional_batches = list()


        for i in batches:

            batchsize = ""

            # batch details
            details = i.ul
            details = details.find_all('li')

            # batch start date and end date
            dates = details[0].text.strip()
            year = re.findall("\s\d\d\d\d", dates)[0]
            dates = re.findall("\w+\s\d+", dates)
            stdate = dates[0]+f",{year}"
            edate = dates[1]+f",{year}"
            
            stdate = datetime.datetime.strptime(stdate, '%b %d, %Y')
            stdate = stdate.strftime('%Y-%m-%dT00:00:00.000Z')
            edate = datetime.datetime.strptime(edate, '%b %d, %Y')
            edate = edate.strftime('%Y-%m-%dT00:00:00.000Z')

            # kpis with no details present 
            enrollstdate = ""
            # batchlist.append(enrollstdate)
            enrolledate = ""
            # batchlist.append(enrolledate)
            totalduration = ""
            # batchlist.append(totalduration)
            totaldurunit = ""
            # batchlist.append(totaldurunit)

            # free or paid and pricing
            paidimg = "https://www.xebiaacademyglobal.com/assets/frontend/images/price-icon.svg"
            if details[4].img["src"] == paidimg:
                pricingtype = "Paid"
                price = details[4].text.strip()
                price = re.findall("\d+", price)
                regular_price = price[0]
                sale_price = price[1]
            else:
                pricingtype = "Free"

            btype = details[0].text.strip().split(',')[1].strip()
            if btype.lower() == "weekend":
                # bat = "Weekend (Sat - Sun)"
                batch_type = "1"
            elif btype.lower() == "weekday":
                # bat = "Weekday (Mon - Fri)"
                batch_type = "2"

            btimezone = "Indian Standard Time"
            # currently taking only IST batch hence hardcoding Timezone ID
            time_zone_id = "90"

            btimings = details[1].text.strip().split('-')
            start_time = btimings[0]
            start_time = start_time.strip()
            start_time = re.sub("\s\[.*\]", "", start_time)
            start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
            start_time = datetime.datetime.strftime(start_time, "%H:%M")
            start_time = start_time+":00"

            end_time = btimings[1]
            end_time = end_time.strip()
            end_time = re.sub("\s\[.*\]", "", end_time)
            end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
            end_time = datetime.datetime.strftime(end_time, "%H:%M")
            end_time = end_time+":00"


            additional_batches.append(  {
                        'batch_start_date':stdate,
                        'batch_end_date':edate,
                        'batch_time_zone': {'id': time_zone_id},
                        'batch_type': {'id': batch_type},
                        'batch_start_time': start_time,
                        'batch_end_time': end_time,
                        'pricing_type': pricingtype,
                        'regular_price': regular_price,
                        'sale_price': sale_price
                    }   )

        yield {
            "regular_price": regular_price,
            "price": sale_price,
            "additional_batches": additional_batches
            }