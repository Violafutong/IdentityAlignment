import pandas as pd

# dict1 = {
#     '123456': 'yryl1w9HwC63xR1dm2D8gdpTfT7agNluZKdLpv5LPst49ZlEWgulLFjxfU8lP54b',
#     '456789': 'UikjOjXSosi2RaFJYiWvINQMZK7WtN4hmVK3OYTX9JU0TX5XdWq2TLPY6ayBRIOv'
# }
# dataTwo = pd.read_csv("dataTwo/dataTwitterPostsCross.csv")
# for key in dict1:
#     user_data = dataTwo[dataTwo['Cookie'] == key]
#     user_time_list = user_data['Time'].tolist()

trackdata = """,Time,Event,Label,Domain,Cookie
0,2022-05-19 17:19:35,Posts,both,Twitter,123456
1,2022-06-20 12:34:20,Posts,both,Twitter,123456
2,2022-06-26 09:31:01,Posts,both,Twitter,123456
3,2022-07-18 11:49:47,Posts,both,Twitter,123456
4,2023-03-03 18:25:34,Posts,both,Twitter,123456
5,2023-06-21 00:02:00,Posts,both,Sina,123456
6,2021-08-20 04:43:29,Posts,both,Twitter,456789
7,2022-02-24 05:10:26,Posts,both,Twitter,456789
8,2022-04-06 01:37:29,Posts,both,Twitter,456789
9,2022-05-29 03:56:51,Posts,both,Twitter,456789
10,2022-06-15 05:50:26,Posts,both,Twitter,456789
11,2023-07-15 02:07:40,Posts,both,Twitter,456789
12,2023-09-27 18:41:15,Posts,both,Twitter,456789
13,2022-09-26 18:20:03,Posts,both,Sina,456789
14,2022-09-26 18:40:03,Posts,both,Sina,456789
15,2022-09-26 19:00:07,Posts,both,Sina,456789"""

dict1 = {
    '123456': 'yryl1w9HwC63xR1dm2D8gdpTfT7agNluZKdLpv5LPst49ZlEWgulLFjxfU8lP54b',
    '456789': 'UikjOjXSosi2RaFJYiWvINQMZK7WtN4hmVK3OYTX9JU0TX5XdWq2TLPY6ayBRIOv'
}

# 将trackdata按行分割
lines = trackdata.strip().split('\n')
header = lines[0]  # 保存标题行
data = lines[1:]  # 保存数据行

# 替换Cookie为相应的trackingID
for i in range(len(data)):
    line = data[i]
    parts = line.split(',')  # 将行按逗号分割为字段列表
    cookie = parts[5]  # 获取Cookie
    if cookie in dict1:
        parts[5] = dict1[cookie]  # 根据字典替换Cookie为trackingID
    data[i] = ','.join(parts)  # 重新组合字段为一行数据

# 将替换后的数据重新组合为完整的trackdata
trackdata_new = '\n'.join([header] + data)
print(trackdata_new)