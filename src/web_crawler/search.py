import scrapy
from scrapy_splash import SplashRequest
import re

from ..items import Item

proxy ='http//your.proxy.com:PORT'

current_page_xpath='//div[your x path selector]/text()'
last_page_xpath='//div[your other x path selector]/text()'

class spider(scrapy.Spider):

    name = 'my_spider'
    allowed_domains =['domain.com']

    start_urls =['https://www.domaintoscrape.com/page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta ={'proxy':proxy})

    def get_page_nbr(value):

        #you may need more complex regex to get page numbers.
        #most of the time they are in form "page X of Y"
        #google is your friend

        if re.search('\d+',value):
            value = re.search('\d+',value)
            value = value[0]
        else:
            value =None
        return  value