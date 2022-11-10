from scrapy import Request


class SeleniumStealthRequest(Request):
    def __init__(self, wait_time: int = None, wait_until=None, screenshot: bool = False,
                 script: str = None, *args, **kwargs):
        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script

        super().__init__(*args, **kwargs)
