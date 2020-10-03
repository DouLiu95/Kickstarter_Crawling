import scrapy
from scrapy import Selector
from kick.items import DmozItem
from kick.items import KickItem
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import json
import re
from kick.spiders.check import check_comments,check_updates,check_txt,get_link,miss_link,miss_story,get_own_link,miss_updates



import pandas as pd
path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
df = pd.read_csv(path)
# urls = miss_link(link1,link2)
# print(urls,len(urls))
# urls = miss_updates(df)
urls=[(1177221773,"https://www.kickstarter.com/projects/hypnonightmares/the-lucid-nightmare-project/posts"),
      (1177221773,"https://www.kickstarter.com/projects/hypnonightmares/the-lucid-nightmare-project/comments")]
# 1 6 7 16
# file = r'C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\tech_link.csv'
# df = pd.read_csv(file)
# urls = list(df.loc[13846:15000,'link'])
# print(urls)

class KickSpider(scrapy.Spider):
    name = "updates"
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
            if r'/posts' in url[1]:

                yield scrapy.Request(url=url[1], callback=self.parse_posts,meta={'url':url})
            elif r'/comments' in url[1]:
                yield scrapy.Request(url=url[1], callback=self.parse_comments,meta={'url':url})
            # def __init__(self):


    def parse_posts(self, response):
        id = response.meta['url']
        item = KickItem()
        item['id'] = id[0]
        item['updates_url'] = id[1]
        item['category'] = 0
        item['updates_count'] = response.xpath(".//*[@id='updates-emoji']/span/text()").extract()
        hearts = []
        content = []
        title = []
        date = []
        creator = []
        comments = []
        for sel in response.xpath(".//*[@id='project-post-interface']/div/div/div/div"):
            number = sel.xpath(
                "div[2]/div/article/header/div[1]/div/span[1]/text()|a/div/article/header/div[1]/div/span/text()").extract()
            if len(number) != 0:
                if 'Update' in number[0]:
                    con = sel.xpath("string(.//div[@class='rte__content']/div)").extract()
                    if con == ['']:
                        con = sel.xpath("div[2]/div/article/div/h3/text()").extract()
                    tit = sel.xpath("a/div/article/header/h2/text()|div[2]/div/article/header/h2/text()").extract()
                    dat = sel.xpath(
                        "a/div/article/header/div[2]/div[2]/span/text()|div[2]/div/article/header/div[2]/div[2]/span/text()").extract()
                    creat = sel.xpath(
                        "a/div/article/header/div[2]/div[2]/div/text()|div[2]/div/article/header/div[2]/div[2]/div/text()").extract()
                    heart = sel.xpath(
                        "a/div/article/footer/div/div/span[2]/text()|div[2]/div/article/footer/div/div/span[2]/text()").extract()
                    if len(heart) == 0:
                        heart = ['0']
                    else:
                        pass
                    comment = sel.xpath(
                        "a/div/article/footer/div/div/span[1]/text()|div[2]/div/article/footer/div/div/span[1]/text()").extract()
                    if len(comment) == 0:
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

        yield item
            # yield item


    def parse_comments(self, response):
        id = response.meta['url']
        item = KickItem()
        item['id'] = id[0]
        item['comments_url'] = id[1]
        item['category'] = 1
        item['comments_count'] = response.xpath(".//*[@id='comments-emoji']/span/data/text()").extract()
        content = []
        title = []
        date = []
        name = []
        reply_contents = []
        reply_titles = []
        reply_dates = []
        reply_names = []

        if int(space_number(item['comments_count'])[0]) != 0:
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
                    if len(sel.xpath("div[2]/ul/li/div").extract()) != 0:
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
                                reply_dat = reply.xpath("div[1]/div/div/a/time/text()").extract()
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