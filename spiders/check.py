import pandas as pd
import pymongo
import copy
import os
path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/kick.csv"

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# change db name here
mydb = myclient["kick"]

col_kick = mydb["kick"]
col_budget = mydb["budget"]
col_comments = mydb["comments"]
col_community = mydb["community"]
col_faq = mydb["faq"]
col_pledge = mydb["pledge"]
col_updates = mydb["updates"]



def get_link(df_own,df_all):
    # get all the link in df_own
    link_own = [(y, x.replace(r'/creator_bio','')) for y,x in zip(df_own['project_id'],df_own['creator_url'])]

    link_all = [x for x in df_all['link']]
    return link_own,link_all

def get_own_link(df_own):
    link_own = [(y, x.replace(r'/creator_bio','')) for y,x in zip(df_own['project_id'],df_own['creator_url'])]
    return link_own



def delete_all(query):
    col_kick.delete_one(query)
    col_budget.delete_one(query)
    col_comments.delete_one(query)
    col_community.delete_one(query)
    col_faq.delete_one(query)
    col_pledge.delete_one(query)
    col_updates.delete_one(query)
    return 0

# link1,link2 =get_link(df,df_art)

def miss_link(record_own,record_all):
    id_include_list = []
    link_missing = copy.deepcopy(record_all)
    for i in range(len(record_own)):
        for j in range(len(record_all)):
            # 找出没有出现在csv中的link
            if record_own[i][1] in record_all[j]:
                id_include_list.append(record_own[i][0])
                if record_all[j] in link_missing:
                    link_missing.remove(record_all[j])
                print(len(link_missing))
                break
            # 删除掉不属于该类别的link的记录
            elif j == len(record_all)-1:
                print(record_all[i][0])
                myquery = {"project_id":record_all[i][0]}
                delete_all(myquery)
    return link_missing

def check_txt(id):
    # 没有问题变True, 有问题回复False
    if os.path.exists(r"C:\Users\LDLuc\PycharmProjects\kick"+'\\'+str(id)+".txt"):
        with open(r"C:\Users\LDLuc\PycharmProjects\kick"+'\\'+str(id)+".txt", "r", encoding="utf8") as f:
            data = f.read()
            # 判断是否为空的文档
            if len(data)<=10:
                return False
            else:
                return True
    else:
        return False

def check_updates(id):
    # 没有问题变True, 有问题回复False

    myquery = {"project_id":id}
    if col_updates.count_documents(myquery) == 0:
        return False
    else:
        mydoc = col_updates.find(myquery)
        for x in mydoc:
            if x['updates_title'] == 'Error':
                #print("error exist")
                return False

        return True

def check_comments(id):
    # 没有问题变True, 有问题回复False

    myquery = {"project_id":id}
    count = col_comments.count_documents(myquery)
    if count == 0:
        return False
    else:
        return True

def miss_story(link):
    link_missing = []
    for i in link:

        if check_txt(i[0]):
            pass
        else:
            link_missing.append(str(i[1])+r"?ref=discovery_category_ending_soon")
    print("There are {} stories missing".format(len(link_missing)))
    return link_missing

def miss_updates(df):
    link_missing = []
    df = df[['project_id','updates_count','comments_count','updates_url','comments_url']]

    for index, row in df.iterrows():
        print(index)
        if row[1]==0 and row[2] ==0:
            pass
        elif row[1]!=0 and row[2] ==0:
            if check_updates(row[0]):
                pass
            else:
                link_missing.append((int(row[0]),(str(row[3]))))
        elif row[1]==0 and row[2] !=0:
            if check_comments(row[0]):
                pass
            else:
                link_missing.append((int(row[0]),str(row[4])))
        else:
            a = check_updates(row[0])
            b = check_comments(row[0])
            if a and b:
                pass
            elif not a and b:
                link_missing.append((int(row[0]),str(row[3])))
            elif a and not b:
                link_missing.append((int(row[0]),str(row[4])))
            else:
                link_missing.append((int(row[0]),str(row[3])))
                link_missing.append((int(row[0]),str(row[4])))
    print(len(link_missing))
    return link_missing
def check_updates_csv(id, df):
    if id not in df["project_id"].values:
        # print(1)
        return False
    else:
        row = df[df['project_id']==id]
        # print(row)
        if row.size ==1:
            if row['updates_content']=='Error':
                return False
            else:
                return True
        else:

            return True

import re
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
def check_comments_csv(id,df):
    if id not in df.values:
        return False
    else:
        return True
def miss_updates_csv(df):
    link_missing = []
    df = df[['project_id','updates_count','comments_count','updates_url','comments_url']]
    df_comments = pd.read_csv(r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\comments.csv')
    df_updates = pd.read_csv(r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\updates.csv')

    df_comments = df_comments['project_id']
    df_updates = df_updates[['project_id','updates_title']]
    # print(df_updates)
    # print(check_updates_csv(527377731,df_updates))
    # print(df_comments)
    # print(check_comments_csv(1620551633356,df_comments))
    for index, row in df.iterrows():
        print(index)
        if row[2]>1000 or row[1]>1000:

            # print(row[1],row[2])
            if row[1]==0 and row[2] ==0:
                pass
            elif row[1]!=0 and row[2] ==0:
                if check_updates_csv(row[0],df_updates):
                    pass
                else:
                    link_missing.append((int(row[0]),(str(row[3]))))
            elif row[1]==0 and row[2] !=0:
                if check_comments_csv(row[0],df_comments):
                    pass
                else:
                    link_missing.append((int(row[0]),str(row[4])))
            else:
                a = check_updates_csv(row[0],df_updates)
                b = check_comments_csv(row[0],df_comments)
                if a and b:
                    pass
                elif not a and b:
                    link_missing.append((int(row[0]),str(row[3])))
                elif a and not b:
                    link_missing.append((int(row[0]),str(row[4])))
                else:
                    link_missing.append((int(row[0]),str(row[3])))
                    link_missing.append((int(row[0]),str(row[4])))
        else:
            pass
    return link_missing

def miss_budget(data_name):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    # change db name here
    mydb = myclient[data_name]
    missing_link = []
    col_kick = mydb["kick"]
    col_budget = mydb["budget"]
    col_comments = mydb["comments"]
    col_community = mydb["community"]
    col_faq = mydb["faq"]
    col_pledge = mydb["pledge"]
    col_updates = mydb["updates"]

    myquery = {"goal": {"$in": ['None','N']}}
    count = col_kick.count_documents(myquery)
    print("The number of missing budget is {}".format(count))
    mydoc = col_kick.find(myquery)
    for i in mydoc:
        print(i['project_id'])
        search = {'project_id':i['project_id']}
        if col_budget.count_documents(search) ==0:
            print('yes')
            missing_link.append((i["project_id"],i['faq_url'].replace(r'/faqs',r"?ref=discovery_category_ending_soon")))
    print("====================the missing link=====================")
    print(missing_link)
    print("====================    end  ============================")
    return missing_link
# miss_budget("kick")

def find_error(data_name):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    # change db name here
    mydb = myclient[data_name]
    missing_link = []
    col_kick = mydb["kick"]
    col_budget = mydb["budget"]
    col_comments = mydb["comments"]
    col_community = mydb["community"]
    col_faq = mydb["faq"]
    col_pledge = mydb["pledge"]
    col_updates = mydb["updates"]
    myquery = {"pledged":  {"$in": ['None','N']}}
    myquery2 = {'image_count': {"$in": ['0','FALSE','False','false',0]},'video_count': {"$in": ['0','FALSE','False','false',0]}}
    condition = {"$or": [myquery,myquery2 ]}
    count = col_kick.count_documents(condition)
    print("The number of missing image is {}".format(count))
    doc = col_kick.find(condition)
    for i in doc:
        missing_link.append((i['project_id'],i['faq_url'].replace(r'/faqs',r"?ref=discovery_category_ending_soon")))
    print(len(list(set(missing_link))))
    return list(set(missing_link))

find_error('kick')


# check_comments(77950910)
# path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
# df = pd.read_csv(path)
# df_art = pd.read_csv(r'art_link.csv')
# link1 = get_own_link(df)
# urls = miss_link(link1,link2)
# print(urls,len(urls))
# missing_story = miss_story(link1)
# print(missing_story)
##----------------------------------------------------------------------
## check the missing story
# path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
# df = pd.read_csv(path)
# link1 = get_own_link(df)
# # urls = miss_link(link1,link2)
# # print(urls,len(urls))
# urls = miss_story(link1)
# print(len(urls))

##----------------------------------------------------------------------
## check missing updates and comments
# path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
# df = pd.read_csv(path)
# link = miss_updates_csv(df)
# print(len(link))
# print(check_updates(1632554331))