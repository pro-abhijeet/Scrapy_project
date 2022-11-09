import scrapy
import requests
from scrapy.selector import Selector
import re
import json

class Geekster1(scrapy.Spider):
    name = 'geekster1'
    start_urls = ['https://geekster.in/full-stack-web-development-program','https://geekster.in/codeschool']

    def parse(self, response):
        link = response.request.url
        a = requests.get(link)
        body = a.text
        response = Selector(text=body)
        if link=='https://geekster.in/full-stack-web-development-program':
            title = response.xpath("//title/text()").get()
            short_description = response.xpath("//div[@class='p-1 pl-0 text-hero--sub']/span/text()").get()
            Duration = response.xpath("//div[contains(text(), 'Duration')]/following-sibling::div/text()").get()
            batch_date = response.xpath("//div[contains(text(), 'Next Batch Starts on')]/following-sibling::div/text()").get()
            batch_days = response.xpath("//div[contains(text(), 'Class Timings')]/following-sibling::div/text()").get()
            batch_timing = response.xpath("//div[contains(text(), 'Class Timings')]/following-sibling::div//p/text()").get()
            rev_name = response.xpath("//div[@class='jsx-51d1b9cc143adc6d name']/text()").getall()
            rev_name = " |".join(rev_name)
            rev_img = response.xpath("//div[@class='jsx-51d1b9cc143adc6d student-say-new__picture']/img/@src").getall()
            rev_img = " |".join(rev_img)
            reviews = response.xpath("//div[@class='jsx-51d1b9cc143adc6d student-say-new__content--text']/p/text()").getall()
            reviews = " |".join(reviews)
            price_data_url = 'https://geekster.in/_next/static/chunks/326.6c7b6e970c2b4fe2.js'
            price_data = requests.get(price_data_url).text
            regular_price = re.findall(r'\d+,\d+ | \d+,\d+', price_data)[3]
            offer_price = regular_price
            emi_price = re.findall(r'\d+,\d+ | \d+,\d+', price_data)[4]
            what_you_learn = response.xpath("//div[@class='styles_skill_container__c029c flex-center']/span/text()").getall()
            what_you_learn = [ 'You will learn about '+ele for ele in what_you_learn]
            mentors_data_url = 'https://geekster.in/_next/static/chunks/598-1d7f298521a7290e.js'
            mentors_data = requests.get(mentors_data_url).text
            mentors_data = re.search(r'i.Z=(.*)},2', mentors_data).group(1)
            mentors_data = mentors_data.replace('cover:', '"cover":').replace('name:', '"name":').replace('linkedin:', '"linkedin":').replace('designation:', '"designation":').replace('company:', '"company":')
            mentors_data = json.loads(mentors_data)
            mentors = []
            mentors_img = []
            for i in mentors_data:
                mentors.append(i['name'])
                mentors_img.append(i['cover'])
            mentors = " |".join(mentors)
            mentors_img = " |".join(mentors_img)
            src_file = response.xpath("//script[13]/@src").get()
            src_file = 'https://geekster.in' + str(src_file)
            data = requests.get(src_file).text
            data = re.search(r',o={(.*),r=', data).group(1)
            data = '{' + data
            data = data.replace('description', '"description"').replace('courses', '"courses"').replace('duration', '"duration"').replace('sections', '"sections"').replace('highlights', '"highlights"').replace('subtopics', '"subtopics"').replace('title', '"title"').replace('content', '"content"').replace('projects:', '"projects":')
            data = re.sub(r'\bsub\b', '"sub"', data)
            data = re.sub(r'\btype\b', '"type"', data)
            data = json.loads(data)
            description = data['description']
            modules = []
            submodules = []
            for i in data['courses']:
                for j in i['sections']:
                    modules.append(j['title'])
                    try:
                        sub = j['content']
                    except:
                        sub = j['highlights']
                    
                    submodules.append(sub)
            modulenum = 1
            modlist = []
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
            yield{
            'Title':title,
            'Link':link,
            'Short Description': short_description,
            'Description': description,
            'Course Duration':Duration,
            'Regular Price':regular_price,
            'Offer Price': offer_price,
            #'Emi Price':emi_price,
            #'Batch Date':batch_date,
            #'Batch Days':batch_days,
            #'Batch Timing': batch_timing,
            'What You Learn':what_you_learn,
            'Mentors': mentors,
            'Mentor Image': mentors_img,
            'Review Name':rev_name,
            'Review Image': rev_img,
            'Review': reviews,
            'Curriculum':content
        }
        else:
            short_description = response.xpath("//p[@class='styles_tracks_container_items_text_innertext__aI9yD']/text()").get()
            reviews = ""
            rev_img = ""
            rev_name = ""
            mentors = response.xpath("//div[@class='jsx-22f131badd6a4704 w-100']//text()").getall()
            mentors = " |".join(mentors)
            mentors_img = response.xpath("//div[@class='jsx-22f131badd6a4704 image-container']/img[1]/@src").getall()
            mentors_img = " |".join(mentors_img)
            src_file = response.xpath("//script[10]/@src").get()
            src_file = 'https://geekster.in' + str(src_file)
            data = requests.get(src_file).text
            data1 = re.search("s}}\);var\Wn=(.*?),s=\[", data).group(1)
            data1 = data1.replace('title', '"title"').replace('listTitle', '"listTitle"').replace('content', '"content"').replace('shortDesc', '"shortDesc"').replace('primaryBackground', '"primaryBackground"').replace('secondaryBackground', '"secondaryBackground"').replace('highLights', '"highLights"').replace('moduleNo', '"moduleNo"').replace('offerName', '"offerName"').replace('oldFee', '"oldFee"').replace('newFee', '"newFee"')
            data1 = re.sub(r'\bimage\b', '"image"', data1)
            data1 = re.sub(r'\bdesc\b', '"desc"', data1)
            data1 = re.sub(r'\bdes\b', '"des"', data1)
            data1 = re.sub(r'\bduration\b', '"duration"', data1)
            data1 = re.sub(r'\bpanel\b', '"panel"', data1)
            data1 = re.sub(r'topics:', '"topics":', data1)
            data1 = re.sub(r'\"highLights\":\[,', '\"highLights\":[', data1)
            data1 = json.loads(data1)
            for list in data1:
                title = list[1]['title']
                title = title.replace('About ', '')
                description = (list[1]['content'])
                description = "<p>" + description + "</p>"
                Duration = list[0]['content'][0]['title']
                what_you_learn = list[3]['content']
                regular_price = list[5]['content']['oldFee']
                offer_price = list[5]['content']['newFee']
                module = []
                submodule = []
                for i in (list[4]['content']):
                    module.append(i['title'])
                    sub = (i['content']['topics'])
                    submodule.append(sub)
                modulenum = 1
                modlist = []
                for i in range(len(module)):
                    mod = f"<module{modulenum}><heading>{module[i]}</heading>"
                    modlist.append(mod)
                    modlist.append("<subheading>")
                    submodnum = 1
                    for j in submodule[i]:
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

                yield{
                    'Title':title,
                    'Link':link,
                    'Short Description': short_description,
                    'Description': description,
                    'Course Duration':Duration,
                    'Regular Price':regular_price,
                    'Offer Price': offer_price,
                    'What You Learn':what_you_learn,
                    'Mentors': mentors,
                    'Mentor Image': mentors_img,
                    'Review Name':rev_name,
                    'Review Image': rev_img,
                    'Review': reviews,
                    'Curriculum':content
                }