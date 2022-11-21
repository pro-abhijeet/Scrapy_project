import dateutil.parser as parser
import scrapy
import re


class EmiritusSpider(scrapy.Spider):
    name = "emeritus"

    start_urls = [
        "https://emeritus.org/explore-topics/"
    ]

    def parse(self, response):

        all_links = response.xpath("//*[@class='thb-portfolio-link']/@href").extract()
        #print(len(all_links))
        for links in all_links:
            links = links.replace("courses/", "online-")
            links = re.sub("\/$", "-courses/", links)
            yield scrapy.Request(links, callback=self.parse_links)

    def parse_links(self, response):

        all_course_links = response.xpath("//*[@class='row']//*[@class='small-12 medium-6 large-4  columns']//*[contains(@href,'https:')]//@href").extract()

        for links in all_course_links:
            links = re.sub("\?.*", "", links)
            yield scrapy.Request(links, callback=self.parse_course)

    def parse_course(self, response):
        try:
            # Extracting price by eliminating the empty strings from the list ['', 'US$2,423', '']-->['US$2,423']
            price_list = list(filter(lambda x: x != '', [i.strip() for i in response.xpath('//p[@class="box__price paragraph--large strong margin-bottom-small ignore-screenshot"]/text()').extract()]))
            # Extracting the price
            price_list_num = [i for i in re.findall(r'\d+', price_list[0])]
            display_price = "".join(price_list_num)

            currency = price_list[0].split(price_list_num[0])[0]

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