import scrapy
import requests
import regex as re
from collections import OrderedDict

class CareerSpider(scrapy.Spider):
    name = "aipathshala"
    allowed_domains = ['aipatasala.com']
    start_urls = ['https://aipatasala.com/all-courses']

    def parse(self, response):
        global link
        uxls = response.xpath('//div[@class="ant-col ant-col-xs-10 ant-col-sm-8"]//@href').getall()
        # pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"').findall(f"{uxls}") #Used Regex for extracting href tag but got the alternative
        for key in uxls:
            if key not in ("tel: 91-606-22221","mailto: info@aipatasala.com","https://g.page/aipatasala?share"):
                link = f'https://aipatasala.com{key}/'
            yield scrapy.Request(link, callback=self.parse_url)

    def replace_all(text, dic): #For removing unneccessary tags present inside the contents of what_will_you_learn and target_students
        for i, j in dic.items():
            text = text.replace(i, j)
        return text.strip()

    def parse_url(self,response):
        title = response.xpath('//h1/text()').extract_first()#Formatted
        instruction_type = ','.join(response.xpath('//h3[@class="ant-typography fee_category_heading"]/text()').extract())#Formatted
        self_paced_retail_price = response.xpath('//div[@class="ant-col price"]/text()')[1].get()#Formatted
        self_paced_discounted_price = response.xpath('//div[@class="ant-col discount_price"]/text()')[1].get()#Formatted
        online_instructor_led_retail_price = response.xpath('//div[@class="ant-col price"]/text()')[3].get()#formatted
        online_instructor_led_discounted_price = response.xpath('//div[@class="ant-col discount_price"]/text()')[5].get()#Formatted
        skill = ' | '.join(response.xpath('//h3[@class="ant-typography course_overview_skill_item"]/text()').getall())#Formatted
        instructor_name = ' | '.join(response.xpath('//div[@class="instructor_name"]/text()').getall()) #Formatted
        instructor_experience =  ' | '.join(response.xpath('//h3[@class="ant-typography instructor_exp_desc"]/text()').getall())#Formatted
        instructor_image = ' | '.join(response.xpath('//img[@class="instructor_avatar"]/@src').getall())#Formatted
        instructor_linkedin_url = ' | '.join(response.xpath('//div[@class="social_icon"]/a/@href').getall())#Formatted                
        reviewer_name = ' | '.join(response.xpath('//div[@class="ant-card-meta-title"]/text()').getall()) #Formatted
        reviewer_position = ' | '.join(response.xpath('//div[@class="ant-card-meta-description"]/text()').getall()) #Formatted
        chunk = response.xpath('//script/@src')[35].get()
        res = requests.get('https://aipatasala.com'+f'{chunk}')
        data_ = res.text
        what_will_you_learn = []
        od = OrderedDict([("</li><li>",""), ("</li>",""),("<li>",""),("<b>",""),("\\u2019s",""),("</b>",""),("</b><b>",""),("\\u201c",""),("<br><br>",""),("\\u201d","")])
        pattern = re.compile(r'answer\":\"([^\"]+)\"*')
        x = (pattern.findall(f"{data_}"))[1].split('.')
        for i in x:
            what_will_you_learn.append(CareerSpider.replace_all(i,od))
        target_pattern = re.compile(r'question\":\"([^\"]+)\"*')
        x = (target_pattern.findall(f"{data_}"))
        z = 0
        for idx, val in enumerate(x):
            if val.startswith('Who'):
                z = idx
        target_students = []
        y = (pattern.findall(f"{data_}"))[z]
        for i in y.split('.')[1:]:
            target_students.append(CareerSpider.replace_all(y,od))
        faq_question = ""
        yes = requests.get(f'{link}')
        faq_question_value = yes.text
        faq_question += " | ".join(re.compile(r'name\":\"([^\"]+)\"*').findall(f"{faq_question_value}")[5:-1])
        faq_answer = ""
        yes = requests.get(f'{link}')
        faq_answer_value = yes.text
        faq_answer += " | ".join(re.compile(r'text\":\"([^\"]+)\"*').findall(f"{faq_answer_value}")[3:-1])

        yield{
            'title':title,
            'instruction_type':instruction_type,
            'self_paced_retail_price': self_paced_retail_price,
            'self_paced_discounted_price':self_paced_discounted_price,
            'online_instructor_led_retail_price':online_instructor_led_retail_price,
            'online_instructor_led_discounted_price':online_instructor_led_discounted_price,
            'skill': skill,
            'instructor_name':instructor_name,
            'instructor_experience':instructor_experience,
            'instructor_image':instructor_image,
            'instructor_linkedin_url':instructor_linkedin_url,
            'reviewer_name':reviewer_name,
            'reviewer_position':reviewer_position,
            'what_will_you_learn':what_will_you_learn,
            'target_students':target_students,
            'faq_questions':faq_question,
            'faq_answer':faq_answer
        }