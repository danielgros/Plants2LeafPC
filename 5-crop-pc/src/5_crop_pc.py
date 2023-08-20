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
    return pc_coor

def preprocessing_pc(point_cloud, pc_maxX, pc_maxY):
    x_max = round(pc_maxX) + 1
    y_max = round(pc_maxY) + 1

    processed_point_cloud = [None] * x_max
    for i in range(x_max):
        processed_point_cloud[i] = [None] * y_max
        for k in range(y_max):
            processed_point_cloud[i][k] = []

    for point in point_cloud:
        x, y, z = point
        # truncated_point = '%.2f'%(x), '%.2f'%(y), '%.2f'%(z)
        x_rounded = round(x)
        y_rounded = round(y)
        # print('x_max :' + str(x_max))
        # print('y_max :' + str(y_max))
        # print('x :' + str(x_rounded))
        # print('y :' + str(y_rounded))

        processed_point_cloud[x_rounded][y_rounded].append(point)

    return processed_point_cloud



# def is_close_enough(x, y, required_dist, pc_x_coor, pc_y_coor):
#     if math.dist([x, y], [pc_x_coor, pc_y_coor]) <= required_dist:
#         return True
#     else:
#         return False


def add_points(point_cloud_leaf, preprocessed_point_cloud, pc_x_coor, pc_y_coor):
# def add_points(point_cloud_leaf, preprocessed_point_cloud, pc_x_coor, pc_y_coor, f):
    
    # distance to coordinate
    # required_dist = 1       # at most 1 pixels far away

    # for point in point_cloud:
    #     x, y, z = point
    #     if is_close_enough(x, y, required_dist, pc_x_coor, pc_y_coor):
    #         point_cloud_leaf.append(point)
            # f.write(str(x) + ',' + str(y) + ',' + str(z))

    mask_x_coor = round(pc_x_coor)
    mask_y_coor = round(pc_y_coor)

    if preprocessed_point_cloud[mask_x_coor] and preprocessed_point_cloud[mask_x_coor][mask_y_coor]:
        points = preprocessed_point_cloud[mask_x_coor][mask_y_coor]
        for point in points:
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
    mask_2_path = sys.argv[3]

    
    # numpy array with shape (1024, 1024, 1) where data is False / True
    with open(mask_path, 'rb') as f:
        mask = pickle.load(f)

    with open(mask_2_path, 'rb') as f:
        mask_2 = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(mask.keys())
    print(np.array(mask[list(mask.keys())[0]]).shape)

    mask_maxX = len(mask[list_keys[0]])
    mask_maxY = len(mask[list_keys[0]][0])

    # numpy array with shape (number of points, 3) where data is (x,y,z)
    with open(point_cloud_path, 'rb') as f:
        point_cloud = pickle.load(f)

    print((np.array(point_cloud).shape))

    pc_maxX, pc_maxY, pc_maxZ = get_max(point_cloud)


    # hard coded first dict value FOR NOW ->> TO BE CHANGED TO APPLY TO MORE THAN ONE LEAF MASK
    mask_leaf = mask[list_keys[0]]
    point_cloud_leaf = []

    # TEMPORARY
    # counter = 0

    

    f2 = open("5_cropped_point_cloud.csv", "w")
    f2.write("x_coor,y_coor,z_coor\n")
    f2.close()
    
    preprocessed_point_cloud = preprocessing_pc(point_cloud, pc_maxX, pc_maxY)

    for x in range(0, len(mask_leaf)):
        for y in range(0, len(mask_leaf[x])):
            if mask_leaf[x][y][0]:
                # print(x)
                # print(y)

                pc_x_coor = scale_coor(x, mask_maxX, pc_maxX)
                pc_y_coor = scale_coor(y, mask_maxY, pc_maxY)

                # print(pc_x_coor)
                # print(pc_y_coor)

                add_points(point_cloud_leaf, preprocessed_point_cloud, pc_x_coor, pc_y_coor) 
                # add_points(point_cloud_leaf, preprocessed_point_cloud, pc_x_coor, pc_y_coor, f3) 

        #         counter += 1
        #         if counter >= 10000:
        #             break

        # if counter >= 10000:
        #             break
        
    # print(counter)

    print(np.array(point_cloud_leaf).shape)

    # point_cloud_for_csv = minimize_pc(point_cloud_leaf)
    point_cloud_for_csv = point_cloud_leaf

    f3 = open("2_cropped_point_cloud.csv", "a")
    for point in point_cloud_for_csv:
        x, y, z = point
        f3.write(str(x) + ',' + str(y) + ',' + str(z) + '\n')

    f3.close()
    
    # print(point_cloud_leaf)

    # with open('2_cropped_point_cloud.txt', 'wb') as f:
    #     pickle.dump(point_cloud_leaf, f)


if __name__ == "__main__":
    main()