import pandas as pd
import numpy as np
from datetime import datetime
import pytz

exp_id = 834447

path = f'libcity/cache/{exp_id}/model_cache/'

# 替换 'file_path.npy' 为您的文件路径
labels = np.load(path + 'eta_labels.npy')
preds = np.load(path + 'eta_preds.npy')

print(preds)

eta_test = pd.read_csv('result/eta_test.csv', delimiter=';')
eta_test_traj_id = eta_test['id']

eta_dict = {}
index = 0
for i in eta_test_traj_id:
    eta_dict[i] = index
    index += 1

df = pd.read_csv('result/eta_task.csv', delimiter=',')

# 确保 'time' 列被识别为数值类型（如果它不是的话）
# df['time'] = pd.to_numeric(df['time'], errors='coerce')

print(df)

# 遍历DataFrame的行
for i in range(len(df)):
    # 对于第一行和第二行，我们不能计算前两行的和，因此可以选择跳过或填充为0

    if pd.isna(df.at[i, 'time']):
        traj_id = df.at[i, 'traj_id']

        if traj_id in eta_dict:
            last = df.at[i - 1, 'time']
            timestamp_begin = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
            timestamp_int_begin = int(timestamp_begin.timestamp())
            duration = float(preds[eta_dict[traj_id]])
            duration = int(duration * 60)
            timestamp_int_end = duration + timestamp_int_begin

            # 将时间戳转换为datetime对象
            date_time = datetime.utcfromtimestamp(timestamp_int_end)

            # 将datetime对象格式化为 'YYYY-MM-DDTHH:MM:SSZ' 格式
            formatted_date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            df.at[i, 'time'] = formatted_date_time
        else:
            print(f'traj_id is {traj_id}, row is {i}')

# 保存修改后的DataFrame到新的CSV文件
df.to_csv('result/eta_task_filled.csv', index=False)

"""
11190;69159,59868;0.000107824,0.000998677;0.00457661,0.000126341;0.012957;LINESTRING(116.460890913 39.8805646342,116.466080585 39.871270372);69159,69121,69126,69127,3882,49084,46242,46234,46231,59868;69159,69121,69126,69127,3882,49084,46242,46234,46231,59868;LINESTRING(116.460890913 39.8805646342,116.4616007 39.8805593,116.4616101 39.878194,116.4616104 39.8781244,116.4616146 39.8770453,116.4616232 39.8748837,116.4616232 39.8748302,116.4616268 39.8736164,116.4625079 39.8736235,116.4638849 39.8725147,116.4653186 39.8715073,116.4655653 39.8714167,116.4660788 39.8713967,116.466080585 39.871270372);0.999999976748,0.999998005291;0,0.867758882977;0.00528641401096,0.00133743354975;0;0
"""

'''
11190;[34576,34557,34559,34560,1940,24540,23119,23115,23114,29931];[1381254300,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0];735.9830623011111;0;0;10;254;0;0;2013-10-08
'''
