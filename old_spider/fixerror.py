import scrapy
from scrapy import Selector
from kick.items import DmozItem
from kick.items import KickItem
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import json
import re
from kick.spiders.check import check_comments,check_updates,check_txt,get_link,miss_link,miss_story,get_own_link,miss_updates,miss_updates_csv,miss_budget,find_error



import pandas as pd

# urls = find_error('kick')

class KickSpider(scrapy.Spider):
    name = "error"


    def start_requests(self):
        urls = [ ('1903666410', 'https://www.kickstarter.com//projects/norenrealm/moth-moon-and-stag?ref=discovery_category_ending_soon')]
        for url in urls:
            yield scrapy.Request(url=url[1], callback=self.parse,meta={'url':url})

    def parse(self, response):

        id = response.meta['url']
        item = KickItem()
        item['id'] = id[0]
        item['link'] = id[1]
        item['project_status'] = response.xpath(
            ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[3]/div[1]/text()").extract()
        pattern = re.compile(r'\?ref\=.*')


        if len(item['project_status']) == 1:
            if item['project_status'][0] == "Funding Unsuccessful":
                item['pledged'] = response.xpath(
                    ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/span[1]/span/text()").extract()
                if not item['pledged']:
                    item['pledged'] = ['None']
                item['goal'] = \
                    response.xpath(
                        ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[1]/span/span[2]/span/text()").extract()
                if not item['goal']:
                    item['goal'] = response.xpath(
                        ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[1]/span/span[2]/button/span/span/text()").extract()
                    if not item['goal']:
                        item['goal'] = ['None']
                item['backers_count'] = response.xpath(
                    ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[2]/div/span/text()").extract()
                item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
                item['video'] = response.xpath(".//*/descendant::video/source/@src").extract()
                budget1 = []
                budget2 = []
                budget3 = []
                budget4 = []
                for sel in response.xpath(".//*[@id='project-budget']/div/div[1]/div/div[1]/div"):
                    category = sel.xpath(".//div[@class='flex flex1 items-center m0 type-16']/text()").extract()
                    sub_category = sel.xpath(".//div[@class='flex flex1 m0 clip clamp-3 type-16 mr2']/text()").extract()
                    category_cost = sel.xpath(".//div[@class='m0 pl1 pr3 type-16 text-nowrap']/text()").extract()
                    sub_category_cost = sel.xpath(".//div[@class='m0 type-16 text-nowrap']/text()").extract()

                    if len(category) >= 1:
                        budget1.append(category)
                        budget2.append(sub_category)
                        budget3.append(category_cost)
                        budget4.append(sub_category_cost)

                item['budget_category'] = budget1
                item['budget_sub_category'] = budget2
                item['budget_category_cost'] = budget3
                item['budget_sub_category_cost'] = budget4
                yield item

        else:
            # for sel in response.xpath(".//*[@id='content-wrap']"):
            # normalize-space()去掉换行符等

            item['pledged'] = response.xpath(
                "normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/h3/span/text())").extract()
            if not item['pledged']:
                item['pledged'] = ['None']
            item['goal'] = response.xpath(
                ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/div/span/text()").extract()
            if not item['goal']:
                item['goal'] = ['None']
            item['backers_count'] = response.xpath(
                "normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[2]/h3/text())").extract()





            item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
            item['video'] = response.xpath(".//*/descendant::video/source/@src").extract()


            budget1 = []
            budget2 = []
            budget3 = []
            budget4 = []
            for sel in response.xpath(".//*[@id='project-budget']/div/div[1]/div/div[1]/div"):
                category = sel.xpath(".//div[@class='flex flex1 items-center m0 type-16']/text()").extract()
                sub_category = sel.xpath(".//div[@class='flex flex1 m0 clip clamp-3 type-16 mr2']/text()").extract()
                category_cost = sel.xpath(".//div[@class='m0 pl1 pr3 type-16 text-nowrap']/text()").extract()
                sub_category_cost = sel.xpath(".//div[@class='m0 type-16 text-nowrap']/text()").extract()

                if len(category) >= 1:
                    budget1.append(category)
                    budget2.append(sub_category)
                    budget3.append(category_cost)
                    budget4.append(sub_category_cost)

            item['budget_category'] = budget1
            item['budget_sub_category'] = budget2
            item['budget_category_cost'] = budget3
            item['budget_sub_category_cost'] = budget4

            yield item


def space_number(list):
    if len(list)>=1 :
        new_list = []
        for element in list:
            if element == '\n':
                pass
            else:
                a = re.sub(r'\s+','', element)
                new_element = re.sub("[^0-9]", "",a)
                new_list.append(new_element)
        ls = [x for x in new_list if x != '']
        return ls
    else:
        return [int(0)]