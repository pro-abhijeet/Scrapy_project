import scrapy
import datetime

class MainSpider(scrapy.Spider):
    name = 'main'
    start_urls = ['https://www.codingninjas.com/']
    headers = {
        "Accept" : "application/json",
        "Referer" : "https://www.codingninjas.com/",
        "sec-ch-ua" : '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile" : "?0",
        "sec-ch-ua-platform" : "Windows",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    
    def parse(self, response):
        link = 'https://api.codingninjas.com/api/v4/course/courses_info'
        yield scrapy.Request(url=link, callback=self.parse_main, headers=self.headers)

    def parse_main(self, response):
        data = response.json()
        course_list = []
        for category in data['data']['course_categories']:
            for sub_category in category['course_sub_categories']:
                for title in sub_category['courses']:
                    url1 = f"https://api.codingninjas.com/api/v4/course/course_plans?title={title['online_title']}&marketing_token=03ad65c9c928411475414dd0ad8720be&ab_test_groups='"

                    yield scrapy.Request(url=url1, callback=self.parse_page, headers=self.headers)


    def parse_page(self, response):
        pass