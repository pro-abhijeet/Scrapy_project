import scrapy
import re


class ImsSpyder(scrapy.Spider):
    name = "imsdata"
    allowed_domain = ['https://www.internetmarketingschool.co.in']
    start_urls = ['https://www.internetmarketingschool.co.in/all-courses/']

    def parse(self, response):
        hrefs = response.xpath("//div[@class='elementor-image']/a/@href").extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_page)
        # yield from self.parse_page(self, response)
        
        

    def parse_page(self, response):
        try:
            title = response.xpath("//h2[@class='elementor-heading-title elementor-size-default']/text()").get()
            currency = response.xpath("//p[@class='price']/del/span/bdi/span/text()").get()
            currency = currency.replace('\u20b9', '₹')
            regular_p = response.xpath("//p[@class='price']/del/span/bdi/text()").get()
            sale_p = response.xpath("//p[@class='price']/ins/span/bdi/text()").get()
            
            link = response.request.url

            short_d = response.xpath("(//div[@class='elementor-widget-container'])[4]/p").get()   # some issues here which is tried to solved in except block 
            short_d = re.sub('<[^>]+>', '',short_d)

            duration = response.xpath("(//p[@class='elementor-icon-box-description'])[1]/text()").get().strip()
            batch_date = response.xpath("(//p[@class='elementor-icon-box-description'])[2]/text()").get().strip()
            delivery = response.xpath("(//p[@class='elementor-icon-box-description'])[3]/text()").get().strip()
            tm = response.xpath("(//p[@class='elementor-icon-box-description'])[4]/text()").get().strip()

            about = response.xpath("(//div[@class='elementor-widget-container'])[13]/ul/li").extract()
            about = [re.sub('<[^>]+>', '',i) for i in about]

            skills = response.xpath("//span[@class='elementor-icon-list-text']/text()").extract()

            yield {
                'link': link,
                'Title': title,
                'short_description': short_d,
                'duration': duration,
                'batch_start_date': batch_date,
                'delivery_method': delivery,
                'Time': tm,
                'regular_price': currency + " " + regular_p,
                'sale_price': currency + " " + sale_p,

                'about_the_course': about,
                'skills': skills
                
            }
        except:
            title = response.xpath("//h2[@class='elementor-heading-title elementor-size-default']/text()").get()
            currency = response.xpath("//p[@class='price']/del/span/bdi/span/text()").get()
            currency = currency.replace('\u20b9', '₹')
            regular_p = response.xpath("//p[@class='price']/del/span/bdi/text()").get()
            sale_p = response.xpath("//p[@class='price']/ins/span/bdi/text()").get()
            
            link = response.request.url

            # short_d = response.xpath("(//div[@class='elementor-widget-container'])[4]").get()   # issue here
            # short_d = re.sub('<[^>]+>', '',short_d)


            # copied the xpath from inspect element
            short_d = response.xpath("/html/body/div[2]/section[1]/div/div/div/section/div/div[1]/div/div[3]/div/text()[2]").get().strip()

            duration = response.xpath("(//p[@class='elementor-icon-box-description'])[1]/text()").get().strip()
            batch_date = response.xpath("(//p[@class='elementor-icon-box-description'])[2]/text()").get().strip()
            delivery = response.xpath("(//p[@class='elementor-icon-box-description'])[3]/text()").get().strip()
            tm = response.xpath("(//p[@class='elementor-icon-box-description'])[4]/text()").get().strip()

            about = response.xpath("(//div[@class='elementor-widget-container'])[13]/p[3]").extract()
            about = [re.sub('<[^>]+>', '',i) for i in about]

            skills = response.xpath("//span[@class='elementor-icon-list-text']/text()").extract()

            yield {
                'link': link,
                'Title': title,
                'short_description': short_d,
                'duration': duration,
                'batch_start_date': batch_date,
                'delivery_method': delivery,
                'Time': tm,
                'regular_price': regular_p,
                'sale_price': sale_p,
                'about_the_course': about,
                'skills': skills
                
            }
