import pandas as pd
import os
import glob
Folder_Path = r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\linux'  # 要拼接的文件夹及其完整路径，注意不要包含中文
Main_path =r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick'
SaveFile_Path = r'C:\Users\LDLuc\Downloads\2020-09\kick_data\kick\merged'  # 拼接后要保存的文件路径

# 修改当前工作目录
os.chdir(Folder_Path)
# 将该文件夹下的所有文件名存入一个列表
file_list = os.listdir()
print(file_list)


def marge(csv_list, SaveFile_Path):
    for inputfile in csv_list:
        f1 = open(Folder_Path + '\\'+ inputfile, 'r', encoding="utf-8")
        f2 = open(Main_path + '\\'+ inputfile, 'r', encoding="utf-8")
        data1 = pd.read_csv(f1)
        data2 = pd.read_csv(f2)
        data1.to_csv(SaveFile_Path+ '\\'+ inputfile, mode='a', index=False)
        data2.to_csv(SaveFile_Path+ '\\'+ inputfile, mode='a', index=False)
        df = pd.read_csv(SaveFile_Path+ '\\'+ inputfile, header=None)
        datalist = df.drop_duplicates()
        datalist.to_csv(SaveFile_Path+ '\\'+ inputfile, index=False, header=False)
        print('完成去重')
    print('完成合并')




if __name__ == '__main__':

    marge(file_list, SaveFile_Path)
