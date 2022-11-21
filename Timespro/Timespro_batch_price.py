import scrapy
import ast
import json
import requests

class times_pro_Spider(scrapy.Spider):

    name = "timespro"

    def start_requests(self):
        url = "https://web3.timespro.com/api/courses/courseslist?isdraft=0&is_active=1&is_publish=1&searchkey=undefined&courseType=undefined&courseType=undefined&duration=undefined&duration=undefined&duration=undefined&fees=undefined&fees=undefined&fees=undefined"

        yield scrapy.Request(url=url, callback=self.parse)
    # start_urls = ["https://web3.timespro.com/courses#"]

    def parse(self, response):

        # url = "https://web3.timespro.com/api/courses/courseslist?isdraft=0&is_active=1&is_publish=1&searchkey=undefined&courseType=undefined&courseType=undefined&duration=undefined&duration=undefined&duration=undefined&fees=undefined&fees=undefined&fees=undefined"
        # r = requests.get(url)
        data = response.json()
        # request = scrapy.Request(url, callback=self.parse_api)
        # yield request

        courses_data = data['data'] # it is list type

        for i in range(len(courses_data)):
            course_details = courses_data[i] # it is dict type
            class_timing = course_details['courseInclude'][0]

            title = course_details['title']
            regular_price = course_details['fees_filter']
            duration = course_details['fees_filter']

            timing = class_timing['CourseCovered']

            yield {
                'title': title ,
                'regular_price': regular_price,
                'course_duration': duration,
                'timning': timing
            }



    # #'C:\Users\prave\PycharmProjects\Times Pro\venv\Scripts\python.exe'.
    # def parse_json(self, response):
    #     data = response.json()
    #
    # def parse_courses(self, response):
    #     data = response.json()
    #     yield {
    #         'title':data['title']
    #
    #     }

    # def parse_api(self,response):
    #     base_url = 'https://web3.timespro.com/api/courses/courseviewdetail?name='
    #     raw_data = response.body
    #     data = json.loads(raw_data)
    #     for page in data:
    #         course = ast.literal_eval(page)
    #         page_name = course['data'][0]['page_name']
    #         course_url = base_url + page_name
    #         request = scrapy.Request(course_url, callback=self.parse_courses)
    #
    #         yield request
    #
    # def parse_courses(self,response):
    #     raw_data = response.body
    #     data = json.loads(raw_data)
    #     yield {
    #         'title':data['data'][0]['title']
    #     }