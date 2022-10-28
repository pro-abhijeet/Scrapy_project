import scrapy

class Simplivlearn(scrapy.Spider):
    name = 'simplivlearn'
    start_urls = [
        "https://www.simplivlearning.com/search"
    ]
    def parse(self, response):
        for i in range(1,478):
            url = f"https://www.simplivlearning.com/search?filter=%7B%22course_language_id%22:%7B%22operation%22:%22in%22,%22value%22:[%225a9925e100887bb70fc05f73%22]%7D%7D&sort=-:rating&page={i}"
            payload = f"filter=%7B%22course_language_id%22:%7B%22operation%22:%22in%22,%22value%22:[%225a9925e100887bb70fc05f73%22]%7D%7D&sort=-:rating&page={i}"
            yield scrapy.Request(url,body=payload,callback=self.parser_content)
    def parser_content(self, response):
        for i in response.xpath("//div[@class='course-body']"):
            title = i.xpath("./div[@class='course-title dotdotdot']/a/text()").get().strip()
            link = i.xpath("./div[@class='course-title dotdotdot']/a/@href").get().strip()
            offer_price = i.xpath(".//div[@class='course-prise']/text()[1]").get().strip()
            regular_price = i.xpath(".//div[@class='course-prise']/span/text()").get().strip()
            if regular_price != '$ 0.00':

                if '$' in regular_price:
                    currency = 'USD'

                regular_price = regular_price.replace('$', '')
                regular_price = float(regular_price)

                yield{
                    'title': title,
                    'course url': link,
                    'price': offer_price,
                    'regular_price': regular_price
                }