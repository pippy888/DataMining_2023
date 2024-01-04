import csv
from datetime import datetime

with open('data/eta_task.csv') as f:
    reader = csv.reader(f)
    csv_list = [row for row in reader]
head = csv_list[0]
csv_list.remove(head)
length = reader.line_num

# id;x;y;timestamp
# 0;116.318726;40.009014;1381225500
# 0;116.315102;40.004784;1381225605

attribute = ['id', 'traj_id', 'time', 'entity_id', 'coordinates', 'current_dis', 'speeds', 'holidays']
s = 'id;x;y;timestamp\n'
for i in range(0, length - 1, 2):
    id = csv_list[i][attribute.index('traj_id')]

    coordinates_start = csv_list[i][attribute.index('coordinates')]
    coordinates_start = coordinates_start[1:-1].replace(',', ';')
    time_begin = csv_list[i][attribute.index('time')]
    timestamp_begin = datetime.strptime(time_begin, "%Y-%m-%dT%H:%M:%SZ")
    timestamp_int_begin = int(timestamp_begin.timestamp())

    i = i + 1
    coordinates_end = csv_list[i][attribute.index('coordinates')]
    coordinates_end = coordinates_end[1:-1].replace(',', ';')
    timestamp_int_end = timestamp_int_begin

    s += id
    s += ';'
    s += coordinates_start
    s += ';'
    s += str(timestamp_int_begin)
    s += '\n'

    s += id
    s += ';'
    s += coordinates_end
    s += ';'
    s += str(timestamp_int_end)
    s += '\n'

    # print(s)
with open('gps_eta_task.csv', 'w') as w:
    w.write(s)
