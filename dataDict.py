import json

import pandas as pd


def transTrackingData(filepath):
    # 假设data是包含DataFrame数据的变量
    trackingData = pd.read_csv(filepath)
    # 将时间列转换为datetime类型
    trackingData['Time'] = pd.to_datetime(trackingData['Time'])
    # 创建一个空字典，用于存储整理后的数据
    result_dict = {}
    # 遍历DataFrame的每一行
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    for index, row in trackingData.iterrows():
        time = row['Time']
        UniqueID = row['Tracking ID']
        source = row['Domain']

        # 如果时间已经是字典的键，则将对应的('User', 'Domain')对添加到列表中
        if time in result_dict:
            result_dict[str(time)].append({'Tracking ID': UniqueID, 'Domain': source})
        # 如果时间还不是字典的键，则创建一个新的列表，并将对应的('User', 'Domain')对添加到列表中
        else:
            result_dict[str(time)] = [{'Tracking ID': UniqueID, 'Domain': source}]
    # 打印整理后的字典
    with open("data1/tracking_result_dict.json", "w") as f:
        json.dump(result_dict, f, indent=4, ensure_ascii=False)

    return result_dict


def transSinaData(filepath):  # 将新浪数据转为dict格式
    # 假设data是包含DataFrame数据的变量
    sinaData = pd.read_csv(filepath)
    # 创建字典
    data_dict = {}
    # 遍历每一行数据
    for index, row in sinaData.iterrows():
        time = row['Time']
        user = row['User']

        # 如果时间已经存在于字典中，则将用户添加到对应的列表中
        if time in data_dict:
            data_dict[time].append(user)
        # 如果时间不存在于字典中，则创建一个新的列表并将用户添加进去
        else:
            data_dict[time] = [user]
    with open("data1/tracking_sina_dict.json", "w") as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)

    return data_dict


def transSinaUser(filepath):  # 将新浪数据转为以user为key，以user对应的time组成的list作为value的dict
    # 创建一个空字典
    user_dict = {}
    df = pd.read_csv(filepath)

    # 遍历数据框中的每一行
    for _, row in df.iterrows():
        user = row['User']
        time = row['Time']
        if user in user_dict:
            user_dict[user].append(time)
        else:
            user_dict[user] = [time]
    with open("data1/sina_user_dict.json", "w") as f:
        json.dump(user_dict, f, indent=4, ensure_ascii=False)
    return user_dict


if __name__ == '__main__':
    tracking_dict = transTrackingData("data1/TrackingDataExtended.csv")  # 将追踪数据转为以时间为键的方便查找

    sina_dict = transSinaData("data1/dataSinaPosts.csv")
    transSinaUser("data1/dataSinaPosts.csv")
