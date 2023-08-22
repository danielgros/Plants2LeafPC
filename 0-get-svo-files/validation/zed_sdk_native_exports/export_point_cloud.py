########################################################################
#
# Copyright (c) 2021, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import sys

import pyzed.sl as sl
import re


def main():
    # Create a ZEDCamera object
    zed = sl.Camera()

    # Get input and output parameters
    svo_input_path = sys.argv[1]
    
    remove1 = re.finditer(r"/", svo_input_path)
    remove2 = re.search(r"\b.svo", svo_input_path)
    *_, second_last, last = remove1
    beginning = 0
    middle_before_svo_folder = second_last.span()[1]
    middle_after_svo_folder = last.span()[1]
    end = remove2.span()[0]
    svo_file_path = svo_input_path[beginning:middle_before_svo_folder] + "native_export_output/"
    svo_file_name = svo_input_path[middle_after_svo_folder:end]
    
    output_path = svo_file_path + svo_file_name + "_fpc.obj"

    # Set up svo file input
    input_type = sl.InputType()
    input_type.set_from_svo_file(svo_input_path)

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    
    # Use a right-handed Y-up coordinate system
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Enable positional tracking with default parameters.
    # Positional tracking needs to be enabled before using spatial mapping
    # py_transform = sl.Transform()
    # tracking_parameters = sl.PositionalTrackingParameters(init_pos=py_transform)
    tracking_parameters = sl.PositionalTrackingParameters()
    err = zed.enable_positional_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Enable spatial mapping
    mapping_parameters = sl.SpatialMappingParameters()
    mapping_parameters.map_type = sl.SPATIAL_MAP_TYPE.FUSED_POINT_CLOUD
    mapping_parameters.resolution_meter = mapping_parameters.get_resolution_preset(sl.MAPPING_RESOLUTION.HIGH)
    mapping_parameters.range_meter = 3.5
    err = zed.enable_spatial_mapping(mapping_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Grab data during 3000 frames
    frame = 0
    py_fpc = sl.FusedPointCloud()  # Create a Mesh object
    runtime_parameters = sl.RuntimeParameters()

    while frame < 3000:
        # For each new grab, mesh data is updated
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # In the background, spatial mapping will use newly retrieved images, depth and pose to update the mesh
            mapping_state = zed.get_spatial_mapping_state()

            print("\rImages captured: {0} / 3000 || {1}".format(frame, mapping_state))

            frame = frame + 1
        else:
            break

    print("\n")

    # Extract, filter and save the mesh in an obj file
    print("Extracting Point Cloud...\n")
    err = zed.extract_whole_spatial_map(py_fpc)
    print(repr(err))
    print("Saving Point Cloud...\n")
    py_fpc.save(output_path)

    # Disable tracking and mapping and close the camera
    zed.disable_spatial_mapping()
    zed.disable_positional_tracking()
    zed.close()

if __name__ == "__main__":
    main()
