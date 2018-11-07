# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


from scrapy.spiders import Rule, CrawlSpider


def field_validator(field):
    if field:
        field = field
    else:
        field = 'n/a'

    return field


class DealsSpider(CrawlSpider):
    name = 'deals'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        DealsSpider.rules = [
           Rule(LinkExtractor(unique=True), callback='parse_products'),
        ]
        super(DealsSpider, self).__init__(*args, **kwargs)


    def parse_products(self, response):
        products = response.xpath('//a[@class="link"]/@href').extract()
        for product in products:
            yield Request(product, callback=self.parse_page)

        # next page URL
        # next_page_url = response.xpath(
        #     '//a[@title="Next"]/@href').extract_first()
        # yield Request(next_page_url)

    def parse_page(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first()
        product_url = response.url
        brand = response.xpath(
            '//div[@class="sub-title"]/a/text()').extract_first()
        price = '#' + response.xpath(
            '//span[contains(@class, "price")]/span[@dir="ltr"]/@data-price'
        ).extract_first()
        rating1 = response.xpath(
            '//div[@class="container"]/i/following-sibling::span/text()'
        ).extract_first()
        rating2 = response.xpath(
            '//div[@class="container"]/following-sibling::footer/text()'
        ).extract_first()
        rating = rating1 + ': ' + rating2
        rating = rating.replace(',', '.')
        image_urls = response.xpath(
            '//div[@id="thumbs-slide"]/a/@href').extract()
        description = response.xpath(
            '//div[@class="product-description"]/text()').extract_first()

        # Validate fields
        title = field_validator(title)
        product_url = field_validator(product_url)
        brand = field_validator(brand)
        price = field_validator(price)
        rating = field_validator(rating)
        image_urls = field_validator(image_urls)
        description = field_validator(description)

        return {
            'title': title,
            'product_url': product_url,
            'brand': brand,
            'price': price,
            'rating': rating,
            'image_urls': image_urls,
            'description': description
        }