
from collections import defaultdict

def calculate_weighted_frequency(sequences, weights,threshold):
    user_weighted_freq = defaultdict(int)
    sum = 0
    for sequence, weight in zip(sequences, weights):
        for user in sequence:
            user_weighted_freq[user] += weight
            sum+=weight
    user_support = defaultdict(int)
    for u , score in user_weighted_freq.items():
        weighted_support = score/sum
        user_support[u] = weighted_support
        if weighted_support>=threshold:
            print("高度可疑用户：",u)
        else:
            print("一般可疑用户：",u)
    print(user_support)
    return user_support

# 示例用户序列和权重信息
sequences = [
    {"user1"},
    {"user1", "user2"},
    {"user3", "user4"},
    {"user1", "user3", "user5"},
    {"user2", "user3", "user4"},
    {"user1", "user3"},
    {"user2", "user4", "user5"},
    {"user1", "user2", "user3"},
    {"user1", "user2", "user3", "user4"},
    {"user1", "user2", "user4", "user5"},
    {"user1"},
    {"user1", "user2"},
    {"user3", "user2", "user4"},
    {"user1", "user2", "user3", "user5"},
    {"user2", "user3", "user3", "user4"},
    {"user1"},
    {"user2", "user5"},
    {"user1", "user4", "user5"},
    {"user1", "user2", "user3", "user4"},
    {"user1", "user2", "user3", "user4"}
]
sequences1 = [{2432598031},  # 0.2*0.33
          {7827267955, 1821773133, 2432598031},  # 0.2*0.33
          {7827267955, 1821773133, 2432598031}  # 0.15*0.33
        , {2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074}  # 0.15*0.33
        , {2126292232, 2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074, 7855319775}  # 0.15*0.33
          # 0.15*0.33

        , {2432598031}  # 0.2*0.33
        , {1821773133, 2432598031}  # 0.2*0.33
        , {7827267955, 1821773133, 2432598031}  # 0.15*0.33
        , {2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074}  # 0.15*0.33
        , {2243166245, 2126292232, 2330174060, 1821773133, 1778758223, 2432598031, 7827267955, 1345454230, 1644538074,
           3957042973, 7855319775}  # 0.15*0.33
        , {2432598031}  # 0.2*0.33
        , {7827267955, 1821773133, 2432598031}  # 0.2*0.33
        , {7827267955, 1821773133, 2432598031}  # 0.15*0.33
        , {2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074}  # 0.15*0.33
        , {2243166245, 2126292232, 2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074, 7855319775}
          # 0.15*0.33
        , {2432598031}  # 0.2*0.33
        , {7827267955, 1821773133, 2432598031}  # 0.2*0.33
        , {7827267955, 1821773133, 2432598031}  # 0.15*0.33
        , {2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074}  # 0.15*0.33
        , {2243166245, 2126292232, 2330174060, 1821773133, 2432598031, 7827267955, 1345454230, 1644538074, 7855319775}
          ]
weights = [0.15, 0.15, 0.15, 0.15, 0.15, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.37, 0.37,0.37,0.37,0.37]

# 调用函数计算用户的加权出现次数
user_support = calculate_weighted_frequency(sequences1, weights,0.2)
sum  = 0
# 输出每个用户的加权出现次数
for user, freq in user_support.items():
    print(f"{user}: {freq}")
    sum+=freq
