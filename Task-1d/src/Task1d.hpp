//
//  Task1d.hpp
//  cse408_project01
//
//  Created by Matthew Weser on 11/28/15.
//  Copyright © 2015 mweser. All rights reserved.
//

#ifndef Task1d_hpp
#define Task1d_hpp
#define VERBOSE		1

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
VideoCapture video_cap;

string filename;
string outfile;

    // currentBlock
    // nextBlock














#endif /* Task1d_hpp */
