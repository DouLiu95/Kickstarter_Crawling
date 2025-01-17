# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class KickBudgetPipeline:
    collection = 'kick'
    collection2 = 'budget'

    def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        '''
        保存story risk environmentalcommitments
        '''
        filter_kick = {'project_id':item['id']}

        table = self.db[self.collection]
        # table.insert_one(data)

        # Updating fan quantity form 10 to 25.

        # Values to be updated.
        newvalues = {"$set": {'image_count': len(item['image']),
                              'video_count': len(item['video']),
                              'pledged':item['pledged'][0],
                              'goal':item['goal'][0],
                              'backers_count':item['backers_count'][0]}}

        # Using update_one() method for single
        # updation.
        table.update_many(filter_kick, newvalues)
        self.txtname = r"C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\fixerror.txt"
        self.file = open(self.txtname, 'w', encoding='utf-8')
        try:
            self.file.write(item['link'] + '\n')

        except:
            pass
        self.file.close()
        if len(item['budget_category']) >=1:
            cost  = 0
            for i in range(len(item['budget_category_cost'])):
                cost += int(space_number(item['budget_category_cost'][i])[0])


            for i in range(len(item['budget_category'])):
                category = item['budget_category'][i][0]
                category_cost = item['budget_category_cost'][i][0]
                category_count = len(item['budget_category'])
                if item['budget_sub_category'][i]==[]:
                    data_budget = {
                        'project_id': item['id'],
                        'total_budget': cost,
                        'category': category,
                        'category_cost': category_cost,
                        'category_count': category_count,
                        'sub_category': 'Empty',
                        'sub_category_cost': 'Empty',
                        'sub_category_count': 'Empty'

                    }
                    table = self.db[self.collection2]
                    table.insert_one(data_budget)
                else:
                    for j in range(len(item['budget_sub_category'][i])):
                        sub_category = item['budget_sub_category'][i][j]
                        sub_category_cost = item['budget_sub_category_cost'][i][j]
                        sub_category_count = len(item['budget_sub_category'][i])
                        data_budget = {
                            'project_id': item['id'],
                            'total_budget':cost,
                            'category' : category,
                            'category_cost': category_cost,
                            'category_count':category_count,
                            'sub_category': sub_category,
                            'sub_category_cost':sub_category_cost,
                            'sub_category_count':sub_category_count

                        }
                        table = self.db[self.collection2]
                        table.insert_one(data_budget)
        return item

class KickUpdatesCommentsPipeline:
    collection = 'updates'
    collection2 = 'comments'

    def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        '''
        保存story risk environmentalcommitments
        '''
        if item['category'] == 0:
            filter = {'project_id': item['id'],'updates_title': 'Error'}
            print(filter)
            table = self.db[self.collection]
            table.remove(filter)
            for i in range(len( item['updates_title'])):
                date = Date2(item['updates_date'][i][0])
                if len(item['updates_content'][i]) == 0:
                    item['updates_content'][i].append('No content')
                data_updates = {
                    'project_id': item['id'],
                    'updates_count': int(space_number(item['updates_count'])[0]),
                    'updates_title': item['updates_title'][i][0],
                    'updates_creator': item['updates_creator'][i][0],
                    'updates_date': date,

                    'updates_content': item['updates_content'][i][0],
                    'updates_heart': int(item['updates_heart'][i][0]),
                    'updates_comments': int(item['updates_comments'][i][0])

                }
                # table = self.db[self.collection]
                table.insert_one(data_updates)
        elif item['category'] == 1:
            if True:
                for i in range(len(item['comments_name'])):
                    if len(item['comments_date'][i]) == 0:
                        pass

                    elif len(item['recomments_name_list'][i]) != 0:
                        for j in range(len(item['recomments_name_list'][i])):
                            data_comments = {
                                'project_id': item['id'],
                                'comments_count': int(space_number(item['comments_count'])[0]),
                                'comments_name': item['comments_name'][i][0],
                                'comments_title': item['comments_title'][i][0],
                                'comments_date': item['comments_date'][i][0],
                                'comments_content': item['comments_content'][i][0],
                                'reply_count': len(item['recomments_name_list'][i]),
                                'reply_name': item['recomments_name_list'][i][j][0],
                                'reply_title': item['recomments_title_list'][i][j][0],
                                'reply_date': item['recomments_date_list'][i][j][0],
                                'reply_content': item['recomments_content_list'][i][j][0],
                            }
                            table = self.db[self.collection2]
                            table.insert_one(data_comments)
                    else:
                        data_comments = {
                            'project_id': item['id'],
                            'comments_count': int(space_number(item['comments_count'])[0]),
                            'comments_name': item['comments_name'][i][0],
                            'comments_title': item['comments_title'][i][0],
                            'comments_date': item['comments_date'][i][0],
                            'comments_content': item['comments_content'][i][0],
                            'reply_count': 0,
                            'reply_name': 'None',
                            'reply_title': 'None',
                            'reply_date': 'None',
                            'reply_content': 'None',
                        }
                        table = self.db[self.collection2]
                        table.insert_one(data_comments)
        return item

class KickStoryPipeline:
    collection = 'kick'

    def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        '''
        保存story risk environmentalcommitments
        '''
        pattern_story = re.compile(r'(\n)+')
        if len(item['story']) == 0:
            item['story'] = "No description for story"
        else:
            new_story = re.sub(pattern_story,'\n',item['story'][0])
            item['story'] = new_story

        if len(item['risks']) == 0:
            item['risks'] = "No description for risks"
        else:
            new_risk = re.sub(pattern_story, '\n', item['risks'][0])
            item['risks'] = new_risk

        if len(item['environmental_commitments']) == 0:
            item['environmental_commitments'] = "No description for environmental_commitments"
        else:
            new_environmental_commitments = re.sub(pattern_story, '\n', item['environmental_commitments'][0])
            item['environmental_commitments'] = new_environmental_commitments

        self.txtname = r"C:\Users\LDLuc\PycharmProjects\kick"+"\\"+str(item['id'])+'.txt'
        self.file = open(self.txtname, 'w', encoding = 'utf-8')
        try:
            self.file.write(item['story']+'\n')
            self.file.write(item['risks']+'\n')
            self.file.write(item['environmental_commitments']+'\n')

        except:
            pass
        self.file.close()


        if len(item['daystogo'])>=1:
            return item

        filter = {'project_id':  int(item['id'])}

        table = self.db[self.collection]
        # table.insert_one(data)

        # Updating fan quantity form 10 to 25.


        # Values to be updated.
        newvalues = {"$set": {'image_count': len(item['image']),
            'video_count': len(item['video']),}}

        # Using update_one() method for single
        # updation.
        table.update_one(filter, newvalues)

        return item

class KickMongoPipeline:
    collection = 'kick'
    collection2 = 'faq'

    collection3 = 'updates'
    collection4 = 'comments'
    collection5 = 'community'
    collection6 = 'pledge'
    collection7 = 'budget'
    def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        '''
        保存story risk environmentalcommitments
        '''
        pattern_story = re.compile(r'(\n)+')
        if len(item['story']) == 0:
            item['story'] = "No description for story"
        else:
            new_story = re.sub(pattern_story,'\n',item['story'][0])
            item['story'] = new_story

        if len(item['risks']) == 0:
            item['risks'] = "No description for risks"
        else:
            new_risk = re.sub(pattern_story, '\n', item['risks'][0])
            item['risks'] = new_risk

        if len(item['environmental_commitments']) == 0:
            item['environmental_commitments'] = "No description for environmental_commitments"
        else:
            new_environmental_commitments = re.sub(pattern_story, '\n', item['environmental_commitments'][0])
            item['environmental_commitments'] = new_environmental_commitments


        self.txtname =  r"C:\Users\LDLuc\PycharmProjects\kick\kick\story\{}.txt".format(str(item['id']) )
        self.file = open(self.txtname, 'w', encoding = 'utf-8')
        try:
            self.file.write(item['story']+'\n')
            self.file.write(item['risks']+'\n')
            self.file.write(item['environmental_commitments']+'\n')

        except:
            pass
        self.file.close()

        if not item['project_name']:
            return item
        if len(item['daystogo'])>=1:
            return item
        if len(item['community_url']) == 1:
            community_url = 'https://www.kickstarter.com'+item['community_url'][0]
        else:
            community_url = '0'



        # pledge_name = space(item["pledge_name"])
        creator_back_list = space_number(item['creator_backed_count'])
        if len(creator_back_list) ==1:
            creator_back = int(creator_back_list[0])
        elif len(creator_back_list)==0:
            creator_back = int(0)

        creator_create_list = space_number(item['creator_created_count'])
        if len(creator_create_list) ==1:
            creator_create = int(creator_create_list[0])
        elif len(creator_create_list)==0:
            creator_create = int(0)

        if len(item['creator_facebook']) >=1:
            creator_facebook = item['creator_facebook'][0]
        else:
            creator_facebook = int(0)

        if len(item['creator_website'])==0:
            creator_website= int(0)
        else:
            creator_website = item['creator_website']
        last_login = Date(item['creator_lastlogin'][0])
        if len(item['creator_id']) >=1 :
            creator_id = item['creator_id'][0]
        else:
            creator_id = 'None'
        if len(item['backers_count']) == 0:
            backers = int(0)
        else:
            backers = int(space_number( item['backers_count'])[0])
        if len(item['faq_count']) == 0:
            faq_count = 0
        else:
            faq_count = int(space_number(item['faq_count'])[0])
        if len(item['updates_count']) == 0:
            updates_count = 0
        else:
            updates_count = int(space_number(item['updates_count'])[0])

        if len(item['comments_count']) == 0:
            comments_count = 0
        else:
            comments_count = int(space_number(item['comments_count'])[0])

        if item['start_date'] != 'None':
            start_date = Date(item['start_date'][0])
        if item['end_date'] != 'None':
            end_date = Date(item['end_date'][0])

        if not item['creator_location']:
            creator_location = 'None'
        else:
            creator_location = item['creator_location'][0]

        if not item['creator_description']:
            creator_description = 'None'
        else:
            creator_description = item['creator_description'][0]

        if not item['creator_realname']:
            creator_realname = 'None'
        else:
            creator_realname = item['creator_realname'][0]
        data={
            'project_id': item['id'],
            'state': item['state'],

            'project_name':item['project_name'],
            'project_description':item['project_description'],
            'project_location':item['project_location'],
            'category':item['category'],
            'subcategory':item['subcategory'],
            'start_date': start_date,
            'end_date': end_date,

            'creator':item['creator'],
            'creator_url': 'https://www.kickstarter.com' + item['creator_url'],
            'pledged': item['pledged'][0],
            'goal': item['goal'][0],
            'backers_count': backers,
            'image_count': len(item['image']),
            'video_count': len(item['video']),

            'creator_id': creator_id,

            'creator_location' :creator_location,
            'creator_description' : creator_description,
            'creator_realname' : creator_realname,
            'creator_lastlogin' : last_login,
            'creator_facebook': creator_facebook,
            'creator_created_count' : creator_create,
            'creator_backed_count' : creator_back,
            'creator_website' : creator_website,
            'faq_count':faq_count,
            'updates_count': updates_count,

            'comments_count': comments_count,
            'faq_url':'https://www.kickstarter.com/' + item['faq_url'],
            'updates_url': 'https://www.kickstarter.com' + item['updates_url'],
            'comments_url': 'https://www.kickstarter.com' + item['comments_url'],
            'community_url': community_url

        }
        table = self.db[self.collection]
        table.insert_one(data)

        if len(item['faq_question']) >= 1:
            for i in range(len(item['faq_question'])):
                faq_question = item['faq_question'][i].replace("\n", "")
                data_faq = {
                    'project_id': item['id'],
                    'faq_count': int(space_number(item['faq_count'])[0]),

                    'faq_question': faq_question,
                    'faq_answer': item['faq_answer'][i]

                }
                table = self.db[self.collection2]
                table.insert_one(data_faq)


        # data2 = {
        #     'project_id': item['id'],
        #     'faq_url': 'https://www.kickstarter.com' + item['faq_url'],
        #     'faq_count': item['faq_count'],
        #
        #     'faq_question': item['faq_question'],
        #     'faq_answer': item['faq_answer']
        #
        # }
        # table = self.db[self.collection2]
        # table.insert_one(data2)
        # if item['updates_count'][0] !=  '0':
        #     new_updates_contents = []
        #     for url in item['updates_content'][0]:
        #         if len(url)>=1:
        #             new_link = 'https://www.kickstarter.com' + url[0]
        #             new_updates_contents.append(new_link)
        #         else:
        #             pass


        if item['updates_count'][0] !=  '0' and len(item['updates_content'])!=0:
            for i in range(len(item['updates_title'])):
                date = Date2(item['updates_date'][i][0])
                if len(item['updates_content'][i]) == 0:
                    item['updates_content'][i].append('No content')
                data_updates = {
                    'project_id': item['id'],
                    'updates_count': int(space_number(item['updates_count'])[0]),
                    'updates_title': item['updates_title'][i][0],
                    'updates_creator': item['updates_creator'][i][0],
                    'updates_date':date,

                    'updates_content':item['updates_content'][i][0],
                    'updates_heart': int(item['updates_heart'][i][0]),
                    'updates_comments': int(item['updates_comments'][i][0])

                }
                table = self.db[self.collection3]
                table.insert_one(data_updates)
        if item['updates_count'][0] !=  '0' and len(item['updates_content'])==0:
            data_updates = {
                'project_id': item['id'],
                'updates_count': int(space_number(item['updates_count'])[0]),
                'updates_title': 'Error'}
            table = self.db[self.collection3]
            table.insert_one(data_updates)

            # data3 = {
        #     'project_id': item['id'],
        #     'updates_url': 'https://www.kickstarter.com' + item['updates_url'],
        #     'updates_count': item['updates_count'],
        #     'updates_title': item['updates_title'],
        #     'updates_date':item['updates_date'],
        #     'updates_content':new_updates_contents
        #
        # }
        # table = self.db[self.collection3]
        # table.insert_one(data3)

        if int(item['comments_count'][0]) != 0:
            for i in range(len(item['comments_name'])):
                if len(item['recomments_name_list'][i]) != 0:
                    for j in range(len(item['recomments_name_list'][i])):

                        data_comments = {
                            'project_id': item['id'],
                            'comments_count': int(space_number(item['comments_count'])[0]),
                            'comments_name': item['comments_name'][i][0],
                            'comments_title': item['comments_title'][i][0],
                            'comments_date': item['comments_date'][i][0],
                            'comments_content': item['comments_content'][i][0],
                            'reply_count': len(item['recomments_name_list'][i]),
                            'reply_name':item['recomments_name_list'][i][j][0],
                            'reply_title': item['recomments_title_list'][i][j][0],
                            'reply_date': item['recomments_date_list'][i][j][0],
                            'reply_content': item['recomments_content_list'][i][j][0],
                        }
                        table = self.db[self.collection4]
                        table.insert_one(data_comments)
                else:
                    data_comments = {
                        'project_id': item['id'],
                        'comments_count': int(space_number(item['comments_count'])[0]),
                        'comments_name': item['comments_name'][i][0],
                        'comments_title': item['comments_title'][i][0],
                        'comments_date': item['comments_date'][i][0],
                        'comments_content': item['comments_content'][i][0],
                        'reply_count': 0,
                        'reply_name': 'None',
                        'reply_title': 'None',
                        'reply_date': 'None',
                        'reply_content': 'None',
                    }
                    table = self.db[self.collection4]
                    table.insert_one(data_comments)

        # data4 = {
        #     'project_id': item['id'],
        #     'comments_url': 'https://www.kickstarter.com' + item['comments_url'],
        #     'comments_count': item['comments_count'],
        #     'comments_name': item['comments_name'],
        #     'comments_date': item['comments_date'],
        #     'comments_content': item['comments_content']
        # }
        # table = self.db[self.collection4]
        # table.insert_one(data4)

        if len(item['project_status']) == 1:
            if item['project_status'][0] == "Funding Unsuccessful":
                pass
        if len(item['community_url']) == 0:
            pass
        else:
            topcity_backers = space_number(item['community_topcity_backers'])
            topcountry_backers = space_number(item['community_topcountry_backers'])
            for i in range(len(item['community_topcity_city'])):
                city = item['community_topcity_city'][i]
                country = item['community_topcity_country'][i]
                backers = int(space_number(topcity_backers)[i])
                if len(item['community_topcountry_country']) > i:

                    country2 = item['community_topcountry_country'][i]
                    backers2 = int(space_number(topcountry_backers)[i])
                else:
                    country2 = "None"
                    backers2 = int(0)
                data5 = {
                    'project_id': item['id'],
                    'community_url': community_url,
                    'city_ranking': int(i+1),
                    'community_topcity_city': city,
                    'community_topcity_country': country,
                    'community_topcity_backers': backers,
                    'country_ranking': int(i + 1),
                    # 'community_topcity_city': city,
                    'community_topcountry_country': country2,
                    'community_topcountry_backers': backers2,
                    'newbacker': int(space_number(item['newbacker'])[0]),
                    'oldbacker': int(space_number(item['oldbacker'])[0])

                }

                table = self.db[self.collection5]
                table.insert_one(data5)

            # for i in range(len(item['community_topcountry_country'])):
            #     # city = item['community_topcity_city'][i]
            #     if len(['community_topcountry_country'][i]) > i:
            #
            #         country2 = item['community_topcountry_country'][i]
            #         backers2 = int(topcountry_backers[i])
            #     else:
            #         country2 = "None"
            #         backers2 = int(0)
            #     data5 = {
            #         'project_id': item['id'],
            #         'community_url': community_url,
            #         'country_ranking': int(i+1),
            #         # 'community_topcity_city': city,
            #         'community_topcountry_country': country2,
            #         'community_topcountry_backers': backers2,
            #         'newbacker': int(item['newbacker'][0]),
            #         'oldbacker': int(item['oldbacker'][0])
            #
            #     }
            #
            #     table = self.db[self.collection5]
            #     table.insert_one(data5)


            # topcity_backers = space_number(item['community_topcity_backers'])
            # topcountry_backers = space_number(item['community_topcountry_backers'])
            # data5 = {
            #     'project_id': item['id'],
            #     'community_url': community_url,
            #     'community_topcity_city': item['community_topcity_city'],
            #     'community_topcity_country': item['community_topcity_country'],
            #     'community_topcity_backers': topcity_backers,
            #     'community_topcountry_country': item['community_topcountry_country'],
            #     'community_topcountry_backers': topcountry_backers,
            #
            #     'newbacker': int(item['newbacker'][0]),
            #     'oldbacker': int(item['oldbacker'][0])
            #
            # }
            #
            # table = self.db[self.collection5]
            # table.insert_one(data5)

        if len(item['pledge_money'])>=1:

            for i in range(len(item['pledge_money'])):

                if len(item['pledge_description'][i])==0:
                    description = 'None'
                else:

                    description = re.sub(pattern_story,'\n',item['pledge_description'][i][0])
                pledge_name = re.sub(pattern_story,'',item['pledge_name'][i][0])
                # if len(item['pledge_includes'][i])==0:
                #     include = 'None'
                # else:
                #     include = space( item['pledge_includes'][i])
                # backer = space_number_list(item['pledge_backer'])
                if len(item['pledge_ship'][i]) == 0:
                    ship = 'None'
                else:
                    ship = item['pledge_ship'][i][0]
                if len(item['pledge_delivery'][i]) == 0:
                    delivery = 'None'
                else:
                    delivery = item['pledge_delivery'][i][0]

                data_pledge = {
                    'project_id': item['id'],
                    'pledge_money': item['pledge_money'][i],
                    'pledge_name': pledge_name,
                    'pledge_description': description,
                    # 'pledge_includes': include,
                    'pledge_delivery': delivery,

                    'pledge_backer': int(item['pledge_backer'][i]),
                    'pledge_ship': ship

                }
                table = self.db[self.collection6]
                table.insert_one(data_pledge)

        if len(item['budget_category']) >=1:
            cost  = 0
            for i in range(len(item['budget_category_cost'])):
                cost += int(space_number(item['budget_category_cost'][i])[0])


            for i in range(len(item['budget_category'])):
                category = item['budget_category'][i][0]
                category_cost = item['budget_category_cost'][i][0]
                category_count = len(item['budget_category'])
                for j in range(len(item['budget_sub_category'][i])):
                    sub_category = item['budget_sub_category'][i][j]
                    sub_category_cost = item['budget_sub_category_cost'][i][j]
                    sub_category_count = len(item['budget_sub_category'][i])
                    data_budget = {
                        'project_id': item['id'],
                        'total_budget':cost,
                        'category' : category,
                        'category_cost': category_cost,
                        'category_count':category_count,
                        'sub_category': sub_category,
                        'sub_category_cost':sub_category_cost,
                        'sub_category_count':sub_category_count

                    }
                    table = self.db[self.collection7]
                    table.insert_one(data_budget)

        # data6 = {
        #     'project_id': item['id'],
        #     'pledge_money': item['pledge_money'],
        #     'pledge_name': pledge_name,
        #     'pledge_description': item['pledge_description'],
        #     'pledge_includes': item['pledge_includes'],
        #     'pledge_delivery': item['pledge_delivery'],
        #
        #     'pledge_backer': item['pledge_backer'],
        #     'pledge_ship': item['pledge_ship']
        #
        # }
        # table = self.db[self.collection6]
        # table.insert_one(data6)


        return item

class KickFAQPipeline:
    collection = 'faq'

    def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''
        if not item['project_name']:
            return item

        data={
            'project_name':item['project_name'],
            'faq_url':'https://www.kickstarter.com/' + item['faq_url'],
            'faq_question': item['faq_question'],
            'faq_answer': item['faq_answer']

        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item

import re



def space(list):
    if len(list)>=1 :
        new_list = []
        for element in list:
            new_element = re.sub(r'\s+','', element)
            new_list.append(new_element)
        return new_list
    else:
        return ['None']

# remove the space and only keep the number
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

def space_number_list(list):
    if len(list)>=1 :
        new_list = []
        for element in list:
            for ele in element:
                if ele == '\n':
                    pass
                else:
                    a = re.sub(r'\s+','', ele)
                    new_element = re.sub("[^0-9]", "",a)
                    new_list.append(new_element)
        ls = [x for x in new_list if x != '']
        return ls
    else:
        return [int(0)]



def Date(Date):
    list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for number,mon in enumerate(list):
        if mon in Date:
            Date = re.sub(mon,str(number+1),Date)
    date = re.sub(' ','/',Date)
    return date

def Date2(Date):
    list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for number, mon in enumerate(list):
        if mon in Date:
            Date = re.sub(mon, str(number + 1), Date)
    date = re.sub(' ', '/', Date)
    date=date.replace(',','')
    return date