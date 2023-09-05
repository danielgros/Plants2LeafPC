import numpy as np
import cv2
import csv
import math

def anglesToIndex(x_degree, y_degree, width, height, max_x_degree, max_y_degree):
    x_interval = max_x_degree*2/width
    y_interval = max_y_degree*2/height
    x_shifted = x_degree+max_x_degree
    if x_shifted < 0:
        x_shifted = 0
    y_shifted = y_degree+max_y_degree
    if y_shifted < 0:
        y_shifted = 0
    x_pos = (x_shifted)/x_interval
    y_pos = (y_shifted)/y_interval
    if x_pos > width-1:
        x_pos = width-1
    if y_pos > height-1:
        y_pos = height-1
    return int(x_pos),int(y_pos)

def pointCloudToImage():
    height = 1440
    width = int((height/9)*16)
    img = np.zeros([height,width,3])
    overlap = np.zeros([height,width])
    with open('../data/pc_2023-01-31_08.00.00_png_ultra.csv', mode = 'r') as file:
        reader = csv.reader(file)
        points = []
        dict = {}
        first_line = True
        # neg = 0
        # pos = 0
        for lines in reader:
            if first_line:
                first_line = False
                continue
            x_coord = float(lines[0])
            y_coord = float(lines[1])
        #     if x_coord > 0:
        #         pos = pos + 1
        #     else:
        #         neg = neg + 1
        # print(neg, pos)
            z_coord = float(lines[2])
            r = int(lines[3])
            g = int(lines[4])
            b = int(lines[5])
            x_degrees = math.degrees(math.atan(x_coord/z_coord))
            y_degrees = math.degrees(math.atan(y_coord/z_coord))

        #     points.append([x_coord,y_coord,x_coord,r,g,b,x_degrees,y_degrees])
        #     if dict.get(y_degrees,-1) == -1:
        #         dict[y_degrees] = 1
        #     else:
        #         dict[y_degrees] = dict[y_degrees] + 1
        # for elem in dict.items():
        #     print(elem)
        # print(max(dict.keys()), )

            x_pos,y_pos = anglesToIndex(x_degrees, y_degrees, width, height, 45, 30)
            # print(x_pos)
            img[y_pos,x_pos,0] += r
            img[y_pos,x_pos,1] += g
            img[y_pos,x_pos,2] += b
            overlap[y_pos,x_pos] += 1
    for r in range(0,height):
        for c in range(0,width):
            if overlap[r,c] > 1:
                img[r,c,0] /= overlap[r,c]
                img[r,c,1] /= overlap[r,c]
                img[r,c,2] /= overlap[r,c]

    # cv2.imshow("image",img)
    # cv2.waitKey(0)
    cv2.imwrite("../data/projected_image_new.png", img)

pointCloudToImage()