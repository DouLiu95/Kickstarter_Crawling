import pandas as pd
import re
from pandas import set_option


def to_number(df,column_name):
    # df.loc[df[column_name] == 'false'] = '0'
    # df.loc[df[column_name] == 'true'] = '1'
    # df.loc[df[column_name] == 'True'] = '1'
    # df.loc[df[column_name] == 'False'] = '0'
    # df.loc[df[column_name] == 'FALSE'] = '0'
    # df.loc[df[column_name] == 'TRUE'] = '1'
    df[column_name] = df[column_name].map(lambda x: str(x).replace('true','1'))
    df[column_name] = df[column_name].map(lambda x: str(x).replace('false','0'))

    # df[column_name] = df[column_name].map(lambda x: re.sub('True', '1', x))
    # df[column_name] = df[column_name].map(lambda x: re.sub('False', '0', x))
    # df[column_name] = df[column_name].map(lambda x: re.sub('FALSE', '0', x))
    # df[column_name] = df[column_name].map(lambda x: re.sub('TRUE', '1', x))

    return df

def without(df,column_name):
    df[column_name] = df[column_name].map(lambda x: x.replace(r'["','').replace(r'"]','').replace(r',',''))
    df[column_name] = df[column_name].map(lambda x: x.replace(r'["','').replace(r'"]','').replace(r',',''))
    return df
path1 = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\art_apple\kick.csv"

def pipeline_kick(path):
    df = pd.read_csv(path)
    name_list1 = ['creator_backed_count', 'video_count', 'image_count', 'backers_count', 'creator_facebook',
                  'creator_created_count', 'creator_website', 'faq_count',
                  'updates_count', 'comments_count', 'community_url']
    name_list2 = ['pledged', 'goal']
    for i in name_list1:
        df = to_number(df, i)
    for i in name_list2:
        df = without(df, i)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates(['project_id'])
    return df

def pipeline_updates(path):
    df = pd.read_csv(path)
    name_list = ['updates_count', 'updates_heart','updates_comments']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(df[df.updates_title == 'Error'].index, inplace=True)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates()
    return df
    # outputpath=r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\art_apple\updates_new.csv'
    # df.to_csv(outputpath,sep=',',index=False,header=True)
def pipeline_comments(path):
    df = pd.read_csv(path)
    name_list = ['comments_count', 'reply_count']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(columns='_id', inplace=True)
    # pd.concat([df.drop_duplicates(),df.drop_duplicates(keep = False)]).drop_duplicates(keep = False)
    df = df.drop_duplicates()
    return df
    # outputpath=r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\art_apple\comments_new.csv'
    # df.to_csv(outputpath,sep=',',index=False,header=True)
def pipeline_community(path):
    df = pd.read_csv(path)
    name_list = ['city_ranking', 'community_topcity_backers','country_ranking','community_topcountry_backers','newbacker','oldbacker']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates()
    return df


def pipeline_faq(path):
    df = pd.read_csv(path)
    name_list = ['faq_count']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates()
    return df

def pipeline_pledge(path):
    df = pd.read_csv(path)
    name_list = ['pledge_backer']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates()
    return df

def pipeline_budget(path):
    df = pd.read_csv(path)
    name_list = ['sub_category_count']
    for i in name_list:
        # print(df[i])
        df = to_number(df, i)
    df.drop(columns='_id', inplace=True)
    df = df.drop_duplicates()
    return df
def pipeline(path):

    path_kick = path+r'\kick.csv'
    path_updates = path + r'\updates.csv'
    path_comments = path + r'\comments.csv'
    path_community = path + r'\community.csv'
    path_budget = path + r'\budget.csv'
    path_pledge = path + r'\pledge.csv'

    path_faq = path + r'\faq.csv'


    df_kick = pipeline_kick(path_kick)
    df_updates = pipeline_updates(path_updates)
    df_comments = pipeline_comments(path_comments)
    df_faq = pipeline_faq(path_faq)
    df_community = pipeline_community(path_community)
    df_budget = pipeline_budget(path_budget)
    df_pledge = pipeline_pledge(path_pledge)

    outpath_kick = path +r'\good' +r'\kick.csv'
    outpath_updates = path+r'\good' + r'\updates.csv'
    outpath_comments = path +r'\good'+ r'\comments.csv'
    outpath_community = path +r'\good'+ r'\community.csv'
    outpath_budget = path +r'\good'+ r'\budget.csv'
    outpath_pledge = path +r'\good'+ r'\pledge.csv'
    outpath_faq = path +r'\good'+ r'\faq.csv'

    df_kick.to_csv(outpath_kick,sep=',',index=False,header=True)
    df_updates.to_csv(outpath_updates,sep=',',index=False,header=True)
    df_comments.to_csv(outpath_comments,sep=',',index=False,header=True)
    df_faq.to_csv(outpath_faq,sep=',',index=False,header=True)
    df_community.to_csv(outpath_community,sep=',',index=False,header=True)
    df_budget.to_csv(outpath_budget,sep=',',index=False,header=True)
    df_pledge.to_csv(outpath_pledge,sep=',',index=False,header=True)


path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all"
# pd.set_option('display.max_columns', None)


pipeline(path)
# pipeline_faq(path)
# outputpath=r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\art_apple\kick_new.csv'
# df.to_csv(outputpath,sep=',',index=False,header=True)
