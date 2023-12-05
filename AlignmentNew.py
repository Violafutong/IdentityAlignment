import json
from datetime import datetime, timedelta, time
from datetime import timedelta
from collections import defaultdict
import pandas as pd
import time


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
    return result_dict


def findUserinTwitter(UserName, time1, time_window, file):  # twitter用户名， 起始时间，时间窗口，数据文件
    user_time_list = []
    serch_condition_times = []
    datetime1 = pd.to_datetime(time1)
    # datetime1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    before_target_time1 = datetime1 - timedelta(days=time_window)
    after_target_time1 = datetime1 + timedelta(days=time_window)
    data = pd.read_csv(file)
    user_data = data[data['User'] == UserName]
    user_time_list = user_data['Time'].tolist()

    for u_time in user_time_list:
        u_datatime = datetime.strptime(u_time, '%Y-%m-%d %H:%M:%S')
        if before_target_time1 <= u_datatime <= after_target_time1:
            serch_condition_times.append(u_datatime)

    return serch_condition_times


# 从追踪器数据中找到
def findUIDinTracking(serch_condition_times, tracking_dict, time_period):  # 根据犯罪嫌疑人发布的信息，提取一段时间的行为信息
    fuzzy_results = []
    # 假设timeList是时间列表，time_window是时间窗口大小（以分钟为单位）
    # 创建一个空的哈希表，用于存储result_dict的哈希映射
    hash_map = defaultdict(list)
    # 将result_dict中的数据构建成哈希映射
    for time, result_list in tracking_dict.items():
        # timedate = pd.to_datetime(time)
        timedate = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        hash_map[timedate].extend(result_list)
    # 创建有序的HashMap
    sorted_keys = sorted(hash_map.keys())
    sorted_hash_map = {}

    for key in sorted_keys:
        sorted_hash_map[key] = hash_map[key]
    # 创建一个空列表，用于存储模糊查询的结果
    fuzzy_results = []
    flag = 0

    # 遍历时间列表中的每个时间
    for time in serch_condition_times:
        # 将时间字符串转换为datetime类型
        # target_time = pd.to_datetime(time)
        # 计算时间窗口的起始时间和结束时间
        before_target_time = time - timedelta(seconds=time_period)
        after_target_time = time + timedelta(seconds=time_period)

        # 初始化一个空列表，用于存储符合条件的('User', 'Domain')对的字典
        temp_results = []
        # 遍历哈希映射中的时间键范围
        for key in hash_map:
            if before_target_time <= key <= after_target_time:
                temp_results.extend([item for item in hash_map[key] if item['Domain'] != 'Sina'])
        # 将模糊查询的结果添加到fuzzy_results中
        fuzzy_results.append((time, temp_results))
    # 打印模糊查询的结果
    unique_ids = [item['Tracking ID'] for _, result_list in fuzzy_results for item in result_list]
    # 去除重复的唯一 ID
    unique_ids = list(set(unique_ids))
    return unique_ids


# 在网站b中筛选用户
def findUserInforByUID(unique_ids, filepath, filepath1):
    sina_times = []
    for unique_id in unique_ids:
        trackingData = pd.read_csv(filepath)
        user_data = trackingData[trackingData['Tracking ID'] == unique_id]  # 筛选Tracking ID是unique_id的
        user_data1 = user_data[user_data['Domain'] == 'Sina']  # 筛选Domain是Sina的用户数据
        sina_times.append(user_data1['Time'].tolist())  # 这部分的时间列表放到里面
    dataSinaPosts = pd.read_csv(filepath1)
    usernameslist = []

    # 提取符合条件的用户名列表
    # 同一个用户的每个
    # 筛选sina_time的列表中的每个元素都存在于带筛选的
    for sina_time in sina_times:  # 筛选对于原始数据中的每个元素，检查它是否存在于待筛选的值中
        filtered_df = dataSinaPosts[dataSinaPosts['Time'].isin(sina_time) & dataSinaPosts['User'].isin(
            dataSinaPosts[dataSinaPosts['Time'].isin(sina_time)]['User'].value_counts()[
                dataSinaPosts[dataSinaPosts['Time'].isin(sina_time)]['User'].value_counts() == len(sina_time)].index)]

        # 提取符合条件的用户名列表
        usernames = filtered_df['User'].unique()
        usernameslist.append(usernames[0])
        # 打印用户名列表
    usernameset = set(usernameslist)
    print(usernameset, " ", len(usernameset))


# userTime(timeList1, 10)
# findUser("@cnavigato")
# timelists = {["2019-09-26 12:34:01","2019-09-26 12:34:01", "2019-09-26 12:34:01"]}
# dataTwo = {["2019-09-26 12:34:01","usera"],["2019-09-26 12:34:01", "usera"],[ "2019-09-26 12:34:01", "usera"],[ "2019-09-26 12:34:01", "userb"]}
if __name__ == '__main__':
    filefold = "/Temp"
    for time_window in range(30, 91, 30):#时间窗口多少天
        username = "@opinno"#用户名
        startdatetime = '2023-10-07 05:39:11'#起始时间
        print("Time Window: {} days ______________________________________".format(time_window))

        serch_condition_times = findUserinTwitter(username, startdatetime,time_window, 'dataTwo{}/dataTwitterPosts.csv'.format(filefold))
        tracking_dict = transTrackingData("dataTwo{}/trackingData.csv".format(filefold))  # 将追踪数据转为以时间为键的方便查找
        for i in range(0, 56, 5):#时间模糊范围多少秒
            unique_ids = findUIDinTracking(serch_condition_times, tracking_dict, i)  # 设置模糊查询的时间窗口为10min
            print("Time range: {} seconds".format(i))
            findUserInforByUID(unique_ids, "dataTwo{}/trackingData.csv".format(filefold), "dataTwo{}/dataSinaPosts.csv".format(filefold))
