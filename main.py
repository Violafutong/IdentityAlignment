# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import random

import pandas as pd


def datamade(df):
    grouped = df.groupby("Label")
    twitter_df = grouped.get_group("twitter")
    sina_df = grouped.get_group("Sina")
    print("Twitter DataFrame:")
    print(twitter_df)
    print()
    print("Sina DataFrame:")
    print(sina_df)
    return


def analysis():
    return


def readData():
    with open('data/UserPostsAllTwitter.json', 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(columns=["UserName", "Time", "Label"])
    index = 1

    for key, values in data.items():
        values.sort()  # 对时间列表进行排序
        n = len(values)
        half_n = n // 2  # 50%的数量

        # 添加"twitter"标签
        twitter_samples = random.sample(values, half_n)
        for value in twitter_samples:
            df = df.append({"UserName": key, "Time": value, "Label": "twitter", "Event": "PublishPosts"},
                           ignore_index=True)

        sina_samples = list(set(values) - set(twitter_samples))
        for value in sina_samples:
            df = df.append({"UserName": key, "Time": value, "Label": "Sina", "Event": "PublishPosts"}, ignore_index=True)
        index += 1
    print(df)
    return df


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readData()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
