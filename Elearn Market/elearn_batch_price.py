import scrapy   
import json

class Elearn(scrapy.Spider):
    name = 'elearn1'
    start_urls = [
        "https://www.elearnmarkets.com/courses"
    ]
    def parse(self, response):
        for i in range(1,16):
            url = f"https://www.elearnmarkets.com/courses/getCourseListNew?page={i}&sort=rank&direction=asc"
            payload = '[{"key":"language","val":"1","text":"English","type":5,"index":"2","min":"","max":""}]'
            yield scrapy.Request(url,body=payload ,callback=self.parser_content)
    def parser_content(self, response):
        data = json.loads(response.body)
        data1 = data['data']
        for i in data1:
            link = i['slug']
            link = "https://www.elearnmarkets.com/courses/display/" + link
            title = i['name']
            original_price = round(i['actual_price'])
            current_price = round(i['offer_price'])
            course_del = i['course_deliverymode_id']
            if course_del == 1:
                course_del_mode = "REC"
            elif course_del == 2:
                course_del_mode = "LIVE"
            else:
                course_del_mode = "REGULAR"
            yield{
                'Course Title': title,
                'Link': link,
                'Original Price': original_price,
                'Current Price': current_price,
                'Course Delivery Mode': course_del_mode
            }