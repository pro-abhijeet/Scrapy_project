import scrapy
import requests
import re
from bs4 import BeautifulSoup
import dateutil.parser as parser
from datetime import datetime


class emeritusscrapy(scrapy.Spider):
    name = "emeritus"
    start_urls = [
        "https://emeritus.org/explore-topics/"
    ]

    def parse(self, response):

        domain_links = response.xpath('//div[@class="portfolio-holder"]//a/@href').extract()

        for i in range(len(domain_links)):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                "Connection": "close", "Upgrade-Insecure-Requests": "1"
            }
            response = requests.get(domain_links[i], headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            domain_sp_links = [i["href"] for i in soup.find_all("a", class_="nohover", href=True)]

            try:
                for j in range(len(domain_sp_links)):
                    yield scrapy.Request(domain_sp_links[j], callback=self.courses)
            except:
                pass

    def courses(self, response):

        try:
            display_price = "".join([i for i in re.findall(r'\d+' ,list(filter(lambda x: x != '', [i.strip() for i in response.xpath('//p[@class="box__price paragraph--large strong margin-bottom-small ignore-screenshot"]/text()').extract()]))[0])])
            k = [i for i in re.findall(r'\d+' ,list(filter(lambda x: x != '', [i.strip() for i in response.xpath('//p[@class="box__price paragraph--large strong margin-bottom-small ignore-screenshot"]/text()').extract()]))[0])]
            currency = list(filter(lambda x: x != '', [i.strip() for i in response.xpath('//p[@class="box__price paragraph--large strong margin-bottom-small ignore-screenshot"]/text()').extract()]))[0].split(k[0])[0]
        except:
            display_price = ""
            currency = ""

        try:
            start_date = "".join([i.strip() for i in response.xpath('//p[@class="box__deadline paragraph--large strong ignore-screenshot"]//span/text() | //div[@class="row programme-features-row"]//span[@class="main-text"]/text() | //p[@class="box__deadline paragraph--large strong ignore-screenshot"]/text()').extract_first()])
            start_date = parser.parse(start_date).isoformat()
        except:
            start_date = ""

        yield {
            "link": response,
            "start_date": start_date,
            "display_price": display_price,
            "currency": currency
        }