import scraper_helper
import scrapy
from bs4 import BeautifulSoup
import scraper_helper as sh
from requests import request
from lxml import html
import re


class qspider(scrapy.Spider):
    name = "dv"
    start_urls = ['https://www.digitalvidya.com/']

    def parse(self, response):
        for href in response.xpath('//div[@id="university_programs"]/div[2]/div/div/div/div/h4/a/@href | //div[@id="dp-carouselccourses"]/div/div//div/div/div/h4/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):

        #title
        title = response.xpath('//span[@style="font-size: 44px;"]//span[@style="color: rgb(255, 255, 255); font-family: Roboto; font-weight: 500; font-style: normal;"]/text() | //h1[@style = "text-align: center;"]/text() | //div[@id="top"]/div/div[1]/div/h1/text() | //div[@class="et_pb_row et_pb_row_0 et_pb_equal_columns et_pb_gutters2"]/div[1]/div[1]/div/text() | //h1/span/span/strong/text() | //h1/text()').extract()
        title = [titl.strip() for titl in title]
        title = "".join(title)
        title = title.replace("Certified Digital Marketing CourseCertified Digital Marketing Course","Certified Digital Marketing Course")


        #description
        description = response.xpath('//div[@class="et_pb_module et_pb_text et_pb_text_4  et_pb_text_align_left et_pb_bg_layout_light"]//div//p[1]/text() | //div[@id="lp-pom-text-280"]//p//span/text() | //div[@class="et_pb_with_border et_pb_section et_pb_section_4 et_pb_with_background et_section_regular"]/div[2]/div[1]/div[1]/div[1]//p/text() | //div[@class="et_pb_section et_pb_section_9 et_section_regular"]/div[1]/div[1]/div[2]/div[1]/*/text() | //div[@class="et_pb_section et_pb_section_8 et_section_regular"]/div[1]/div[1]/div[2]/div[1]/*/text() | //div[@class="et_pb_section et_pb_section_1 et_section_regular"]/div[2]/div/div/div//p//span/text() | //div[@class="et_pb_all_tabs"]/div[1]/div/text() | //div[@class="et_pb_row et_pb_row_9"]/div/div/div/p[1]/text() | //div[@class="et_pb_row et_pb_row_3"]/div/div/div//p/text() | //div[@class="et_pb_section et_pb_section_14 et_pb_with_background et_section_regular"]/div/div/div[2]/div/p/text() | //div[@id="lp-pom-text-135"]/p/span/text()').extract()
        description = [desc.strip() for desc in description]
        description = "".join(description)
        description = description.replace(":","")
        short_desc = description.split(". ")[0]
        description = "<p>"+description+"</p>"

        cover_image = response.xpath('//div[@class="lp-positioned-content"]/div[2]/div/a/img/@src | //div[@class="et_pb_column et_pb_column_1_4 et_pb_column_1_tb_header  et_pb_css_mix_blend_mode_passthrough"]/div/div/a/img/@src | //div[@class="lp-element lp-pom-image logo"]/div/img/@src').extract()
        cover_image = [cov.strip() for cov in cover_image]
        cover_image = "".join(cover_image)

        # short_desc = response.xpath('//h2[@style="text-align: center; font-size: 14px !Important;"]/text() | //div[@class="lp-positioned-content"]//div[@id="lp-pom-text-552"]//p//span/text() | //h2[@style="text-align: center; font-size: 22px !important; color: #2f3b5f !important;"]/text() | //div[@id="top"]/div/div/div/h2/text()').extract()
        # short_desc = [sho.strip() for sho in short_desc]
        # short_desc = "".join(short_desc)


        #total_duration
        total_duration = response.xpath('//div[@class="et_pb_with_border et_pb_module et_pb_blurb et_pb_blurb_3 et_clickable  et_pb_text_align_center  et_pb_blurb_position_top et_pb_bg_layout_dark"]//div[@class="et_pb_module_header"]//a/text() | //div[@id="lp-pom-text-242"]//p[1]//span/text() | //div[@class="et_pb_column et_pb_column_1_5 et_pb_column_3  et_pb_css_mix_blend_mode_passthrough et-last-child"]//div[@class="et_pb_with_border et_pb_module et_pb_blurb et_pb_blurb_4 top-section et_hover_enabled et_clickable et_pb_section_video_on_hover  et_pb_text_align_center  et_pb_blurb_position_top et_pb_bg_layout_dark"]//div[@class="et_pb_blurb_container"]//a/text() | //div[@id="top-section-python-course"]/div[3]/div[1]/div/div[2]/div/div/a/text() | //div[@id="first_fold"]/div/div/div/div/div//p/text()[preceding-sibling::br] | //div[@class="et_pb_row et_pb_row_1 et_pb_gutters2 et_pb_row_1-2_1-6_1-6_1-6"]/div[2]/div[1]/div/div/h4/a/text() | //div[@class="et_pb_with_border et_pb_row et_pb_row_2 et_pb_equal_columns et_pb_gutters2"]/div[2]//ul//li[2]/span[2]/text() | //div[@id="lp-pom-root"]/div[2]/div[@id="lp-pom-text-36"]/p//span/text() | //div[@id="top-section-python-course"]/div[3]/div[2]/div/div[2]/h4/a/text()').extract()
        total_duration = [tot.strip() for tot in total_duration]
        total_duration = "".join(total_duration)
        total_duration = re.sub('\(.*?\)', '', total_duration)
        total_duration = total_duration.replace("Hours of Doubt Clearing Sessions","").replace("of Self Paced Learning Videos & Live Instructor led Online Sessions","").replace("+","").replace("Hours","").replace("months","").replace("105","5")


        #total_duration_unit
        total_duration_unit = response.xpath('//div[@class="et_pb_with_border et_pb_module et_pb_blurb et_pb_blurb_3 et_clickable  et_pb_text_align_center  et_pb_blurb_position_top et_pb_bg_layout_dark"]//p/text() | //div[@class="et_pb_column et_pb_column_1_5 et_pb_column_3  et_pb_css_mix_blend_mode_passthrough et-last-child"]//div[@class="et_pb_with_border et_pb_module et_pb_blurb et_pb_blurb_4 top-section et_hover_enabled et_clickable et_pb_section_video_on_hover  et_pb_text_align_center  et_pb_blurb_position_top et_pb_bg_layout_dark"]//div[@class="et_pb_blurb_container"]//p/text() | //div[@id="top-section-python-course"]/div[3]/div[1]/div/div[2]/div/p/text() | //div[@class="et_pb_with_border et_pb_row et_pb_row_2 et_pb_equal_columns et_pb_gutters2"]/div[2]//ul//li[2]/span[2]/text() | //div[@id="lp-pom-root"]/div[2]/div[@id="lp-pom-text-36"]/p//span/text() | //div[@id="lp-pom-text-242"]//p[1]//span/text() | //div[@id="top-section-python-course"]/div[3]/div[2]/div/div[2]/div/p/text()').extract()
        total_duration_unit = [unit.strip() for unit in total_duration_unit]
        total_duration_unit = "".join(total_duration_unit)
        total_duration_unit = total_duration_unit.replace("Classes ","").replace("Hrs","Hours").replace("Class ","").replace("hours","Hours").replace("Training & Exercise ","").replace("Industry Experts","").replace("of Doubt Clearing Sessions","").replace("8","").replace("of Self Paced Learning Videos & Live Instructor led Online Sessions","").replace("10+","").replace(' (8 hours/week) Instructor-led, Online','').replace('4 ','').replace(' ( Hours/week)','').replace("months","Months")


        #regular_price
        regular_price = response.xpath('//div[@class="et_pb_column right et_pb_column_1_4555  et_pb_css_mix_blend_mode_passthrough et-last-child"]//div[@class="et_pb_module et_pb_text et_pb_text_align_left et_pb_bg_layout_light"]//center[1]//h3/text() | //div[@id="discount"]/div[2]/div[4]//div[@class="et_pb_blurb_description"]/text() | //div[@id="et_main_row_box"]/div[4]/div[1]//div[@class="et_pb_blurb_description"]/text() | //div[@id="discount"]/div[2]/div[4]//div[@class="et_pb_blurb_description"]/p/text() | //div[@id="discount"]/div[2]/div[4]/div/div/div[2]/h4/span/text()[preceding-sibling::br] | //div[@id="first_fold"]/div[3]/div/div/div/div//p/text() | //div[@class="et_pb_row et_pb_row_7 et_pb_equal_columns et_pb_gutters3"]/div[2]/div/div/div[2]/div/text() | //*[@id="post-197467"]/div/div/div/div[6]/div/div[2]/div[2]/div[2]/div/div/text() | //div[@id="lp-pom-box-121"]//span[@id="price"]/text() | //div[@id="lp-pom-text-571"]/h4/span[1]/text()').extract()
        regular_price = [reg.strip() for reg in regular_price]
        regular_price = "".join(regular_price)
        regular_price = regular_price.replace("INR ","").replace("(+18% GST)","").replace("+ GST","").replace("/-*","").replace("Rs","").replace("₹","").replace(" 11,900 11,900","11,900")


        #sale_price
        sale_price = response.xpath('//*[@id="post-197467"]/div/div/div/div[6]/div/div[2]/div[2]/div[3]/div/div/text()').extract()
        sale_price = [sale.strip() for sale in sale_price]
        sale_price = "".join(sale_price)


        #currency
        currency = "INR"


        #batch_date
        batch_date = response.xpath('//table[@style="border-collapse: collapse; width: 100%;"]//tbody//tr//td[1]/text() | //div[@id="discount"]/div[2]/div[1]//div[@class="et_pb_blurb_description"]//p/text() | //div[@id="et_main_row_box"]/div[1]/div[1]//div[@class="et_pb_blurb_description"]//p/text() | //div[@class="et_pb_row et_pb_row_7 et_pb_equal_columns et_pb_gutters3"]/div[1]/div/div/div[2]/div/text()').extract()
        batch_date = [date.strip() for date in batch_date]
        batch_date = "|".join(batch_date)
        batch_date = batch_date.replace("Oct ","October ")


        #batch_timing
        batch_timing = response.xpath('//table[@style="border-collapse: collapse; width: 100%;"]//tbody//tr//td[2]/text() | //div[@id="et_main_row_box"]/div[2]/div[1]//div[@class="et_pb_blurb_description"]//p/text() | //div[@id="discount"]/div[2]/div[2]//div[@class="et_pb_blurb_description"]//p/text()').extract()
        batch_timing = [tim.strip() for tim in batch_timing]
        batch_timing = "|".join(batch_timing)
        batch_timing = batch_timing.replace("to","-")
        batch_timing = re.sub('\(.*?\)', '', batch_timing)


        #batch_days
        batch_days = response.xpath('//table[@style="border-collapse: collapse; width: 100%;"]//tbody//tr//td[3]/text() | //div[@id="et_main_row_box"]/div[3]/div[1]//div[@class="et_pb_blurb_description"]//p/text() | //div[@id="discount"]/div[2]/div[3]//div[@class="et_pb_blurb_description"]//p/text()').extract()
        batch_days = [days.strip() for days in batch_days]
        batch_days = " | ".join(batch_days)
        batch_days = batch_days.replace("Tue ","Tuesday ").replace("Tue-","Tuesday-").replace("Mon-","Monday-").replace("Wed-","Wednesday").replace("Thu ","Thursday").replace("Fri ","Friday").replace("Sat ","Saturday").replace(" Sun","Sunday").replace("&","-")


        #batch_price
        batch_price = response.xpath('//div[@id="et_main_row_box"]/div[4]/div[1]//div[@class="et_pb_blurb_description"]/text() | //div[@id="discount"]/div[2]/div[4]//div[@class="et_pb_blurb_description"]/text() | //div[@id="discount"]/div[2]/div[4]//div[@class="et_pb_blurb_description"]/p/text()').extract()
        batch_price = [pri.strip() for pri in batch_price]
        batch_price = "|".join(batch_price)


        #what_will_learn
        what_will_learn = response.xpath('//div[@class="et_pb_tab_content"]//h4/text() | //div[@id="lp-pom-text-280"]//ul//li//span/text() | //*[@id="Curriculum"]/div/div/div/div/div/ul/li/text() | //div[@id="Curriculum"]//ol//li/text() | //div[@class="et_pb_with_border et_pb_section et_pb_section_4 et_pb_with_background et_section_regular"]/div[2]/div/div[2]/div/div/div/ul//li/span[2]/text() | //div[@class="et_pb_all_tabs"]/div[1]/div/ul//li/text() | //div[@class="et_pb_row et_pb_row_8"]/div[2]/div[2]//ul//li[@style="margin-bottom:10px"]/text() | //div[@class="et_pb_section et_pb_section_13 et_pb_with_background et_section_regular"]/div[2]/div/div/div/ul//li/span[2]/text()').extract()
        what_will_learn = [what.strip() for what in what_will_learn]
        what_will_learn = "|".join(what_will_learn)
        what_will_learn = re.sub('\[.*?\]', '', what_will_learn)
        what_will_learn = what_will_learn.replace("||","|")


        #instructor_image
        instructor_image = response.xpath('//picture[@class="trainer wp-post-image sp-no-webp"]//img/@src | //div[@class="team w-100 h-100 p-3"]//img/@src | //div[@class="et_pb_with_border et_pb_section et_pb_section_9 et_pb_with_background et_section_regular"]/div[2]/div/div/div/div/div/div/div/figure/picture//img/@src | //div[@class="et_pb_row et_pb_row_3 et_pb_equal_columns et_pb_gutters1 et_pb_row_4col"]/div/div/div/div/span/picture/img/@src').extract()
        instructor_image = [ins.strip() for ins in instructor_image]
        instructor_image = " | ".join(instructor_image)
        instructor_image = instructor_image.replace("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20220%20143'%3E%3C/svg%3E |","").replace("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20220%20220'%3E%3C/svg%3E |","").replace("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20220%20143'%3E%3C/svg%3E |","").replace(" data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20195%20127'%3E%3C/svg%3E |","").replace(" data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20150%20150'%3E%3C/svg%3E |","").replace("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20197%20127'%3E%3C/svg%3E |","")


        #instructor_name
        instructor_name = response.xpath('//div[@class="et_pb_column et_pb_column_1_4 et_pb_column_45555    et_pb_css_mix_blend_mode_passthrough trainer-content"]//div[@class="et_pb_text_inner"]//div[@class="h5"]/text() | //div[@class="team w-100 h-100 p-3"]//h4/text() | //div[@class="et_pb_with_border et_pb_section et_pb_section_9 et_pb_with_background et_section_regular"]/div[2]/div/div/div/div/div/div/div/div/h4/text() | //*[@id="post-87923"]/div/div/div/div[3]/div[2]/div/div/div/div[2]/h4/span/text()').extract()
        instructor_name = [nam.strip() for nam in instructor_name]
        instructor_name = "|".join(instructor_name)


        #instructor_description
        instructor_description = response.xpath('//div[@class="team w-100 h-100 p-3"]//p/text() | //div[@class="et_pb_with_border et_pb_section et_pb_section_9 et_pb_with_background et_section_regular"]/div[2]/div/div/div/div/div/div/div/div/div//p/text() | //*[@id="post-87923"]/div/div/div/div[3]/div[2]/div/div/div/div[2]/div//p/text()').extract()
        instructor_description = [desc.strip() for desc in instructor_description]
        instructor_description = "|".join(instructor_description)


        #instructor_designation
        instructor_designation = response.xpath('//div[@class="et_pb_row111 et_pb_equal_columns et_pb_gutters2 et_pb_row_4col team-member-design"]/div/div/div/a//p/text()').extract()
        instructor_designation = [des.strip() for des in instructor_designation]
        instructor_designation = "|".join(instructor_designation)


        #reviewer_review
        reviewer_review = response.xpath('//div[@class="et_pb_testimonial_description_inner"]//div[@class="et_pb_testimonial_content"]//p/text() | //div[@class="testimonials w-100 h-100 p-3"]//p/text() | //div[@class="et_pb_row et_pb_row_30"]/div/div/div/div/div/div/div/div/div[2]/text()').extract()
        reviewer_review = [img.strip() for img in reviewer_review]
        reviewer_review = " | ".join(reviewer_review)


        #reviewer_name
        reviewer_name = response.xpath('//span[@class="et_pb_testimonial_author"]/text() | //div[@class="testimonials w-100 h-100 p-3"]//h4/text() | //div[@class="et_pb_row et_pb_row_30"]/div/div/div/div/div/div/div/div/h4/text()').extract()
        reviewer_name = [nam.strip() for nam in reviewer_name]
        reviewer_name = "|".join(reviewer_name)


        #reviewer_image
        reviewer_image = response.xpath('//div[@class="testimonials w-100 h-100 p-3"]//img/@src').extract()
        reviewer_image = [imgg.strip() for imgg in reviewer_image]
        reviewer_image = " | ".join(reviewer_image)


        #faq_question
        faq_question = response.xpath('//div[@class="et_pb_section et_pb_section_19 et_section_regular"]//div//h5/text() | //div[@class="et_pb_row et_pb_row_44"]//h5/text() | //div[@class="et_pb_section et_pb_section_13 et_section_regular"]/div[2]//h5/text() | //div[@class="et_pb_section et_pb_section_12 et_section_regular"]/div[2]//h5/text() | //div[@class="et_pb_section et_pb_section_13 et_section_regular"]/div[3]//h5/text() | //div[@class="et_pb_all_tabs"]/div[4]/div//b/text() | //*[@id="post-146290"]/div/div/div/div[17]/strong/strong/div/div/div/h5/text() | //div[@class="et_pb_row et_pb_row_37"]//div/div/h5/text() | //div[@class="et_pb_row et_pb_row_47"]//div/div/h5/text() | //div[@class="et_pb_section et_pb_section_15 et_section_regular"]/div//div/div/h5/text() | //div[@id="lp-code-432"]/div/div/div/div/div/div/div/label/text()').extract()
        faq_question = [ques.strip() for ques in faq_question]
        faq_question = "|".join(faq_question)
        faq_question = faq_question.replace("Q.","").replace("Question:","")


        #faq_answers
        faq_answers = response.xpath('//div[@class="et_pb_section et_pb_section_19 et_section_regular"]//div//h5/following-sibling::div/*/text() | //div[@class="et_pb_section et_pb_section_13 et_section_regular"]/div[2]//h5/following-sibling::div/*/text() | //div[@class="et_pb_section et_pb_section_12 et_section_regular"]/div[2]//h5/following-sibling::div/*/text() | //div[@class="et_pb_section et_pb_section_13 et_section_regular"]/div[3]//h5/following-sibling::div/p[1]/text() | //div[@class="et_pb_all_tabs"]/div[4]/div//p/text() | //*[@id="post-146290"]/div/div/div/div[17]/strong/strong/div/div/div/div//p[1]/text() | //div[@class="et_pb_row et_pb_row_47"]//div/div/div/p[1]/text() | //div[@class="et_pb_section et_pb_section_15 et_section_regular"]/div//div/div//p/text() | //div[@id="lp-code-432"]//div[@class="tabs"]//label/following-sibling::div/*/text() | //div[@id="lp-code-432"]//div[@class="tabs"]/div/div[@class="tab-content"]/div/div/div/text()').extract()
        faq_answers = [ans.strip() for ans in faq_answers]
        faq_answers = "|".join(faq_answers)
        faq_answers = faq_answers.replace("Answer:","").replace("A.","")
        faq_answers = scraper_helper.cleanup(faq_answers)


        #emi_installment_time
        emi_installment_time = response.xpath('//div[@id="lp-pom-text-420"]//tbody//tr//td[1]/text() | //div [@class="et_pb_row et_pb_row_32"]/div[2]/div/div/table/tbody//tr/td[1]/text()').extract()
        emi_installment_time = [emi.strip() for emi in emi_installment_time]
        emi_installment_time = "|".join(emi_installment_time)


        #emi_installment
        emi_installment = response.xpath('//div[@id="lp-pom-text-420"]//tbody//tr//td[2]/text() | //div [@class="et_pb_row et_pb_row_32"]/div[2]/div/div/table/tbody//tr/td[2]/text()').extract()
        emi_installment = [emi.strip() for emi in emi_installment]
        emi_installment = "|".join(emi_installment)


        #target_students
        target_students = response.xpath('//div[@id="lp-code-432"]//div[@class="tabs"]//label[@for="chck1"]/following-sibling::div/text() | //div[@id="interview"]/div[5]/div[2]/ul/li/span[1]/text() | //div[@class="et_pb_section et_pb_section_1 et_section_regular"]/div[2]/div/div/div/ul//li//span/text() | //div[@id="interview"]/div[3]/div[2]/ul/li/span[1]/text() | //div[@class="et_pb_row et_pb_row_4"]/div[2]/div[2]//ul//li/text()').extract()
        target_students = [tar.strip() for tar in target_students]
        target_students = "|".join(target_students)
        target_students = target_students.replace("Answer", "")


        #prerequisites
        prerequisites = response.xpath('//div[@id="interview"]/div[5]/div/div/div/ul//li/text() | //div[@id="lp-code-432"]/div/div/div/div[1]/div[@class="tab-content"]/div/div[2]/div/text()').extract()
        prerequisites = [pre.strip() for pre in prerequisites]
        prerequisites = "|".join(prerequisites)
        prerequisites = prerequisites.replace("Answer:", "")


        #content
        content = response.xpath('//div[@id="syllabus"]/div/div/div[3]/ul//li//a/text() | //div[@id="modules"]/div/div/div[2]//ul/li//a/text() | //div[@id="lp-code-340"]/div/div/div//div//label/text() | //div[@class="et_pb_row et_pb_row_21 et_pb_equal_columns et_pb_gutters2"]/div/div/div//h5/text() | //div[@id="Curriculum"]/div/div[2]/ul//li//a/text() | //div[@id="Curriculum"]/div/div/div//ol//li/text() | //div[@class="et_pb_section et_pb_section_5 et_section_regular"]/div/div/div[2]/ul//li//a/text() | //div[@class="et_pb_all_tabs"]/div[2]/div/ol//li/text() | //div[@class="et_pb_row et_pb_row_16 et_pb_equal_columns et_pb_gutters2"]/div/div/div/h5/text()').extract()
        number = 1
        head = []
        for cont in content:
            if cont.strip() == "" or cont.strip() == "</div></div>": continue
            heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
            head.append(heading)
            number += 1
        heading = "".join(head)


        #total_video_content
        total_video_content = response.xpath('//div[@class="et_pb_with_border et_pb_row et_pb_row_2 et_pb_equal_columns et_pb_gutters2"]/div[2]/div/div/ul/li[3]/span[2]/text()').extract()
        total_video_content = [tot.strip() for tot in total_video_content]
        total_video_content = "".join(total_video_content)
        total_video_content = total_video_content.replace("learning video hours","")

        #instruction_type
        instruction_type = response.xpath('//div[@id="top"]/div/div[1]/div/h2/text() | //div[@id="lp-pom-text-242"]//p[2]/span/text() | //div[@class="et_pb_row et_pb_row_5"]/div[1]/div/div/ul/li[1]/text() | //div[@class="et_pb_row et_pb_row_18 et_pb_equal_columns et_pb_gutters2 et_pb_row_5col"]/div[4]/div/div/div[2]/h4/span/text()').extract()
        instruction_type = [typoi.strip() for typoi in instruction_type]
        instruction_type = "".join(instruction_type)
        instruction_type = instruction_type.replace("Online Training for Digital Marketing","").replace(", Online","").replace(" Sessions","").replace("Live","").replace("BEST SEO TRAINING COURSE","").replace("Upskilling","").replace("1-MONTH INSTRUCTOR-LED ONLINE COURSE","")
        if "Instructor-Led" in instruction_type:
            instructor = "Instructor Paced"
        elif "Instructor-led" in instruction_type:
            instructor = "Instructor Paced"
        elif " Instructor-led" in instruction_type:
            instructor = "Instructor Paced"
        else:
            instructor = "Self Paced"
        instruction_type1 = instructor

        yield {
            'title' : title,
            'description' : description,
            'short_description' : short_desc,
            'total_duration' : total_duration,
            'total_duration_unit' : total_duration_unit,
            'regular_price' : regular_price,
            'sale_price' : sale_price,
            'currency' : currency,
            'batch_date' : batch_date,
            'batch_timing' : batch_timing,
            'batch_days' : batch_days,
            'batch_price' : batch_price,
            'what_will_learn' : what_will_learn,
            'instructor_image' : instructor_image,
            'instructor_name' : instructor_name,
            'instructor_designation' : instructor_designation,
            'reviewer_review' : reviewer_review,
            'reviewer_name' : reviewer_name,
            'faq_question' : faq_question,
            'faq_answers' : faq_answers,
            'reviewer_image' : reviewer_image,
            'instructor_description' : instructor_description,
            'emi_installment_time' : emi_installment_time,
            'emi_installment' : emi_installment,
            'target_students' : target_students,
            'prerequisites' : prerequisites,
            'heading' : heading,
            'total_video_content' : total_video_content,
            'instruction_type' : instruction_type1,
            'cover_image' : cover_image
        }