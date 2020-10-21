# '''
# path = r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\budget.csv"
# import pandas as pd
# from datetime import datetime
#
# df = pd.read_csv(path)
# budget = list(set(list(df['project_id'])))
# print(len(budget))
# path2 =  r"C:\Users\LDLuc\Downloads\2020-09\kick_data\all_data\kick.csv"
# df2 = pd.read_csv(path2)
# # time = []
# # for i in budget:
# #     res = df2[df2['project_id'] == i]
# #     # y = datetime.strptime(res['start_date'].values[0], '%m/%d/%Y')
# #     time.append(res['start_date'].values[0])
# #     print(res['start_date'].values[0])
# # print(time)
#
# date_str = r'11/17/2019'
# rule = datetime.strptime(date_str, '%m/%d/%Y')
# date = df2['start_date'].values
# a = 0
# for i in date:
#     if len(i)>2:
#         y = datetime.strptime(i, '%m/%d/%Y')
#         # print(y)
#         if y>rule:
#             a = a+1
#             print(a)
#         else:
#             pass
# '''

path = r"C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\link_to_collect.csv"
import pandas as pd
df = pd.read_csv(path)
df = df[df['category_id']==1]
df = df.drop_duplicates()
output_path = r'C:\Users\LDLuc\PycharmProjects\kick\kick\spiders\crafts.csv'
df.to_csv(output_path,sep=',',index=False,header=True)
