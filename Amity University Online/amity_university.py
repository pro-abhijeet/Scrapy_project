from datetime import datetime
import scrapy
import json
import re


class MyprojectSpider(scrapy.Spider):

    name = "amity_prices" 
    # download_delay = 1

    def start_requests(self):

        link = 'https://amityonline.com/'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        links = [
        'https://amityonline.com/master-of-business-administration-online',
        'https://amityonline.com/master-of-commerce-financial-management-online',
        'https://amityonline.com/master-of-arts-journalism-and-mass-communication-online',
        'https://amityonline.com/bachelor-of-arts-journalism-and-mass-communication-online',
        'https://amityonline.com/bachelor-of-arts-online',
        'https://amityonline.com/bachelor-of-computer-applications-online',
        'https://amityonline.com/master-of-computer-applications-online',
        'https://amityonline.com/bachelor-of-business-administration-online']

        links_id = {
        'https://amityonline.com/master-of-business-administration-online': '440',
        'https://amityonline.com/master-of-commerce-financial-management-online': '245',
        'https://amityonline.com/master-of-arts-journalism-and-mass-communication-online': '246',
        'https://amityonline.com/bachelor-of-arts-journalism-and-mass-communication-online': '242',
        'https://amityonline.com/bachelor-of-arts-online': '244',
        'https://amityonline.com/bachelor-of-computer-applications-online': '241',
        'https://amityonline.com/master-of-computer-applications-online': '515',
        'https://amityonline.com/bachelor-of-business-administration-online': '240'
        }


        
        # fetching links  --------

        data = response.xpath('//script[@type="text/javascript"]/text()').extract()
        data = re.sub('\n+','',data[4])
        data = re.findall('if \(val\.ID == "\d+"\) \{.*?\}', data)


        for i in data:

            urls_fetched = re.findall('href="(.*?)"', i)

            for link in urls_fetched:

                if 'val.ID' in link: continue

                links.append(link)

        #  ------------- fetched links (above code)

        for link in links:

            if link in links_id:

                val_id = links_id[link]
                
                url = f'https://amityonline.com/Home/GetProgramDetails?ProgramId={val_id}&Categoryid=0&Sessionid=0&CurrencyType=53'

                payload = f"ProgramId={val_id}&Categoryid=0&Sessionid=0&CurrencyType=53"

                yield scrapy.Request(url=url, callback=self.prices_payload, method="POST", body=payload, cb_kwargs={'link': link})



            
            yield scrapy.Request(url=link, callback=self.prices)



    def prices(self, response):


        try:
            regular_price = response.xpath('//h2[@id="pfees"]/following::h3[1]/text() | //div[@id="dvFeesContainerINR"]//div[@id="dvOneTimeG"]//span[@class=""]//text() | //div[@id="dvFeesContainerINR"]//div[@id="dvOneTimeG-one"]//span[@class=""]//text()').get()
        except:
            regular_price = ''
            
        regular_price_usd = response.xpath('//div[@id="dvSemTotal"]//span[@class="fa fa-usd"]/following-sibling::span/text()').get()
        regular_price = regular_price.strip()

        regular_price = re.sub('[^0-9]', '', regular_price)
        regular_price = float(regular_price)
        
        try:
            regular_price_usd = re.sub('[^0-9]', '',  regular_price_usd)
            regular_price_usd = float(regular_price_usd)
            currency_usd = ''
        except:
            regular_price_usd = ''

        currency = 'INR'

        sale_price = regular_price

        sale_price_usd = regular_price_usd

        yield {
            'course_url': response.url,
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }


    def prices_payload(self, response, link):

        data = response.text

        regular_price = re.findall('FeeStructureJson":.*?,', data)[0]
        regular_price = re.sub('[^0-9]', '', regular_price)

        currency = 'INR'

        try:
            regular_price_usd = re.findall('FeeStructureJsonUSD":.*?(fAmount.*?),', data)[0]
            currency_usd = 'USD'
            regular_price_usd = re.sub('[^0-9]', '', regular_price_usd)
        except:
            regular_price_usd = ''
        
        sale_price_usd = regular_price_usd
        sale_price = regular_price

        


        yield {
            'course_url': link,
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }
        