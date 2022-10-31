from locale import currency
import scrapy
import re



class MyprojectSpider(scrapy.Spider):

    name = "govmlab" 
    # download_delay = 3

    def start_requests(self):

        link = 'https://www.govmlab.com/course/vmware-vsphere-install-configure-and-manage-v65'

        yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        regular_price = response.xpath("//div[@class='program_fees']/p[1]/span/text()").extract_first()

        if "INR" in regular_price:
            currency = 'INR'

        regular_price = re.findall('\d+|\d+,\d+', regular_price)[0]


        sale_price = response.xpath("//div[@class='program_fees']/p[1]/text()").extract_first()
        sale_price = re.findall('\d+|\d+,\d+', sale_price)[0]


        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }

