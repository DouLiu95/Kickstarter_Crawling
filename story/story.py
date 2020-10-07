import scrapy
from scrapy import Selector
from kick.items import DmozItem
from kick.items import KickItem
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import json
import re
from kick.spiders.check import check_comments,check_updates,check_txt,get_link,miss_link,miss_story,get_own_link

chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")

import pandas as pd
path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
df = pd.read_csv(path)
link1 = get_own_link(df)
# urls = miss_link(link1,link2)
# print(urls,len(urls))
urls = miss_story(link1)
# 1 6 7 16
# file = r'C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\tech_link.csv'
# df = pd.read_csv(file)
# urls = list(df.loc[13846:15000,'link'])
# print(urls)

class KickSpider(scrapy.Spider):
    name = "story"
    # start_urls = [
    #     "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/artenvielfalt-ac/bluh-und-bienenwiese-in-der-aachener-region?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/sparrgames/keep-an-eye-out-make-100?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/1286014/love-yourself-photography-book?ref=discovery_category_ending_soon"
    # ]

    def start_requests(self):
        # urls = [
        #     # "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon",
        # # "https://www.kickstarter.com/projects/artenvielfalt-ac/bluh-und-bienenwiese-in-der-aachener-region?ref=discovery_category_ending_soon",
        # # "https://www.kickstarter.com/projects/sparrgames/keep-an-eye-out-make-100?ref=discovery_category_ending_soon",
        # # "https://www.kickstarter.com/projects/1286014/love-yourself-photography-book?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/cloudy-comics/cloudy-comics-merchandise?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/unbornartstudios/rave-pin-series-1?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/saphirrannart/monsters-of-fantasy?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/trupotreats/vegan-crunch-bars?ref=recommendation-no-result-discoverpage-4",
        # #     "https://www.kickstarter.com/projects/ksscomics/tales-from-neroesville-issues-1-2-and-3?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/valimor/makaidos-swiss-automatic-movt-watches-and-patented?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/pigeonoverlord/pigeon-overlord-geeky-unisex-shirts?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/256270160/warrior-cats-enamel-pins?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/1110317881/pms-bites-take-the-bite-out-of-pms?ref=discovery_category_ending_soon",
        # #     "https://www.kickstarter.com/projects/50545525/union-webseries?ref=discovery_category_ending_soon",
        #     "https://www.kickstarter.com/projects/cloudy-comics/cloudy-comics-merchandise?ref=discovery_category_ending_soon",
        #     "https://www.kickstarter.com/projects/541894646/adventure-time-cmon-grab-your-friends-posters?ref=discovery_tag",
        #     "https://www.kickstarter.com/projects/monsterwax/horrible-ugly-monsters-monsterwax-trading-cards-promo-1?ref=discovery_tag"
        # ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # def __init__(self):


    def parse(self, response):

        item = KickItem()
        item['project_status'] = response.xpath(
            ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[3]/div[1]/text()").extract()
        pattern = re.compile(r'\?ref\=.*')
        item['daystogo'] = response.xpath(".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[3]/div/div/span[2]/text()").extract()
        if len(item['daystogo']) >=1 :
            yield item

        item['link'] = re.sub(pattern,'',response.url)
        if len(item['project_status']) == 1:
            if item['project_status'][0] == "Funding Unsuccessful":



                item['json_url'] = item['link']  + '/stats.json?v=1'

                item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
                item['video'] = response.xpath(".//*[@id='react-campaign']/descendant::video/source/@src").extract()



                item['story'] = response.xpath("string(.//div[@class='rte__content'])").extract()
                item['risks'] = response.xpath("string(.//div[@id='risks-and-challenges'])").extract()
                item['environmental_commitments'] = response.xpath(
                    "string(.//div[@id='environmentalCommitments'])").extract()
                if item['story'][0] == '':
                    item['image'] = response.xpath(".//*[@class='mb3']/descendant::img/@src").extract()
                    item['video'] = response.xpath(".//*[@class='mb3']/descendant::video/source/@src").extract()

                    item['story'] = response.xpath("string(.//div[@class='rte__content js-full-description responsive-media'])").extract()
                    item['risks'] = response.xpath("string(.//div[@id='mb3 mb10-sm mb3 js-risks'])").extract()
                json_url = item['json_url']
                yield scrapy.Request(json_url, callback=self.parse_json, meta={'item': item})
        else:
            # for sel in response.xpath(".//*[@id='content-wrap']"):
            # normalize-space()去掉换行符等




            item['json_url'] = item['link'] + '/stats.json?v=1'


            item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
            item['video'] = response.xpath(".//*[@id='react-campaign']/descendant::video/source/@src").extract()



            item['story'] = response.xpath("string(.//div[@class='rte__content'])").extract()
            item['risks'] = response.xpath("string(.//div[@id='risks-and-challenges'])").extract()
            item['environmental_commitments'] = response.xpath("string(.//div[@id='environmentalCommitments'])").extract()
            if item['story'][0] == '':
                item['image'] = response.xpath(".//*[@class='mb3']/descendant::img/@src").extract()
                item['video'] = response.xpath(".//*[@class='mb3']/descendant::video/source/@src").extract()

                item['story'] = response.xpath(
                    "string(.//div[@class='rte__content js-full-description responsive-media'])").extract()
                item['risks'] = response.xpath("string(.//div[@id='mb3 mb10-sm mb3 js-risks'])").extract()
            json_url = item['json_url']
            yield scrapy.Request(json_url, callback=self.parse_json, meta={'item': item})
            # yield item


    def parse_json(self, response):
        item = response.meta['item']

        item['state'] =json.loads(Selector(response=response).xpath('//pre/text()').get())['project']['state']
        item['id'] =json.loads(Selector(response=response).xpath('//pre/text()').get())['project']['id']

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