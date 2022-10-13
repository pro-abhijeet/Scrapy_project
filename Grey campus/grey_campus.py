from ctypes.wintypes import tagMSG, tagRECT
import scrapy
import re
from bs4 import BeautifulSoup


class GreyCapmus(scrapy.Spider):
    name = 'grey'
    allowed_domains = ['www.greycampus.com']
    def start_requests(self):
            url = "https://www.greycampus.com"    
            yield scrapy.Request(url)
    def parse(self, response):
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[1]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents1)
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[2]/div/div[2]/ul//li//@href").getall():
           yield scrapy.Request(response.urljoin(link), callback=self.parser_contents2)
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[3]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents3)
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[4]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents4)
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[5]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents5)
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[6]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents3) # no course in this section
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[7]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents7)
        
        for link in response.xpath("//*[@id='hs_cos_wrapper_All_courses']/div/ul/li[8]/div/div[2]/ul//li//@href").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parser_contents8)
        
        
    def parser_contents1(self, response):
        #links
        links = response.request.url
        if links != 'https://www.greycampus.com/enterprise':
            # Title
            title = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/h1//span//text()").getall()
            title = " ".join(title)
            #Short Description
            short_desc = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/p[1]/span/text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            short_desc = [ele for ele in short_desc if ele.strip()]
            short_desc = " ".join(short_desc)
            #Description
            cond = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-8_']/h2//text()").get()
            if  cond is not None and ('program overview' in cond.lower() or 'about' in cond.lower() or 'exam' in cond.lower()):
                description = response.xpath("//*[@id='Second']//div//div/span//text() | //*[@id='Second']//div//div/p//text() | //*[@id='Second_1']/div//div/text() | //*[@id='scrollspy1_1']/div/p//text()").getall()
                description = [ele for ele in description if ele.strip()]
                description = " ".join(description)
            else:
                description = short_desc
                x = ""
                for i in short_desc:
                    if i==".":
                        break
                    else:
                        x = x + i
                short_desc = x
            if description == "":
                description = short_desc
                x = ""
                for i in short_desc:
                    if i==".":
                        break
                    else:
                        x = x + i
                short_desc = x
            if title == 'Project Management Fundamentals':
                description = short_desc
                x = ""
                for i in short_desc:
                    if i==".":
                        break
                    else:
                        x = x + i
                short_desc = x
            description = '<p>' + description + '</p>'
            #Faq_q
            faq_q = []
            faq_a = [] 
            for i in range(1,len(response.xpath("//*[@id='registration']/div | //*[@id='hs_cos_wrapper_dnd_area-module-53']/div/div | //*[@id='certification']/div | //*[@id='first']/div | //*[@id='FAQ']/div"))-1):    
                x =response.xpath(f"//*[@id='certificationheading{i}']/button//text() | //*[@id='heading{i}']/button//text() | //*[@id='FAQheading{i}']/button//text() | //*[@id='registrationheading{i}']/button//text() | //*[@id='firstheading{i}']/button//text()").get()
                if x is not None:
                    x = x.strip()
                    faq_q.append(x)
                     
                if not response.xpath(f"//*[@id='certificationcollapse{i}']//table | //*[@id='FAQcollapse{i}']//table"):
                    ans = response.xpath(f"//*[@id='registrationcollapse{i}']//text() | //*[@id='certificationcollapse{i}']//text() |//*[@id='collapse{i}']//text() | //*[@id='FAQcollapse{i}']//text() | //*[@id='firstcollapse{i}']//text()").getall()
                    ans = [ele for ele in ans if ele.strip()]
                    ans = " ".join(ans)
                    faq_a.append(ans)
                else:
                    faq_a.append("N/A")
            if title=='ITIL® 4 Foundation Training and Certification':
                faq_q=[]
                faq_a=[]
                for i in range(1,len(response.xpath("//*[@id='registration']/div"))):
                    x =response.xpath(f"//*[@id='registrationheading{i}']/button//text()").get()
                    if x is not None:
                        x = x.strip()
                        faq_q.append(x)
                    ans = response.xpath(f"//*[@id='registrationcollapse{i}']/div//text()").getall()
                    ans = [ele for ele in ans if ele.strip()]
                    ans = " ".join(ans)
                    faq_a.append(ans)
            #print(len(faq_q))
            #print(len(faq_a))
            if len(faq_q) > 1:
                faq_q = " |".join(faq_q)
                faq_a = " |".join(faq_a)
            faq_q = re.sub("Q\.", "", faq_q)
            faq_q = re.sub("Q\:", "", faq_q)
            faq_a = re.sub("A\.", "", faq_a)
            faq_a = re.sub("A\:", "", faq_a)
            #print(len(faq_a))
            #print(len(faq_q))
            #syllabus
            modules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                modules.append(response.xpath(f"//*[@id='curriculumheading{i}']/button//text()").get().strip())
            modules = list(map(lambda a:a.strip(), modules))
            modules = list(map(lambda a:re.sub("(^\d*)", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            modules = list(map(lambda a:re.sub("(^Lesson\W\d\:)","", a), modules))
            submodules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                x = response.xpath(f"//*[@id='curriculumcollapse{i}']/div//text()").getall()
                x = [ele for ele in x if ele.strip()]
                x = list(map(lambda a:re.sub("[a-g]\.", "", a), x))
                x = list(map(lambda a:re.sub("^\d\W", "", a), x))
                x = list(map(lambda a:re.sub("^\d", "", a), x))
                submodules.append(x)

            #print(modules)
            #print(submodules)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            curriculum = "".join(modlist)
            x = response.xpath("//*[@id='Second_1']/div/ul/li[1]/text()").get()
            if x is not None:
                if (re.search('hours', x) or re.search('days', x)) is not None:
                    x = response.xpath("//*[@id='Second_1']/div/ul/li[1]/text() | //*[@id='Second_1']/div/p[1]//text()").get()
                    duration = (re.search("(^\d.*days)", x)).group()
            else:
                duration = 'N/a'

            #What you will Learn
            if 'Introduction' in modules:
                modules.remove('Introduction')
            if 'Course Introduction' in modules:
                modules.remove('Course Introduction')
            if 'Course Overview' in modules:
                modules.remove('Course Overview')
            what_will_learn = ['You will learn '+ ele for ele in modules]
            what_will_learn = " |".join(what_will_learn)
            #reviews
            rev_n = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4/text()").getall()
            rev = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div//text()").getall()
            rev_n = [ele for ele in rev_n if ele.strip()]

            rev = [ele for ele in rev if ele.strip()]
            
            if response.xpath("//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul//li[1]/div/div/div//img"):
                rating = []
                for i in range(1,len(rev)+1):
                    rat = len(response.xpath(f"//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul//li[{i}]/div/div/div//img"))
                    rating.append(rat)
                rating = list(filter(lambda a:a!=0, rating ))
                ratings = " | ".join(str(i) for i in rating)

            else:
                ratings = 'N/A'
            rev_n = " |".join(rev_n)
            rev = " |".join(rev)
            review_date = '2021-04-12'
            #Pre_requisites'
            prereq = []
            soup = BeautifulSoup(response.body,'html.parser')
            if soup.findAll(text = re.compile("Pre-requisites")):
                for i in soup.findAll(text = re.compile("Pre-requisites")):
                    prereq.append((i.find_next()).text)
                prereq = list(map(lambda a:a.strip().replace("\n\n\n\n\n\n", " | "), prereq))
                print(prereq)
                prereq = " |".join(prereq)
            else:
                prereq = 'N/A'
            target_aud = "N/A"
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'

            yield {
                "Course Title": title,
                'Links':links,
                'Short Description': short_desc,
                "Description": description,
                'Duration': duration,
                'What you will Learn': what_will_learn,
                'Pre_Requisites':prereq,  
                'Target Audience':target_aud,
                'Reviews Name': rev_n,
                'Review': rev,
                'Ratings':ratings,
                'Review Date': review_date,
                'Curriculum': curriculum,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
            }




    def parser_contents2(self, response):
        #links
        link = response.request.url
        if ((link != 'https://www.greycampus.com/enterprise') or (link != 'https://www.greycampus.com/quality-management')):
            links = link
            #Title
            x = response.css("span.hs_cos_wrapper.hs_cos_wrapper_widget.hs_cos_wrapper_type_rich_text")[0]
            if x.css("h1 span"):
                title = x.css("h1 span::text").get()
            elif x.css("h1"):
                title = x.css("h1::text").get()
            desc = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/p/text()  | //*[@id='hs_cos_wrapper_dnd_area-module-2_']/div/div/div/div/text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']/div[2]//p//text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']/p//text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']/div[2]/div/div/p/text()").getall()
            if desc is not None and len(desc)>1:
                desc = [ele for ele in desc if ele.strip()]
    
            if len(desc)==1 and desc is not None:
                short_desc = ""
                for i in desc:
                    if i=='.':
                        break
                    else:
                        short_desc = short_desc + i
            if len(desc)>1:
                short_desc = desc[0]
            desc = " ".join(desc)
            if desc=="":
                desc = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/div/p/text()").get()
                short_desc = ""
                for i in desc:
                    if i=='.':
                        break
                    else:
                        short_desc = short_desc + i
                desc = '<p>' + desc + '<\p>'
            desc = '<p>' + desc + '<\p>'

            if response.css("span.hs_cos_wrapper.hs_cos_wrapper_widget.hs_cos_wrapper_type_rich_text")[2].css("::text").get()=='Exam Insights':
                a = response.css("span.hs_cos_wrapper.hs_cos_wrapper_widget.hs_cos_wrapper_type_rich_text")[2].css("p::text").get()
                b = response.css("span.hs_cos_wrapper.hs_cos_wrapper_widget.hs_cos_wrapper_type_rich_text")[2].css("span::text").get()
                if a:
                    duration = (re.search("(..hours)", a)).group()
                elif b:
                    duration = (re.search("(..hours)", b)).group()
            elif response.xpath("//*[@id='Third_2']/h4/text()").get()=='Exam Demo':
                a = response.xpath("//*[@id='Third_2']/div/p//text()").get()
                duration = (re.search("(..day)", a)).group()
            else:
                duration = 'N/A'
            x = response.xpath("//*[@id='hs_cos_wrapper_widget_1642769334144_']/p/text()")
            #reviews
            rev_name = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4//text()").getall()
            rev_name = " |".join(rev_name)
            review = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div/p//text()").getall()
            review = " |".join(review)
            review_date = '2021-06-08'
            ratings = 'N/A' 
            #Syllabus
            modules = response.css(".dnd_area-row-3-background-color").css(".collapsed::text").getall()
            modules = list(map(lambda a:a.strip(), modules))
            modules = list(map(lambda a:re.sub("(^\d*\.)","", a), modules))
            modules = list(map(lambda a:a.strip(), modules))

            submodules = []
            for i in range(1,len(modules)+1):
                if response.xpath("//*[@id='Curriculum']"):
                    x = response.xpath(f"//*[@id='Curriculumcollapse{i}']")[0].css(" ::text").getall()
                else:
                    x = response.xpath(f"//*[@id='firstcollapse{i}']")[0].css(" ::text").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            #syllabus
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            content = "".join(modlist)
            #What you will learn
            modules = [ele for ele in modules if ele!="Course Overview"]
            modules = list(map(lambda a:re.sub("(^Module*\ \d)","", a), modules))
            modules = [ele for ele in modules if ele.strip()]
            if len(modules)==0:
                what_will_learn = 'N/A'
            else:
                what_will_learn = ['You will learn '+ ele for ele in modules]
                what_will_learn = " |".join(what_will_learn)
            # FAQ
            soup = BeautifulSoup(response.body, "html.parser")
            faq_q = []
            faq_a = []
            for soup1 in soup.find_all('h2',{'class':'accordion-header bg-dark'}):
                for i in soup1.findAll('button', text=re.compile("(Q\.\ |Q\:\ )")):
                    faq_q.append(i.text)
                    faq_a.append(i.find_next().text)
            if soup.findAll('h2', text=re.compile("(FAQs)")):
                for soup1 in soup.find_all('h2',{'class':'accordion-header bg-dark'}):
                    for i in soup1.findAll('button', text=re.compile("([1-9][.])")):
                        faq_q.append(i.text)
                        faq_a.append(i.find_next().text)
            faq_q = list(map(lambda a:a.strip(), faq_q))
            faq_q = list(map(lambda a:re.sub("(^\d\W|^\w\W)", "", a), faq_q))
            faq_a = list(map(lambda a:a.strip().replace("\n", ""), faq_a))
            faq_a = list(map(lambda a:re.sub("(^\d\W|^\w\W)", "", a), faq_a))
            
            if len(faq_q) >0:
                faq_q = " |".join(faq_q)
                faq_a = " |".join(faq_a)
            else:
                faq_q = "N/A"
                faq_a = "N/A"
            prereq = [] 
            #Pre_requisites
            if soup.findAll(text = re.compile("Pre-requisites")):
                for i in soup.findAll(text = re.compile("Pre-requisites")):
                    prereq.append((i.find_next()).text)
                prereq = " |".join(prereq)
            else:
                prereq = 'N/A'
            if soup.findAll(text = re.compile("Who can do this certification?")):
                for i in soup.findAll(text = re.compile("Who can do this certification?")):
                    target_aud = i.find_next().text
            else:
                target_aud = "N/A"
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'
                 
            yield{
                'Course Title': title,
                'Links': links,
                'Short Description': short_desc,
                'Description': desc,
                'Duration': duration,
                'What you will Learn': what_will_learn,
                'Pre_Requisites': prereq,
                'Target Audience': target_aud,
                'Reviews Name': rev_name,
                'Review': review,
                'Ratings': ratings,
                'Review Date': review_date,
                'Curriculum': content,
               'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
            }
        else:
            pass




    def parser_contents3(self, response):
        #link
        link = response.request.url
        if link != 'https://www.greycampus.com/enterprise':
            links = link
            #Title
            x = response.css("span.hs_cos_wrapper.hs_cos_wrapper_widget.hs_cos_wrapper_type_rich_text")[0]
            if x.css("h1 span"):
                title = x.css("h1 span::text").get()
            elif x.css("h1"):
                title = x.css("h1::text").get()
            #reviews
            rev_name = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4//text()").getall()
            rev_name = " |".join(rev_name)
            review = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div/p//text()").getall()
            review = " |".join(review),
            ratings = 'N/A'
            review_date = '2021-05-01'
            # FAQ
            faq_q = response.xpath("//*[@id='first']")[1].css(".collapsed::text").getall()
            faq_a = []
            for i in range(len(response.xpath("//*[@id='first']")[1].css("div.accordion-item.border-0.bg-dark"))):
                x = response.xpath("//*[@id='first']")[1].css("div.accordion-item.border-0.bg-dark")[i].css("div.text-white ::text").getall()
                x = [ele for ele in x if ele.strip()]
                x = " ".join(x)
                faq_a.append(x)
            faq_q = list(map(lambda a:a.strip(), faq_q))
            faq_q = " |".join(faq_q)
            faq_q = re.sub("Q.", "", faq_q)
            faq_a = " |".join(faq_a)
            faq_a = re.sub("A.", "", faq_a)
            #Syllabus
            modules = response.css(".dnd-section")[2].css(".collapsed::text").getall()
            modules = list(map(lambda a:a.strip(), modules))
            modules = list(map(lambda a:re.sub("(^\d*)", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            #print(modules)
            submodules = []
            for i in range(len(response.xpath("//*[@id='first']")[0].css("div.accordion-item.border-0.bg-dark"))):
                x = response.xpath("//*[@id='first']")[0].css("div.accordion-item.border-0.bg-dark")[i].css("div.text-white ::text").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            content = "".join(modlist)

            desc = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/p//text()").getall()
            desc = [ele for ele in desc if ele.strip()]
            short_desc = desc[0]
            desc = " ".join(desc)
            desc = '<p>' + str(desc) + '</p>'
            duration = 'N/A'
            skills = [ 'You will learn ' + str(ele) for ele in modules]
            skills = " |".join(skills)
            prereq = 'N/A'
            target_aud = "N/A"
            #print(skills)
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'
            yield{
                'Course Title': title,
                'Links': links,
                'Short Description': short_desc,
                'Description': desc,
                'Duration': duration,
                'What you will Learn': skills,
                'Pre_Requisites':prereq,
                'Target Audience': target_aud,
                'Reviews Name': rev_name,
                'Review': review,
                'Ratings':ratings,
                'Review Date': review_date,
                'Curriculum': content,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
                }
        else:
            pass




    def parser_contents4(self, response):
        links = response.request.url
        if ((links == 'https://www.greycampus.com/enterprise') or (links == 'https://www.odinschool.com/datascience-bootcamp')):
            pass
        else:
            #title
            title = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/h1//text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']//text()").get()
            #description
            short_descr = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            short_descr = [ele for ele in short_descr if ele.strip()]
            description = response.xpath("//*[@id='Second_1']/div//text()").getall()
            description = [ele for ele in description if ele.strip()]     
            short_descr = " ".join(short_descr)
            description = " ".join(description)
            description = '<p>' + str(description) + '</p>'

            #Curriculum
            modules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                modules.append(response.xpath(f"//*[@id='curriculumheading{i}']/button//text()").get().strip())
            #print(modules)
           
            submodules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                x = response.xpath(f"//*[@id='curriculumcollapse{i}']/div//text()").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            #print(submodules)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            curriculum = "".join(modlist)
            #reviews
            review_name = response.xpath("//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul//li//a//text()").getall()    
            review_name = " |".join(review_name)
            reviews = response.xpath("//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul//li/div/div/div/div//text()").getall()
            reviews = [ele for ele in reviews if ele.strip()]
            rating = []
            for i in range(1,len(reviews)+1):
                r= len(response.xpath(f"//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul/li[{i}]/div/div/div//img"))
                rating.append(r)
                
        
            if rating is not None:
                rating = list(filter(lambda a:a!=0,rating))
                ratings = " | ".join(str(i) for i in rating)
            review_date = '2021-07-02'
            #Duration
            dur = response.xpath("//*[@id='Third_1']/div/section[1]/div/p[1]/text()").get()
            if dur is not None:
                dur = re.sub("^\d\.", "", dur)
            if dur is not None:
                duration = (re.search("(\d)", dur)).group()
                duration = duration + '+ hours'
            else:
                duration = 'N/A'
            skill_learned = response.xpath("//*[@id='scrollspy1_1']/div/p/text()").get()
            if skill_learned is None:
                skill_learned = ['You will learn ' + ele for ele in modules]
            skill_learned = " |".join(skill_learned)
            #Faq_q
            faq_q = []
            faq_a = [] 
            for i in range(1,len(response.xpath("//*[@id='registration']/div | //*[@id='hs_cos_wrapper_dnd_area-module-53']/div/div | //*[@id='certification']/div | //*[@id='first']/div | //*[@id='FAQ']/div"))-1):    
                faq_q.append(response.xpath(f"//*[@id='certificationheading{i}']/button//text() | //*[@id='heading{i}']/button//text() | //*[@id='FAQheading{i}']/button//text() | //*[@id='registrationheading{i}']/button//text() | //*[@id='firstheading{i}']/button//text()").get().strip())
                
                if not response.xpath(f"//*[@id='certificationcollapse{i}']//table"):
                    ans = response.xpath(f"//*[@id='certificationcollapse{i}']//text()").getall()
                    ans = [ele for ele in ans if ele.strip()]
                    ans = " ".join(ans)
                    faq_a.append(ans)
                else:
                    faq_a.append("N/A")
            faq_q = " |".join(faq_q)
            faq_q = re.sub("Q.", "", faq_q)
            faq_a = " |".join(faq_a)
            faq_a = re.sub("A.", "", faq_a)
            prereq = 'N/A'
            if response.css(".dnd_area-row-4-vertical-alignment"):
                target_aud = response.css(".dnd_area-row-4-vertical-alignment").css("p ::text").getall()
                target_aud = [ele for ele in target_aud if ele.strip()]
                target_aud = list(map(lambda a:a.strip(), target_aud))
                target_aud = " |".join(target_aud)
            elif response.css(".dnd_area-row-3-vertical-alignment"):
                target_aud = response.css(".dnd_area-row-3-vertical-alignment").css("p ::text").get()
            else:
                target_aud = "N/A"
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'
            yield {
                'Course Title': title,
                'Links': links,
                'Short Description': short_descr,
                'Description': description,
                'Duration': duration,
                'What you will Learn': skill_learned,
                'Pre_Requisites':prereq,
                'Target Audience': target_aud,
                'Reviews Name': review_name,
                'Review': reviews,
                'Review Date': review_date,
                'Ratings': ratings,
                'Curriculum': curriculum,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
            }




    def parser_contents5(self, response):
        links = response.request.url
        if ((links == 'https://www.greycampus.com/enterprise') or (links == 'https://www.odinschool.com/datascience-bootcamp')):
            pass
        else:
            #title
            title = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/h1//text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']//text()").get()
            #description
            description = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            description = [ele for ele in description if ele.strip()]
            short_descr = description[0]
            description = " ".join(description)
            description = '<p>' + str(description) + '</p>'

            #Curriculum
            modules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                modules.append(response.xpath(f"//*[@id='curriculumheading{i}']/button//text()").get().strip())
            #print(modules)
           
            submodules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                x = response.xpath(f"//*[@id='curriculumcollapse{i}']/div//text()").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            #print(submodules)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            curriculum = "".join(modlist)
            #reviews
            review_name = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4//text()").getall()
            review_name = " |".join(review_name)
            reviews = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div/p//text()").getall()
            reviews = " |".join(reviews)
            ratings = 'N/A'
            review_date = '2021-03-01'
            #Duration
            duration = ''
            dur = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-22']/div/div/div/ul/li[1]/text()").get()
            for i in dur:
                if i == " ":
                    break
                else:
                    duration = duration + i
            skill_learned = response.xpath("//*[@id='scrollspy1_1']/div/p/text()").get()
            faq_q = 'N/a'
            faq_a = 'N/A'
            prereq = response.xpath("//*[@id='scrollspy1_3']/div/p[2]/text()").get()
            target_aud = response.xpath("//*[@id='scrollspy1_3']/div/p[1]/text()").get()
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'

            yield {
                'Course Title': title,
                'Links': links,
                'Short Description': short_descr,
                'Description': description,
                'Duration': duration,
                'What you will Learn': skill_learned,
                'Pre_Requisites': prereq,
                'Target Audience':target_aud,
                'Reviews Name': review_name,
                'Review': reviews,
                'Ratings': ratings,
                'Review Date': review_date,
                'Curriculum': curriculum,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
            }



    def parser_contents7(self, response):
        links = response.request.url
        if links != 'https://www.greycampus.com/enterprise':
            # Title
            title = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/h1//span//text()").getall()
            title = " ".join(title)
            title.replace("\xa0", "")
            #Description
            description = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            description = [ele for ele in description if ele.strip()]
            short_descr = description[0]
            if len(short_descr)<10:
                    short_descr = short_descr + description[1]
            short_descr = short_descr.replace("\xa0", "")
            description = " ".join(description)
            description = description.replace("\xa0", "")
            description = '<p>' + str(description) + '</p>'
            
            #Curriculum
            modules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                modules.append(response.xpath(f"//*[@id='curriculumheading{i}']/button//text()").get().strip())
            modules = list(map(lambda a:a.strip(), modules))
            modules = list(map(lambda a:re.sub("(^\d*)", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            modules = list(map(lambda a:re.sub("^\W", "", a), modules))
            submodules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                x = response.xpath(f"//*[@id='curriculumcollapse{i}']/div//text()").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            #print(submodule)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            curriculum = "".join(modlist)
            #Learning[
            skill_learned = response.xpath("//*[@id='scrollspy1_1']/div/p/text()").get()
            #Duration
            duration = ''
            dur = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-22']/div/div/div/ul/li[1]/text()").get()
            if dur is not None:
                for i in dur:
                    if i == " ":
                        break
                    else:
                        duration = duration + i
            else:
                duration = 'N/A'
             #reviews
            review_name = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4//text()").getall()
            review_name = " |".join(review_name)
            reviews = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div/p//text()").getall()
            reviews = " |".join(reviews)
            ratings = 'N/A'
            review_date = '2021-09-11'
            #FAQ
            faq_q = 'N/A'
            faq_a = 'N/A'
            if response.xpath("//*[@id='scrollspy1_3']/h4/text").get()=='WHO THIS COURSE IS FOR ?':
                target_aud = response.xpath("//*[@id='scrollspy1_3']/div/p[1]/text()").get()
                if response.xpath("//*[@id='scrollspy1_3']/div/p[2]/text()"):
                    prereq = response.xpath("//*[@id='scrollspy1_3']/div/p[2]/text()").get()
                else:
                    prereq = 'N/A'
            else:
                prereq = 'N/A'
                target_aud = 'N/A'
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'

            yield {
                'Course Title': title,
                'Links': links,
                'Short Description': short_descr,
                'Description': description,
                'Duration': duration,
                'What you will Learn': skill_learned,
                'Pre_Requisites': prereq,
                'Target Audience':target_aud,
                'Reviews Name': review_name,
                'Review': reviews,
                'Ratings': ratings,
                'Review Date': review_date,
                'Curriculum': curriculum,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link': brochure_link
            }



            
    def parser_contents8(self, response):
        links = response.request.url
        if ((links == 'https://www.greycampus.com/enterprise') or (links == 'https://www.odinschool.com/datascience-bootcamp')):
            pass
        else:
            #title
            title = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']/h1//text() | //*[@id='hs_cos_wrapper_dnd_area-module-2_']//text()").get()
            #description
            if response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-8_']//text()").get()=='Description':
                description = response.xpath("//*[@id='Second_1']/div//p//text()").getall()
            else:
                description = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            description = [ele for ele in description if ele.strip()]
            short_descr = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-2_']//p//text()").getall()
            short_descr = [ele for ele in description if ele.strip()]
            short_descr = short_descr[0]
            
            description = " ".join(description)
            description = '<p>' + str(description) + '</p>'
            #Curriculum
            modules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                modules.append(response.xpath(f"//*[@id='curriculumheading{i}']/button//text()").get().strip())
            #print(modules)
           
            submodules = []
            for i in range(1,len(response.css("div#curriculum.accordion div h2"))+1):
                x = response.xpath(f"//*[@id='curriculumcollapse{i}']/div//text()").getall()
                x = [ele for ele in x if ele.strip()]
                submodules.append(x)
            #print(submodules)
            modulenum = 1
            modlist = list()
            for i in range(len(modules)):
                mod = f"<p><strong>Module{modulenum}: {modules[i]}</strong>"
                modlist.append(mod)
                try:
                    submodnum = 1
                    if submodules[i] is not None:
                        for j in submodules[i]:
                            submodule = f"<br>{submodnum}. {j}"
                            modlist.append(submodule)
                            submodnum += 1
                    else:
                        pass
                except:
                    pass
                modulenum +=1
                modlist.append("</p>")
            curriculum = "".join(modlist)
            #reviews
            review_name = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/a/h4//text() | //*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul/li[2]/div/div/div/a/h4//text()").getall()
            review_name = " |".join(review_name)
            reviews = response.xpath("//*[@id='glide-review']/div/ul//li/div/div/div[2]/div/p//text() | //*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul//li//div/div/div/div/p//text()").getall()
            reviews = " |".join(reviews)
            rating = []
            for i in range(1,len(reviews)+1):
                r = len(response.xpath(f"//*[@id='hs_cos_wrapper_widget_1631535023475']/div/div[1]/ul/li[{i}]/div/div/div//img"))
                if r is not None:
                    rating.append(r)
            if rating is not None:
                rating = list(filter(lambda a:a!=0, rating))
                ratings = " | ".join(str(i) for i in rating)

            review_date = '2021-07-08'
            #Duration
            duration = ''
            dur = response.xpath("//*[@id='hs_cos_wrapper_dnd_area-module-22']/div/div/div/ul/li[1]/text()").get()
            if dur is not None:
                for i in dur:
                    if i == " ":
                        break
                    else:
                        duration = duration + i
            else:
                duration = 'N/A'
            skill_learned = response.xpath("//*[@id='scrollspy1_1']/div/p/text()").get()
            
            if skill_learned is None:
                skill_learned = ['You will learn ' + ele for ele in modules]
                skill_learned = " |".join(skill_learned)
            
            #Faq_q
            faq_q = []
            faq_a = [] 
            for i in range(1,len(response.xpath("//*[@id='registration']/div | //*[@id='hs_cos_wrapper_dnd_area-module-53']/div/div | //*[@id='certification']/div | //*[@id='first']/div | //*[@id='FAQ']/div"))-1):    
                faq_q.append(response.xpath(f"//*[@id='certificationheading{i}']/button//text() | //*[@id='heading{i}']/button//text() | //*[@id='FAQheading{i}']/button//text() | //*[@id='registrationheading{i}']/button//text() | //*[@id='firstheading{i}']/button//text()").get().strip())
                
                if not response.xpath(f"//*[@id='certificationcollapse{i}']//table"):
                    ans = response.xpath(f"//*[@id='certificationcollapse{i}']//text()").getall()
                    ans = [ele for ele in ans if ele.strip()]
                    ans = " ".join(ans)
                    faq_a.append(ans)
                else:
                    faq_a.append("N/A")
            faq_q = " |".join(faq_q)
            faq_q = re.sub("Q.", "", faq_q)
            faq_a = " |".join(faq_a)
            faq_a = re.sub("A.", "", faq_a)
            #pre requisites
            if response.xpath("//*[@id='scrollspy1_3']/h4/text").get()=='WHO THIS COURSE IS FOR ?':
                target_aud = response.xpath("//*[@id='scrollspy1_3']/div/p[1]/text()").get()
                if response.xpath("//*[@id='scrollspy1_3']/div/p[3]/text()"):
                    prereq = response.xpath("//*[@id='scrollspy1_3']/div/p[3]/text()").get()
                else:
                    prereq = response.xpath("//*[@id='scrollspy1_3']/div/p[]/text()").get()
            else:
                prereq = 'N/A'
                target_aud = 'N/A'
            #Brochure
            if response.xpath("//*[contains(text(), 'Download Brochure')]"):
                brochure_link = response.xpath("//script[@src='/_hcms/forms/v2.js']/following-sibling::script/text()").get()
                if re.search("redirectUrl:(.*).pdf", brochure_link):
                    brochure_link = re.search("redirectUrl:(.*).pdf", brochure_link).group(1)
                    brochure_link = brochure_link + '.pdf'
                    brochure_link = brochure_link.strip().replace('"', '').replace("\\", "")
                else:
                    brochure_link = 'N/A'
            else:
                brochure_link = 'N/A'
 

            yield {
                'Course Title': title,
                'Links': links,
                'Short Description': short_descr,
                'Description': description,
                'Duration': duration,
                'What you will Learn': skill_learned,
                'Pre_Requisites':prereq,
                'Target Audience':target_aud,
                'Reviews Name': review_name,
                'Review': reviews,
                'Ratings': ratings,
                'Review Date': review_date,
                'Curriculum': curriculum,
                'Faq Ques': faq_q,
                'Faq Ans': faq_a,
                'Brochure Link':brochure_link
            }
        