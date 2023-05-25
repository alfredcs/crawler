import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = 'myspider'
    #start_urls = ['http://example.com', 'http://example2.com', ]  # Your target URLs here
    start_urls = ['https://www.mayoclinic.org/drugs-supplements', ]  # Your target URLs here
    splash_url = 'http://localhost:8050'  # Assuming Splash is running on your local machine

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5}, endpoint='render.html')

    def parse(self, response):
        # Handle the crawled data here
        self.log('Visited %s' % response.url)
        # Example of extracting data:
        page_title = response.css('title::text').extract_first()
        self.log('Page title is: %s' % page_title)
