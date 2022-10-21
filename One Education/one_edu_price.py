import scrapy   

class OneEducation(scrapy.Spider):
    name = 'one_ed'
    start_urls = [
        "https://www.oneeducation.org.uk/courses/"
    ]
    header = {
                'authority': 'www.oneeducation.org.uk' ,
                'accept': '*/*' ,
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8' ,
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8' ,
                'cookie': '_gcl_au=1.1.1376393868.1666100942; _omappvp=DQHqe5Mrbgjz6qiUpZjh4RTOrXYVkYVdi0gsn98hvudLHzQnsGeppiMj2IwtbtPJUgTBpUxlfnacXGRMOTOJQyekNUcC39Tz; Affc=; _gid=GA1.3.65934756.1666100942; cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-non-necessary=yes; _fbp=fb.2.1666100943843.66694060; __adroll_fpc=d241e1342ca8a5431761bec0791be66d-1666100948217; bp-course-list=grid; omSeen-c76dhgrtodjqz7lsvo8v=1666101188252; omSuccess-c76dhgrtodjqz7lsvo8v=1666101213353; omSuccessCookie=1666101213353; om-c76dhgrtodjqz7lsvo8v=1666101215364; bp-activity-oldestpage=1; bp-course-filter=; bp-course-extras=%7B%7D; PHPSESSID=6502a8437b1215619b2abf3c18dd0d3e; _clck=14y3g33|1|f5u|0; omCountdown-zglyoxntsf229y98l8wr-fYxRohyQn3SNKtsEoztA=1666185459346; omSeen-zglyoxntsf229y98l8wr=1666171059352; omCountdown-mb0fitm7q6ismchvnayn-vzfBnzxEndOoliOePP5p=1666186120638; omSeen-mb0fitm7q6ismchvnayn=1666175629866; _gat_UA-125757854-1=1; __ar_v4=IS2RDFAR5FH4TIVEZ7PDCX%3A20221017%3A14%7CRM5K4QE265HGPPTPLU6U7J%3A20221017%3A2%7C4YKSE645CJGQVPC6F7ZVFO%3A20221017%3A20%7CRW4JPSY66FCPHJ3TQC4VGA%3A20221017%3A20%7C4K5EILH6HNFYPKRD7W6P4M%3A20221017%3A2%7CASDK5D3AO5GJ3JZ75S3JDZ%3A20221017%3A2; _clsk=1lh8fds|1666177416873|14|1|e.clarity.ms/collect; _ga_W1BD7DC0FT=GS1.1.1666174449.5.1.1666177423.0.0.0; _ga=GA1.1.1169806902.1666100942; _uetsid=a0a744904eeb11edb35f55ce662f80a2; _uetvid=a0a7cb104eeb11ed97dd393394907f0c; bp-course-scope=' ,
                'origin': 'https://www.oneeducation.org.uk' ,
                'referer': 'https://www.oneeducation.org.uk/courses/?items_page=1' ,
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
    }
    def parse(self, response):
        url = "https://www.oneeducation.org.uk/wp-admin/admin-ajax.php"
        for i in range(1,277):
            payload = f"action=course_filter&cookie=bp-course-list%253Dgrid%2526bp-activity-oldestpage%253D1%2526bp-course-filter%253D%2526bp-course-extras%253D%25257B%25257D%2526bp-course-scope%253D&object=course&filter=&search_terms=&scope=&page={i}&extras=%7B%7D"
            yield scrapy.Request(url, method='POST',body=payload,headers=self.header, callback=self.parser_content)
    def parser_content(self, response):
        for i in response.xpath("//div[@class='item']"):
            title = i.xpath(".//div[@class='item-title']/a//text()").get()
            link = i.xpath(".//div[@class='item-title']/a//@href").get()
            yield scrapy.Request(link, callback=self.parser_content2, cb_kwargs={'title':title, 'link':link})
    def parser_content2(self,response,link,title):
        if response.xpath("//*[@id='course-pricing']/div[1]//ins"):
            original_price = response.xpath("//div[@class='content-price-box']//del//text()").getall()
            original_price = " ".join(original_price)
            current_price = response.xpath("//div[@class='content-price-box']//ins//text()").getall()
            current_price = " ".join(current_price)
        else:
            original_price = "N/A"
            current_price = "N/A"
        yield{
            'Course Title': title,
            'Link':link,
            'Current Price': current_price,
            'Original Price': original_price
        }
        
            # Subscription Price has not been attached
