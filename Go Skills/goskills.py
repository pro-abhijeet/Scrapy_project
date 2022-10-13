import scraper_helper
import scrapy
from bs4 import BeautifulSoup
import scraper_helper as sh
from requests import request
from lxml import html


class qspider(scrapy.Spider):
    name = "goskills"
    urls = ["https://www.goskills.com/Course/Excel-Power-Pivot"]
    sub_price = request(method="GET", url=urls[0] + "/Pricing?source=course-about")
    request_response = html.fromstring(sub_price.content)
    pricing = request_response.xpath("//*[@id='course-pricing']//*[@class='panel-body']/h4[contains(text(),'Year')]/..//*[@class='before-decimal-point']//text()")[0]

    def start_requests(self):
        urls = ["https://www.goskills.com/Course/Microsoft-Excel-Basico-y-Avanzado"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'price':self.pricing})

    def parse(self, response, price):
        title = response.xpath('//h1/text()').extract()
        title = [tit.strip() for tit in title]
        title = "".join(title)

        description = response.xpath('//div[@id="course-about-outline"]//div[@class="col-md-10"]//p/text()').extract()
        description = [desc.strip() for desc in description]
        description = "".join(description)
        description = "<p>"+description+"</p>"

        level = response.xpath('//div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][1]//span[@class="summary-text"]/text()').extract()
        level = [lev.strip() for lev in level]
        level = "".join(level)

        prerequisites = response.xpath('//div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][5]//span[@class="summary-text"]//a/text() | //div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][5]//span[@class="summary-text"]/text()').extract()
        prerequisites = [pre.strip() for pre in prerequisites]
        prerequisites = "|".join(prerequisites)

        total_video = response.xpath('//div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][7]//span[@class="summary-text"]/text()').extract()
        total_video = [vid.strip() for vid in total_video]
        total_video = "".join(total_video)

        course_duration = response.xpath('//div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][8]//span[@class="summary-text"]/text()').extract()
        course_duration = [dur.strip() for dur in course_duration]
        course_duration = "".join(course_duration)
        course_duration = course_duration.replace(" for all materials","")

        accredation_name = response.xpath('//div[@id="course-about-summary"]//div[@class="col-md-10"]//div[@class="col-xs-12 col-sm-6 summary"][4]//span[@class="summary-text"]/text()').extract()
        accredation_name = [acc.strip() for acc in accredation_name]
        accredation_name = "|".join(accredation_name)

        accredation_image = response.xpath('//div[@id="course-about-accreditations"]//div[@class="col-md-10"]//a[1]//img/@src').extract()
        accredation_image = ["https://www.goskills.com"+image.strip() for image in accredation_image]
        accredation_image = "|".join(accredation_image)


        instructor_image = response.xpath('//div[@id="course-about-tutors"]//div[@class="col-md-10"]//img/@src').extract()
        instructor_image = ["https://www.goskills.com"+ins.strip() for ins in instructor_image]
        instructor_image = "|".join(instructor_image)

        instructor_name = response.xpath('//div[@id="course-about-tutors"]//div[@class="col-md-10"]//h3/text()').extract()
        instructor_name = [inss.strip() for inss in instructor_name]
        instructor_name = "|".join(instructor_name)

        instructor_designation = response.xpath('//div[@id="course-about-tutors"]//div[@class="col-md-10"]//p').extract()
        instructor_designation = [desig.strip() for desig in instructor_designation]
        instructor_designation = "|".join(instructor_designation)


        reviewer_name = response.xpath('//div[@id="testimonials-carousel"]//cite[@class="small"]/text()').extract()
        reviewer_name = [rev.strip() for rev in reviewer_name]
        reviewer_name = "|".join(reviewer_name)

        reviewer_review = response.xpath('//div[@id="testimonials-carousel"]//p[1]/text()').extract()
        reviewer_review = [revi.strip() for revi in reviewer_review]
        reviewer_review = "|".join(reviewer_review)

        content = response.xpath('//div[@id="course-about-syllabus-accordion"]//div[@class="panel-heading"]//h3/text()').extract()
        number = 1
        head = []
        for cont in content:
            if cont.strip() == "" or cont.strip() == "</div></div>": continue
            heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
            head.append(heading)
            number += 1
        heading = "".join(head)

        syllabus = response.xpath('//div[@id="course-about-syllabus-accordion"]/following-sibling::p//a/@href').extract()
        syllabus = ["https://www.goskills.com"+syl.strip() for syl in syllabus]
        syllabus = "".join(syllabus)


        what_will_learn = response.xpath('//div[@id="course-about-outline"]//div[@class="col-md-10"]//ul//li[@aria-level="1"]/text() | //div[@id="course-about-outline"]//div[@class="col-md-10"]//ul//li/text()').extract()
        what_will_learn = [what.strip() for what in what_will_learn]
        what_will_learn = "|".join(what_will_learn)

        faq_question = response.xpath("//*[@id='faq-list']//*[@class='panel-title collapsed']//following-sibling::text()[2]").extract()
        faq_question = [faq.strip() for faq in faq_question]
        faq_question = "|".join(faq_question)

        faq_answer = response.css('#faq-list p::text').extract()
        faq_answer = [ans.strip() for ans in faq_answer]
        faq_answer = "|".join(faq_answer)

        yield{
            'title' : title,
            'regular_price' : price,
            'description' : description,
            'level' : level,
            'prerequisites' : prerequisites,
            'total_video_content' : total_video,
            'total_duration' : course_duration,
            'accredation_name' : accredation_name,
            'accredation_image' : accredation_image,
            'instructor_image' : instructor_image,
            'instructor_name' : instructor_name,
            'instructor_designation' : instructor_designation,
            'reviewer_name' : reviewer_name,
            'reviewer_review' : reviewer_review,
            'content' : heading,
            'syllabus' : syllabus,
            'what_will_learn' : what_will_learn,
            'faq_question' : faq_question,
            'faq_answer' : faq_answer







        }