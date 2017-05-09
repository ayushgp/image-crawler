import re

import scrapy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector

from ..DBUtil import DBUtil


class PixabayScraper(scrapy.Spider):
    name = "pixabay"
    WEBSITE_ID = 2
    start_urls = ["https://www.pixabay.com/"]
    base_url = "https://www.pixabay.com/"

    # Only follow links that have this prefix
    url_matcher = re.compile('https\:\/\/pixabay\.com\/en\/(?!(videos\/)).*')

    db_util = DBUtil()

    # Regex matchers for all fields for an image
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    def start_requests(self):
        url = "https://www.pixabay.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if response.status == 200:
            #body = Selector(text=response.body)
            #images = body.css('img.image-section__image').extract()
            hxs = Selector(response)
            images = hxs.xpath('//img[@itemprop="contentURL"]').extract()
            stemmer = PorterStemmer()

            for image in images:
                img_url = PixabayScraper.src_extractor.findall(image)[0]
                img_id = self.get_image_id(response.url)
                extracted_tags = [tag.replace(',', '').lower() for tag in PixabayScraper.tags_extractor.findall(image)[0].split(' ')]

                tags = [stemmer.stem(word) for word in extracted_tags if word not in stopwords.words('english')]

                PixabayScraper.db_util.create_index(img_id,
                                                   PixabayScraper.WEBSITE_ID,
                                                   img_url,
                                                   response.url,
                                                   tags)

            link_extractor = LinkExtractor(allow=PixabayScraper.url_matcher)
            next_links = filter(self.check_if_extracted,
                                map(lambda x: x.url, link_extractor.extract_links(response)))
            for link in next_links:
                yield scrapy.Request(link, self.parse)

    """
    Checks the database for the given url, if the image has already been extracted.
    Works based off of id for this particular website. 
    """
    def check_if_extracted(self, img_url):
        return not PixabayScraper.db_util.check_if_image_exists(PixabayScraper.WEBSITE_ID, self.get_image_id(img_url))

    def get_image_id(self, url):
        # Image urls are of type: https://www.pexels.com/photo/agriculture-countryside-crop-cropland-392100/
        return url.split('/')[-2].split('-')[-1]

