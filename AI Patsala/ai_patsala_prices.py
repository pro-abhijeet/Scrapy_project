import scrapy

class CareerSpider(scrapy.Spider):
    name = "Course"
    allowed_domains = ['aipatasala.com']
    start_urls = ['https://aipatasala.com/data-science-course-training-in-india']  # same structure for all links

    def parse(self,response):
        title = response.xpath('//h1/text()').extract()[0]
        instruction_type = response.xpath('//h3[@class="ant-typography fee_category_heading"]/text()').extract()[0]

        regular_price  = response.xpath('//div[@class="ant-col price"]/text()').extract()[1]
        sale_price = response.xpath('//div[@class="ant-col discount_price"]/text()').extract()[1]

        online_instructor_led_retail_price = response.xpath('//div[@class="ant-col price"]/text()').extract()[3]
        online_instructor_led_discounted_price = response.xpath('//div[@class="ant-col discount_price"]/text()').extract()[3]
        skill = response.xpath('//h3[@class="ant-typography course_overview_skill_item"]//text()').extract()

        currency = 'INR'

        yield {
            'regular_price': regular_price,
            'price': sale_price,
            'currency': currency
        }