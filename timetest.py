import pandas as pd

data = pd.read_csv("data/dataTwitterPosts.csv")
datatime = data['Time']
print(datatime.min())