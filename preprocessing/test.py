import csv
from datetime import datetime, timezone
import math

import pandas as pd

test_in = 'data/output.csv'
test_out = 'result/bj_test.csv'

eta_in = 'data/traj_eta.csv'
eta_out = 'result/bj_test_eta.csv'

jump_in = 'data/traj_jump.csv'
jump_out = 'result/bj_test_jump.csv'


in_ = jump_in
out_ = jump_out


csv_list = []
with open(in_) as f:
    reader = csv.reader(f)
    csv_list = [row for row in reader]
csv_list.remove(csv_list[0])

traj = []
with open('data/traj.csv', 'r') as f:
    reader = csv.reader(f)
    traj = [row for row in reader]
traj.remove(traj[0])

traj_id = -1
traj_neat = []
for i, list_traj in enumerate(traj):

    traj_id_now = int(list_traj[3])
    if traj_id_now != traj_id:
        if i != 0:
            traj_neat[-1].update({"end_time": traj[i - 1][1]})
        traj_id += 1
        map = {}
        map.update({"traj_id": traj_id})
        map.update({"start_time": list_traj[1]})
        map.update({"entity_id": list_traj[2]})
        traj_neat.append(map)
    else:
        continue
traj_neat[-1].update({"end_time": traj[-1][1]})

attribute = ["id", "opath", "error", "offset", "spdist", "pgeom", "cpath", "tpath", "mgeom", "ep", "tp", "length",
             "duration", "speed"]
vector = []
for row in csv_list:
    index = 0
    key = attribute[index]
    tmp = []
    map = {}
    for i in range(len(row)):
        if row[i].__contains__(";"):
            split_list = row[i].split(";")
            if len(split_list) == 2:
                tmp.append(split_list[0])
                map.update({key: tmp})
                # 更新
                tmp = []
                tmp.append(row[i].split(";")[1])
                index += 1
                key = attribute[index]
            else : # 3
                tmp.append(split_list[0])
                map.update({key: tmp})

                tmp = []
                tmp.append(row[i].split(";")[1])
                index += 1
                key = attribute[index]
                map.update({key: tmp})

                tmp = []
                tmp.append(row[i].split(";")[2])
                index += 1
                key = attribute[index]
        else:
            tmp.append(row[i])
    map.update({key: tmp})
    if index != 13:
        print(csv_list.index(row))
    if index == 13:
        vector.append(map)
print('!!!')

real_road_dict = {}
rr = pd.read_csv('result/shift.csv')
for _, row in rr.iterrows():
    real_road_dict[int(row['fake'])] = int(row['real'])



traj_id = -1
s = "id;path;tlist;length;speed;duration;hop;usr_id;traj_id;vflag;start_time\n"
with open(out_, 'w') as f:
    f.write(s)
max = 0
for i, v in enumerate(vector):
    # id
    s = ''
    s += v['id'][0]
    s += ';['
    # path
    cpath = v['cpath']
    for c in cpath:
        # if str(math.floor((int(c) + 1) / 2)) == '38026':
        #     print(f'c is {c}')
        if int(c) not in real_road_dict:
            print('jile')
            print(c)
        s += str(real_road_dict[int(c)])
        s += ','
    s = s[:-1] + ']'
    s += ';['

    # tlist
    traj_tmp = traj_neat[i]
    start_time = traj_tmp['start_time'].split('T')[0]
    timestamp = datetime.fromisoformat(traj_tmp['start_time'].replace("Z", "+00:00"))
    unix_timestamp_start = int(timestamp.replace(tzinfo=timezone.utc).timestamp())
    unix_timestamp = unix_timestamp_start
    s += str(unix_timestamp) + ','

    for duration in v['duration']:
        unix_timestamp += int(duration)
        # s += str(unix_timestamp)
        # s += ','
    duration = unix_timestamp - unix_timestamp_start
    mean_time = duration / (len(cpath) - 1)
    tmp = unix_timestamp_start
    for i in range(len(cpath) - 1):
        tmp += mean_time
        s += str(tmp)
        s += ','
    s = s[:-1] + ']'
    s += ';'
    # length
    sum = 0
    for length in v['length']:
        sum += float(length)
    sum = 40000000 * sum / 360

    s += str(sum)
    s += ';'
    # speed

    if duration == 0:
        speed = 0
    else:
        speed = sum / duration

        if int(speed) > 40:
            print(speed)

            if max < speed:
                max = speed
                print(max)
    s += str(speed)
    s += ';'
    # duration
    s += str(duration)
    s += ';'
    # hops
    s += str(len(v['cpath']))
    s += ';'
    # user_id
    s += traj_tmp['entity_id']
    s += ';'
    # traj_id
    s += str(traj_tmp['traj_id'])
    s += ';'
    # vflag
    s += '0'
    s += ';'
    # start_time
    s += start_time
    s += '\n'
    # if i == 10:
    # break
    with open(out_, 'a') as f:
        f.write(s)
