import pandas as pd

df = pd.read_csv('data/rel.csv', delimiter=',')

df.rename(columns={'id': 'rel_id'}, inplace=True)

df['geo'] = 'geo'
df.to_csv('result/bj_roadmap_edge.rel', index=False)


df = pd.read_csv('data/road.csv', delimiter=',')

df.rename(columns={'id': 'geo_id'}, inplace=True)

df['type'] = 'LineString'

df.to_csv('result/bj_roadmap_edge.geo', index=False)
