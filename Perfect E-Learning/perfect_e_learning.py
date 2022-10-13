import scraper_helper
import scrapy
from bs4 import BeautifulSoup
import scraper_helper as sh
from requests import request
from lxml import html
import re



class qspider(scrapy.Spider):
    name = "quotes"
    allowed_doamins = ["perfectelearning.com"]
    start_urls = ["https://perfectelearning.com/courses/?page=1","https://perfectelearning.com/courses/?page=2"]


    def parse(self,response):
        for href in response.xpath('//div[@class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"]//a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):



        #title
        title = response.css('.title::text').extract()
        title = [titl.strip() for titl in title]
        title = "".join(title)



        #description
        description = response.xpath('//div[@class="col-12"][2]//p/text() | //div[@class="col-12"][2]//p[3]//span/text() | //div[@class="col-12"][2]//p//span//span/text()').extract()
        description = [desc.strip() for desc in description]
        description = "".join(description)
        description = "<p>"+description+"</p>"
        description = scraper_helper.cleanup(description)



        #short_description
        short_desc = response.xpath('//p[@class="description"]/text() | //div[@class="col-12"][2]//p//span/text()').extract()
        short_desc = [sho.strip() for sho in short_desc]
        short_desc = "".join(short_desc)
        short_desc = short_desc.split(".")[0]



        #rating
        rating = response.xpath('//div[@class="average"]/text()').extract()
        rating = [rat.strip() for rat in rating]
        rating = "".join(rating)



        #what_will_learn
        what_will_learn = response.xpath('//*[@class="learn-list"]//p/text() | //*[@class="learn-list"]//ul//li/text() | //*[@class="learn-list"]//ol//li/text() | //div[@class="learn-list"]//ul//li//span/text()').extract()
        what_will_learn = [what.strip() for what in what_will_learn]
        what_will_learn = "|".join(what_will_learn)
        what_will_learn = scraper_helper.cleanup(what_will_learn)



        #instructor_image
        instructor_image = response.xpath('//div[@class="mentor-pic"]//div[@class="img-container"]//img/@src').extract()
        instructor_image = [img.strip() for img in instructor_image]
        instructor_image = "".join(instructor_image)



        #instructor_name
        instructor_name = response.xpath('//div[@class="mentor-info text-light"]//p[@class="name text-85"]//a/text()').extract()
        instructor_name = [name.strip() for name in instructor_name]
        instructor_name = "".join(instructor_name)



        #instructor_designation
        instructor_designation = response.xpath('//div[@class="mentor-info text-light"]//p[3]/text()').extract()
        instructor_designation = [ins.strip() for ins in instructor_designation]
        instructor_designation = "".join(instructor_designation)



        #instructor_deescription
        instructor_description = response.xpath('//p[@class="text-light text-85"]/text() | //div[@class="mentor-info text-light"]//p/text()').extract()
        instructor_description = [inss.strip() for inss in instructor_description]
        instructor_description = "".join(instructor_description)
        instructor_description = scraper_helper.cleanup(instructor_description)



        #reviewer_review
        reviewer_review = response.xpath('//div[@class="card-body"]//div[@class="card-content"]/text()').extract()
        reviewer_review = [revi.strip() for revi in reviewer_review]
        reviewer_review = "|".join(reviewer_review)
        reviewer_review = scraper_helper.cleanup(reviewer_review)
        reviewer_review = reviewer_review.replace("||","|")



        #reviewer_name
        reviewer_name = response.xpath('//div[@class="user-detail"]//p/text()').extract()
        reviewer_name = [name.strip() for name in reviewer_name]
        reviewer_name = "|".join(reviewer_name)
        reviewer_name = re.sub('\(.*?\)', '', reviewer_name).replace('||', '|').replace("- ","")



        #reviewer_image
        reviewer_image = response.xpath('//div[@class="user-pic-container"]//img/@src').extract()
        reviewer_image = [image.strip() for image in reviewer_image]
        reviewer_image = " | ".join(reviewer_image)



        #prerequisites
        prerequisites = response.xpath('//ul[@style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"][1]//li[3]//p//span/text() | //div[@class="col-12"][2]//ul[@style="margin-top:0cm"][1]//li[3]//span/text()').extract()
        prerequisites = [pre.strip() for pre in prerequisites]
        prerequisites = "".join(prerequisites)



        #target_students
        target_students = response.xpath('//ul[@style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"][2]//li//p//span/text() | //div[@class="col-12"][2]//ul[@style="margin-top:0cm"][2]//li/span/text()').extract()
        target_students = [tag.strip() for tag in target_students]
        target_students = "|".join(target_students)
        target_students = scraper_helper.cleanup(target_students)



        #price
        price = response.xpath('//span[@class="price"]/text() | //div[@class="course-price mt-2 mb-4"]//span/text() | //div[@class="course-price mt-2 mb-4"]//ins//span/text()').extract()
        price = [pri.strip() for pri in price]
        price = "".join(price)
        price = re.sub('\(.*?\)', '', price)
        price = scraper_helper.cleanup(price)


        #content
        content = response.xpath('//div[@class="lecture-accordion-toggler"]//button[@class="btn"]/text()').extract()
        number = 1
        head = []
        for cont in content:
            if cont.strip() == "" or cont.strip() == "</div></div>": continue
            heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
            head.append(heading)
            number += 1
        heading = "".join(head)
        
        yield {'title' : title, 'description' : description, 'short_desc' : short_desc, 'rating': rating, 'what_will_learn': what_will_learn,
                'instructor_image': instructor_image, 'instructor_name' : instructor_name, 'instructor_designation': instructor_designation,
                'instructor_description': instructor_description, 'reviewer_review': reviewer_review, 'reviewer_name': reviewer_name, 'reviewer_image': reviewer_image,
                'prerequisites': prerequisites, 'target_students': target_students, 'price': price, 'heading': heading}


