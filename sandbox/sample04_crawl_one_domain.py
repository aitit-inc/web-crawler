import hashlib
from pathlib import Path
from scrapy import signals
from scrapy.signalmanager import dispatcher

import scrapy


class ExtAllTextSpider(scrapy.Spider):
    name = 'ext_all_text'
    start_urls = ['https://about.surpassone.com/news/']
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    base_dir = Path('data')

    def __init__(self, *args, **kwargs):
        super(ExtAllTextSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)

    def spider_opened(self, spider):
        self.base_dir.mkdir(exist_ok=True)

    def parse(self, response):
        page_domain = response.url.split('/')[2]
        domain_dir = self.base_dir / page_domain
        domain_dir.mkdir(exist_ok=True)

        page_hash = hashlib.md5(response.url.encode()).hexdigest()
        filename = f'{page_hash}.html'
        file_path = domain_dir / filename

        with open(file_path, 'wb') as f:
            f.write(response.body)

        count = 0
        for link in response.css('a::attr(href)').getall():
            count += 1
            yield response.follow(link, self.parse)
            if count > 30:
                break
