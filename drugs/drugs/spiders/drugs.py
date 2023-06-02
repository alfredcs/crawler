import scrapy
from scrapy_splash import SplashRequest

'''
%scrapy shell
fetch('http://localhost:8050/render.html?url=https://medlineplus.gov/druginfo')
response.css('span::text').getall()
response.css('li a::attr("href")').getall()
response.css('a.drug_Aa,html').get()
'''


class drugsSpider(scrapy.Spider):
    name = 'drugs'

    def start_request(self):
        url = 'https://medlineplus.gov/druginformation.html'
        #url = 'https://medlineplus.gov/druginfo'

        yield SplashRequest(url=url, callback=self.parse)
    '''
    def parse(self, response):
        drugs = response.css('a.drug_Aa,html.drug_Ba,html.drug_Cc,html.drug_Dd,html.drug_Ee,html')
        for item in drugs:
            yield {
            'name': itemcss('h2::text').get(),
            'desciption': item.css('span.text::text').get(),
            }
    '''
    def parse(self, response):
        # Extracting links on the page and continue crawling
        #for href in response.css('a::attr(href)').extract():
        for href in response.css('a::attr(href)').extract():
            yield SplashRequest(
                response.urljoin(href),
                callback=self.parse,
            )
        # Extracting data from the page (example: the text from p tags)
        for href2 in response.css('a::attr("href")').extract():
            #yield {'text': paragraph}
            yield SplashRequest(
                response.urljoin(href2),
                callback=self.parse,
            )
        for paragraph in response.css('p').extract():
            yield {'text': paragraph}
