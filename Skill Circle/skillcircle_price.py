import scrapy

class Skillcircle(scrapy.Spider):
    name = 'skillcir'
    start_urls = [
        'https://www.skillcircle.in'
    ]
    def parse(self, response):
        for i in response.xpath("//li[@id='menu-item-1583']/ul//ul//a"):
            link = i.xpath("./@href").get()
            title = i.xpath("./text()").get()
            yield scrapy.Request(response.urljoin(link),callback=self.parser_content,cb_kwargs={'link':link,'title':title})
    def parser_content(self,response,link,title):
        price = response.xpath("//div[@class='elementor-widget-container']/h2//text() | //div[@class='elementor-widget-container']/h6//text()").get().strip()
        yield{
            'Course Title': title,
            'Link': link,
            'Price': price
        }