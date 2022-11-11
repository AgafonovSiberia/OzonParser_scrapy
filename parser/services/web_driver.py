from scrapy import Request
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_web_driver_stealth() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    s = Service(ChromeDriverManager().install())
    stealth_driver = webdriver.Chrome(service=s, options=options)

    stealth(stealth_driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return stealth_driver


class SeleniumStealthRequest(Request):
    def __init__(self, timeout: int = 0, page_scroll: bool = False, screenshot: bool = False,
                 *args, **kwargs):
        self.timeout = timeout
        self.page_scroll = page_scroll
        self.screenshot = screenshot

        super().__init__(*args, **kwargs)
