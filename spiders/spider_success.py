import scrapy
from scrapy import Selector
from kick.items import DmozItem
from kick.items import KickItem
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import json
import re

chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")

import pandas as pd

# 1 6 7 16
file = r'C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\art_link.csv'
df = pd.read_csv(file)
urls = list(df.loc[501:1000,'link'])

# class DmozSpider(scrapy.Spider):
#     name = "dmoz"
#     allowed_domains = ["dmoz-odp.org"]
#     start_urls = [
#         "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon"
#     ]
#     # def parse(self, response):
#     #     for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
#     #         url = response.urljoin(response.url, href.extract())
#     #         yield scrapy.Request(url, callback=self.parse_dir_contents)
#     def __init__(self):
#         self.browser = webdriver.Chrome(chrome_options=chorme_options)
#         super().__init__()
#
#     def start_requests(self):
#         url = "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon"
#         response = scrapy.Request(url, callback=self.parse)
#         yield response
#
#         # 整个爬虫结束后关闭浏览器
#     def close(self, spider):
#         self.browser.quit()
#
#     def parse(self, response):
#         for sel in response.xpath(".//*[@id='site-list-content']/div"):
#             # 实例化 DmozItem()
#             item = DmozItem()
#             item['title'] = sel.xpath('div[3]/a/div/text()').extract()
#             item['link'] = sel.xpath('div[3]/a/@href').extract()
#             item['desc'] = sel.xpath('div[3]/div/text()').extract()
#             yield item

class KickSpider(scrapy.Spider):
    name = "kick"
    # start_urls = [
    #     "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/artenvielfalt-ac/bluh-und-bienenwiese-in-der-aachener-region?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/sparrgames/keep-an-eye-out-make-100?ref=discovery_category_ending_soon",
    #     "https://www.kickstarter.com/projects/1286014/love-yourself-photography-book?ref=discovery_category_ending_soon"
    # ]

    def start_requests(self):
        # urls = [
        # #     # "https://www.kickstarter.com/projects/papershredder/sugar-high-birthday-card?ref=discovery_category_ending_soon",
        # # # "https://www.kickstarter.com/projects/artenvielfalt-ac/bluh-und-bienenwiese-in-der-aachener-region?ref=discovery_category_ending_soon",
        # # # "https://www.kickstarter.com/projects/sparrgames/keep-an-eye-out-make-100?ref=discovery_category_ending_soon",
        # # # "https://www.kickstarter.com/projects/1286014/love-yourself-photography-book?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/cloudy-comics/cloudy-comics-merchandise?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/unbornartstudios/rave-pin-series-1?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/saphirrannart/monsters-of-fantasy?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/trupotreats/vegan-crunch-bars?ref=recommendation-no-result-discoverpage-4",
        # # #     "https://www.kickstarter.com/projects/ksscomics/tales-from-neroesville-issues-1-2-and-3?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/valimor/makaidos-swiss-automatic-movt-watches-and-patented?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/pigeonoverlord/pigeon-overlord-geeky-unisex-shirts?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/256270160/warrior-cats-enamel-pins?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/1110317881/pms-bites-take-the-bite-out-of-pms?ref=discovery_category_ending_soon",
        # # #     "https://www.kickstarter.com/projects/50545525/union-webseries?ref=discovery_category_ending_soon",
        #     "https://www.kickstarter.com/projects/cloudy-comics/cloudy-comics-merchandise?ref=discovery_category_ending_soon",
        #     "https://www.kickstarter.com/projects/997998703/gravel-travel-system?ref=discovery_tag",
        #     "https://www.kickstarter.com/projects/wtfism/general-newsense-having-fun-creatively-corrupting-corruption?ref=discovery_category_ending_soon"
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
                item['project_name'] = \
                    response.xpath(
                        ".//*[@id='react-project-header']/div/div/div[2]/div/div[2]/div/h2/text()").extract()[0]
                item['project_description'] = response.xpath(
                    "normalize-space(.//*[@id='react-project-header']/div/div/div[2]/div/div[2]/div/p/text())").extract()[
                    0]
                item['project_location'] = response.xpath(".//span[@class='ml1']/text()").extract()[0].replace("\n","")
                item['subcategory'] = response.xpath(".//span[@class='ml1']/span/text()").extract()[0].replace("\n","")

                item['start_date'] = \
                    response.xpath(
                        ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[4]/p/time[1]/text()").extract()[
                        0]
                item['end_date'] = \
                    response.xpath(
                        ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[4]/p/time[2]/text()").extract()[
                        0]

                item['pledged'] = response.xpath(".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/span[1]/span/text()").extract()[
                    0]
                item['goal'] = \
                    response.xpath(
                        ".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[1]/span/span[2]/span/text()").extract()[
                        0]
                item['backers_count'] = response.xpath(".//*[@id='react-project-header']/div/div/div[1]/div[2]/div[2]/div[2]/div/span/text()").extract()

                item['creator_url'] = item['link'] + '/creator_bio'
                creatorurl = item['creator_url']
                item['creator_url'] = item['creator_url'].replace("https://www.kickstarter.com", '')
                item['faq_url'] = response.xpath(".//*[@id='faq-emoji']/@href").extract()[0]
                item['updates_url'] = response.xpath(".//*[@id='updates-emoji']/@href").extract()[0]
                item['comments_url'] = response.xpath(".//*[@id='comments-emoji']/@href").extract()[0]
                item['community_url'] = response.xpath(".//*[@id='community-emoji']/@href").extract()
                item['json_url'] = item['link']  + '/stats.json?v=1'
                if item['community_url'] is None:
                    item['community_url'] = ['None']
                item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
                item['video'] = response.xpath(".//*[@id='react-campaign']/descendant::video/source/@src").extract()
                item['pledge_money'] = response.xpath(
                    ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/h2/span[1]/text()").extract()
                item['pledge_name'] = response.xpath(
                    ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/h3/text()").extract()
                description = []
                ship = []
                backers = []
                delivery = []
                for sel in response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li"):
                    new_description = sel.xpath(
                        "string(.//div[@class='pledge__reward-description pledge__reward-description--expanded'])").extract()
                    # new_include = sel.xpath("div[2]/div[1]/ul/li/text()").extract()
                    new_backers = sel.xpath(
                        ".//span[@class='block pledge__backer-count']/text()|.//span[@class='pledge__backer-count']/text()").extract()
                    new_ship = sel.xpath("div[2]/div[2]/div[2]/span[2]/text()").extract()
                    new_delivery = sel.xpath("div[2]/div[2]/div[1]/span[2]/time/text()").extract()
                    new_backers = space_number(new_backers)[0]
                    description.append(new_description)
                    # include.append((new_include))
                    backers.append(new_backers)
                    ship.append(new_ship)
                    delivery.append(new_delivery)


                    # item['pledge_description'] = response.xpath(
                    #     ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/div[1]/p/text()").extract()
                    # # item['pledgoe_includes'] = response.xpath(
                    # #     ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/div[1]/ul/li/text()").extract()
                    # item['pledge_delivery'] = response.xpath(
                    #     ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/div[2]/div[1]/span[2]/time/text()").extract()
                    # item['pledge_backer'] = response.xpath(
                    #     ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/div[3]/span/text()").extract()
                    # item['pledge_ship'] = response.xpath(
                    #     ".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[2]/div/ol/li/div[2]/div[2]/div[2]/span[2]/text()").extract()
                item['pledge_description'] = description
                # item['pledge_includes'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/div[1]/ul/li/text()").extract()
                # item['pledge_includes']=include
                item['pledge_delivery'] = delivery
                # item['pledge_backer'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/div[3]/span/text()").extract()
                item['pledge_ship'] = ship
                item['pledge_backer'] = backers

                item['story'] = response.xpath("string(.//div[@class='rte__content'])").extract()
                item['risks'] = response.xpath("string(.//div[@id='risks-and-challenges'])").extract()
                item['environmental_commitments'] = response.xpath(
                    "string(.//div[@id='environmentalCommitments'])").extract()

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
                yield scrapy.Request(creatorurl, callback=self.parse_creator, meta={'item': item})

        else:
            # for sel in response.xpath(".//*[@id='content-wrap']"):
            # normalize-space()去掉换行符等



            item['project_name'] = response.xpath("normalize-space(.//*[@id='content-wrap']/section/div[3]/div[1]/h2/span/a/text())").extract()[0]
            item['project_description'] = response.xpath("normalize-space(.//*[@id='content-wrap']/section/div[3]/div[2]/div/div[2]/div[1]/div[2]/span/span/text())").extract()[0]
            # item['project_location'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[1]/div/div/a[1]/text())").extract()[0]
            item['project_location'] = response.xpath(".//a[@class='grey-dark mr3 nowrap type-12']/text()").extract()[0].replace('\n','')

            # item['subcategory'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[1]/div/div/a[2]/text())").extract()[0]
            item['subcategory'] = response.xpath(".//a[@class='grey-dark mr3 nowrap type-12']/text()").extract()[1].replace('\n','')
            item['start_date'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div/p/time[1]/text()").extract()[0]
            item['end_date'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div/p/time[2]/text()").extract()[0]

            item['pledged'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/h3/span/text())").extract()[0]
            item['goal'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/div/span/text()").extract()[0]
            item['backers_count'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[1]/div/div/div[2]/div[2]/h3/text())").extract()

            item['creator_url'] = response.xpath(".//*[@id='content-wrap']/section/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/a/@href").extract()[0]
            creatorurl = 'https://www.kickstarter.com/' + item['creator_url']
            item['faq_url'] = response.xpath(".//*[@id='faq-emoji']/@href").extract()[0]
            item['updates_url'] = response.xpath(".//*[@id='updates-emoji']/@href").extract()[0]
            item['comments_url'] = response.xpath(".//*[@id='comments-emoji']/@href").extract()[0]
            item['community_url'] = response.xpath(".//*[@id='community-emoji']/@href").extract()
            item['json_url'] = item['link'] + '/stats.json?v=1'

            if item['community_url'] is None:
                item['community_url'] = ['None']
            item['image'] = response.xpath(".//*[@id='react-campaign']/descendant::img/@src").extract()
            item['video'] = response.xpath(".//*[@id='react-campaign']/descendant::video/source/@src").extract()

            item['pledge_money'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/h2/span[1]/text()").extract()
            item['pledge_name'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/h3/text()").extract()
            # item['pledge_description'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/div[1]/p/text()").extract()
            description = []
            ship = []
            backers = []
            delivery = []
            for sel in response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li"):
                new_description = sel.xpath("string(.//div[@class='pledge__reward-description pledge__reward-description--expanded'])").extract()
                # new_include = sel.xpath("div[2]/div[1]/ul/li/text()").extract()
                new_backers = sel.xpath(".//span[@class='block pledge__backer-count']/text()|.//span[@class='pledge__backer-count']/text()").extract()
                new_ship = sel.xpath("div[2]/div[2]/div[2]/span[2]/text()").extract()
                new_delivery = sel.xpath("div[2]/div[2]/div[1]/span[2]/time/text()").extract()
                new_backers = space_number(new_backers)[0]
                description.append(new_description)
                # include.append((new_include))
                backers.append( new_backers)
                ship.append(new_ship)
                delivery.append(new_delivery)
            item['pledge_description'] = description
            # item['pledge_includes'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/div[1]/ul/li/text()").extract()
            # item['pledge_includes']=include
            item['pledge_delivery'] = delivery
            # item['pledge_backer'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[1]/div/div/div/div[2]/div/div[1]/div/ol/li/div[2]/div[3]/span/text()").extract()
            item['pledge_ship'] = ship
            item['pledge_backer']=backers

            item['story'] = response.xpath("string(.//div[@class='rte__content'])").extract()
            item['risks'] = response.xpath("string(.//div[@id='risks-and-challenges'])").extract()
            item['environmental_commitments'] = response.xpath("string(.//div[@id='environmentalCommitments'])").extract()

            budget1 = []
            budget2 = []
            budget3 = []
            budget4 = []
            for sel in response.xpath(".//*[@id='project-budget']/div/div[1]/div/div[1]/div"):
                category = sel.xpath(".//div[@class='flex flex1 items-center m0 type-16']/text()").extract()
                sub_category = sel.xpath(".//div[@class='flex flex1 m0 clip clamp-3 type-16 mr2']/text()").extract()
                category_cost = sel.xpath(".//div[@class='m0 pl1 pr3 type-16 text-nowrap']/text()").extract()
                sub_category_cost = sel.xpath(".//div[@class='m0 type-16 text-nowrap']/text()").extract()

                if len(category) >=1:
                    budget1.append(category)
                    budget2.append(sub_category)
                    budget3.append(category_cost)
                    budget4.append(sub_category_cost)

            item['budget_category'] = budget1
            item['budget_sub_category']=budget2
            item['budget_category_cost']=budget3
            item['budget_sub_category_cost']=budget4

            yield scrapy.Request(creatorurl, callback=self.parse_creator, meta={'item': item})



    def parse_creator(self, response):

        item = response.meta['item']
        item['creator'] = response.xpath(
            "normalize-space(.//*[@id='main_content']/header/div/div/div[2]/h1/a/text())").extract()[
            0]
        item['creator_location'] = response.xpath(".//*[@id='main_content']/header/div/div/div[2]/p/text()").extract()
        item['creator_description'] = response.xpath(".//*[@id='bio']/div/div[1]/div[1]/p/text()").extract()
        item['creator_realname'] = response.xpath("normalize-space(.//*[@id='bio']/div/div[2]/div[1]/span/span/text())").extract()
        item['creator_lastlogin'] = response.xpath("normalize-space(.//*[@id='bio']/div/div[2]/div[2]/time/text())").extract()
        item['creator_facebook'] = response.xpath(".//*[@id='bio']/div/div[2]/div[3]/span[2]/a/@href").extract()
        item['creator_created_count'] = response.xpath("normalize-space(.//*[@id='bio']/div/div[2]/div[4]/a[1]/text())").extract()
        item['creator_backed_count'] = response.xpath("normalize-space(.//*[@id='bio']/div/div[2]/div[4]/a[2]/text())").extract()
        item['creator_website'] = response.xpath(".//*[@id='bio']/div/div[1]/div[2]/ul/li/a/@href").extract()
        item['creator_id'] = re.findall("projects/(\w+)/",response.url)
        if len(item['creator_id']) == 0:
            item['creator_id'] = re.findall("projects/(\w+-\w+)/", response.url)

        #
        # faq_url = 'https://www.kickstarter.com' + item['faq_url']
        #
        # yield scrapy.Request(faq_url, callback=self.parse_faq, meta={'item':item})
        json_url = item['json_url']
        yield scrapy.Request(json_url, callback=self.parse_json, meta={'item':item})


    def parse_json(self, response):
        item = response.meta['item']

        item['state'] =json.loads(Selector(response=response).xpath('//pre/text()').get())['project']['state']
        item['id'] =json.loads(Selector(response=response).xpath('//pre/text()').get())['project']['id']

        faq_url = 'https://www.kickstarter.com' + item['faq_url']

        yield scrapy.Request(faq_url, callback=self.parse_faq, meta={'item':item})


    def parse_faq(self, response):
        item = response.meta['item']
        item['faq_count'] = response.xpath(".//*[@id='faq-emoji']/span/text()").extract()
        # item['faq_question'] = response.xpath(".//*span[@class='type-14 navy-700 medium']/text()").extract()
        item['faq_question'] = response.xpath(".//span[@class='type-14 navy-700 medium']/text()").extract()

        # for sel in response.xpath("//*[@id='project-faqs']/div/div/div[2]/ul/li/div[2]/div[1]"):
        #     answer = sel.xpath("")
        item['faq_answer'] = response.xpath(".//*[@id='project-faqs']/div/div/div[2]/ul/li/div[2]/div[1]/p/text()").extract()

        updates_url = 'https://www.kickstarter.com' + item['updates_url']

        yield scrapy.Request(updates_url, callback=self.parse_updates, meta={'item':item})

    def parse_updates(self, response):
        item = response.meta['item']
        item['updates_count'] = response.xpath(".//*[@id='updates-emoji']/span/text()").extract()
        hearts = []
        content = []
        title =[]
        date = []
        creator = []
        comments = []
        for sel in response.xpath(".//*[@id='project-post-interface']/div/div/div/div"):
            number = sel.xpath("div[2]/div/article/header/div[1]/div/span[1]/text()|a/div/article/header/div[1]/div/span/text()").extract()
            if len(number) !=0:
                if 'Update' in number[0]:
                    con = sel.xpath("string(.//div[@class='rte__content']/div)").extract()
                    if con == ['']:
                        con = sel.xpath("div[2]/div/article/div/h3/text()").extract()
                    tit = sel.xpath("a/div/article/header/h2/text()|div[2]/div/article/header/h2/text()").extract()
                    dat = sel.xpath("a/div/article/header/div[2]/div[2]/span/text()|div[2]/div/article/header/div[2]/div[2]/span/text()").extract()
                    creat = sel.xpath("a/div/article/header/div[2]/div[2]/div/text()|div[2]/div/article/header/div[2]/div[2]/div/text()").extract()
                    heart = sel.xpath("a/div/article/footer/div/div/span[2]/text()|div[2]/div/article/footer/div/div/span[2]/text()").extract()
                    if len(heart )==0:
                        heart = ['0']
                    else:
                        pass
                    comment= sel.xpath("a/div/article/footer/div/div/span[1]/text()|div[2]/div/article/footer/div/div/span[1]/text()").extract()
                    if len(comment)==0:
                        comment = ['0']
                    else:
                        pass
                    hearts.append(heart)
                    content.append(con)
                    title.append(tit)
                    date.append(dat)
                    creator.append(creat)
                    comments.append(comment)
        item['updates_content'] = content
        item['updates_title'] = title
        item['updates_date'] = date
        item['updates_creator'] = creator
        item['updates_heart'] = hearts
        item['updates_comments'] = comments
        # item['updates_content'] = response.xpath(".//*[@id='project-post-interface']/div/div/div/div/a/@href").extract()
        # item['updates_title'] = response.xpath(".//*[@id='project-post-interface']/div/div/div/div/a/div/article/header/h2/text()").extract()
        # item['updates_date'] = response.xpath(".//*[@id='project-post-interface']/div/div/div/div/a/div/article/header/div[2]/div[2]/span//text()").extract()

        comments_url = 'https://www.kickstarter.com' + item['comments_url']
        yield scrapy.Request(comments_url, callback=self.parse_comments, meta={'item':item})

        # if len(item['community_url']) == 1:
        #     community_url =  'https://www.kickstarter.com' +item['community_url'][0]
        #     yield scrapy.Request(community_url, callback=self.parse_community, meta={'item':item})
        # else:
        #     yield item

    def parse_comments(self, response):
        item = response.meta['item']

        ################
        item['comments_count'] = response.xpath(".//*[@id='comments-emoji']/span/data").extract()
        content = []
        title = []
        date = []
        name = []
        reply_contents = []
        reply_titles = []
        reply_dates = []
        reply_names = []

        if int(item['comments_count'][0]) != 0:
            for sel in response.xpath(".//*[@id='react-project-comments']/ul/li"):
                if sel.xpath("div[1]/p/a/text()").extract() == ['Show the comment.']:
                    con = ['Canceled']
                    tit = ['Canceled']
                    dat = ['Canceled']
                    nam = ['Canceled']
                else:
                    con = sel.xpath("string(div/div[2]/div/p)").extract()

                    tit = sel.xpath("div/div[1]/div/div/span[2]/span/text()").extract()
                    if tit == []:
                        tit = ['None']
                    dat = sel.xpath(
                        "div/div[1]/div/div/a/time/text()").extract()
                    nam = sel.xpath(
                        "div/div[1]/div/div/span[1]/text()").extract()

                    reply_content = []
                    reply_title = []
                    reply_date = []
                    reply_name = []
                    if len(sel.xpath("div[2]/ul/li/div").extract())!=0:
                        for reply in sel.xpath("div[2]/ul/li/div"):
                            if reply.xpath("p/a/text()").extract() == ['Show the comment.']:
                                reply_nam = ['Canceled']
                                reply_tit = ['Canceled']
                                reply_dat = ['Canceled']
                                reply_con = ['Canceled']
                            else:
                                reply_nam = reply.xpath("div[1]/div/div/span[1]/text()").extract()
                                reply_tit = reply.xpath("div[1]/div/div/span[2]/span/text()").extract()
                                if reply_tit == []:
                                    reply_tit = ['None']
                                reply_dat = reply.xpath("div[1]/div/div/a/time").extract()
                                reply_con = reply.xpath("string(div[2]/div/p)").extract()
                            reply_content.append(reply_con)
                            reply_title.append(reply_tit)
                            reply_date.append(reply_dat)
                            reply_name.append(reply_nam)

                content.append(con)
                title.append(tit)
                date.append(dat)
                name.append(nam)
                reply_contents.append(reply_content)
                reply_titles.append(reply_title)
                reply_dates.append(reply_date)
                reply_names.append(reply_name)
            item['comments_content'] = content
            item['comments_title'] = title
            item['comments_date'] = date
            item['comments_name'] = name
            item['recomments_name_list'] = reply_names
            item['recomments_date_list'] = reply_dates
            item['recomments_title_list'] = reply_titles
            item['recomments_content_list'] = reply_contents
        ################

        # item['comments_count'] = response.xpath(".//*[@id='comments-emoji']/span/data/text()").extract()
        # item['comments_name'] = response.xpath(".//*[@id='react-project-comments']/ul/li/div[1]/div[1]/div/div/span[1]/text() | .//*[@id='react-project-comments']/ul/li/div[2]/ul/li/div/div[1]/div/div/span[1]/text()").extract()
        # item['comments_date'] = response.xpath(".//*[@id='react-project-comments']/ul/li/div/div[1]/div/div/a/time/text() | .//*[@id='react-project-comments']/ul/li/div[2]/ul/li/div/div[1]/div/div/a/time/text()").extract()
        # item['comments_content'] = response.xpath(".//*[@id='react-project-comments']/ul/li/div/div[2]/div/p/text() | .//*[@id='react-project-comments']/ul/li/div[2]/ul/li/div/div[2]/div/p/text()").extract()

        # item['updates_count'] = response.xpath(".//*[@id='updates-emoji']/span/text()").extract()
        print(item['community_url'])
        if len(item['community_url']) == 1:
            community_url =  'https://www.kickstarter.com' +item['community_url'][0]
            yield scrapy.Request(community_url, callback=self.parse_community, meta={'item':item})
        else:
            yield item

    def parse_community(self, response):
        item = response.meta['item']
        item['community_topcity_city'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[8]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/a/text()").extract()
        item['community_topcity_country'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[8]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/a/text()").extract()
        item['community_topcity_backers'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[8]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div/text()").extract()

        item['community_topcountry_country'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[8]/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[1]/div/a/text()").extract()
        item['community_topcountry_backers'] = response.xpath(".//*[@id='content-wrap']/div[2]/section[8]/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/div/text()").extract()

        item['newbacker'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[8]/div/div[3]/div/div/div/div/div[1]/div[1]/text())").extract()
        item['oldbacker'] = response.xpath("normalize-space(.//*[@id='content-wrap']/div[2]/section[8]/div/div[3]/div/div/div/div/div[2]/div[1]/text())").extract()

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