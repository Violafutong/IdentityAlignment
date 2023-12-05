import numpy as np
import pandas as pd

trackingData = pd.read_csv("data\customer.csv", header=None)
trackingData.columns = ['ID', 'domain', 'timestamp', 'event']
siteaData = pd.read_csv("data\sitea.csv", header=None)
siteaData.columns = ['UID', 'UserName', 'Time']
sitebData = pd.read_csv("data\siteb.csv", header=None)
sitebData.columns = ['UID', 'UserName', 'Time']

x = trackingData[['domain']]
domainTrackingData = np.array(trackingData[['domain']].stack()).tolist()
timeTrackingData = np.array(trackingData[['timestamp']].stack()).tolist()

usernamelst = {}
i = 0
value_result = siteaData.loc[(siteaData['Time'] == '2023-09-17 12:22:55'), ['UID', 'UserName', 'Time']].index
# print(value_result)

while (i < len(domainTrackingData)):
    if (domainTrackingData[i] == "sitea.com"):
        targetUser = siteaData.loc[(siteaData['Time'] == timeTrackingData[i]), ['UID', 'UserName', 'Time']]
        targetUserName = np.array(targetUser.stack()).tolist()

        if len(targetUserName) > 0:
            usernamelst['sitea'] = targetUserName[1]
            print(targetUserName)
    if (domainTrackingData[i] == "siteb.com"):
        targetUser = sitebData.loc[(sitebData['Time'] == timeTrackingData[i]), ['UID', 'UserName', 'Time']]
        targetUserName = np.array(targetUser.stack()).tolist()

        if len(targetUserName) > 0:
            usernamelst['siteb'] = targetUserName[1]
    i = i + 1

print(usernamelst)


# for site in domainTrackingData

def tracking():
    print("")


if __name__ == '__main__':
    tracking()
