import scrapy


class ExtAllTextSpider(scrapy.Spider):
    name = 'ext_all_text'
    start_urls = ['https://about.surpassone.com']
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        for text in response.xpath('//body//text()').extract():
            stripped_text = text.strip()
            if stripped_text:
                yield {'text': stripped_text}
                break

        count = 0
        for link in response.css('a::attr(href)').getall():
            count += 1
            yield response.follow(link, self.parse)
            if count > 10:
                break
