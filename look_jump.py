import ast
import json
import math

import numpy as np
import pandas as pd

from datetime import datetime

exp_id = 401518

path = f'libcity/cache/{exp_id}/model_cache/'

# 替换 'file_path.npy' 为您的文件路径
labels = np.load(path + 'nextloc_labels.npy')
preds = np.load(path + 'nextloc_preds.npy')

# 从文件中读取 index2loc
with open('trans/trans.csv', 'r') as file:
    data = json.load(file)
    index2loc = data["index2loc"]

# 应用映射
mapped_array = [index2loc[i] if i < len(index2loc) else None for i in preds]

print(mapped_array[242])

jump_test = pd.read_csv('result/jump_test.csv', delimiter=';')
jump_test_traj_id = jump_test['id']

jump_dict = {}
index = 0
for i in jump_test_traj_id:
    jump_dict[i] = index
    index += 1

df = pd.read_csv('result/jump_task.csv', delimiter=',')

# 确保 'time' 列被识别为数值类型（如果它不是的话）
# df['time'] = pd.to_numeric(df['time'], errors='coerce')

print(df)
edges = pd.read_csv('result/bj_roadmap_edge.geo', delimiter=',')
edges_dict = {}
for _, row in edges.iterrows():
    id = row['geo_id']
    coordinates = row['coordinates']
    edges_dict[row['geo_id']] = ast.literal_eval(row['coordinates'])


def cal_dis(cur, old):
    cur = ast.literal_eval(cur)
    dis_x = math.fabs(cur[0] - old[0]) * 40000 / 360
    dis_y = math.fabs(cur[1] - old[1]) * 40000 / 360
    dis = math.sqrt(dis_x * dis_x + dis_y * dis_y)

    return dis


def get_nearest(edges, old):
    min = 114514
    min_point = edges[0]
    for point in edges:
        cal = cal_dis(old, point)
        if cal < min:
            min = cal
            min_point = point

    # min_point = (min_point + old) * ()
    return min_point


# 遍历DataFrame的行
for i in range(len(df)):
    # 对于第一行和第二行，我们不能计算前两行的和，因此可以选择跳过或填充为0

    if pd.isna(df.at[i, 'coordinates']):
        traj_id = df.at[i, 'traj_id']

        if traj_id in jump_dict:
            road_id = mapped_array[jump_dict[traj_id]]

            coord = get_nearest(edges_dict[road_id], df.at[i - 1, 'coordinates'])

            # coord = edges_dict[road_id][0]
            dis = (float(df.at[i - 1, 'current_dis'])) + \
                  cal_dis(df.at[i - 1, 'coordinates'], coord)

            last_speed = df.at[i-1, 'speeds']
            cur_speed = df.at[i, 'speeds']
            last_time = df.at[i-1, 'time']
            cur_time = df.at[i, 'time']

            time_leap = int(datetime.strptime(cur_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()) - \
                        int(datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ").timestamp())

            speed = (last_speed + cur_speed) / 2
            real_dis = speed / 3.6 * time_leap / 1000 + float(df.at[i - 1, 'current_dis'])

            cur_point = ast.literal_eval(df.at[i - 1, 'coordinates'])

            coord[0] = cur_point[0] + (coord[0] - cur_point[0]) * (real_dis / dis)
            coord[1] = cur_point[1] + (coord[1] - cur_point[1]) * (real_dis / dis)

            coord[0] = round(coord[0], 6)
            coord[1] = round(coord[1], 6)
            df.at[i, 'current_dis'] = real_dis
            df.at[i, 'coordinates'] = coord

        else:
            print(f'traj_id is {traj_id}, row is {i}')

# 保存修改后的DataFrame到新的CSV文件
df.to_csv('result/jump_task_filled.csv', index=False)

"""
11190;69159,59868;0.000107824,0.000998677;0.00457661,0.000126341;0.012957;LINESTRING(116.460890913 39.8805646342,116.466080585 39.871270372);69159,69121,69126,69127,3882,49084,46242,46234,46231,59868;69159,69121,69126,69127,3882,49084,46242,46234,46231,59868;LINESTRING(116.460890913 39.8805646342,116.4616007 39.8805593,116.4616101 39.878194,116.4616104 39.8781244,116.4616146 39.8770453,116.4616232 39.8748837,116.4616232 39.8748302,116.4616268 39.8736164,116.4625079 39.8736235,116.4638849 39.8725147,116.4653186 39.8715073,116.4655653 39.8714167,116.4660788 39.8713967,116.466080585 39.871270372);0.999999976748,0.999998005291;0,0.867758882977;0.00528641401096,0.00133743354975;0;0
"""

'''
11190;[34576,34557,34559,34560,1940,24540,23119,23115,23114,29931];[1381254300,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0,1381254300.0];735.9830623011111;0;0;10;254;0;0;2013-10-08
'''
