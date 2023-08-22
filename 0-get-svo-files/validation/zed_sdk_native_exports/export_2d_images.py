import sys
import cv2
import pyzed.sl as sl
import re


def main():

    # Get input parameters
    svo_input_path = sys.argv[1]

    remove1 = re.finditer(r"/", svo_input_path)
    *_, second_last, last = remove1
    beginning = 0
    middle_before_svo_folder = second_last.span()[1]
    middle_after_svo_folder = last.span()[1]
    end = -4
    svo_file_path = svo_input_path[beginning:middle_before_svo_folder] + "native_export_output/"
    svo_file_name = svo_input_path[middle_after_svo_folder:end]
    
    output_path = svo_file_path + svo_file_name + "_L.jpg"

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
    cv2.imwrite(output_path, mat.get_data())

    # cam.retrieve_image(mat, sl.VIEW.RIGHT)
    # cv2.imwrite(output_path + '_R.png', mat.get_data())


if __name__ == "__main__":
    main()