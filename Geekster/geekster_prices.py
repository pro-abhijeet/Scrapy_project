import scrapy
import requests
from scrapy.selector import Selector
import re
import json

class Geekster1(scrapy.Spider):
    name = 'geekster_prices'
    start_urls = ['https://geekster.in/full-stack-web-development-program','https://geekster.in/codeschool']


    def parse(self, response):

        link = response.request.url
        a = requests.get(link)
        body = a.text
        response = Selector(text=body)

        if link=='https://geekster.in/full-stack-web-development-program':
            
            price_data_url = 'https://geekster.in/_next/static/chunks/326.6c7b6e970c2b4fe2.js'
            price_data = requests.get(price_data_url).text

            regular_price = re.findall(r'\d+,\d+ | \d+,\d+', price_data)[3]
            sale_price = regular_price

            emi_price = re.findall(r'\d+,\d+ | \d+,\d+', price_data)[4]

            currency = 'INR'
            
            yield {
            
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
            }

        if link == 'https://geekster.in/codeschool':

            src_file = response.xpath("//script[10]/@src").get()
            src_file = 'https://geekster.in' + str(src_file)

            data = requests.get(src_file).text
            
            data1 = re.search("s}}\);var\Wn=(.*?),s=\[", data).group(1)
            data1 = data1.replace('title', '"title"').replace('listTitle', '"listTitle"').replace('content', '"content"').replace('shortDesc', '"shortDesc"').replace('primaryBackground', '"primaryBackground"').replace('secondaryBackground', '"secondaryBackground"').replace('highLights', '"highLights"').replace('moduleNo', '"moduleNo"').replace('offerName', '"offerName"').replace('oldFee', '"oldFee"').replace('newFee', '"newFee"')
            
            # formatting string so it becomes a valid json
            data1 = re.sub(r'\bimage\b', '"image"', data1)
            data1 = re.sub(r'\bdesc\b', '"desc"', data1)
            data1 = re.sub(r'\bdes\b', '"des"', data1)
            data1 = re.sub(r'\bduration\b', '"duration"', data1)
            data1 = re.sub(r'\bpanel\b', '"panel"', data1)
            data1 = re.sub(r'topics:', '"topics":', data1)
            data1 = re.sub(r'\"highLights\":\[,', '\"highLights\":[', data1)

            data1 = json.loads(data1)

            for list in data1:
                
                regular_price = list[5]['content']['oldFee']
                sale_price = list[5]['content']['newFee']

                currency = 'INR'

                yield{
                    
                    'regular_price': regular_price,
                    'price': sale_price,
                    'currency': currency
                }