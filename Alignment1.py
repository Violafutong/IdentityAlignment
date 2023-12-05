import json
from collections import Counter

tweet_data = {}
with open("data/UserPostsAllTwitter.json", 'r') as file:
    tweet_data = json.load(file)
# 假设推文数据是一个字典，键存储用户ID，值存储发送推文的时间列表
# tweet_data = {
#     'user1': ['2023-10-05 10:30:00', '2023-10-05 11:15:00', '2023-10-05 13:45:00'],
#     'user2': ['2023-10-05 09:45:00', '2023-10-05 12:30:00'],
#     'user3': ['2023-10-05 11:30:00', '2023-10-05 13:15:00', '2023-10-05 14:00:00'],
#     # 其他用户...
# }

# 统计有多少用户在同一时间发过推文
timestamp_counts = {}  # 用于存储时间戳及其对应的用户数量

for user_tweets in tweet_data.values():
    for timestamp in user_tweets:
        if timestamp in timestamp_counts:
            timestamp_counts[timestamp] += 1
        else:
            timestamp_counts[timestamp] = 1
print(len(tweet_data))
# 输出统计结果
maxcount = "2023-12-05T07:10:22.000Z"
i = 1
for timestamp, count in timestamp_counts.items():
    if count > 1:
        print(f"在时间 {timestamp} 发推文的用户数量为 {count} 人")
        if maxcount < timestamp:
            maxcount = timestamp
        i += 1

print("sumcount", maxcount)
print("avgcount", maxcount / i)
