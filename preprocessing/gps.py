import pandas as pd
import ast
from datetime import datetime

data = pd.read_csv('data/traj.csv')
traj_id = data['traj_id']
coordinates = data['coordinates']
time = data['time']
len = len(data)

output = 'result/gps.csv'
with open(output, 'w') as f:
    f.write("id;x;y;timestamp\n")
    for i in range(len):
        traj_id_i = traj_id[i]
        point_list = ast.literal_eval(coordinates[i])
        x_i = point_list[0]
        y_i = point_list[1]
        time_i = time[i]
        timestamp = datetime.strptime(time_i, "%Y-%m-%dT%H:%M:%SZ")
        timestamp_int = int(timestamp.timestamp())
        f.write(f"{traj_id_i};{x_i};{y_i};{timestamp_int}\n")

# print(14 * 128)
# print()
#
# ori = datetime.strptime("2013-10-08T17:45:00Z", "%Y-%m-%dT%H:%M:%SZ").timestamp()
#
# end = datetime.strptime("2013-10-08T18:14:11Z", "%Y-%m-%dT%H:%M:%SZ").timestamp()
#
# print(int(end) - int(ori))

# timestamp_int = int(timestamp.timestamp())
