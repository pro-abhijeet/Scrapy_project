import scrapy
import json
import operator
import pandas
import re


class Spyder3Spider(scrapy.Spider):
    name = "guvi"
    start_urls = [
        "https://www.guvi.in/courses"
    ]



    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'authority': 'www.guvi.in' ,
                 'accept': '*/*',
                 'accept-language': 'en-US,en;q=0.9',
                 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'cookie': '_gid=GA1.2.484299214.1665058674; _gcl_au=1.1.823907283.1665058674; _fbp=fb.1.1665058674792.24615472; ORG50223=0490f33a-012a-42fe-bfe1-9524d0bf8504; __stgeo="0"; __stdf=0; USER_DATA=%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%22e9e0fab3-eca2-4666-b44e-9b6cf401fd0c%22%2C%22deviceAdded%22%3Atrue%7D; first_url=https://www.guvi.in/automation-testing-with-selenium?utm_source=GUVI-Website&utm_medium=Homepage-Breadcrumbs&utm_campaign=AT-Homepage-Breadcrumbs; final_url=https://www.guvi.in/automation-testing-with-selenium?utm_source=GUVI-Website&utm_medium=Homepage-Breadcrumbs&utm_campaign=AT-Homepage-Breadcrumbs; deduplication_cookie=GUVI-Website; deduplication_cookie=GUVI-Website; _cc_id=10aab9d0b27432f37ca16d77b5166400; HARD_ASK_STATUS=%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; MXCookie=MXCookie; moe_uuid=e9e0fab3-eca2-4666-b44e-9b6cf401fd0c; _clck=1aw7l3a|1|f5i|0; __stp={"visit":"returning","uuid":"91505573-d392-4e22-8d29-574248176fa7"}; __stbpnenable=0; SETUP_TIME=1665154081089; panoramaId_expiry=1665247727736; mp_74656ccf168534edf5fa89bedde46fb3_mixpanel=%7B%22distinct_id%22%3A%20%22183ad3b209017-0d67f926f8b9b1-11462c6d-144000-183ad3b2091e77%22%2C%22%24device_id%22%3A%20%22183ad3b209017-0d67f926f8b9b1-11462c6d-144000-183ad3b2091e77%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.guvi.in%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.guvi.in%22%2C%22utm_source%22%3A%20%22GUVI-Website%22%2C%22utm_medium%22%3A%20%22Homepage-Breadcrumbs%22%2C%22utm_campaign%22%3A%20%22AT-Homepage-Breadcrumbs%22%7D; _gat=1; lotame_domain_check=guvi.in; _clsk=1gvv6r3|1665174142947|10|1|b.clarity.ms/collect; __sts={"sid":1665172699335,"tx":1665174143030,"url":"https%3A%2F%2Fwww.guvi.in%2F","pet":1665174143030,"set":1665172699335,"pUrl":"https%3A%2F%2Fwww.guvi.in%2Fcourses%2FseleniumAutomationPythonEng%3Fitm_source%3Dcourses_page%26itm_medium%3Dclick","pPet":1665173591767,"pTx":1665173591767}; _ga=GA1.2.2027221331.1665058674; _gat_UA-53114947-1=1; _ga_NSG5GX8MNW=GS1.1.1665172700.6.1.1665174145.0.0.0',
                 'origin: https://www.guvi.in' 
                 'referer': 'https://www.guvi.in/courses',
                 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                 'sec-ch-ua-platform': "Linux",
                 'sec-fetch-dest': 'empty',
                 'sec-fetch-mode': 'cors' ,
                 'sec-fetch-site': 'same-origin', 
                 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
                 'x-requested-with: XMLHttpRequest'}




                 
    """def start_requests(self):
        url = "https://www.guvi.in/courses"
        yield scrapy.Request(url)"""



    def parse(self, response):
        url = "https://www.guvi.in/model/v2/courseFetchByCategory.php"
        payload = "myData=%7B%22requestType%22%3A%22allCourses%22%2C%22authtoken%22%3Anull%2C%22originUrl%22%3A%22www.guvi.in%22%7D"
        yield scrapy.Request(url,method='POST',body=payload, headers=self.headers,callback=self.parser_contents)



    def parser_contents(self, response):
        data = json.loads(response.body)
        a = (data['allCourses']['courses'])
        for i in a:
            if (i["courseType"]=="Premium"and i['lang']=="English"):
                ckey = i['ckey']
                c_name = i['cname']
                language = i['lang']
                duration = i['duration']
                price = i['price']
                st_enrolled = i['enrolled']
                disc_price = i['discountPrice']
                url = "https://www.guvi.in/model/v2/course_details.php"
                payload = f'myData=%7B%22requestType%22%3A%22details%22%2C%22key%22%3A%22{ckey}%22%2C%22source%22%3Afalse%2C%22medium%22%3Afalse%2C%22campaign%22%3Afalse%2C%22authtoken%22%3Anull%2C%22originUrl%22%3A%22www.guvi.in%22%7D'
                yield scrapy.Request(url,method='POST',body=payload, headers=self.headers,callback=self.parser_contents1, cb_kwargs={'c_name':c_name,'price':price,'disc_price':disc_price,'ckey':ckey,'language':language, 'duration':duration,'st_enrolled':st_enrolled})
    
    
    
    def parser_contents1(self, response,ckey, c_name, price, disc_price,language,duration,st_enrolled):
        data = json.loads(response.body)
        l = (data['details'])
        description = l[0]['description']
        short_description = re.search("^(.*?)[\.]", description).group(1) + "."
        description = "<p>" + description + "<\p>"
        instructor_name = l[0]['author']['name']
        instructor_about = l[0]['author']['description']
        who_should_enroll = l[0]['who_can_take']
        who_should_enroll = " |".join(who_should_enroll)
        what_you_will_achieve = l[0]['achieve']
        what_you_will_achieve = " |".join(what_you_will_achieve)
        a = operator.itemgetter('reviews')
        topics = list(map(a, l))
        sum1=0
        sum2= 0
        for i in topics[0]:
            a = int(i['total'])
            b = int(i['rating'])
            sum1 += a*b
            sum2 += a
        if sum2!=0:
            rating = round(sum1/sum2, 1)
        else:
            rating = '4.1'
        url = "https://www.guvi.in/model/v2/course_content.php"
        payload = f'myData=%7B%22type%22%3A%22preview%22%2C%22courseId%22%3A%22{ckey}%22%2C%22authtoken%22%3Anull%7D'
        yield scrapy.Request(url,method='POST',body=payload, headers=self.headers,callback=self.parser_contents2, cb_kwargs={'c_name':c_name,'price':price,'disc_price':disc_price,'ckey':ckey, 'language':language,'duration':duration,'rating':rating,'st_enrolled':st_enrolled,'description':description, 'short_description':short_description,'who_should_enroll':who_should_enroll,'what_you_will_achieve':what_you_will_achieve,'instructor_name':instructor_name,'instructor_about':instructor_about})
    
    
    
    def parser_contents2(self, response,ckey, c_name, price, disc_price, language,duration,rating,st_enrolled,description,short_description,instructor_name,instructor_about,what_you_will_achieve,who_should_enroll):
        data = json.loads(response.body)
        x = (data['data'])
        data2 = json.loads(x)
        l = (data2['previewData'])
        l = l[1:]
        a = operator.itemgetter('level') 
        b = operator.itemgetter('topic')
        levels = list(map(a, l))
        topics = list(map(b, l))
        dict = {'Mod': levels, 'Submod': topics}
        df = pandas.DataFrame(dict)
        syllabus = df.groupby('Mod')['Submod'].apply(list).to_dict()
        modules = list(syllabus.keys())
        for i in range(len(modules)):
            if modules[i]=='l1':
                modules[i] = 'Beginner Module'
            elif modules[i]=='l2':
                modules[i] = 'Intermediate Module'
            elif modules[i] == 'l3':
                modules[i] = 'Advanced Module'
            else:
                modules[i] = 'Expert Module'
        submodules = list(syllabus.values())
        c_link = f"https://www.guvi.in/courses/{ckey}"
        yield scrapy.Request(url= c_link, callback=self.parser_contents3, cb_kwargs={'c_name':c_name,'price':price,'disc_price':disc_price,'modules':modules, 'submodules':submodules, 'language':language,'duration':duration,'rating':rating,'st_enrolled':st_enrolled,'description':description,'short_description':short_description,'who_should_enroll':who_should_enroll,'what_you_will_achieve':what_you_will_achieve,'instructor_name':instructor_name,'instructor_about':instructor_about})
        
    
    
    def parser_contents3(self,response, c_name, price, disc_price,modules,submodules, language,duration,rating,st_enrolled,description,short_description,instructor_name,instructor_about,what_you_will_achieve,who_should_enroll):
        faq_q = response.css(".col-lg-8").css(".accordion-button div::text").getall()
        faq_a = response.css(".col-lg-8").css(".faQ_body::text").getall()
        faq_q = " |".join(faq_q)
        faq_a = " |".join(faq_a)
        link = response.request.url
        duration = str(duration) + " hrs"
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
        content = "".join(modlist)
        
        
        
        yield {
            'Name': c_name,
            'Link':link,
            'Short Description':short_description,
            'Description':description,
            'Language':language,
            'Ratings':rating,
            'Course Duration':duration,
            'Discount Price':disc_price,
            'Original Price':price,
            'Students Enrolled':st_enrolled,
             'What you will achieve': what_you_will_achieve,
            'Who should Enroll':who_should_enroll,
            'Instructor Name':instructor_name,
            'Instructor About': instructor_about,
            'Curriculum':content,
            'FAQ Questions': faq_q,
            'FAQ Answers': faq_a
        }