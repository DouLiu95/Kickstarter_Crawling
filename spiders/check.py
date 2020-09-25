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
        with open(r"C:\Users\LDLuc\PycharmProjects\kick"+'\\'+str(id)+".txt", "r") as f:
            data = f.read()
            # 判断是否为空的文档
            if len(data)<=4:
                return False
            else:
                return True
    else:
        return False

def check_updates(id):
    # 没有问题变True, 有问题回复False

    myquery = {"project_id":id}
    mydoc = col_updates.find(myquery)
    for x in mydoc:
        if x['updates_title'] == 'Error':
            print("error exist")
            return False
    return True

def check_comments(id):
    # 没有问题变True, 有问题回复False

    myquery = {"project_id":id}
    mydoc = col_comments.find(myquery)
    for x in mydoc:
        if x['project_id'] == id:
            print('exist')
            return True
    return False


# check_comments(77950910)
# path = r"C:/Users/LDLuc/Downloads/2020-09/kick_data/kick/merged/kick.csv"
# df = pd.read_csv(path)
# df_art = pd.read_csv(r'art_link.csv')
# link1,link2 =get_link(df,df_art)
# urls = miss_link(link1,link2)
# print(urls,len(urls))