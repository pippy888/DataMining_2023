import pandas as pd
import ast

df = pd.read_csv('bj_test.csv', delimiter=';')

for _, row in df.iterrows():
    path = ast.literal_eval(row['path'])
    tlist = ast.literal_eval(row['tlist'])
    if len(path) != len(tlist):
        print(f'{row["id"]}, {len(path) - len(tlist)}')
