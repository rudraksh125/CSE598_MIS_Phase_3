/* Matthew Weser
 * CSE 408 Phase III
 * 29 Nov 2015
 */

#ifndef Task1d_hpp
#define Task1d_hpp
#define VERBOSE		0

#include <stdio.h>
#include <iostream>
#include <string.h>
#include <fstream>

    //OpenCV libraries included
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/core.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/imgcodecs.hpp"

using namespace std;
using namespace cv;


/* Fields for printing */
int frame_id;
int block_coord;
int diff_comp_id;
int pixelcount;

int n;
int num_bins;
double bin_diff;
int start_median;

int pixelcount_array[256] = {0};

VideoCapture video_cap;
int frame_rows = 64;
int frame_cols = 64;
bool framebyframe = false;


string filename;
string outfile;

#endif /* Task1d_hpp */
