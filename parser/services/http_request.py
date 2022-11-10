from scrapy import Request


class SeleniumStealthRequest(Request):
    def __init__(self, timeout: int = 0, page_scroll: bool = False, screenshot: bool = False,
                 *args, **kwargs):
        self.timeout = timeout
        self.page_scroll = page_scroll
        self.screenshot = screenshot

        super().__init__(*args, **kwargs)
