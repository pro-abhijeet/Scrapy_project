from datetime import datetime
import scrapy
import re

class MyprojectSpider(scrapy.Spider):

    name = "pma" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://projectmanagementacademy.net/pmp-certification'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        for batch in response.xpath("//div[@class='scheduleCard card my-2 virtualBorder']"):

            dates = batch.xpath(".//div[@class='col-6 pt-1']/div[1]/text()").extract_first()
            timing = batch.xpath(".//div[@class='col-6 pt-1']/div[2]/text()").extract_first()

            regular_price = batch.xpath(".//div[@class='d-none d-lg-block col-12 text-right']/span[1]/text()").extract_first()
            sale_price = batch.xpath(".//div[@class='d-none d-lg-block col-12 text-right']/span[1]/text()").extract_first()

            print(dates)
            print(timing)
            print(regular_price)
            print(sale_price)
