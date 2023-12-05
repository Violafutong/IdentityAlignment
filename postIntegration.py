import json
import os

# 创建一个空字典用于存储合并后的结果
merged_dict = {}
label = "Twitter"
# 遍历目标文件夹中的所有 JSON 文件
folder_path = r'D:\BUPT\IdentityAlignment\data\Alldata'  # 替换为实际的文件夹路径
file_path = "data/FUserPostsAll{}.json".format(label)
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)

        # 读取 JSON 文件内容并加载为字典结构
        with open(file_path, 'r') as file:
            data = json.load(file)
        # 遍历字典中的键值对
        for key, value in data.items():
            # 检查键是否已存在于结果字典中，如果不存在则添加
            if key not in merged_dict:
                merged_dict[key] = value

# 打印合并后的字典
print(merged_dict)
with open("data/FUserPostsAllTwitter.json", 'w') as f:
    json.dump(merged_dict, f, indent=4, ensure_ascii=False)
    #json.dump(merged_dict, f)

print(len(merged_dict))
