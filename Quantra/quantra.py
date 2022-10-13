from bs4 import BeautifulSoup
import scrapy
import json
import re
import time

class MyprojectSpider(scrapy.Spider):

    name = "quantsi" 

    def start_requests(self):

            link = 'https://quantra-api-elb.quantinsti.com/v2/courses'

            yield scrapy.Request(url=link, callback=self.parse)



    def parse(self, response):
        allcourses = response.text
        allcourses = json.loads(allcourses)

        allcourses = allcourses['courseList']
        print(allcourses[1])

        for course in allcourses:

            cid = course['courseId']
            title = course['courseName']
            url = course['url']
            if url == None: url = ''
            skills = course['technologiesCovered']

            faq_url = f'https://quantra-api-elb.quantinsti.com/v2/faqs?type=course&courseId={cid}'

            yield scrapy.Request(url=faq_url, callback=self.faqdata, cb_kwargs={'title': title, 'cid': cid, 'skills': skills, 'partnerurl': url})
            # yield scrapy.Request(url=url, callback=self.coursedata, cb_kwargs={'title': title, 'skills': skills, 'cid': cid})


    def faqdata(self, response, cid, title, skills, partnerurl):

        faqs = response.text
        faqs = json.loads(faqs)

        faqs_list = list()

        for i in faqs:
            question = i['question']
            answer = i['answer']

            faqs_list.append(question)
            faqs_list.append(answer)

        if faqs != []:
            faqs = "|".join(faqs_list)

        try:
            faqs = re.sub('<.*?>', '', faqs)
        except:
            faqs = ''
        
        details_url = f'https://quantra-api-elb.quantinsti.com/v2/course-meta/{cid}'
        
        yield scrapy.Request(url=details_url, callback=self.detailsdata, cb_kwargs={'title': title, 'skills': skills, 'cid': cid, 'faqs': faqs, 'partnerurl': partnerurl})




    def detailsdata(self, response, title, skills, cid, faqs, partnerurl):

        details = response.text
        details = json.loads(details)

        details = details['courseMeta']

        preq = details['prerequisites'].strip()
        preq = re.sub('<p>|</p>', '', preq)
        preq = preq.split('.')
        
        try:
            wwl = details['liveTradingSection']['content']
            wwl_list = list()
            if '<ul>' in wwl:
                wwl = BeautifulSoup(wwl, "html.parser")
                wwl = wwl.find_all('li')
                for line in wwl:
                    line = line.text.strip()
                    wwl_list.append(line)

            wwl = wwl_list
            # print(wwl)
            # time.sleep(1)
    
        except:
            wwl = ''

        reviews_url = f'https://quantra-api-elb.quantinsti.com/v2/course-testimonials?courseId={cid}'

        yield scrapy.Request(url=reviews_url, callback=self.reviewsdata, cb_kwargs={'title': title, 'skills': skills, 'cid': cid, 'faqs': faqs, 
        'preq': preq, 'wwl': wwl, 'partnerurl': partnerurl})


    def reviewsdata(self, response, title, skills, cid, faqs, preq, wwl, partnerurl):
        

        reviews = response.text
        reviews = json.loads(reviews)
        rev_limit = 1

        reviewer_name = ''
        reviewer_photo = ''
        review = ''
        review_date = ''
        reviewer_rating = ''

        rnames = list()
        rphoto = list()
        rreview = list()
        rrating = list()
        rdate = list()

        for rev in reviews['testimonialList']:
            if rev_limit == 11: break

            name = rev['name']
            rnames.append(name)

            photo = rev['image']
            if photo == None: photo = '' 
            rphoto.append(photo)

            review = rev['testimony']
            review = re.sub('<.*?>', '', review)
            rreview.append(review)

            rating = rev['rating']
            try:
                rating = str(rating)
            except:
                rating = ''
            rrating.append(rating)

            date = rev['created_at']
            if date == None: date = ''
            rdate.append(date)

            rev_limit += 1

        try:
            reviewer_name = "|".join(rnames)
            reviewer_photo = "|".join(rphoto)
            review = "|".join(rreview)
            review_date = "|".join(rdate)
            reviewer_rating = "|".join(rrating)
        except:
            pass

        course_url = f'https://quantra-api-elb.quantinsti.com/getCourseDetailsById/{cid}'

        yield scrapy.Request(url=course_url, callback=self.coursedata, cb_kwargs={'title': title, 'skills': skills, 'cid': cid, 'faqs': faqs, 
        'preq': preq, 'wwl': wwl, 'reviewer_name': reviewer_name, 'reviewer_photo': reviewer_photo, 'review': review, 'review_date': review_date,
        'reviewer_rating': reviewer_rating, 'partnerurl': partnerurl})


    def coursedata(self, response, title, skills, cid, faqs, wwl, preq, reviewer_name, reviewer_photo, review, review_date, reviewer_rating, partnerurl):

        data = response.text
        data = json.loads(data)

        learn_type = 'Certification'

        delivery_method = 'Online'

        description = data['result']['courseDescription']
        short_description = description.split('.')[0]

        totaldurr = data['result']['totalDuration']
        totaldurr = totaldurr.split(' ')
        total_duration_unit = totaldurr[1]
        total_duration = totaldurr[0]

        level = data['result']['levelName']

        sale_price = float(data['result']['Amount'])
        regular_price = float(data['result']['amount_actual'])

        usa_sale_price = float(data['result']['amount_usd'])
        usa_regular_price = float(data['result']['amount_actual_usd'])

        other_sale_price = float(data['result']['amount_usd_developing_nations'])
        other_regular_price = float(data['result']['amount_actual_usd_developing_nations'])

        embedded_video_url = data['result']['youtube_url']

        # total_users = data['result']['total_users']



        instructors_name = list()
        instructors_bio = list()
        instructors_image = list()

        for inst in data['result']['courseAuthors']:

            name = inst['name']
            instructors_name.append(name)

            bio = inst['description']
            instructors_bio.append(bio)

            image = inst['image']
            instructors_image.append(image)

        instructor_name = "|".join(instructors_name)
        instructor_bio = "|".join(instructors_bio)
        instructor_image = "|".join(instructors_image)


        course_start_date = data['result']['start_date']


        # Content Modules
        modules = list()
        headcount = 1

        for mod in data['result']['sections']:

            header = mod['sectionName']
            header = f"<module{headcount}><heading>{header}</heading>"
            modules.append(header)
            modules.append('<subheading>')
            subcount = 1

            for submod in mod['units']:
                sub = submod['unit_name']
                sub = f"<item{subcount}>{sub}</item{subcount}>"
                modules.append(sub)
                subcount += 1

            modules.append('</subheading>')
            modules.append(f'</module{headcount}>')
            headcount += 1

        modules.insert(0, '<mainmodule>')
        modules.append('</mainmodule>')
        modules.insert(0, '<?xml version="1.0"?>')

        content_module = "".join(modules)

        url = 'https://quantra.quantinsti.com/course/' + partnerurl

        yield {'title': title, 'skills': skills, 'cid': cid, 'faqs': faqs, 'preq': preq, 'wwl': wwl, 'reviewer_name': reviewer_name, 
        'reviewer_photo': reviewer_photo, 'review': review, 'review_date': review_date,'reviewer_rating': reviewer_rating, 'learn_type': learn_type,
        'delivery_method': delivery_method, 'description': description, 'short_description': short_description, 'total_duration_unit': total_duration_unit,
        'total_duration': total_duration, 'level': level, 'sale_price': sale_price, 'regular_price': regular_price, 'embedded_video_url': embedded_video_url,
        'instructor_name': instructor_name, 'instructor_bio': instructor_bio, 'instructor_image': instructor_image, 'course_start_date': course_start_date,
        'content_module': content_module, 'partner_course_url': url}