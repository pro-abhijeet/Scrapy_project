from datetime import datetime
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "fore" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.fsm.ac.in/enhancing-assertiveness-and-positive-attitude'

        yield scrapy.Request(url=link, callback=self.parse)