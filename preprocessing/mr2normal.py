import ast
import pandas as pd

print(0.562623059 *1000/ 105)

exit()




mr_data = pd.read_csv('result/mrr.csv', sep=';')

for _, row in mr_data.iterrows():
    print(row['mgeom'])

    break

traj_data = pd.read_csv('data/traj.csv')

output = []

for _, row in traj_data.iterrows():
    traj_id = row['traj_id']
    coord = ast.literal_eval(row['coordinates'])

    if traj_id == 0:
        output.append(coord)
    else:
        break

str = 'LINESTRING('
for i in output:
    str += f'{i[0]} {i[1]}, '

str = str[:-2] + ')'
print(str)