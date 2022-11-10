import time
from scrapy import signals
from scrapy.http import HtmlResponse

from parser.services.http_request import SeleniumStealthRequest
from parser.services.web_driver import create_web_driver_stealth
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumStealthMiddleware:
    """ Execute requests by using selenium_web_driver_stealth """
    driver = create_web_driver_stealth()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumStealthRequest):
            return None

        self.driver.get(request.url)

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie({'name': cookie_name, 'value': cookie_value})

        if request.page_scroll:
            time.sleep(request.timeout)
            self.driver.execute_script("window.scrollTo(5, 4000);")
            time.sleep(request.timeout)

        if request.screenshot:
            self.driver.save_screenshot("screen.png")

        body = str.encode(self.driver.page_source)

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.driver.close()
        self.driver.quit()


