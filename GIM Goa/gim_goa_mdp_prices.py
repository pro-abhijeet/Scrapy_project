import scrapy
import re

class gimscrapy(scrapy.Spider):
    name = "gim"
    start_urls = [
        "https://gim.ac.in/programmes/mdp"
    ]

    def parse(self, response):
        dates = response.xpath('//div[@class="date"]/text()').extract()
        del dates[2]
        links = response.xpath('//div[@class="body-section"]//a[@class="gim-btn-primary"]/@href').getall()
        del links[2]
        del links[3]
        brochure_pdfs = response.xpath('//a[@class="gim-btn-secondary"]/@href').getall()[:-3]


        for i in range(len(links)):
            yield scrapy.Request(links[i], callback=self.parser_contents, cb_kwargs={"date":dates[i], "link":links[i], "brochure_pdfs":brochure_pdfs[i]})

    def parser_contents(self, response, date, link, brochure_pdfs):

        title = response.xpath('//div[@class="banner-text"]//h1/text()').extract_first()

        display_price = response.xpath('//span[@class="fee-price"]/text()').extract_first()
        print(display_price)
        # display_price = Price.fromstring(display_prices).amount_float

        currency = response.xpath('//span[@class="fee-price"]/text()').extract_first().split()[0]

        yield {
            "link": link,
            "date": date,
            "title": title,
            "display_price": display_price,
            "currency": currency,
            "brochure_pdfs": brochure_pdfs
        }