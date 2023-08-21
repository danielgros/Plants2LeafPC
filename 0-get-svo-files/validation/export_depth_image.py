import sys
import cv2
import pyzed.sl as sl
import re


def main():

    # Get input parameters
    svo_input_path = sys.argv[1]

    remove1 = re.finditer(r"/", svo_input_path)
    remove2 = re.search(r"\b.svo", svo_input_path)
    *_, last = remove1
    beginning = 0
    middle = last.span()[1]
    end = remove2.span()[0]
    svo_file_name = svo_input_path[beginning:middle] + "output/" + svo_input_path[middle:end]
    
    output_path = svo_file_name + "_depth.jpg"

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

    cam.retrieve_image(mat, sl.VIEW.DEPTH)
    cv2.imwrite(output_path, mat.get_data())

if __name__ == "__main__":
    main()