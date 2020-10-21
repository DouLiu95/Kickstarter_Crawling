import os
import re
import shutil
import os
import pandas as pd
def remove_file(old_path, new_path, name_list):
    print(old_path)
    print(new_path)

    for file in name_list:
        filename = str(file) + r".txt"
        src = os.path.join(old_path, filename)
        dst = os.path.join(new_path, filename)
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)
def copyfile(old_path,new_path):
    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        shutil.copy(src,dst)

def find_enviroment_list(story_path,new_path):
    filelist = os.listdir(story_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for file in filelist:
        src = os.path.join(story_path, file)
        dst = os.path.join(new_path, file)

        with open(src,'r',encoding='utf-8') as f:
            data = f.read()
            f.close()

            if "Environmental commitments" in data:
                shutil.move(src, dst)

def merge_csv(path1,path2,path3,path4):
    path_art = path1 + "\kick.csv"
    path_design = path2 + "\kick.csv"
    path_fashion = path3 + "\kick.csv"
    path_tech = path4 + "\kick.csv"

    df1 = pd.read_csv(path_art)
    # print(df1)
    df2 = pd.read_csv(path_design)
    df3= pd.read_csv(path_fashion)
    df4 = pd.read_csv(path_tech)

    df1['category'] = 'Art'
    df2['category'] = 'Design'
    df3['category'] = 'Fashion'
    df4['category'] = 'Technology'

    result = df1.append(df2).append(df3).append(df4)
    print(result)
    result.to_csv(r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\kick.csv",sep=',',index=False,header=True)

def merge_csv_seperate(path1,path2,path3,path4,son):
    path_art = path1 + son
    path_design = path2 + son
    path_fashion = path3 + son
    path_tech = path4 + son

    df1 = pd.read_csv(path_art)
    # print(df1)
    df2 = pd.read_csv(path_design)
    df3= pd.read_csv(path_fashion)
    df4 = pd.read_csv(path_tech)

    # df1['category'] = 'Art'
    # df2['category'] = 'Design'
    # df3['category'] = 'Fashion'
    # df4['category'] = 'Technology'

    result = df1.append(df2).append(df3).append(df4)
    print(result)
    result.to_csv(r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data" + son,sep=',',index=False,header=True)

def move_story(path1,path2,path3,path4):

    dst = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\environment_commitment"
    copyfile(path1,dst)
    copyfile(path2,dst)
    copyfile(path3,dst)
    copyfile(path4,dst)

path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\environment_commitment"
filelist = os.listdir(path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
for file in filelist:
    src = os.path.join(path, file)
    dst = os.path.join(r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\environmental_commitment",file)
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
        environment = data[data.rfind('Environmental commitments'):]
        newf = open(dst, 'w',encoding='utf-8')
        newf.write(environment)
        newf.close()
        f.close()

# path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\environment_commitment\443074.txt"
# with open(path, 'r', encoding='utf-8') as f:
#     data = f.read()
#     environment = data[data.rfind('Environmental commitments'):]
#     print(environment)
# path_art = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\art_apple\environment_art"
# path_design = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\environment"
# path_fashion = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\fashion\environment"
# path_tech = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\tech_all\environment"
# s1 = r"\budget.csv"
# s2 = r"\updates.csv"
# s3 = r"\comments.csv"
# s4 = r"\pledge.csv"
# s5 = r"\community.csv"
# s6 = r"\faq.csv"
# move_story(path_art,path_design,path_fashion,path_tech)

# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s1)
# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s2)
# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s3)
# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s4)
# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s5)
# merge_csv_seperate(path_art,path_design,path_fashion,path_tech,s6)




# merge_csv(path_art,path_design,path_fashion,path_tech)
# merge_csv(r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\failed\budget.csv",r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\budget.csv")

# path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\good\kick.csv"
# df = pd.read_csv(path)
# name_list = list(df['project_id'])
# old_path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\old_story"
# new_path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\story"
# remove_file(old_path,new_path,name_list)
# find_enviroment_list(new_path,r"C:\Users\LDLuc\Downloads\2020-09\kick_data\design_all\environment")