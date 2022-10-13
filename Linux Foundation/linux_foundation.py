import random

import scrapy
import datetime
import re
import time

class Linuxspider(scrapy.Spider):
    name = 'linux'
    allowed_domains = ["linuxfoundation.org"]
    start_urls = ['https://training.linuxfoundation.org/full-catalog/']

    def parse(self, response):
        for href in response.xpath('//div[@data-content="result"]/div[@class="search-filter-results"]//a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self,response):

        #title
        title = response.xpath('//h1/text()').extract()
        title = [tit.strip() for tit in title]
        title = "".join(title)


        #description
        description = response.xpath('//div[@id="lf_pdp_fundamentals_who_is_it_for_view"]/section[3]/div[@class="lf-pdp-content"]/div/text() | //div[@class="wpb_text_column wpb_content_element  vc_custom_1644788286562"]/div//p/text()').extract()
        description = [desc.strip() for desc in description]
        description = "".join(description)
        description = "<p>"+description+"</p>"


        #short_description
        short_desc = ""
        short_dis = response.xpath('//div[@class="wpb_text_column wpb_content_element  lf-pdp-header-text"]/div/p//span/text() | //div[@class="wpb_text_column wpb_content_element  lf-cloud-enginer-header-text"]/div//p/text() | //div[@class="wpb_text_column wpb_content_element  lf-pdp-header-text"]/div/p//em/text()').extract()
        for sho in short_dis:
            if sho in short_dis is None:
                short_desc = description.split(".")[:1]
            else:
                short_desc = short_dis

        short_desc = "".join(short_desc)




        #what_will_learn
        what_will_learn = response.xpath('//div[@id="lf_pdp_fundamentals_who_is_it_for_view"]/section[2]/div[@class="lf-pdp-content"]/div[@class="lf-pdp-content-body"]/text() | //div[@class="wpb_row vc_row-fluid vc_row inner_row  vc_custom_1590323591690 lf-cloud-enginer-learn-more-section"]/div[2]/div/div/div//div[@class="iwt-text"]/text() | //div[@id="lf_pdp_fundamentals_who_is_it_for_view"]/section[2]/div[2]/div/text() | //div[@class="vc_col-sm-4 wpb_column column_container vc_column_container col child_column no-extra-padding inherit_tablet inherit_phone "]/div/div/div[2]/div/text()').extract()
        for what in what_will_learn:
            what_will_learn = what.split(". ")
        what_will_learn = "|".join(what_will_learn)


        #target_students
        target_students = response.xpath('//div[@id="lf_pdp_fundamentals_who_is_it_for_view"]/section[1]/div[@class="lf-pdp-content"]/div/text()').extract()
        for tar in target_students:
            target_students = tar.split(". ")
        target_students = "|".join(target_students)



        #sale_price
        sale_price = response.xpath('//div[@class="wpb_wrapper"]//div[@class="lf_pdp_fundamentals-buy"][1]/section/article/section/section/div[@class="lf_pdp_fundamentals-buy-body-card-info-price"]/text() | //div[@class="lf-bootcamp-header-price"]/text()').extract()
        sale_price = [sale.strip() for sale in sale_price]
        sale_price = "".join(sale_price)
        sale_price = sale_price.replace("$","")


        #currency
        currency = response.xpath('//div[@class="wpb_wrapper"]//div[@class="lf_pdp_fundamentals-buy"][1]/section/article/section/section/div[@class="lf_pdp_fundamentals-buy-body-card-info-price"]/text() | //div[@class="lf-bootcamp-header-price"]/text()').extract()
        currency = [curr.strip() for curr in currency]
        currency = "".join(currency)
        if "$" in currency.lower().strip():
            currency = "USD"
        currence = currency


        #level
        level = response.xpath('//div[@class="lf_pdp_fundamentals-experience_level lf-pdp-component-container"][1]//section[@class="lf_pdp_fundamentals-experience_level-title"][1]/span/text()').extract()
        level = [lev.strip() for lev in level]
        level = "".join(level)


        #prerequisites
        prerequisites = response.xpath('//div[@class="lf_pdp_fundamentals-prerequisites-lab-info lf-pdp-component-container"]/section/article/ul//li/*/text() | //div[@class="wpb_wrapper"]//div[@class="lf_pdp_fundamentals-prerequisites-lab-info lf-pdp-component-container"][1]/section/article/ul//li//span/text() | //div[@class="wpb_wrapper"]//div[@class="lf_pdp_fundamentals-prerequisites-lab-info lf-pdp-component-container"][1]/section/article/text() | //div[@class="wpb_wrapper"]//div[@class="lf_pdp_fundamentals-prerequisites-lab-info lf-pdp-component-container"][1]/section/article/ul//li//a//i/text() | //div[@class="lf_pdp_fundamentals-prerequisites-lab-info lf-pdp-component-container"]/section/article/span/text()').extract()
        for pre in prerequisites:
            prerequisites = pre.split(". ")
        prerequisites = "|".join(prerequisites)


        #delivery_method
        delivery_method = response.xpath('//div[@class="lf_pdp_fundamentals-includes lf-pdp-component-container"][1]/section[2]/article[1]/span/text()').extract()
        delivery_method = [deli.strip() for deli in delivery_method]
        delivery_method = "".join(delivery_method)
        if "live" in delivery_method.lower().strip():
            delivery_method = "In Class"
        delivery_method = delivery_method.replace(", Self Paced","").replace("Self Placed","").replace("Self-Paced","")



        #instruction_type
        instruction_type = response.xpath('//div[@class="wpb_row vc_row-fluid vc_row inner_row standard_section lf-cloud-enginer-how-work-container "][1]/div[2]/div[1]/div/div[2]/div[2]/div/p/text() | //div[@class="lf_pdp_fundamentals-includes lf-pdp-component-container"][1]/section[2]/article[1]/span/text()').extract()
        instruction_type = [ins.strip() for ins in instruction_type]
        instruction_type = "".join(instruction_type)
        if "Live" in instruction_type.strip():
            instruction_type = "Instructor Paced"
        else:
            instruction_type = "Self Paced"
        instruction_type = instruction_type.replace("Online, ","").replace("Online","").replace(" Exam Delivery","").replace("Proctored  Exam Delivery","")


        #total_duration
        total_duration = response.xpath('//div[@class="lf_pdp_fundamentals-includes lf-pdp-component-container"][1]/section[2]/article[2]/span/text() | //div[@class="wpb_row vc_row-fluid vc_row inner_row standard_section lf-cloud-enginer-how-work-container "][1]/div[2]/div[2]/div/div[2]/div[2]/div/p/text()').extract()
        total_duration = [tot.strip() for tot in total_duration]
        total_duration = "".join(total_duration)
        total_duration = total_duration.replace(" of Course Material","").replace("Duration of Exam","").replace("Exam Duration","").replace("10-15 hours a week for ","").replace("10 hours a week for","").replace("of Instructor-led class time","").replace("15-20 hours a week for ","").replace("Certification Valid for 3 Years","").replace("months","").replace("Months","").replace("days","").replace("Hours","").replace("hours","")



        #total_duration_unit
        total_duration_u = ""
        total_duration_unit =  response.xpath('//div[@class="lf_pdp_fundamentals-includes lf-pdp-component-container"][1]/section[2]/article[2]/span/text() | //div[@class="wpb_row vc_row-fluid vc_row inner_row standard_section lf-cloud-enginer-how-work-container "][1]/div[2]/div[2]/div/div[2]/div[2]/div/p/text()').extract()
        total_duration_unit = [dur.strip() for dur in total_duration_unit]
        total_duration_unit = "".join(total_duration_unit)
        if "hours" in total_duration_unit.lower().strip():
            total_duration_u = "Hours"
        elif "days" in total_duration_unit.lower().strip():
            total_duration_u = "Days"
        elif "months" in total_duration_unit.lower().strip():
            total_duration_u = "Months"
        total_duration_unit = total_duration_u


        #reviewer_review
        reviewer_review = response.xpath('//div[@id="review_module"]/section[2]/article/section[2]/div[2]/text() | //div[@class="wpb_row vc_row-fluid vc_row"][2]/div[2]/div/div/div/div[2]/div//p//em/text()').extract()
        reviewer_review = [rev.strip() for rev in reviewer_review]
        reviewer_review = "|".join(reviewer_review)


        #reviewer_date
        reviewer_date = datetime.datetime.now().isoformat()


        #reviewer_rating
        reviewer_rating = response.xpath('//div[@class="vc_col-sm-4 lf-pdp-content-sidebar wpb_column column_container vc_column_container col no-extra-padding inherit_tablet inherit_phone "]/div/div/div[@class="lf_pdp_fundamentals-course_rating lf-pdp-component-container-no-style"]/section[2]/a/span/text()').extract()
        for rat in reviewer_rating:
            reviewer_rating = rat.split("/")
            reviewer_rating = reviewer_rating[:1]
            reviewer_rating = "".join(reviewer_rating)
            reviewer_rating = reviewer_rating.replace("Stars","")


        #efforts_per_week
        efforts_per_week = response.xpath('//div[@class="wpb_row vc_row-fluid vc_row inner_row standard_section lf-cloud-enginer-how-work-container "][1]/div[2]/div[2]/div/div[2]/div[2]/div/p/text()').extract()
        efforts_per_week = [eff.strip() for eff in efforts_per_week]
        efforts_per_week = "".join(efforts_per_week)
        efforts_per_week = efforts_per_week.replace("for 6 months","").replace("a","per")


        #content
        # content = response.xpath('//div[@class="lf_pdp_fundamentals-course_outline lf-pdp-component-container"]/section[2]/article/section/span[1]/text() | //div[@class="vc_col-sm-7 wpb_column column_container vc_column_container col child_column no-extra-padding inherit_tablet inherit_phone "]/div/div/div/div/div[2]/text()').extract()
        # number = 1
        # head = []
        # for cont in content:
        #     if cont.strip() == "" or cont.strip() == "</div></div>": continue
        #     heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
        #     head.append(heading)
        #     number += 1
        # heading = "".join(head)

        embedded_video = response.xpath('//div[@id="lf_video_modal"]/div[2]/div/iframe/@src').extract()
        embedded_video = [emb.strip() for emb in embedded_video]
        embedded_video = "".join(embedded_video)

        k = 1
        modules = []
        count = ""
        content = response.xpath('//div[@class="lf_pdp_fundamentals-course_outline lf-pdp-component-container"]//section[@class="lf_pdp_fundamentals-course_outline-content"]/article/section[1]/span[1]/text()').extract()

        for ii in range(len(content)):
            mod = content[ii].text.strip()
            mod = re.sub("Chapter \d+.", "", mod)
            mod = re.sub("\d\d?%", "", mod)
            mods = "<p><strong>Module " + str(ii + 1) + ": " + mod + "</strong><br/>"
            modules.append(mods)
            count += 1
            submod = content[ii].response.xpath('//div[@class="lf_pdp_fundamentals-course_outline lf-pdp-component-container"]//section[@class="lf_pdp_fundamentals-course_outline-content"]/article/section[2]//preceding-sibling::br/text()').extract()
            val = submod.text.strip()
            submod = val.split('\n')
            submodules = list()
            for count, val in enumerate(submod, 1):
                submodules.append(str(count) + '. ' + val)
            submodules = ("<br/>".join(submodules))
            submodules = re.sub("$", "</p>", submodules)
            modules.append(submodules)

        overview = "".join(modules)

        yield {
            'title': title,
            'short_desc' : short_desc,
            'description' : description,
            'what_will_learn' : what_will_learn,
            'target_students' : target_students,
            'sale_price' : sale_price,
            'currency' : currence,
            'level' : level,
            'prerequisites' : prerequisites,
            'delivery_methiod' : delivery_method,
            'instruction_type' : instruction_type,
            'total_duration' : total_duration,
            'total_duration_unit' : total_duration_unit,
            'reviewer_review' : reviewer_review,
            'reviewer_rating' : reviewer_rating,
            'date' : reviewer_date,
            'course_module' : overview,
            'efforts_per_week' : efforts_per_week,
            'embedded_video' : embedded_video


        }