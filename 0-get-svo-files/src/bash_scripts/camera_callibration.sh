#!/bin/bash

# Bash Script that does the svo recording


#filename=$(first_test)
#echo File Name: ${filename}

python3 /home/user/Documents/svo_recording/src/svo_recording_hevc_ultra.py /home/user/Documents/svo_recording/recordings/camera_callibration/'fake_plant_150_hevc_ultra.svo'
		
python3 /home/user/Documents/svo_recording/src/svo_recording_avchd_ultra.py /home/user/Documents/svo_recording/recordings/camera_callibration/'fake_plant_150_avchd_ultra.svo'
		
python3 /home/user/Documents/svo_recording/src/svo_recording_hevc_neural.py /home/user/Documents/svo_recording/recordings/camera_callibration/'fake_plant_150_hevc_neural.svo'
		
python3 /home/user/Documents/svo_recording/src/svo_recording_png_ultra.py /home/user/Documents/svo_recording/recordings/camera_callibration/'fake_plant_150_png_ultra.svo'
