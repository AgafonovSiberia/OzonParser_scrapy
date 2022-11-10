import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from parser.spider import OzonSpider


settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(OzonSpider)
process.start()
