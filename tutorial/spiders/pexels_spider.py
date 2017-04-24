import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector


class PexelsScraper(scrapy.Spider):
    name = "pexels"
    start_urls = ["https://www.pexels.com/"]
    base_url = "https://www.pexels.com/"

    # Only follow links that have this prefix
    url_matcher = re.compile('https://www.pexels.com/photo/')

    # Regex matchers for all fields for an image
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    def start_requests(self):
        url = "https://www.pexels.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if response.status == 200:
            body = Selector(text=response.body)
            images = body.css('img.image-section__image').extract()

            for image in images:
                img_url = PexelsScraper.src_extractor.findall(image)[0]
                PexelsScraper.tags_extractor.findall(image)

            link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
            next_links = filter(self.check_if_extracted,
                                map(lambda x: x.url, link_extractor.extract_links(response)))
            print next_links

    def check_if_extracted(self, img_url):
        # Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
        img_id = img_url.split('/')[-2].split('-')[-1]

        print img_id
        return True

