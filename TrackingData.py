import json

import pandas as pd
import random
import string

# 读取两个csv文件
df_twitter = pd.read_csv("data1/dataTwitterPosts.csv")
df_sina = pd.read_csv("data1/dataSinaPosts.csv")

# 取出各自前5000个用户
twitter_users = set(df_twitter['User'][:])
sina_users = set(df_sina['User'][:])
print(len(twitter_users))
print(len(sina_users))

# 创建一个空的结果DataFrame
df_result = pd.DataFrame(columns=['Time', 'Event', 'Label', 'Domain', 'Tracking ID'])

twitter_users = list(twitter_users)[:10655]
sina_users = list(sina_users)[:10655]
print(len(twitter_users))
print(len(sina_users))
# 遍历前5000个用户

unique_ids = []
usernames = {}
for i in range(10655):
    twitter_user = twitter_users[i]
    sina_user = sina_users[i]

    # 生成长度为64的唯一标识符
    unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    unique_ids.append(unique_id)
    usernames[unique_id] = {twitter_user, sina_user}
    print(unique_id)

    # 将Twitter用户数据和相关信息添加到结果DataFrame中
    twitter_data = df_twitter[df_twitter['User'] == twitter_user]
    for _, row in twitter_data.iterrows():
        df_result = df_result._append(
            {'Time': row['Time'], 'Event': 'Posts', 'Label': "both", 'Domain': row['Label'],
             'Tracking ID': unique_id}, ignore_index=True)

    # 将Sina用户数据和相关信息添加到结果DataFrame中
    sina_data = df_sina[df_sina['User'] == sina_user]
    for _, row in sina_data.iterrows():
        df_result = df_result._append(
            {'Time': row['Time'], 'Event': 'Posts', 'Label': 'both', 'Domain': row['Label'], 'Tracking ID': unique_id},
            ignore_index=True)

# 打印结果
print(df_result)
with open("data1/SinaAlignmentUser1.json", 'w') as f:
    json.dump(sina_users, f)
with open("data1/TwitterAlignmentUser1.json", 'w') as f:
    json.dump(twitter_users, f)
with open("data1/TrackingUID1.json", "w") as f:
    json.dump(unique_ids, f)

df_result.to_csv("data1/trackingData.csv")
with open('data1/usernames1.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in usernames.items()]
