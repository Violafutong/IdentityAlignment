import random
from datetime import datetime, timedelta
from datetime import timedelta
import re
import json

import pandas as pd


def readFile(filePath):
    with open(r"%s" % filePath, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data


# 将Sina数据整理成标准格式
def cleanSina(filePath):
    data = readFile(filePath)

    def replace_timestamps(data):
        for key, value in data.items():
            for i in range(len(value)):
                if "分钟前" in value[i]:
                    minutes = int(value[i].split("分钟前")[0])
                    timestamp = datetime.now() - timedelta(minutes=minutes)
                    value[i] = timestamp.strftime("%Y-%m-%d %H:%M")
                elif "今天" in value[i]:
                    value[i] = value[i].replace("今天", "2023-10-29")
                elif " " in value[i]:
                    value[i] = value[i].replace(" ", "")
                value[i] = str(value[i].strip(" "))
                if re.search(r'\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}:\d{2}', value[i]):
                    datetime_format = "%Y-%m-%d %H:%M:%S"
                elif re.search(r'\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}', value[i]):
                    datetime_format = "%Y-%m-%d %H:%M"
                elif re.search(r'\d{4}-\d{2}-\d{2}\s{2}\d{2}:\d{2}', value[i]):
                    datetime_format = "%Y-%m-%d  %H:%M"


                else:
                    raise ValueError("无法识别的日期时间格式")
                value[i] = datetime.strptime(value[i], datetime_format)
        return data

    updated_data = replace_timestamps(data)
    serialized_data = {key: [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in value] for key, value in updated_data.items()}

    # Serialize the dataTwo to JSON
    json_data = json.dumps(serialized_data)

    # Write JSON dataTwo to a file
    with open(r"D:\BUPT\IdentityAlignment\data\UserPostsAllSina1.json", 'w') as file:
        file.write(json_data)


# 将Twitter数据整理成标准格式
def cleanTwitter(filePath):
    dataTwitter = readFile(filePath)
    for key, value in dataTwitter.items():
        # 遍历列表中的元素
        for i, item in enumerate(value):
            # 将字符串转换为datetime对象
            dt = datetime.fromisoformat(item.replace("Z", ""))
            # 转换为所需的格式
            new_format = dt.strftime("%Y-%m-%d %H:%M:%S")
            # 更新列表中的元素
            value[i] = new_format

    json_data = json.dumps(dataTwitter)

    # Write JSON dataTwo to a file
    with open(r"D:\BUPT\IdentityAlignment\data1\UserPostsAllTwitter.json", 'w') as file:
        file.write(json_data)




# 将两组数据随机选择5000个用户进行关联，并分配一个长度为64的唯一性标识符，
# 将Twitter中的用户作为集合A,将Sina中的用户作为集合B，两个集合属于追踪器的追踪用户这个大集合C的，
# 其中集合A和集合B的交集可以看作同一个用户，这个交集大小为5000.为集合中的每个元素标注清楚是来自那个数据源，并给每个用户分配一个长度为64的唯一性标识符
def generateTrackerData(data, Label):
    # 创建空的DataFrame
    df = pd.DataFrame(columns=["User", "Time", "Label"])

    # 将字典数据整合到DataFrame
    for key, values in data.items():
        print(key)
        values.sort()  # 对时间列表进行排序
        # 添加"twitter"标签
        for value in values:
            if Label == 'Twitter':
                original_time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                random_seconds = random.choice([ 6, 7, 8, 9, 10])
                # 应用随机分钟数到原始时间
                modified_time = original_time + timedelta(seconds=random_seconds)
                new_row = pd.DataFrame({"User": [key], "Time": [modified_time], "Label": [Label]})
            # new_row = pd.DataFrame({"User": [key], "Time": [value], "Label": [Label]})
                df = pd.concat([df, new_row], ignore_index=True)  # 打印DataFrame
    print(df)
    return df
cleanTwitter(r"D:\BUPT\IdentityAlignment\data1\UserPostsAllTwitter.json")

data2 = readFile(r"D:\BUPT\IdentityAlignment\data1\UserPostsAllTwitter.json")
dataTwitterFrame2 = generateTrackerData(data2, "Twitter")
dataTwitterFrame2.to_csv("data1/dataTwitterPosts.csv")
