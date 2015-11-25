__author__ = 'rahulkrsna'

import cv2
from sys import platform as _platform
import numpy as np

path = ""
num_components = 0
frame_height = 64
frame_width = 64
videoFilePath = ""
videoFileName = ""
outputFilePath = ""

def acceptInput():
    global path
    global num_components
    global videoFilePath
    global videoFileName
    global outputFilePath

    #capture frame numbers as input.
    path = raw_input("Enter the Path of Folder containing video Files: ")
    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    path = path.rstrip(slash)
    path = path + slash


    videoFileName = raw_input('Enter the video file name <v>: ')
    videoFilePath = path+videoFileName
    num_components = 9
    while num_components > 8:
        num_components = int(raw_input("Enter number of significant wavelet components[must be less than 9]: "))
        if num_components < 9:
            break

    outputFilePath = videoFilePath.rsplit(".")[0]
    outputFilePath = "{0}_framedwt_{1}.bwt".format(outputFilePath,num_components)
    extractFrames()

# Extracts Frames and Saves the partial frame information
def extractFrames():
    global videoFilePath
    global frame_width
    global frame_height
    global num_components
    global outputFilePath
    # videoFilePath = '/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-3/CSE598_MIS_Phase_3/Task-1c/R1.mp4'

    cap = cv2.VideoCapture(videoFilePath)
    frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            frame_id += 1
            yuvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            y,u,v = cv2.split(yuvImage)
            input = y.astype(np.float)
            # DWT_2d_Transformation(input,frame_id, frame_height, frame_width) # Apply 2d-DWT Transformation

            for i in range(0,frame_height,8):
                for j in range(0,frame_width,8):
                    output = DWT_2d_Transformation(input[i:i+8,j:j+8])
                    saveToFile(frame_id,i,j,output, num_components)
            # if frame_id == 1:
            #     cap.release()
        else:
            cap.release()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Saved to path {0}".format(outputFilePath))


def haar_1D(data):
  if len(data) == 1:
    return data.copy()

  sum_avg = (data[0::2] + data[1::2]) / np.sqrt(2.)
  diff_avg = (data[0::2] - data[1::2]) / np.sqrt(2.)

  return np.hstack((haar_1D(sum_avg), diff_avg))


def DWT_2d_Transformation(frame):
  h,w = frame.shape
  rows = np.zeros(frame.shape, dtype=float)
  for y in range(h):
    rows[y] = haar_1D(frame[y])
  cols = np.zeros(frame.shape, dtype=float)
  for x in range(w):
    cols[:,x] = haar_1D(rows[:,x])
  return cols


# Zig Zag way of saving the data of a matrix.
def saveToFile(frame_id,coord_x, coord_y,transformed_info, length):

    global outputFilePath

    output_file = open(outputFilePath, 'a') # open the file

    rows,cols = transformed_info.shape # # of rows and columns
    index = 1
    turn = 0
    i = j = 0
    while i < rows and j < cols and index <= length: # Save the m(length) most significant values
        # print ("{0} -> ({1},{2})".format(transformed_info[i][j],i,j))
        stringToOutput = "{0},{1},{2},{3},{4} \n".format(frame_id,coord_x,coord_y,index,transformed_info[i][j])
        # print stringToOutput
        output_file.write(stringToOutput)
        index += 1

        if turn == 0 and i == 0 and j != cols-1:
            j += 1
            turn = 1
        elif turn == 1 and j == 0 and i != rows-1:
            i += 1
            turn = 0
        elif turn == 1 and i == rows-1:
            j += 1
            turn = 0
        elif turn ==0 and j == cols-1:
            i += 1
            turn = 1
        elif turn == 0:
            i -= 1
            j += 1
        elif turn == 1:
            i += 1
            j -= 1

    output_file.close()

# Unit Test Case
def testCase():
    comp = [[10,20,30,40],[20,30,40,50],[30,40,50,60],[40,50,60,70]]
    arr = np.array(comp)
    arr = arr.astype(dtype=np.float)
    DWT_2d_Transformation(arr)
    print arr


# Print to console
def logPrinter(message):
    print message


def main():
    acceptInput()
    # testCase()


if __name__ == '__main__':
    main()