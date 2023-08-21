import pickle
import sys

# filename = sys.argv[1]
filename = '/hdd/gros2/maskrcnn/samples/senior_thesis_project/1-get-pc/data/sample-data/output/pc_2023-01-30_11.00.00_png_ultra.txt'

with open(filename, 'rb') as f:
    point_cloud = pickle.load(f)

filename = '/hdd/gros2/maskrcnn/samples/senior_thesis_project/1-get-pc/data/sample-data/output/pc_2023-01-30_11.00.00_png_ultra.csv'

f = open(filename, "w")
f = open(filename, "a")
f.write("x_coor,y_coor,z_coor,r,g,b,a\n")
for point in point_cloud:
    x, y, z, r, g, b, a = point
    line = str(x) + ',' + str(y) + ',' + str(z) + ',' + str(r) + ',' + str(g) + ',' + str(b) + ',' + str(a) + '\n'
    f.write(line)

f.close()