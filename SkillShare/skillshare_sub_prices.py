import scrapy
import re


class MyprojectSpider(scrapy.Spider):

    name = "skillshare" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.skillshare.com/api/graphql'

        yield scrapy.Request(url=link, method="POST", headers={'content-type': "application/json; charset=utf-8"}, callback=self.parse)

    def parse(self, response):

        print(response.text)