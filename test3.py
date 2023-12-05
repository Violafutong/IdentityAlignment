import numpy as np
import pandas as pd

# 读取原始数据
df = pd.read_csv("data/trackingData.csv")

# 生成随机标签、时间戳和Tracking ID
num_rows = len(df)
labels = np.random.choice(["Twitter", "Sina"], size=num_rows, replace=True)
unique_ids_df = df["Tracking ID"].tolist()

# 创建空的列表用于存储新生成的数据
new_data_list = []
expanded_df = df
# 循环拼接生成新数据
for _ in range(11):
    timestamps = pd.to_datetime(df['Time']) + pd.to_timedelta(np.random.randint(1, 30, size=num_rows), unit='s')
    unique_ids = np.random.choice(unique_ids_df, size=num_rows, replace=True)

    # 创建新的数据
    new_data = {
        'Time': timestamps,
        'Event': "PageView",
        'Label': labels,
        'Domain': df['Domain'],
        'Tracking ID': unique_ids
    }

    # 将新数据转换为DataFrame并添加到列表中
    new_df = pd.DataFrame(new_data)
    new_data_list.append(new_df)
    expanded_df = pd.concat([expanded_df] + new_data_list)
    expanded_df.reset_index(drop=True, inplace=True)

# 合并原始数据和新数据
expanded_df.drop(labels="Unnamed: 0", axis=1, inplace=True)

# 按Tracking ID进行排序
expanded_df.sort_values(by="Tracking ID", inplace=True)
pd.set_option('display.max_rows', None)  # 设置行数为无限制
pd.set_option('display.max_columns', None)  # 设置列数为无限制
pd.set_option('display.width', 1000)  # 设置列宽
pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左
# 打印扩展后的数据的前10行
print(expanded_df.head(10))
print(len(expanded_df))
## 去掉time和tracking ID 重复的用户
df = df.drop_duplicates(subset=['Time', 'Tracking ID'], keep=False)
print(len(expanded_df))

# 保存扩展后的数据到新的CSV文件
expanded_df.to_csv("data/TrackingDataExtended.csv", index=False)