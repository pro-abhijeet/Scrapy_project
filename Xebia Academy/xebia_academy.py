import scraper_helper
import scrapy
from bs4 import BeautifulSoup
import scraper_helper as sh
from requests import request
from lxml import html
import re


class qspider(scrapy.Spider):
    name = "xebia"
    allowed_domains = ["xebiaacademyglobal.com"]

    start_urls = ["https://www.xebiaacademyglobal.com/sitemap"]

    def parse(self, response):
        for href in response.xpath("//li[@class='course-li course-li-top highlight']//ul//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):


        #title : Title of the course
        title = response.xpath('//h1/text()').extract()
        title = [titl.strip() for titl in title]
        title = "".join(title)

        short_desc = response.xpath('//div[@class="course-content-1"]//p//em/text() | //div[@class="course-content-1"]//p/text() | //div[@class="course-content-1"]//p//b//i/text() | //div[@class="col-md-6"]//div[@class="course-content-1"]//p[2]/text() | //div[@class="col-md-6"]//div[@class="course-content-1"]//p//span/text()').extract()
        short_desc = [desci.strip() for desci in short_desc]
        short_desc = "".join(short_desc)

        faq_ques = response.xpath('//div[@class="carrer-accordian"]//h4/text() | //section[@class="faq-library top-tab-sec wow fadeInUp animated"]//div[@class="faqs career-accord"]//div[@class="carrer-accordian"]/text()').extract()
        faq_ques = [faq.strip() for faq in faq_ques]
        faq_ques = "|".join(faq_ques)
        faq_ques = scraper_helper.cleanup(faq_ques)

        faq_answer = response.xpath('//div[@class="career-panel"]//p/text()').extract()
        faq_answer = [ans.strip() for ans in faq_answer]
        faq_answer = "|".join(faq_answer)

        instructor_name = response.xpath('//div[@class="trainer-detail"]//h3/text()').extract()
        instructor_name = [ins.strip() for ins in instructor_name]
        instructor_name = "|".join(instructor_name)

        instructor_image = response.xpath('//div[@class="item"]//div[@class="tainer-img"]//img/@data-src').extract()
        instructor_image = [img.strip() for img in instructor_image]
        instructor_image = " | ".join(instructor_image)

        what_will_learn = response.xpath('//section[@class="program-methodology top-tab-sec"]//div[@class="program-metholgy-text"]//div[@class="row"]//div[@class="col-md-6"]//p//span/text() | //section[@class="program-methodology top-tab-sec"]//div[@class="program-metholgy-text"]//div[@class="row"]//div[@class="col-md-6"]//p/text() | //div[@class="program-metholgy-text"]//div[@class="row"]//div[@class="col-md-4"]//p/text()').extract()
        what_will_learn = [what.strip() for what in what_will_learn]
        what_will_learn = "|".join(what_will_learn)

        target_students = response.xpath('//section[@class="why-should"]//div[@class="container"]//ul//li//p/text() | //section[@class="why-should"]//div[@class="container"]//ul//li//p//span/text()').extract()
        target_students = [tar.strip() for tar in target_students]
        target_students = "|".join(target_students)

        prerequisites = response.xpath('//div[@class="presiquite"]//div[@class="pres-text"]//ul//li//span/text() | //div[@class="presiquite"]//div[@class="pres-text"]//div//p/text() | //div[@class="presiquite"]//div[@class="presi-text"]//ul//li/text() | //div[@class="presiquite"]//div[@class="presi-text"]//h5/text() | //div[@class="presiquite"]//div[@class="pres-text"]//ul//li/text()').extract()
        prerequisites = [pre.strip() for pre in prerequisites]
        prerequisites = "|".join(prerequisites)

        description = response.xpath('//section[@class="course-overview top-tab-sec"]//div[@class="container"]//p/text() | //section[@class="course-overview top-tab-sec"]//div[@class="container"]//p//span/text() | //div[@class="col-md-6"]//div[@class="course-content-1"]//p[2]/text()').extract()
        description = [desc.strip() for desc in description]
        description = "".join(description)
        description = "<p>"+description+"</p>"

        rating = response.xpath('//section[@class="course-box"]//div[@class="container"]//div[@class="row"]//div[@class="col-md-4"][3]//h4/text() | //div[@class="star-text"][1]//p/text()').extract()
        rating = [rat.strip() for rat in rating]
        rating = "".join(rating)
        rating = rating.replace("Rating","")

        original_price = response.xpath('//section[@class="Schedules top-tab-sec"]//div[@class="container"]//div[@class="row"]//div[@class="col-md-4"][1]//ul//li[5]/b/text() | //section[@class="fee-dtls"]//div[@class="col-lg-6 programe-fee"]//div[@class="fee-top"]//h3/text()').extract()
        original_price = [org.strip() for org in original_price]
        original_price = "".join(original_price)

        discount_price = response.xpath('//section[@class="Schedules top-tab-sec"]//div[@class="container"]//div[@class="row"]//div[@class="col-md-4"][1]//ul//li[5]/b/text() | //section[@class="fee-dtls"]//div[@class="col-lg-6 programe-fee"]//h2/text()').extract()
        discount_price = [org.strip() for org in discount_price]
        discount_price = "".join(discount_price)

        batch_date = response.xpath('//section[@class="Schedules top-tab-sec"]//div[@class="container"]//div[@class="row"]//div[@class="col-md-4"]//ul//li[1]/text() | //div[@class="course-schedule"]//ul//li[1]/text()').extract()
        batch_date = [batch.strip() for batch in batch_date]
        batch_date = "|".join(batch_date)

        batch_time = response.xpath('//section[@class="Schedules top-tab-sec"]//div[@class="container"]//div[@class="row"]//div[@class="col-md-4"]//ul//li[2]/text() | //div[@class="course-schedule"]//ul//li[2]/text()').extract()
        batch_time = [tim.strip() for tim in batch_time]
        batch_time = "|".join(batch_time)
        batch_time = batch_time.replace("[]","")

        reviewer_review = response.xpath('//div[@class="head-testi"]//p/text()').extract()
        reviewer_review = [rev.strip() for rev in reviewer_review]
        reviewer_review = "|".join(reviewer_review)

        reviewer_image = response.xpath('//div[@class="bottom-testi"]//figure//img/@src').extract()
        reviewer_image = ["https://www.xebiaacademyglobal.com/"+img.strip() for img in reviewer_image]
        reviewer_image = " | ".join(reviewer_image)

        reviewer_name = response.xpath('//div[@class="bottom-testi"]//div[@class="clientDetail"]//h4/text()').extract()
        reviewer_name = [name.strip() for name in reviewer_name]
        reviewer_name = "|".join(reviewer_name)

        emi_installments = response.xpath('//table[@class="table"]//tbody//tr//td[3]/text()').extract()
        emi_installments = [emi.strip() for emi in emi_installments]
        emi_installments = "|".join(emi_installments)

        content = response.xpath('//div[@class="curriculum"]//ul[@class="curriculumListing"]//a/text() | //div[@class="curriculum"]//div[@class="carrer-accordian"]//h4/text() | //div[@class="curriculum"]//ul//li/text() | //div[@class="curriculum"]//ul//li//a/text() | //div[@class="curriculum"]//ul//li//span/text()').extract()
        number = 1
        head = []
        for cont in content:
            if cont.strip() == "" or cont.strip() == "</div></div>": continue
            heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
            head.append(heading)
            number += 1
        heading = "".join(head)

        course_start_date = response.xpath('//section[@class="course-box"]//div[@class="pro-box"][5]//div[@class="online-1"]//div[@class="text-icon"]//h4/text()').extract()
        course_start_date = [start.strip() for start in course_start_date]
        course_start_date = "".join(course_start_date)

        course_duration = response.xpath('//section[@class="course-box"]//div[@class="pro-box"][2]//div[@class="online-1"]//div[@class="text-icon"]//h4/text()').extract()
        course_duration = [dur.strip() for dur in course_duration]
        course_duration = "".join(course_duration)

        course_duration_unit = response.xpath('//section[@class="course-box"]//div[@class="pro-box"][2]//div[@class="online-1"]//div[@class="text-icon"]//span/text()').extract()
        course_duration_unit = [unit.strip() for unit in course_duration_unit]
        course_duration_unit = "".join(course_duration_unit)

        yield {
            'title' : title,
            'short_description' : short_desc,
            'description' : description,
            'faq_question' : faq_ques,
            'faq_answer' : faq_answer,
            'instructor_name' : instructor_name,
            'instructor_image' : instructor_image,
            'what_will_learn' : what_will_learn,
            'target_students' : target_students,
            'prerequisites' : prerequisites,
            'review_rating' : rating,
            'regular_price' : original_price,
            'sale_price' : discount_price,
            'batch_date' : batch_date,
            'batch_time' : batch_time,
            'reviewer_name' : reviewer_name,
            'reviewer_image' : reviewer_image,
            'reviewer_review' : reviewer_review,
            'installment_price' : emi_installments,
            'content' : heading,
            'total_duration' : course_duration,
            'course_start_date' : course_start_date,
            'total_duration_unit' : course_duration_unit

        }


