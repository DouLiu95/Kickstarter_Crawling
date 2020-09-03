# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Scrapy 内置的 Downloader Middleware 为 Scrapy 供了基础的功能，
# 定义一个类，其中（object）可以不写，效果一样
class SimpleProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                li =[]
                # p = json.loads(response.text).get('data').get('proxy_list')
                p = json.loads(response.text).get('list')
                for key in json.loads(json.dumps(p)):
                    li.append(key)
                i = random.choice(li)
                # p = p.get('data').get('proxy_list')
                # i = random.choice(range(len(p)))
                proxy = '{}:{}@{}:{}'.format(p[i].get('user'),p[i].get('pass'),p[i].get('ip'), p[i].get('port'))

                # proxy = p[random.choice(range(len(p)))]
                print('get proxy ...',proxy)
                # ip = {"http": "http://" + proxy, "https": "https://" + proxy}

                ip = {"http": "http://"+ proxy, "https": "https://" + proxy}
                r = requests.get("https://www.kickstarter.com", proxies=ip, timeout=8)
                if r.status_code == 200:
                    return proxy
        except:
            print('get proxy again ...')
            return self.get_random_proxy()

    def process_request(self, request, spider):
        if 'ref=' in request.url or 'comments' in request.url or 'post' in request.url:
            proxy = self.get_random_proxy()
            if proxy:
                self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
                request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("again response ip:")
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=self.get_random_proxy())
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class KickSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def process_request(self, request, spider):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)

        if 'post' in request.url:
            self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                           executable_path='C:\\Users\\LDLuc\\PycharmProjects\\tutorial-env\\Scripts\\chromedriver.exe')
            try:
                self.driver.get(request.url)
                self.driver.implicitly_wait(1)
                time.sleep(1)
                button = ".//*[@id='project-post-interface']/div/div/div/div/div/button"
                while True:
                    if len(self.driver.find_elements_by_xpath(button))> 0:
                        self.driver.find_element_by_xpath(button).click()
                        time.sleep(2)
                    else:
                        print("No Button")
                        break
                html = self.driver.page_source
                self.driver.quit()
                return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                                request =request)

            except:
                print( "get updates data failed")
        elif 'comments' in request.url:
            self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                           executable_path='C:\\Users\\LDLuc\\PycharmProjects\\tutorial-env\\Scripts\\chromedriver.exe')
            try:
                self.driver.get(request.url)
                self.driver.implicitly_wait(1)
                time.sleep(1)
                button = ".//*[@id='react-project-comments']/div/button"
                while True:
                    if len(self.driver.find_elements_by_xpath(button)) > 0:
                        self.driver.find_element_by_xpath(button).click()
                        time.sleep(2)
                    else:
                        print("No Button")
                        break
                html = self.driver.page_source
                self.driver.quit()
                return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                                request=request)

            except:
                print("get updates data failed")


        else:
        # 指定谷歌浏览器路径
            self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='C:\\Users\\LDLuc\\PycharmProjects\\tutorial-env\\Scripts\\chromedriver.exe')
            self.driver.get(request.url)
            time.sleep(1)
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                            request=request)
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KickDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None
        pass

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
