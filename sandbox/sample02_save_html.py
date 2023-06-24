import hashlib

import scrapy


class ExtAllTextSpider(scrapy.Spider):
    name = 'ext_all_text'
    start_urls = ['https://about.surpassone.com']
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        page_domain = response.url.split('/')[2]
        page_hash = hashlib.md5(response.url.encode()).hexdigest()
        filename = f'{page_domain}_{page_hash}.html'

        with open(filename, 'wb') as f:
            f.write(response.body)
