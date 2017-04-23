import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import re

class PexelsScraper(scrapy.Spider):
    name = "pexels"
    start_urls = ["https://www.pexels.com/"]

    url_matcher = re.compile('https://www.pexels.com/photo/')

    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    def parse(self, response):
        body = response.body
        images = Selector(text = body).css('img.image-section__image').extract()

        print response.url
        for i in images:
            print PexelsScraper.x.findall(i)
            print PexelsScraper.y.findall(i)  #[0].split(', ')
            # print i
        # i = Image(src, web_id, img_page, img_id, tags`)