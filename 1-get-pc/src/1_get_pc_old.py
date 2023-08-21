import sys
import math
import numpy as np
import cv2
import enum
import pyzed.sl as sl
import struct
import pickle
import re



def binaryX(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))


def main():

    # Get input parameters
    svo_input_path = sys.argv[1]

    remove1 = re.finditer(r"/", svo_input_path)
    remove2 = re.search(r"\b.svo", svo_input_path)
    *_, last = remove1
    beginning = 0
    middle = last.span()[1]
    end = remove2.span()[0]
    svo_file_path = svo_input_path[beginning:middle] + "output/"
    svo_file_name = svo_input_path[middle:end]
    
    output_path_pc = svo_file_path + "pc_" + svo_file_name + ".txt"
    output_path_pc_with_colors = svo_file_path + "cpc_" + svo_file_name + ".txt"
    output_path_image = svo_file_path + "left_photo_" + svo_file_name + ".jpg"

    input_type = sl.InputType()
    input_type.set_from_svo_file(svo_input_path)

    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)

    cam = sl.Camera()

    # Check camera is working
    status = cam.open(init)
    print(status)
    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    err = cam.grab(runtime)

    cam.retrieve_image(mat, sl.VIEW.LEFT)
    fd = cv2.imwrite(output_path_image, mat.get_data())

    cam.retrieve_measure(mat, sl.MEASURE.XYZRGBA)
    
    pc_list_with_colors = []
    pc_list = []
    minX = float('inf') # horizontal, positive is towards the door
    minY = float('inf') # vertical, positive is towards the other plants, back of the room
    minZ = float('inf') # depth, positive is towards leaves


    maxX = float('-inf') # horizontal, positive is towards the door
    maxY = float('-inf') # vertical, positive is towards the other plants, back of the room
    maxZ = float('-inf') # depth, positive is towards leaves
        
    for i in range(0, mat.get_width()):
        for j in range(0, mat.get_height()):
            err, val = mat.get_value(i,j)
            
            if not np.isnan(val[0]) and not np.isinf(val[0]):
                pc_list.append(val[0:3])

                if minX > val[0]:
                    minX = val[0]
                if minY > val[1]:
                    minY = val[1]
                if minZ > val[2]:
                    minZ = val[2]

                if maxX < val[0]:
                    maxX = val[0]
                if maxY < val[1]:
                    maxY = val[1]
                if maxZ < val[2]:
                    maxZ = val[2]

                colorVal = binaryX(val[3])
                R, G, B, A = (colorVal[0:8], colorVal[8:16], colorVal[16:24], colorVal[24:32])

                # Convert the colorVal string to an integer
                # colorVal_int = int(colorVal, 2)

                # Extract individual color components using bitwise operations
                # R = (colorVal_int >> 24) & 0xFF
                # G = (colorVal_int >> 16) & 0xFF
                # B = (colorVal_int >> 8) & 0xFF
                # A = colorVal_int & 0xFF

                color_components = [int(R, 2), int(G, 2), int(B, 2), int(A, 2)]
    
                # item.append(R)
                # item.append(G)
                # item.append(B)
                # item.append(A)
                # Convert val to a numpy array
                val_array = np.array(val[0:3], dtype=np.uint8)

                # Combine val_array and color components into a single array
                item = np.concatenate((val_array, color_components), axis=None)
                pc_list_with_colors.append(item)
                

    minX = abs(minX)
    minY = abs(minY)

    for i in range(0, len(pc_list)):
        pc_list[i][0] += minX
        pc_list[i][1] += minY
        pc_list_with_colors[i][0] += minX
        pc_list_with_colors[i][1] += minY
        # pc_list[i][2] += minZ

    # print('mins:')
    # print(minX)
    # print(minY)
    # print(minZ)

    # print('maxs:')
    # print(maxX)
    # print(maxY)
    # print(maxZ)

    # print(pc_list)

    # np_pc_list = np.array(pc_list)
    # np.save(output_path_pc, np_pc_list)

    with open(output_path_pc, 'wb') as f:
        pickle.dump(pc_list, f)


    # filed = open(output_path_pc,'w')
    # filed.write(str(np_pc_list))
    # filed.close()

    with open(output_path_pc_with_colors, 'wb') as f:
        pickle.dump(pc_list_with_colors, f)

    # np_pc_list_with_colors = np.array(pc_list_with_colors)
    # filed = open(output_path_pc_with_colors,'w')
    # filed.write(str(pc_list_with_colors))
    # filed.close()


if __name__ == "__main__":
    main()
