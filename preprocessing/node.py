import ast
import pandas as pd

data = pd.read_csv('data/node.csv')

coord_dict = {}

for i in data['coordinates']:

    x, y = ast.literal_eval(i)

    if coord_dict.__contains__((x, y)):
        print('fuckyou')
    else:
        coord_dict[(x, y)] = True

