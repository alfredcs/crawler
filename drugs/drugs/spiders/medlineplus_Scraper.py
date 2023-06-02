#from os import link
from matplotlib.pyplot import title
import scrapy, os
from scrapy_splash import SplashRequest
from .drug_items import DrugScraperItem
from bs4 import BeautifulSoup

## https://pypi.org/project/scrapy-user-agents/

class medlinkplusScraper(scrapy.Spider):
    name = "medlinkplus"

    start_urls = [
        "https://medlineplus.gov/druginfo",
    ]

    def start_request(self):
        yield SplashRequest(url=self.start_urls[0], callback=self.parse)

    def parse_html(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        p_tags = soup.find_all('p')
        for p in p_tags:
            p.replace_with("")
        return str(soup)        

    def parse_content(self, response):
        items = DrugScraperItem()
        titles = response.css('title::text').extract()
        #contents = response.xpath('//div[@class="section-body"]/p').extract()
        contents = response.css('section div p').getall()
        '''
        soup = BeautifulSoup(contents, 'html.parser')
        p_tags = soup.find_all('p')
        for p in p_tags:
            p.replace_with("")
        contents = str(soup)
        '''

        for i in list(zip(titles, contents)):
            title,content = i
            items['title'] = title
            items['content'] = content
        yield items
        '''
        yield SplashRequest(
                response.urljoin(items['href']),
                callback=self.parse
        )
        '''


    def parse_names(self, response):
        names = response.xpath('//ul[@id="index"]/li/a/@href').extract()
        items = DrugScraperItem()
        for i in list(zip(names)):
            items['name']=self.start_urls[0]+i[0].replace("./", "/")
        #yield items
            yield SplashRequest(
                response.urljoin(items['name']),
                callback=self.parse_content,
            )


    def parse(self, response):
        hrefs = response.xpath('//ul[@class="alpha-links"]/li/a/@href').extract()
        #prices = response.css('.a-price-whole::text').extract()
        items = DrugScraperItem()

        for i in list(zip(hrefs)):
            next_link = self.start_urls[0]+"/"+os.path.basename(i[0])
            items['href']=next_link

            yield SplashRequest(
                    response.urljoin(items['href']),
                    callback=self.parse_names,
            )

'''
        next_page_url = "https://www.amazon.com"+response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "s-pagination-next", " " ))]/@href')[0].extract()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def start_request(self):
        url = 'https://medlineplus.gov/'
        yield SplashRequest(url=url+'druginfo', callback=self.parse)


    def parse(self, response):
        #items = DrugScraperItem()
        #for href in response.xpath('//ul[@class="alpha-links"]/li/a/@href').extract():
        hrefs = response.xpath('//ul[@class="alpha-links"]/li/a/@href').extract()
        yield hrefs

            yield SplashRequest(
                response.urljoin(href),
                callback=self.parse,
            )
            for names in response.xpath('//ul[@id="index"]/li/a/@href').extract():
                yield {'text': names}
        names = response.xpath('//ul[@id="index"]/li/a/@href').extract()

        #prices = response.css('.a-price-whole::text').extract()
        prices = response.css('.a-offscreen::text').extract()
        authors = response.css('.a-color-secondary .a-size-base+ .a-size-base::text').extract()
        ratings = response.css('.s-link-style .s-underline-text::text').extract()

        for i in list(zip(titles,prices,authors,ratings)):
            title,price,author,rating = i
            items['title']=title
            items['price']=price
            items['author']=author
            items['rating']=rating
        
            yield items

        next_page_url = "https://www.amazon.com"+response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "s-pagination-next", " " ))]/@href')[0].extract()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)
'''
