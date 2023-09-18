import numpy as np
from pyzed import sl # pylint: import-error
import pickle
import re
import sys
import cv2


import struct

def binaryX(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))

def main():
    # Get input parameters
    svo_input_path = sys.argv[1]

    remove1 = re.finditer(r"/", svo_input_path)
    *_, second_last, last = remove1
    beginning = 0
    middle_before_svo_folder = second_last.span()[1]
    middle_after_svo_folder = last.span()[1]
    end = -4
    svo_file_path = svo_input_path[beginning:middle_before_svo_folder] + "output/"
    svo_file_name = svo_input_path[middle_after_svo_folder:end]

    output_path_pc = svo_file_path + "pc_" + svo_file_name + ".txt"
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

    # fc = open("camera_information.txt", "w")
    # fc.write(cam.get_camera_information())
    # fc.close()

    cam.retrieve_image(mat, sl.VIEW.LEFT)
    # Suppress the 'no-member' error for cv2.imwrite
    # pylint: disable=no-member
    fd = cv2.imwrite(output_path_image, mat.get_data())

    cam.retrieve_measure(mat, sl.MEASURE.XYZRGBA)

    # filed = open('PointCLD.dat','w+')

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

                # temporary cutoff values to help with mask scaling -> should be removed in future after mask scaling method is improved
                # if (val[0] < -2150 or val[0] > 3095):
                #     continue
                # if (val[1] < -1300 or val[1] > 1200):
                #     continue

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

                # g = str(val[0:3])+'  '
                # filed.write(g)
                colorVal = binaryX(val[3])
                A, R, G, B = (colorVal[0:8], colorVal[8:16], colorVal[16:24], colorVal[24:32])
                # g = str(R)+' '+str(G)+' '+str(B)+' ' +str(A)
                # filed.write(g)
                pc_list.append([val[0], val[1], val[2], int(R, 2), int(G, 2), int(B, 2), int(A, 2)])
                # else:
                #     pc_list.append([0, 0, 0, 0, 0, 0, 0])


            # filed.write('\n')
    # filed.close()

    minX = abs(minX)
    minY = abs(minY)

    # for i in range(0, len(pc_list)):
    #     pc_list[i][0] += minX
    #     pc_list[i][1] += minY

    with open(output_path_pc, 'wb') as f:
        pickle.dump(pc_list, f)

    # np_pc_list = np.array(pc_list)
    # np.save(output_path_pc, np_pc_list)

    # filed = open(output_path_pc,'w')
    # filed.write(str(np_pc_list))
    # filed.close()


if __name__ == "__main__":
    main()
