import scraper_helper
import scrapy
from bs4 import BeautifulSoup
import scraper_helper as sh
from requests import request
from lxml import html
import re


class qspider(scrapy.Spider):
    name = "brainsensei"
    allowed_domains = ["brainsensei.com"]

    start_urls = ["https://brainsensei.com/explore-courses/"]

    def parse(self, response):
        for href in response.css('.box-link::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):

        #reviewer_name

        reviewer_name = response.xpath('//div[@class="slides"]//span[@class="testimonial-name"]/text()').extract()
        reviewer_name = [desc.strip() for desc in reviewer_name]
        reviewer_name = "|".join(reviewer_name)

        #reviewer_description

        reviewer_description = response.xpath('//blockquote//p/text()').extract()
        reviewer_description = [revv.strip() for revv in reviewer_description]
        reviewer_description = "|".join(reviewer_description)
        reviewer_description = reviewer_description.replace("||","|")
        reviewer_description = re.sub("$/|","",reviewer_description)

        #title

        title = response.xpath('//title/text()').extract()
        title = [tit.strip() for tit in title[:1]]
        title = "".join(title)

        #price

        price = response.xpath('//span[@class="woocommerce-Price-amount amount"]//bdi/text()').extract()
        price = [pri.strip() for pri in price]
        price = "".join(price)
        price = scraper_helper.cleanup(price)

        description = response.xpath('//div[@class="wpb_wrapper"]//p/text()').extract()
        description = [desc.strip() for desc in description[:1]]
        description = "".join(description)
        short = description.split(".")[0]
        description = "<p>"+description+"</p>"


        batch_date = response.xpath('//div[@class="simple-col simple-data-date"]/text()').extract()
        batch_date = [str.strip() for str in batch_date]
        batch_date = "|".join(batch_date)


        batch_time = response.xpath('//div[@class="simple-col simple-data-time"]/text()').extract()
        batch_time = [batch.strip() for batch in batch_time]
        batch_time = "|".join(batch_time)
        batch_time = batch_time.replace("to","-")
        batch_time = re.sub('\(.*?\)', '', batch_time).replace('||', '|')


        batch_price = response.css('.simple-data-time+ .simple-col::text').extract()
        batch_price = [batp.strip() for batp in batch_price]
        batch_price = "|".join(batch_price)
        batch_price = batch_price.replace("$","")


        what_will_learn = response.css('.open+ .open li::text , p+ ul li::text').getall()

        what_will_learn = [sho.strip() for sho in what_will_learn]
        what_will_learn = "|".join(what_will_learn)
        what_will_learn = what_will_learn.replace("||","|")
        if what_will_learn == "":
            what_will_learn = response.css('#capmfeatures > div.row_col_wrap_12.col.span_12.dark.left > div > div > div > div.toggles > div:nth-child(2) > div > div > div').extract()
            what_will_learn = what_will_learn[0]
            what_will_learn = what_will_learn.strip().replace('\n', '')
            what_will_learn = re.sub('<div .*?>|<p.*?</p>', '', what_will_learn)
            what_will_learn = what_will_learn.split('</div><div>')
            what_will_learn = "|".join(what_will_learn)
            what_will_learn = re.sub('^\||</div></div>', '', what_will_learn)


        content = response.css('.open+ .open li::text , p+ ul li::text').extract()
        if content == []:
            content = response.css('#capmfeatures > div.row_col_wrap_12.col.span_12.dark.left > div > div > div > div.toggles > div:nth-child(2) > div > div > div').extract()
            content = content[0]
            content = content.strip().replace('\n', '')
            content = re.sub('<div .*?>|<p.*?</p>', '', content)
            content = content.split('</div><div>')
        number = 1
        head = []
        for cont in content:
            if cont.strip() == "" or cont.strip() == "</div></div>": continue
            heading = f"<p><strong>Module {number}: </strong>{cont.strip()}</p>"
            head.append(heading)
            number += 1
        heading = "".join(head)

        yield{
        'title' : title,
        'price' : price,
        'description' : description,
        'reviewer_description' : reviewer_description,
        'what_will_learn' : what_will_learn,
        'reviewer_name' : reviewer_name,
        'batch_date' : batch_date,
        'batch_time' : batch_time,
        'short' : short,
        'batch_price' : batch_price,
        'heading' : heading
        }
        

