//
//  Task1d.cpp
//  cse408_project01
//
//  Created by Matthew Weser on 11/28/15.
//  Copyright © 2015 mweser. All rights reserved.
//

#include "Task1d.hpp"


/* For each frame (except the last) of the video and for each block, the program computes the difference from the same block in the next frame and then
 creates an n-bin difference histogram, by quantizing the obtained differences. The outputs, of the form
 ⟨frame id,block coord,diff comp id,pixelcount⟩ are written into a file of the form
	videofilenamediff n.dhc
 */



    // TODO: FIGURE OUT IF BLOCK VALUE IS SOME SORT OF AVERAGE, OR EACH PIXEL IN THE BLOCK SUMMED UP
    // LOOK AT PYTHON IMPLEMENTATIONS TO FIGURE THIS OUT



/******************** UTILITY FUNCTIONS ***********************/

/* Function opens video for access 
 * requires a global VideoCapture object named "video_cap" to work
 */
void openVideo(string filePath){
    
    bool success = video_cap.open(filePath);
    
    if(success)
    {
	cout << "Video opened" << endl;
    }
    else
    {
	cout << "Video failed to open" << endl;
    }
}


    // Receives the selected frame, the chosen x and y coordinates of the top left corner of the future 8x8 sub image
Mat get_block(Mat frame, int x, int y)
{
    Mat subFrame(frame, Rect(x, y, 8, 8));
    return subFrame;
}


/************************** IMPLEMENTATION FUNCTIONS ************************/

/* Function scans through video file by frame, and each frame by block (nested for loops)
 * Then outputs values to formated histogram file in order:
 *	<frame_id,block_coord,diff_comp_id,pixelcount>
 */

void scan_video()
{
    bool video_not_done = true;
    Mat current_frame;
    Mat prev_frame;
    int row;
    int col;
    
    int block_row;
    int block_col;
    
    Mat prev_block;
    Mat current_block;
    
    frame_id = 0;
    
    ofstream fout;
    fout.open(outfile.c_str());
    
    while (video_not_done)
    {
	/* Grabs next frame */
	if (frame_id == 0)	/* First time through: grab two frames */
	{
	    video_not_done = video_cap.read(prev_frame);
	    video_not_done = video_cap.read(current_frame);
	    frame_id = 2;
	}
	else	/* Set next_frame as prev_frame, and grab new current_frame */
	{
	    prev_frame = current_frame;
	    video_not_done = video_cap.read(current_frame);
	    frame_id++;
	}
	
	block_coord = 0;
	diff_comp_id = 0;
	pixelcount = 0;
	
	if (video_not_done)
	{
	    for (row = 0; row < frame_rows; row += 8)
	    {
		for (col = 0; col < frame_cols; col += 8)
		{
		    /* At next block: increment block pointer and compare */
		    
		    
		    prev_block = get_block(prev_frame, col, row);
		    current_block = get_block(current_frame, col, row);

		    if(VERBOSE)
		    {
			printf("\n<%d,%d>\n",frame_id-1, block_coord);
			for (block_row = 0; block_row < 8; block_row++)
			{
			    for (block_col = 0; block_col < 8; block_col++)
			    {
				printf("%d,%d ", prev_block.at<uchar>(block_row, block_col), current_block.at<uchar>(block_row, block_col));
				
				
			    }
			    cout << endl;

			}
			cout << endl;

		    }
		    
		    
		    
		    
		    fout << frame_id - 1 << "," <<
			    block_coord << "," <<
			    diff_comp_id << "," <<
			    pixelcount << endl;
		    block_coord++;

		    
		}
		
		
	    }

	    
	}
	
	
    }
    
    
    
}






/* Function main:
 * 1. while(!EOF)
 * 2. getFrame()
 * 3. getBlock()
 * 4. diff = currentBlock - nextBlock
 * 5. n-bin difference histogram create() 
 * 6. >> write to file
 */
int main(int argc, char** argv)
{
    
	// use special functions from phase 2 to "get" video file frames
    
    if (argc >= 2)
    {
	filename = argv[1];
	n = stoi(argv[2]);
    }
    else
    {
	printf("Please enter the name of the video file: ");
	cin >> filename;
	
	printf("n: ");
	cin >> n;
    }
    
    if(VERBOSE)printf("Filename is %s\nValue of n is %d\n", filename.c_str(), n);

    openVideo(filename);

    char n_value[16];
    sprintf(n_value, "%d", n);
    
    outfile = filename + "_diff_" + n_value + ".dhc";
    if(VERBOSE) printf("Output filename is %s\n", outfile.c_str());
    
    scan_video();
    
    
    
    return 0;
}













