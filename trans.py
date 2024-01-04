import pandas as pd
from sklearn.model_selection import train_test_split

# 加载原始数据
file_path = 'raw_data/bj_test.csv' # 替换为实际文件路径
data = pd.read_csv(file_path, sep=';')
print("数据加载完成")

# 分割数据集为训练集、验证集和测试集
# train, test = train_test_split(data, test_size=0.2, random_state=42) # 这里保留了 20% 作为测试集
print("数据分割完成")
train, val = train_test_split(data, test_size=0.25, random_state=42) # 从剩余的 80% 中再取 25% 作为验证集
print("数据分割完成")

# 保存为新的文件
train.to_csv('raw_data/bj/bj_train.csv', sep=';',index=False)
val.to_csv('raw_data/bj/bj_eval.csv', sep=';',index=False)
# test.to_csv('raw_data/bj/bj_test.csv', sep=';',index=False)
