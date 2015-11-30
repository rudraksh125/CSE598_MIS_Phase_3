CSE 408/598 Multimedia Information Systems
Phase #3

The Phase #3 part of the project basically helps to compare various images of a frame in a video.

System Requirements:
Python 2.7.10
OpenCV 2.4.12


Execution:
(Executions are on mac osX terminal, but it is mostly the same on every Platform.)
1. Open terminal.
2. To execute a task give python <task-name>
	for example: python task-1a.py
3. Follow the comments on the terminal for complete execution.


Explanation:
Task 1a:
Histogram is calculated on every 8*8 block of each frame. Then all the histograms are output to a file in the format <frame_id, block_coord, gray_instance_id, num_pixels>.

Task 1b:
2D-DCT applied on every 8*8 block of the frame and n most significant wavelet components are written to a file in the form ⟨frame_id,block_id, fred_comp_id ,value⟩ 

Task 1c: 
2D-DWT applied on every 8*8 block of the frame and n most significant wavelet components are written to a file in the form ⟨frame_id,block_coord,wavelet_comp_id,value⟩ 

Task 1d:
Calculated the difference between corresponding blocks in a frame and the frame following, then created a histogram to map the requency of different ranges of values. Placed into a file of [videofile]_diff_[n].dhc in the format <frame_id, block_coord, diff_comp_id, pixelcount>.


Task 2:
2D-DWT applied on every frame of the video and n most significant wavelet components of every frame is written to a file in the form ⟨frame_id,block_coord,wavelet_comp_id,value⟩ 

Task 3:
(a)
Frame by frame, we calculate its histogram. Also we calculate the matching score between current frame and the given frame. We sort all these scores and find the best 10 matching frames. Then frame ids and matching scores of the 10 is printed and all the frames are shown on the screen.

(b) 

(c)

(d)
Frame by frame, we calculate the difference histogram between current frame and the given frame. Based on the difference histogram, we calculate differences between each frame and the given frame. We sort all the differenes and find the smallest 10 values and frames. We print all the ten frames ids and their differences and also show them on screen.
