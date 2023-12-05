import json
from datetime import datetime, timedelta, time
from datetime import timedelta
from collections import defaultdict
import pandas as pd
import time


def findUserinTwitter(UserName, time1, time_window, file):  # twitter用户名， 起始时间，时间窗口，数据文件
    user_time_list = []
    serch_condition_times = []
    datetime1 = pd.to_datetime(time1)
    before_target_time1 = datetime1 - timedelta(days=time_window)
    data = pd.read_csv(file)
    user_data = data[data['User'] == UserName]
    user_time_list = user_data['Time'].tolist()

    for u_time in user_time_list:
        u_datatime = datetime.strptime(u_time, '%Y-%m-%d %H:%M:%S')
        if before_target_time1 <= u_datatime <= datetime1:
            serch_condition_times.append(u_datatime)

    return serch_condition_times


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


def findUIDinTracking(serch_condition_times, tracking_dict, time_period, threshold):  # 根据犯罪嫌疑人发布的信息，提取一段时间的行为信息
    # 假设timeList是时间列表，time_window是时间窗口大小（以分钟为单位）
    # 创建一个空的哈希表，用于存储result_dict的哈希映射
    hash_map = defaultdict(list)
    # 将result_dict中的数据构建成哈希映射
    for time, result_list in tracking_dict.items():
        timedate = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        hash_map[timedate].extend(result_list)
    # 创建一个空列表，用于存储模糊查询的结果
    fuzzy_results = []
    # 遍历时间列表中的每个时间
    for time in serch_condition_times:
        # 将时间字符串转换为datetime类型
        # 计算时间窗口的起始时间和结束时间
        before_target_time = time - timedelta(seconds=time_period)
        after_target_time = time + timedelta(seconds=time_period)

        # 初始化一个空列表，用于存储符合条件的('User', 'Domain')对的字典
        temp_results = []
        # 遍历哈希映射中的时间键范围
        for key in hash_map:
            if before_target_time <= key <= after_target_time:
                temp_results.extend([item for item in hash_map[key] if item['Domain'] == 'Twitter'])
        # 将模糊查询的结果添加到fuzzy_results中
        fuzzy_results.append((time, temp_results))
    unique_ids = []

    id_counts = defaultdict(int)

    for _, result_list in fuzzy_results:
        for item in result_list:
            id_counts[item['Tracking ID']] += 1

    for uid, count in id_counts.items():
        if count >= threshold:
            unique_ids.append(uid)

    unique_ids = list(set(unique_ids))
    print("unique_ids: ", unique_ids)
    return unique_ids


# 在网站b中筛选用户
def findUserInforByUID(unique_ids, filepath, sina_user_dict, time_period, sina_dict, threshold):
    sina_times = []
    usernameslist = []
    trackingData = pd.read_csv(filepath)
    for unique_id in unique_ids:
        user_data = trackingData[trackingData['Tracking ID'] == unique_id]  # 筛选Tracking ID是unique_id的
        user_data1 = user_data[user_data['Domain'] == 'Sina']  # 筛选Domain是Sina的用户数据
        sina_times.append(user_data1['Time'].tolist())  # 这部分的时间列表放到里面
    # 提取符合条件的用户名列表
    # 同一个用户的每个
    # 筛选sina_time的列表中的每个元素都存在于带筛选的
    hash_map = defaultdict(list)
    # 将result_dict中的数据构建成哈希映射
    for sinatime, sinalist in sina_dict.items():
        timedate = datetime.strptime(sinatime, '%Y-%m-%d %H:%M:%S')
        hash_map[timedate].extend(sinalist)#以时间为key，以新浪网页上该时间发布信息的user list为value
    usernameslistUni = []
    for sina_time in sina_times:  # 筛选对于原始数据中的每个元素，检查它是否存在于待筛选的值中,这里的sina_time是一个list
        for user, times in sina_user_dict.items():
            user_valid = True  # 用户是否满足条件的标志
            for time in times:
                time_valid = False  # 单个时间是否满足条件的标志
                time_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                # 遍历sina_time中的每个时间
                for sina_time_item in sina_time:
                    sina_time_obj = datetime.strptime(sina_time_item, "%Y-%m-%d %H:%M:%S")
                    # 检查时间是否在模糊范围内
                    time_diff = abs(time_obj - sina_time_obj)
                    if time_diff.total_seconds() <= time_period:
                        time_valid = True
                        break
                # 如果单个时间不满足条件，则将标志设置为False并跳出循环
                if not time_valid:
                    user_valid = False
                    break
                # 如果用户的所有时间都满足条件，则将用户添加到结果字典中
            if user_valid:
                usernameslistUni.append(user)
    print(usernameslistUni)


if __name__ == '__main__':
    filefold = "/Temp"
    for time_window in range(30, 91, 30):  # 时间窗口多少天
        username = "@JoshDavidson"  # 用户名
        startdatetime = '2023-9-30 05:39:11'  # 起始时间
        print("Time Window: {} days ______________________________________".format(time_window))

        serch_condition_times = findUserinTwitter(username, startdatetime, time_window,
                                                  'data1/dataTwitterPosts.csv')
        with open("data1/tracking_result_dict.json", "r") as f:
            tracking_dict = json.load(f)
        with open("data1/tracking_sina_dict.json", "r") as f:
            sina_dict = json.load(f)
        with open("data1/sina_user_dict.json", "r") as f:
            sina_user_dict = json.load(f)
        print(serch_condition_times)
        for i in range(5, 35, 5):  # 时间模糊范围多少秒
            unique_ids = findUIDinTracking(serch_condition_times, tracking_dict, i,
                                           len(serch_condition_times))  # 设置模糊查询的时间窗口为10min
            print("Time range: {} seconds".format(i))
            for j in range(10,101,10):
                print("result in TrackingDataExtended{}: ".format(j))
                findUserInforByUID(unique_ids, "data1/TrackingDataExtended{}.csv".format(j),
                                   sina_user_dict, i, sina_dict, 1)
