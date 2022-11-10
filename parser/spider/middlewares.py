import time
from scrapy import signals
from scrapy.http import HtmlResponse

from parser.services.selenium_stealth_response import SeleniumStealthRequest
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

        if request.script:
            time.sleep(5)
            self.driver.execute_script(request.script)
            time.sleep(5)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until)

        if request.wait_time:
            time.sleep(request.wait_time)

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


