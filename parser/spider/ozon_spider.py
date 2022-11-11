import json
import pandas as pd

from scrapy import Spider, signals

from parser.spider.settings import custom_settings, PRODUCT_COUNT
from parser.spider.urls import BASE_URL, API_URL, API_URL_PARAMS, BASE_URL_PARAMS_SORTING, CATEGORY_URL

from parser.services.web_driver import SeleniumStealthRequest
from parser.services.utils import parse_os_from_json
from parser.services.logging import base_logger


class OzonSpider(Spider):
    products_urls = []
    products_os = []

    name = 'ozonspider'
    allowed_domains = ['ozon.ru']
    custom_settings = custom_settings

    def start_requests(self):
        base_logger.info("Start scraping")
        url = f"{BASE_URL}{CATEGORY_URL}{BASE_URL_PARAMS_SORTING}"
        print(url)
        yield SeleniumStealthRequest(url=url, callback=self.parse_products_urls, screenshot=True,
                                     page_scroll=True, timeout=5)

    def parse_products_urls(self, response):
        urls = response.css("div.kr4").css("a::attr(href)").extract()
        self.products_urls.extend(urls)

        next_page_button = response.css("div._4-a").css("a::attr(href)").extract_first()
        if next_page_button and len(self.products_urls) < PRODUCT_COUNT:
            print(next_page_button)
            base_logger.info(f"Parse next page")
            yield SeleniumStealthRequest(
                url=f"{BASE_URL}{next_page_button}",
                callback=self.parse_products_urls,
                screenshot=True, page_scroll=True, timeout=5
            )

        base_logger.info(f"Current count urls : {len(self.products_urls)}")

        for url in self.products_urls[:PRODUCT_COUNT]:
            yield SeleniumStealthRequest(url=f"{API_URL}{url}{API_URL_PARAMS}", callback=self.parse_products_os)

    def parse_products_os(self, response):
        response = response.css("pre::text").get()
        if response:
            response_json = json.loads(response)
            os = parse_os_from_json(data_json=response_json)
            self.products_os.append(os)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OzonSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        result_series = pd.Series(self.products_os).value_counts()

        base_logger.info(f"\n{result_series}")

        with open("result.json", "w", encoding="utf-8") as result_file:
            result_file.write(json.dumps(result_series.to_json()))

        base_logger.info(f"Spider closed")
