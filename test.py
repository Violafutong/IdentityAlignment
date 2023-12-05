# import numpy as np
# import pandas as pd
#
# df = pd.read_csv("data/trackingData.csv")
#
#
# labels = np.random.choice(["Twitter", "Sina"], size=len(df), replace=True)
#
# unique_ids_df = df["Tracking ID"].tolist()
#
# unique_ids = np.random.choice(unique_ids_df, size=len(df), replace=True)
# # 生成随机的时间戳
# timestamps = pd.to_datetime(df['Time']) + pd.to_timedelta(np.random.randint(1, 60, size=len(df)), unit='s')
#
# # 生成新的数据
# new_data = {
#     'Time': timestamps,
#     'Event': "PageView",
#     'Label': labels,
#     'Domain': df['Domain'],
#     'Tracking ID': unique_ids
# }
#
# # 将新数据转换为 DataFrame
# new_df = pd.DataFrame(new_data)
#
# # 将原始数据和新数据合并
# expanded_df = pd.concat([df, new_df])
#
# # 重新索引数据框
# expanded_df.reset_index(drop=True, inplace=True)
# expanded_df.drop(labels="Unnamed: 0", axis=1, inplace=True)
# expanded_df.sort_values(by="Tracking ID", inplace=True, ascending=True)
# pd.set_option('display.max_rows', None)  # 设置行数为无限制
# pd.set_option('display.max_columns', None)  # 设置列数为无限制
# pd.set_option('display.width', 1000)  # 设置列宽
# pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左
# # 打印扩展后的数据
# print(expanded_df.head(10))
#
# expanded_df.to_csv("data/TrackingDataAll20231127.csv")
#

import csv

filename = 'data1/TrackingDataExtended.csv'  # CSV 文件名

# 初始化计数器
count = 0

# 打开 CSV 文件
with open(filename, 'r') as file:
    # 创建 CSV 读取器
    csv_reader = csv.reader(file)

    # 遍历每一行数据
    for row in csv_reader:
        count += 1

# 输出数据条数
print("数据条数：", count)