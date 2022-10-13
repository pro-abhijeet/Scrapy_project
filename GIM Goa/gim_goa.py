from dataclasses import replace
import scrapy
import re
from dateutil.parser import parse

class SoalSpyder(scrapy.Spider):
    name = 'gim'
    def start_requests(self):
            url = "https://gim.ac.in/"   
            yield scrapy.Request(url)

    def parse(self, response):
        for link in response.xpath("//div[@class='title']/../div[2]//h3//@href").getall():
            yield scrapy.Request(response.urljoin(link),callback=self.parser_content)
    def parser_content(self, response):
        #Course Title
        title = response.xpath("//div[@class='banner-content']//h1//text()").getall()
        title = [ele for ele in title if ele.strip()]
        title = list(map(lambda a:a.strip() , title))
        title = " ".join(title)
        if title=="":
                title = response.xpath("/html/head/title//text()").get()
                title = re.search("^(.*?)[\|]", title).group(1)
        #course Link
        link = (response.request.url)
        #Course Duration
        duration = response.xpath("//*[contains(text(), 'Duration')]/following-sibling::p/text()").get()
        #course_level = response.xpath("//*[contains(text(), 'Course Level')]/following-sibling::p/text()").get()
        #course type
        course_type = response.xpath("//*[contains(text(), 'Type')]/following-sibling::p/text()").get()
        #student intake
        student_intake = response.xpath("//*[contains(text(), 'Student Intake')]/following-sibling::p/text()").get()
        #Instructors Details
        instructor_name = response.xpath("//div[@class='profile-short-info']/h3/text()").getall()
        instructor_name = " |".join(instructor_name)
        instructors_expertise = response.xpath("//*[contains(text(),'Areas of Expertise')]/../div/p/text()").getall()
        instructors_expertise = [ele for ele in instructors_expertise if ele.strip()]
        instructors_expertise = " |".join(instructors_expertise)
        instructor_pic = response.xpath("//div[@class='faculty-profile-picture']//@src").getall()
        instructor_pic = [ "https://gim.ac.in/" + ele for ele in instructor_pic]
        instructor_pic = " |".join(instructor_pic)
        #FAQ
        faq_q = response.xpath("//h4[@class='accordion-title']//text()").getall()
        faq_a = []
        for i in range(len(faq_q)):
            a = response.xpath("//div[@class='accordion-content']")[i].css(" ::text").getall()
            a = [ele for ele in a if ele.strip()]
            a = " ".join(a)
            faq_a.append(a)
        faq_q = " |".join(faq_q)
        faq_a = " |".join(faq_a)
        #Review Data
        review_name = response.xpath("//div[@class='gim-right-col']/div/strong/span[1]//text()").getall()
        review_name = " ".join(review_name)
        review_pic = response.xpath("//div[@class='image open-video-popup open-video']//@src").getall()
        review_pic = [ "https://gim.ac.in/" + ele for ele in review_pic]
        review_pic = " |".join(review_pic)
        reviews = response.xpath("//div[@class='gim-right-col']/p//text()").getall()
        reviews = " |".join(reviews)
        #Description and Short Description
        if response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()"):
            description = response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()").getall()
            short_description = response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()").get()
            
        else:
            if response.xpath("//li[@class='program-tab-title']/a/text()")[1].get()=='Pedagogy':
                description = response.xpath("//div[@class='program-tab-content']")[1].css(" li::text").getall()
                short_description = response.xpath("//div[@class='program-tab-content']")[1].css(" li::text").get()
            else:
                description = response.xpath("//div[@class='program-tab-content']")[2].css(" li::text").getall()
                short_description = response.xpath("//div[@class='program-tab-content']")[2].css(" li::text").get()
        description = ['<p>'+ele+'</p>' for ele in description]
        description = "".join(description)
        #Target Students
        target_students = response.xpath("//div[@class='pd-box']")[0].css(" ::text").getall()
        target_students = [ele for ele in target_students if ele.strip()]
        target_students = list(map(lambda a:a.strip(), target_students))
        target_students = "".join(target_students)
        # What you will learn 
        if response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()"):
            what_you_learn = response.xpath("//div[@class='gim-right-col gim-col']//ul//li/p//text()").getall()
        else:
            if response.xpath("//li[@class='program-tab-title']/a/text()")[0].get()=='Goals':
                what_you_learn = response.xpath("//div[@class='program-tab-content']")[0].css(" li::text").getall()
            else:
                what_you_learn = response.xpath("//div[@class='program-tab-content']")[1].css(" li::text").getall()
        what_you_learn = " |".join(what_you_learn)
        #Dates
        if response.xpath("//h2[contains(text(), 'Important Dates')]"):
            appl_startdate = response.xpath("//li[@class='unprocess_wrap']/ ..//li")[0].css(" ::text").getall()
            appl_deadline = response.xpath("//li[@class='unprocess_wrap']/ ..//li")[1].css(" ::text").getall()
            appl_startdate = appl_startdate[0] + " " + appl_startdate[2]
            appl_deadline = appl_deadline[0] + " " + appl_deadline[2]
            appl_startdate = appl_startdate.replace("Applications Open: ","")
            appl_deadline = appl_deadline.replace("Applications Close: ","")
            appl_startdate = str(parse(appl_startdate))
            appl_deadline = str(parse(appl_deadline))
        else:
            appl_startdate = 'N/A'
            appl_deadline = 'N/A'
        #Bronchure
        if response.xpath("//*[contains(text(), 'View Brochure')] | //*[contains(text(), 'View brochure')] | //*[contains(text(), 'Download program structure ')]"):
            brochure = response.xpath("//*[contains(text(), 'View Brochure')]//@href | //*[contains(text(), 'View brochure')]//@href | //*[contains(text(), 'Download program structure')]//following-sibling::a//@href").get()
        else:
            brochure = "N/A"
        #Curriculum
        modules = "N/A"
        submodules = []
        if response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()"):
            modules = "N/A"
        elif response.xpath("//li[@class='program-tab-title']/a/text()")[2].get()=='Curriculum':
            modules = response.xpath("//div[@class='program-tab-content']")[2].css("ul li.tab-title a::text").getall()
        else:
            modules = response.xpath("//div[@class='program-tab-content']")[3].css("ul li.tab-title a::text").getall()
        #submodules
        if response.xpath("//*[contains(text(), 'Why FPM?')]/..//li/text()"):
            submodules = "N/A"
        elif response.xpath("//h5[contains(text(), 'Electives')]"):
                for i in range(len(modules)):
                    sub = response.xpath("//h5[contains(text(), 'Core Courses')]//following-sibling::div[1]")[i].css("ul li::text").getall()
                    submodules.append(sub)
        elif response.xpath("//li[@class='program-tab-title']/a/text()")[2].get()=='Curriculum':
            for i in range(len(modules)):
                sub = response.xpath("//div[@class='program-tab-content']")[2].css("div.tab-content")[i].css("ul li::text").getall()
                submodules.append(sub)
        elif response.xpath("//li[@class='program-tab-title']/a/text()")[3].get()=='Curriculum':
            for i in range(len(modules)):
                sub = response.xpath("//div[@class='program-tab-content']")[3].css("div.tab-content")[i].css(" span::text").getall()
                sub = [ele for ele in sub if ele not in ('Electives 1 - Choose from one of the 2 sets','Electives 2 - open to choose from the list','Projects and MOOCs','Foundation Courses','Core Courses')]
                submodules.append(sub)
        #
        if modules == "N/A":
            curriculum = "N/A"
        else:
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<module{modulenum}><heading>{modules[i]}</heading>"
                modlist.append(mod)
                modlist.append("<subheading>")
                submodnum = 1
                for j in submodules[i]:
                    submod = f"<item{submodnum}>{j}</item{submodnum}>"
                    modlist.append(submod)
                    submodnum += 1
                modlist.append("</subheading>")
                modlist.append(f"</module{modulenum}>")
                modulenum +=1
            modlist.insert(0, "<mainmodule>")
            modlist.append("</mainmodule>")
            modlist.insert(0, '<?xml version="1.0"?>')
            curriculum = "".join(modlist)
        curriculum = curriculum.replace("&", "&amp;")

        yield {
            'Name':title,
            'Link':link,
            'Description':description,
            'Short Description':short_description,
            'Course Duration':duration,
            'Course Type':course_type,
            'Student Intake': student_intake,
            'What You will learn':what_you_learn,
            'Target Students': target_students,
            'Application Start Date': appl_startdate,
            'Application Deadline':appl_deadline,
            'Curriculum':curriculum,
            'Brochure':brochure,
            'Instructor Name':instructor_name,
            'Instructor Expertise': instructors_expertise,
            'Instructor Picture': instructor_pic,
            'Reviews Name': review_name,
            'Review': reviews,
            'Review Picture':review_pic,
            'FAQ Ques': faq_q,
            'FAQ Ans': faq_a,
            }