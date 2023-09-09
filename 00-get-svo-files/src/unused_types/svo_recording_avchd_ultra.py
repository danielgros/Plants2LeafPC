########################################################################
#
# Copyright (c) 2022, STEREOLABS.
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
from signal import signal, SIGINT
from pyzed import sl

cam = sl.Camera()

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)

def main():
    if not sys.argv or len(sys.argv) != 2:
        print("Only the path of the output SVO file should be passed as argument.")
        sys.exit(1)

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD2K
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    init.sdk_verbose = 1
    init.sdk_verbose_log_file = "/home/user/Documents/svo_recording/sdk_log_file/log_file"
    # other initial parameters have been left blank because default value is adequate

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        sys.exit(1)

    path_output = sys.argv[1]
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        sys.exit(1)

    runtime = sl.RuntimeParameters()
    cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA, -1)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, 0)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 5)
    cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, -1)
    # other video settings have been left blank because default value is adequate


    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while frames_recorded < 100:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    main()
