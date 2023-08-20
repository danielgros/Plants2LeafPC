#!/bin/bash

# Bash Script that does the svo recording


regex_00min='^00$'

svo_counter=0

while [ True ];
do	
#JR	sleep 60s

	currentMinutes=`date +"%M"`

	currentDate=`date +"%Y-%m-%d_%H.%M.%S"`
	filetype=".svo"
	filename1="${currentDate}_hevc_ultra${filetype}"
	filename2="${currentDate}_avchd_ultra${filetype}"
	filename3="${currentDate}_hevc_neural${filetype}"
	filename4="${currentDate}_png_ultra${filetype}"

	if [[ $currentMinutes =~ $regex_00min ]];
#        if [ true ];
	then
		((svo_counter++))
		echo Number of SVO Recordings Taken: ${svo_counter}

		python3 /home/user/Documents/svo_recording/src/svo_recording_hevc_ultra.py /home/user/Documents/svo_recording/recordings/data_collection/"${filename1}"
	
	        sleep 10s
	        echo Took File 1

		python3 /home/user/Documents/svo_recording/src/svo_recording_avchd_ultra.py /home/user/Documents/svo_recording/recordings/data_collection/"${filename2}"
	

		sleep 10s
		echo Took File 2

		python3 /home/user/Documents/svo_recording/src/svo_recording_hevc_neural.py /home/user/Documents/svo_recording/recordings/data_collection/"${filename3}"
                
		sleep 10s
		echo Took File 3

		python3 /home/user/Documents/svo_recording/src/svo_recording_png_ultra.py /home/user/Documents/svo_recording/recordings/data_collection/"${filename4}"

		sleep 10s
		echo Took File 4
	fi

#	sleep 3420s
done

echo "Loop Stopped. Error?????"
