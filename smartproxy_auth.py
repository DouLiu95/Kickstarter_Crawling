import base64
from scrapy.http import HtmlResponse
from scrapy import signals
from selenium import webdriver

from selenium.webdriver import FirefoxOptions
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium.webdriver.chrome.options import Options
import time
import scrapy
import requests
import json
import logging
import random
class ProxyMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)

        self.user = settings.get('SMARTPROXY_USER')
        self.password = settings.get('SMARTPROXY_PASSWORD')
        self.endpoint = settings.get('SMARTPROXY_ENDPOINT')
        self.port = settings.get('SMARTPROXY_PORT')

    def process_request(self, request, spider):

        user_credentials = '{user}:{passw}'.format(user=self.user, passw=self.password)
        basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
        host = 'http://{endpoint}:{port}'.format(endpoint=self.endpoint, port=self.port)
        self.logger.debug('======' + '使用代理 ' + str(host) + "======")
        request.meta['proxy'] = host
        request.headers['Proxy-Authorization'] = basic_authentication
        self.logger.debug('======'  + str(request) + "======")


