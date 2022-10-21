from datetime import datetime
from subprocess import call
from bs4 import BeautifulSoup
import scrapy
import json
import re
import time
import ast

class MyprojectSpider(scrapy.Spider):

    name = "hh" 
    download_delay = 3

    def start_requests(self):

            link = 'https://www.henryharvin.com/our-courses'

            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        # print(len(response.xpath('//li[@id="wp-megamenu-item-7692"]//a').extract()))
          
        for link in response.xpath('//li[@id="wp-megamenu-item-7692"]//a')[:5]:
            url = link.xpath('./@href').extract_first()
            if 'tefl' in url:
                continue


            if 'https' not in  url:

                url = 'https://www.henryharvin.com/' + url

            
            yield scrapy.Request(url=url, callback=self.coursedetails)


    def brochure(self, response):

        url = response.url

        try:
            pdf = response.xpath("//a[@class='brochure-btn']/@href").extract_first()
        except:
            pdf = ''

        yield scrapy.Request(url=url, callback=self.batchdetails, cb_kwargs={'pdf': pdf})

    
    def batchdetails(self, response):

        # title = response.xpath('//h1/text()').extract_first()
        details = response.xpath("//script[@src='/js/axios.js']/following-sibling::script/text()").extract()
        details = str(details)

        # print(details)
        schedules = re.findall('"data":\[(.*?)\]', details)
        # print(schedules)

        regular_price = ''
        sale_price = ''
        regular_price_usd = ''
        add_regular_price = ''
        add_regular_price_usd = ''
        add_sale_price = ''
        batch_start_date = ''
        batch_end_date = ''
        batch_start_time = ''
        batch_end_time = ''
        pricing_type = ''
        batch_type = ''

        price_type = list()
        btype = list()
        add_regprice = list()
        add_regprice_usd = list()
        add_sprice = list()
        batch_sdate = list()
        batch_edate = list()
        batch_stime = list()
        batch_etime = list()
        

        for batch in schedules:

            batch = ast.literal_eval(batch)



            if type(batch) == tuple:
                
                for item in batch:

                    if item['batch_timing'] == 'Timing': 
                        regular_price = item['batch_price']
                        regular_price_usd = item['batch_price_option']
                        continue

                    add_regular_price = item['batch_price']
                    add_regprice.append(str(add_regular_price))

                    add_regular_price_usd = item['batch_price_option']
                    add_regprice_usd.append(str(add_regular_price_usd))

                    add_sale_price = add_regular_price
                    add_sprice.append(str(add_sale_price))


                    if int(regular_price) <= 0 or regular_price == '':
                        pricing_type = ''
                    else:
                        pricing_type = 'Paid'

                    price_type.append(pricing_type)


                    batch_start_date = item['batchDate']
                    batch_start_date = datetime.strptime(batch_start_date, '%d %B %Y')
                    batch_type_check = batch_start_date
                    batch_start_date = batch_start_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    batch_sdate.append(batch_start_date)


                    weeknum = batch_type_check.weekday()
                    if weeknum >= 0 and weeknum <= 4:
                        batch_type = 'Weekday (Mon - Fri)'
                        btype.append(batch_type)
                    elif weeknum == 5 or weeknum == 6:
                        batch_type = 'Weekend (Sat - Sun)'
                        btype.append(batch_type)


                    batch_end_date = item['batchEndDate']
                    batch_end_date = datetime.strptime(batch_end_date, '%Y-%m-%d')
                    batch_end_date = batch_end_date.strftime('%Y-%m-%dT00:00:00.000Z')
                    batch_edate.append(batch_end_date)



                    timings = item['batch_timing']
                    timings = timings.split('-')

                    try:
                        batch_start_time = timings[0]
                        batch_start_time = datetime.strptime(batch_start_time, "%I:%M%p")
                        batch_start_time = datetime.strftime(batch_start_time, "%H:%M")
                        batch_start_time = batch_start_time+":00"
                    except:
                        batch_start_time = ''
                    batch_stime.append(batch_start_time)
                    

                    try:
                        batch_end_time = timings[1]
                        batch_end_time = datetime.strptime(batch_end_time, "%I:%M%p")
                        batch_end_time = datetime.strftime(batch_end_time, "%H:%M")
                        batch_end_time = batch_end_time+":00"
                    except:
                        batch_end_time = ''
                    batch_etime.append(batch_end_time)

            else:

                regular_price = batch['batch_price']
                regular_price_usd = batch['batch_price_option']



        sale_price = regular_price


        batch_start_date = '|'.join(batch_sdate)
        batch_end_date = '|'.join(batch_edate)
        batch_start_time = '|'.join(batch_stime)
        batch_end_time = '|'.join(batch_etime)
        pricing_type = '|'.join(price_type)
        add_regular_price = '|'.join(add_regprice)
        batch_type = '|'.join(btype)
        add_sale_price = '|'.join(add_sprice)

        add_regular_price_usd = '|'.join(add_regprice_usd)

        # print({'regprice': regular_price, 'saleprice': sale_price, 'regusd': regular_price_usd, 'bsdate': batch_start_date,
        # 'bedate': batch_end_date, 'bstime': batch_start_time, 'betime': batch_end_time, 'ptype': pricing_type, 'addreg': add_regular_price,
        # 'addsale': add_sale_price, 'btype': batch_type})

        yield {'regular_price': regular_price, 'sale_price': sale_price, 'regular_price_usd': regular_price_usd,
        'batch_start_date': batch_start_date, 'batch_end_date': batch_end_date, 'batch_start_time': batch_end_time,
        'pricing_type': pricing_type, 'additional_batch_regular_price': add_regular_price, 'batch_type': batch_type, 
        'additional_batch_sale_price': add_sale_price}


    def coursedetails(self, response):

        url = response.url

        title = ''
        short_desc = ''

        title = response.xpath('//h1/text()').extract_first()
        
        short_desc = response.xpath("//p[@style='font-size: 14px; color:white;']/text()").extract_first()

        try:
            durcheck = response.xpath("//div[@class='price-wrap']//div[@class='price-card'][4]/span/text()").extract_first()
            if 'period' in durcheck.lower().strip():
                duration = response.xpath("//div[@class='price-wrap']//div[@class='price-card'][4]/h4/text()").extract_first()
                duration = duration.split(' ')

                duration_unit = duration[1]
                duration = duration[0]
        except:
            duration_unit = ''
            duration = ''

        desc = response.xpath("//div[@class='content-div']//p/text()").extract()
        description = list()
        for para in desc:
            para = re.sub('\\xa0●|\\xa0|\r|\n', '', para)
            # if para == 'Become a part of the' in para or '3,00,000+ strong Alumni' in para or 'Gold Membership of Henry Harvin' in para: continue
            description.append(para)

        description = " ".join(description)
        description = description.strip()
        if description == "": description = short_desc

        description = '<p>'+description+'</p>'.strip()

        # if description == '<p></p>':
        #     description = '<p>'+short_desc+'</p>'


        wwl = response.xpath("//div[@class='content-div']/h3[contains(text(), 'Learning')]/following-sibling::ul").extract()
        try:
            wwl = BeautifulSoup(wwl[0], 'html.parser')
            wwl = wwl.find_all('li')
            what_youll_learn = list()
            for item in wwl:
                what_youll_learn.append(item.text.strip())
        except:
            wwl = response.xpath("//div[@class='content-div']//p[preceding-sibling::h3[contains(text(), 'Learning')] and following-sibling::h3]").extract()
            what_youll_learn = list()
            wwlcount = 1
            for item in wwl:
                if wwlcount == 11: break
                item = BeautifulSoup(item, 'html.parser')
                item = item.text.strip()
                item = re.sub('●|\xa0', '', item)
                what_youll_learn.append(item)
                wwlcount += 1

        wwl = what_youll_learn


        # content
        content = response.xpath("//div[@class='accordion-item ne_dee']")
        content_list = list()
        headcount = 1
        conv_to_old = False
        try:
            for mod in content:

                heading = mod.xpath(".//a/text()").extract_first()
                heading = re.sub('^\w+ \d+:', '', heading)
                heading = f"<module{headcount}><heading>{heading.strip()}</heading>"
                content_list.append(heading)

                content_list.append("<subheading>")
                subcount = 1
                submods = mod.xpath(".//div[@class='sub_mod']/strong/text()").extract()
                if submods == []:
                    try:
                        submods_list = list()
                        submods = mod.xpath(".//div[@class='module-topics']//ul").extract_first()
                        if submods != None:
                            submods = BeautifulSoup(submods, 'html.parser')
                            submods = submods.find_all('li')
                            for item in submods:
                                item = item.text.strip()
                                item = re.sub('<p>.*|^\w+ \d+:', '', item)
                                item = item.strip()
                                submods_list.append(item)

                            submods = submods_list
                        else:
                            submods = mod.xpath(".//div[@class='module-topics']//p/text()").extract()
                    except:
                        submods = mod.xpath(".//div[@class='module-topics']//p/text()").extract()

                for sub in submods:
                    sub = re.sub('\xa0|•', '', sub)
                    sub = f"<item{subcount}>{sub.strip()}</item{subcount}>"
                    if sub == f"<item{subcount}></item{subcount}>":
                        conv_to_old = True
                    content_list.append(sub)
                    subcount += 1
                    
                content_list.append("</subheading>")
                content_list.append(f"</module{headcount}>")
                headcount += 1

            content_list.insert(0, "<mainmodule>")
            content_list.append("</mainmodule>")
            content_list.insert(0, '<?xml version="1.0"?>')

            content = "".join(content_list)

            if conv_to_old == True:
                content = response.xpath("//div[@class='accordion-item ne_dee']")
                content_list = list()
                headcount = 1

                for mod in content:
                    heading = mod.xpath(".//a/text()").extract_first()
                    heading = re.sub('^\w+ \d+:|^\w+ \d+ :|^\w+\d+:|^\w+\d+ :', '', heading)
                    heading = f"<p><strong>Module {headcount}: </strong>{heading.strip()}</p>"
                    content_list.append(heading)
                    headcount += 1
                    
                content = "".join(content_list)
        except:

            content_list = list()
            headcount = 1

            for mod in content:
                heading = mod.xpath(".//a/text()").extract_first()
                heading = re.sub('^\w+ \d+:|^\w+ \d+ :|^\w+\d+:|^\w+\d+ :', '', heading)
                heading = f"<p><strong>Module {headcount}: </strong>{heading.strip()}</p>"
                content_list.append(heading)
                headcount += 1
                
            content = "".join(content_list)




            # Skills
            skills = ''
            skills = response.xpath("//h2[@class='head-title']//following-sibling::div//p[@class='skill_cover']/text()").extract()

            
            # Reviews
            try:
                reviewer_image = response.xpath("//div[@class='review-item']//div//img/@src").extract()
                reviewer_image = list(set(reviewer_image))
                reviewer_image = "|".join(reviewer_image)
            except:
                reviewer_image = ''

            try:
                reviewer_name = response.xpath("//div[@class='review-item']//div[@class='col-lg-8']//span[@class='name']/text()").extract()
                reviewer_name = list(set(reviewer_name))
                reviewer_name = "|".join(reviewer_name)
                reviewer_name = reviewer_name.replace('\xa0', '')
            except:
                reviewer_name = ''

            try:
                review = response.xpath("//div[@class='review-item']//p[@style='text-align: justify;']/text()").extract()
                review = list(set(review))
                review = "|".join(review)
                review = review.replace('\xa0', '')
            except:
                review = ''



            # FAQS
            questions = response.xpath("//section[@id='faq']//a[@class='accordian-toggle']/text()").extract()
            questions = "|".join(questions)
            questions = questions.replace('\xa0', '')

            answers = response.xpath("//section[@id='faq'//div[@class='accordion-content']//p[@dir='ltr']/span/text()").extract()
            answers = '|'.join(answers)
            answers = answers.replace('\xa0', '')


            # Instructors
            instructor_name = response.xpath('//section[@id="our-trainer"]//div[@class="trainer-profile"]//following-sibling::h4/text()').extract()
            instructor_name = "|".join(instructor_name)

            instructor_image = response.xpath('//section[@id="our-trainer"]//div[@class="trainer-profile"]//img/@src').extract()
            instructor_image = "|".join(instructor_image)
            instructor_image = re.sub('\r|\n', '', instructor_image)

            instructor_bio = response.xpath("//section[@id='our-trainer']//div[@class='trainer-profile']//following-sibling::p/text()").extract()
            instructor_bio = "|".join(instructor_bio)
            instructor_bio = re.sub('\r|\n', '', instructor_bio)


        yield {'ur': url, 'title': title, 'short_desc': short_desc, 'duration': duration, 'duration_unit': duration_unit, 
        'description': description, 'what_youll_learn': wwl, 'content': content}

