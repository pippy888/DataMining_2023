import ast
import pandas as pd

data = pd.read_csv('data/road_old.csv')
cross_nodes = pd.read_csv('data/node.csv')

coordinates_dict = {}
nodes_dict = {}

cnt = 1
for i in data['coordinates']:
    point_list = ast.literal_eval(i)

    for j in point_list:
        longitude, latitude = j

        if (longitude, latitude) not in coordinates_dict:
            cnt += 1
            coordinates_dict[(longitude, latitude)] = cnt

for _, row in cross_nodes.iterrows():
    coord = ast.literal_eval(row['coordinates'])
    highway = row['highway']

    x, y = coord
    if nodes_dict.__contains__((x, y)):
        print('kiss my dick')
    else:
        nodes_dict[(x, y)] = highway

output_file = 'result/point2id.txt'
with open(output_file, 'w') as f:
    for i in coordinates_dict:
        f.write(f'{coordinates_dict[i]} : {i[0], i[1]}\n')

output_file = 'result/edges.csv'

real_road_cnt = -1
real_road_dict = {}

def write_row_in_edges(file, p_list, pid):
    file.write(f'\"LINESTRING (')
    output = ", ".join(f"{x} {y}" for x, y in p_list)
    file.write(f'{output})\"')

    x_source, y_source = p_list[0]
    x_target, y_target = p_list[-1]

    file.write(
        f', \"{pid}\", \"{coordinates_dict[(x_source, y_source)]}\", '
        f'\"{coordinates_dict[(x_target, y_target)]}\", '
        f'\"{x_source}\", \"{y_source}\", \"{x_target}\", \"{y_target}\" \n'
    )


id_cnt = 1
additional_cnt = 1

with open(output_file, 'w') as f:
    f.write('WKT,id,source,target,x1,y1,x2,y2\n')

    for _, i in data.iterrows():

        real_road_cnt += 1

        point_id = int(i['id'])
        point_list = ast.literal_eval(i['coordinates'])
        highway = i['highway']

        start_point = point_list[0]
        start_point = start_point[0], start_point[1]
        end_point = point_list[-1]
        end_point = end_point[0], end_point[1]

        fixed_plist = []
        tmp_plist = [start_point]

        for point in point_list[1:-1]:
            x, y = point
            if (x, y) in nodes_dict:
                tmp_plist.append((x, y))
                fixed_plist.append(tmp_plist)

                tmp_plist = [start_point]
                continue

            tmp_plist.append((x, y))

        tmp_plist.append(end_point)
        fixed_plist.append(tmp_plist)

        flag = False
        if len(fixed_plist) > 1:
            flag = True

        for plist in fixed_plist:
            id_cnt += 2

            if not flag:
                real_road_dict[id_cnt-2] = real_road_cnt
                real_road_dict[id_cnt-1] = real_road_cnt
            elif plist == fixed_plist[-1]:
                real_road_dict[id_cnt-2] = real_road_cnt
                real_road_dict[id_cnt-1] = real_road_cnt


            if flag and plist != fixed_plist[-1]:
                # with open('data/road.csv','a'):
                additional_cnt += 1
                new = 38026 + additional_cnt
                real_road_dict[id_cnt-2] = new
                real_road_dict[id_cnt-1] = new
                print(f'{new},\"{plist}\"'
                      f'{i["highway"]},{i["length"]},{i["lanes"]},'
                      f'{i["tunnel"]},{i["bridge"]},{i["maxspeed"]},'
                      f'{i["width"]},{i["alley"]},{i["roundabout"]}')

            write_row_in_edges(f, plist, id_cnt - 2)
            plist_r = plist[::-1]
            write_row_in_edges(f, plist_r, id_cnt - 1)

with open('result/shift.csv', 'w') as f:
    f.write('fake,real\n')
    for it in real_road_dict:
        f.write(f'{it},{real_road_dict[it]}\n')

print('done')
