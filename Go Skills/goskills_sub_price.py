from datetime import datetime
import scrapy
import re

class gimscrapy(scrapy.Spider):
    name = "gim"
    start_urls = [
        "https://gim.ac.in/programmes/mdp"
    ]

    def parse(self, response):

        dates = response.xpath('//div[@class="date"]/text()').extract()

        links = response.xpath('//div[@class="body-section"]//a[@class="gim-btn-primary"]/@href').getall()
       
        brochure_pdfs = response.xpath('//a[@class="gim-btn-secondary"]/@href').getall()


        for i in range(len(links)):
            yield scrapy.Request(links[i], callback=self.parser_contents, cb_kwargs={"date":dates[i], "link":links[i], "brochure_pdfs":brochure_pdfs[i]})

    def parser_contents(self, response, date, link, brochure_pdfs):

        title = response.xpath('//div[@class="banner-text"]//h1/text()').extract_first()

        regular_price = response.xpath('//span[@class="fee-price"]/text() | //th[text()="Programme Fee:"]//following::td/text()').extract_first()
        print(regular_price)
        currency = re.findall('[A-Z]+', regular_price)[0]

        regular_price = re.sub('[A-Z]+', '', regular_price)
        regular_price = float(regular_price)


        year = re.findall("\d\d\d\d", date)[0]

        date = re.sub('st|th|nd|rd', '', date)
        dates = date.split('–')

        end_date = dates[1].strip()
        start_date = dates[0].strip()

        try:
            month = re.findall('[A-z][a-z]+', start_date)[0]
        except:
            month = re.findall('[A-z][a-z]+', end_date)[0]

        start_date = f"{month} "+start_date+f",{year}"

        try:
            start_date = datetime.strptime(start_date, '%b %d,%Y')
            start_date = start_date.strftime('%Y-%m-%dT00:00:00.000Z')
        except:
            start_date = ''
        
        try:
            end_date = datetime.strptime(end_date, '%d %b %Y')
            end_date = end_date.strftime('%Y-%m-%dT00:00:00.000Z')
        except:
            end_date = ''


        sale_price = regular_price

        yield {
            "link": link,
            "batch_start_date": start_date,
            "batch_end_date": end_date,
            "regular_price": regular_price,
            "price": sale_price,
            "currency": currency,
        }