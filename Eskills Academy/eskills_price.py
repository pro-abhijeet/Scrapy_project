import scrapy 
import json
import re 

class EskillsSpider(scrapy.Spider):
    name = 'eskills' 
    def start_requests(self):
        url = "https://eskills.academy/courses?page={}"
        for i in range(1,3):
            yield scrapy.Request(url.format(i))


    def parse(self, response):

        for i in response.xpath("//div[@class='col-xs-12 col-sm-6 col-md-4']"):
            
            link = "https://eskills.academy"+ i.css("::attr(href)").get()
            

            yield scrapy.Request(url=link, callback=self.coursepage)

    def coursepage(self, response):

        link = response.xpath("//div[@class='banner__button-wrapper']/a/@href").get()

        if 'product_id' in link:
            productid = re.findall('=(.*)', link)[0]
            productname = response.url.split('/')[4]

            schoolid = response.xpath('//div/@data-ss-school-id').get()

            link = f"https://sso.teachable.com/secure/{schoolid}/checkout/{productid}/{productname}"


            yield scrapy.Request(url=link, callback=self.different_format)

        else:

            coupon_code = ''
            if "coupon_code" in link:
                coupon_code = re.findall("=(.*)", link)[0]
                link = re.sub('\?.*', '', link)

            if coupon_code == '':
                link = link+'.json'
            else:
                link = link + f'.json?coupon_code={coupon_code}'


            yield scrapy.Request(url=link, callback=self.prices)


    def different_format(self, response):

        link = response.xpath("//div[@class='view-school']/div/@data-checkout").get()

        link = link.replace('#', '')

        coupon_code = ''
        if "coupon_code" in link:
            coupon_code = re.findall("=(.*)", link)[0]
            link = re.sub('\?.*', '', link)

        if coupon_code == '':
            link = link+'.json'
        else:
            link = link + f'.json?coupon_code={coupon_code}'

        yield scrapy.Request(url=link, callback=self.prices)

    def prices(self, response):

        data = json.loads(response.text)

        data = data['order']

        regular_price = data['cart']['product']['price']

        if '$' in regular_price:
            regular_price = re.sub('\$|,', '', regular_price)
            regular_price = float(regular_price)


        tax_amount = data['cart']['tax']['price']
        tax_amount = tax_amount.replace('+','')

        if '$' in tax_amount:
            tax_amount = re.sub('\$|,', '', tax_amount)
            tax_amount = float(tax_amount)


        sale_price = data['cart']['total']['price']

        if '$' in sale_price:
            sale_price = re.sub('\$|,', '', sale_price)
            sale_price = float(sale_price)


        if sale_price > regular_price:
            sale_price = regular_price

        coupon_code = ''

        currency = data['currency']
        coupon_code = data['coupon_code']
        country_code = data['country_code']


        course_url = data['url']

        yield {
                'course_url': course_url, 
                'regular_price': regular_price, 
                'price': sale_price,
                'coupon_code': coupon_code,
                'currency': currency,
                'country_code': country_code
            }

        



            
