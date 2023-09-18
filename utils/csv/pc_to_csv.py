import pickle
import sys
import re

txt_input_path = sys.argv[1]

remove1 = re.finditer(r"/", txt_input_path)
remove2 = re.search(r"\b.txt", txt_input_path)
*_, last = remove1
beginning = 0
middle = last.span()[1]
end = remove2.span()[0]
svo_file_path = txt_input_path[beginning:middle]
svo_file_name = txt_input_path[middle:end]

output_path = svo_file_path + svo_file_name + ".csv"


with open(txt_input_path, 'rb') as f:
    point_cloud = pickle.load(f)

f = open(output_path, "w")
f = open(output_path, "a")
f.write("x_coor,y_coor,z_coor,r,g,b,a\n")
for point in point_cloud:
    x, y, z, r, g, b, a = point
    line = str(x) + ',' + str(y) + ',' + str(z) + ',' + str(r) + ',' + str(g) + ',' + str(b) + ',' + str(a) + '\n'
    f.write(line)

f.close()
