import sys
import numpy as np
import pickle
import math
import csv



def get_max(point_cloud):
    maxX = float('-inf') # horizontal, positive is towards the door
    maxY = float('-inf') # vertical, positive is towards the other plants, back of the room
    maxZ = float('-inf') # depth, positive is towards leaves

    for i in range(0, len(point_cloud)):
        if maxX < point_cloud[i][0]:
            maxX = point_cloud[i][0]
        if maxY < point_cloud[i][1]:
            maxY = point_cloud[i][1]
        if maxZ < point_cloud[i][2]:
            maxZ = point_cloud[i][2]

    return maxX, maxY, maxZ


# def get_min(point_cloud):
#     minX = float('inf') # horizontal, positive is towards the door
#     minY = float('inf') # vertical, positive is towards the other plants, back of the room
#     minZ = float('inf') # depth, positive is towards leaves

#     for i in range(0, len(point_cloud)):
#         if minX > float(point_cloud[i][0]):
#             minX = float(point_cloud[i][0])
#         if minY > float(point_cloud[i][1]):
#             minY = float(point_cloud[i][1])
#         if minZ > float(point_cloud[i][2]):
#             minZ = float(point_cloud[i][2])

#     return minX, minY, minZ


def scale_coor(mask_coor, mask_max, pc_max):
    pc_coor = mask_coor * pc_max / mask_max
    # pc_coor = mask_coor
    return pc_coor

def preprocessing_pc(point_cloud, pc_max_x, pc_max_y):
    x_max = round(float(pc_max_x)) + 1
    y_max = round(float(pc_max_y)) + 1

    processed_point_cloud = [None] * x_max
    for i in range(x_max):
        processed_point_cloud[i] = [None] * y_max
        for k in range(y_max):
            processed_point_cloud[i][k] = []

    for point in point_cloud:
        x, y, z, r, g, b, a = point
        x_rounded = int(round(x))
        y_rounded = int(round(y))
        
        # print statements:
        # print('x_max :' + str(x_max))
        # print('y_max :' + str(y_max))
        # print('x :' + str(x_rounded))
        # print('y :' + str(y_rounded))

        processed_point_cloud[x_rounded][y_rounded].append(point)

    return processed_point_cloud



# def is_close_enough(x, y, required_dist, mask_x_scaled_to_pc, mask_y_scaled_to_pc):
#     if math.dist([x, y], [mask_x_scaled_to_pc, mask_y_scaled_to_pc]) <= required_dist:
#         return True
#     else:
#         return False


def add_points(point_cloud_leaf, point_cloud_data_structure_turned_to_3d_array, x, y, color_red):
# def add_points(point_cloud_leaf, point_cloud_data_structure_turned_to_3d_array, mask_x_scaled_to_pc, mask_y_scaled_to_pc, f):
    
    # distance to coordinate
    # required_dist = 1       # at most 1 pixels far away

    # for point in point_cloud:
    #     x, y, z = point
    #     if is_close_enough(x, y, required_dist, mask_x_scaled_to_pc, mask_y_scaled_to_pc):
    #         point_cloud_leaf.append(point)
            # f.write(str(x) + ',' + str(y) + ',' + str(z))

    x_coor = int(round(x))
    y_coor = int(round(y))

    if point_cloud_data_structure_turned_to_3d_array[x_coor] and point_cloud_data_structure_turned_to_3d_array[x_coor][y_coor]:
        points = point_cloud_data_structure_turned_to_3d_array[x_coor][y_coor]
        for point in points:
            if color_red:
                x, y, z, r, g, b, a = point
                new_point = [x, y, z, 255, 0, 0, 255]
                point_cloud_leaf.append(new_point)
            else:
                point_cloud_leaf.append(point)


    
# def minimize_pc(point_cloud_leaf):
#     minX, minY, minZ = get_min(point_cloud_leaf)

#     point_cloud_new = []

#     for point in point_cloud_leaf:
#         x, y, z = point
#         x_new = str( float(x) - minX )
#         y_new = str( float(y) - minY )
#         z_new = str( float(z) - minZ )
#         point_new = x_new, y_new, z_new
#         point_cloud_new.append(point_new)

#     return point_cloud_new


def main():

    mask_path = sys.argv[1]
    point_cloud_path = sys.argv[2]

    
    # numpy array with shape (1024, 1024, 1) where data is False / True
    with open(mask_path, 'rb') as f:
        mask = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(mask.keys())
    print(np.array(mask[list(mask.keys())[0]]).shape)

    mask_x_length = len(mask[list_keys[0]])
    mask_y_length = len(mask[list_keys[0]][0])

    # numpy array with shape (number of points, 7) where data is (x,y,z,r,g,b,a)
    with open(point_cloud_path, 'rb') as f:
        point_cloud = pickle.load(f)

    print((np.array(point_cloud).shape))

    pc_max_x, pc_max_y, pc_max_z = get_max(point_cloud)


    for key in list_keys:
        mask_leaf = mask[key]
        point_cloud_leaf = []
        
        # point cloud is now 3d array of shape (pc_max_x, pc_max_y, number of points that correspond to the specific x/y in the point cloud)
        point_cloud_data_structure_turned_to_3d_array = preprocessing_pc(point_cloud, pc_max_x, pc_max_y)

        for x in range(0, len(mask_leaf)):
            for y in range(0, len(mask_leaf[x])):
                if mask_leaf[x][y][0]:
                    # print(x)
                    # print(y)

                    mask_x_scaled_to_pc = scale_coor(x, mask_x_length, pc_max_x)
                    mask_y_scaled_to_pc = scale_coor(y, mask_y_length, pc_max_y)

                    # print(mask_x_scaled_to_pc)
                    # print(mask_y_scaled_to_pc)
                    color_red = True
                    add_points(point_cloud_leaf, point_cloud_data_structure_turned_to_3d_array, mask_x_scaled_to_pc, mask_y_scaled_to_pc, color_red) 
                    # add_points(point_cloud_leaf, point_cloud_data_structure_turned_to_3d_array, mask_x_scaled_to_pc, mask_y_scaled_to_pc, f) 
                else:
                    color_red = False
                    add_points(point_cloud_leaf, point_cloud_data_structure_turned_to_3d_array, x, y, color_red) 

    


        print(np.array(point_cloud_leaf).shape)

        # point_cloud_for_csv = minimize_pc(point_cloud_leaf)
        point_cloud_for_csv = point_cloud_leaf

        filename = "../data/cropped_point_cloud_" + key + ".csv"

        f = open(filename, "w")
        f = open(filename, "a")
        f.write("x_coor,y_coor,z_coor,r,g,b,a\n")
        for point in point_cloud_for_csv:
            x, y, z, r, g, b, a = point
            line = str(x) + ',' + str(y) + ',' + str(z) + ',' + str(r) + ',' + str(g) + ',' + str(b) + ',' + str(a) + '\n'
            f.write(line)

        f.close()
        
        # print(point_cloud_leaf)

        # with open('2_cropped_point_cloud.txt', 'wb') as f:
        #     pickle.dump(point_cloud_leaf, f)


if __name__ == "__main__":
    main()