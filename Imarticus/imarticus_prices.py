import scrapy
from bs4 import BeautifulSoup
import json
import re


class secondscrapy(scrapy.Spider):
    name = "imarticus"
    start_urls = [
        "https://imarticus.org/"
    ]

    def parse(self, response):
        for link in response.xpath('//ul[@class="ulwidth8"]//li//a/@href').getall()[:-5]:
            #print(response.urljoin(link.get()))
            yield scrapy.Request("https://imarticus.org"+link, callback=self.parser_contents1)


    def parser_contents1(self, response):

        display_price = []

        if response.css("span.feesAmount1::text").extract_first() is not None:
            display_price.append(response.css("span.feesAmount1::text").extract_first())

        if response.css("div.csHeader.pt-5.pb-5.text-center").css("p.mabProgramAmount::text").extract_first() is not None:
            display_price.append(response.css("p.fmabProgramAmount::text").extract_first())

        if response.css("div.programFeeCertificateLeft").css("p.programFeePara2::text").extract_first() is not None:
            display_price.append(response.css("div.programFeeCertificateLeft").css("p.programFeePara2::text").extract_first())

        if response.css("div.fsd_amount__5ije0").css("p::text").extract_first() is not None:
            display_price.append(response.css("div.fsd_amount__5ije0").css("p::text").extract_first())

        if response.xpath('//p[@class="mabProgramAmount"]//text()').extract_first() is not None:
            display_price.append(response.xpath('//p[@class="mabProgramAmount"]//text()').extract())

        if response.xpath('//h5[@class="awaHead"]//text()').extract_first() is not None:
            display_price.append(response.xpath('//h5[@class="awaHead"]//text()').extract_first())
            
        if response.xpath('//p[@class="financial-services-capital-markets-management-program-iim-indore_fee__W6osi"]//text()').extract_first() is not None:
            display_price.append(response.xpath('//p[@class="financial-services-capital-markets-management-program-iim-indore_fee__W6osi"]//text()').extract_first())

        if response.xpath('//p[@class="pgB_F_fee__6jGrp"]//text()').extract_first() is not None:
            display_price.append(response.xpath('//p[@class="pgB_F_fee__6jGrp"]//text()').extract_first())

        if response.xpath('//div[@class="klu_fees__85TIR"]//p/text() | //div[@class="fsd_amount__QWGno"]//p/text() | //div[@class="bimtech_section8_fee_amount___Jdf8"]//p/text() | //p[@class="financial-services-capital-markets-management-program-iim-indore_fee__wd_Ak"]/text() | //p[@class="pgB_F_fee___Vegk"]/text() | //div[@class="csHeader pt-sm-5 pb-5"]//h5[@class="awaHead"]/text()').extract_first() is not None:
            display_price.append(response.xpath('//div[@class="klu_fees__85TIR"]//p/text() | //div[@class="fsd_amount__QWGno"]//p/text() | //div[@class="bimtech_section8_fee_amount___Jdf8"]//p/text() | //p[@class="financial-services-capital-markets-management-program-iim-indore_fee__wd_Ak"]/text() | //p[@class="pgB_F_fee___Vegk"]/text() | //div[@class="csHeader pt-sm-5 pb-5"]//h5/text()').extract_first())

        display_price = list(filter(None, display_price))

        if display_price is not None:
            try:
                display_price = [i for i in re.findall(r'-?\d+\.?\d*', display_price[0])]
            except:
                try:
                    display_price = [i for i in re.findall(r'-?\d+\.?\d*', display_price[0][0])]
                except:
                    pass
        else:
            display_price = display_price

        try:
            display_price = "".join(display_price)
            display_price = float(display_price)
        except:
            pass

        if display_price == "":
            currency = ""
        else:
            currency = "INR"



        emi_start = []
        try:
            if response.css("p.feesType3").css("span.feesAmount2::text").extract_first() is not None:
                emi_start.append(response.css("span.feesAmount2::text").extract_first())
            if response.css("div.fsd_emiamount__HJKLH").css("p::text").extract_first() is not None:
                emi_start.append(response.css("div.fsd_emiamount__HJKLH").css("p::text").extract_first())
            if response.xpath('//div[@class="fsd_emiamount__SHRmE"]//p/text() | //div[@class="bimtech_section8_emi_amount__j2IZ4"]//p/text() | //div[@class="feesHead feesHeadcolor2"]//span[@class="feesAmount2"]/text() | //div[@class="feesHead feesHeadcolor2"]//span[@class="feesAmount1"]/text()').extract_first() is not None:
                emi_start.append(response.xpath('//div[@class="fsd_emiamount__SHRmE"]//p/text() | //div[@class="bimtech_section8_emi_amount__j2IZ4"]//p/text() | //div[@class="feesHead feesHeadcolor2"]//span[@class="feesAmount2"]/text() | //div[@class="feesHead feesHeadcolor2"]//span[@class="feesAmount1"]/text()').extract_first())
        except:
            if response.css("p.feesType1").css("span.feesAmount1::text").extract_first() is not None:
                emi_start.append(response.css("span.feesAmount1::text").extract_first())

        try:
            emi_start = [i for i in re.findall(r'-?\d+\.?\d*', emi_start[0])]
        except:
            pass

        try:
            emi_start = "".join(emi_start)
            emi_start = float(emi_start)
        except:
            pass

        sale_price = display_price

        yield{
            'course link': response.url,
            'regular_price': display_price,
            'price': sale_price,
            'currency': currency,
            'Emi': emi_start
        }