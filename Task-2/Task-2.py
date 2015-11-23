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

    path.rstrip(slash)
    path = path + slash


    videoFileName = raw_input('Enter the video file name <v>: ')
    videoFilePath = path+videoFileName
    num_components = int(raw_input("Enter number of significant wavelet components: "))
    outputFilePath = videoFilePath.rsplit(".")[0]
    outputFilePath = "{0}_framedwt_{1}.fwt".format(outputFilePath,num_components)
    extractFrames()

# Extracts Frames and Saves the partial frame information
def extractFrames():
    global videoFilePath
    global frame_width
    global frame_height
    global num_components
    global outputFilePath
    # videoFilePath = '/Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-3/CSE598_MIS_Phase_3/Task-2/R1.mp4'

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
            DWT_2d_Transformation(y,frame_id)
            # if frame_id == 1:
            #     cap.release()
        else:
            cap.release()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Saved to path {0}".format(outputFilePath))



def DWT_2d_Transformation(y_component, frame_id):
    global frame_height
    global frame_width
    global num_components

    output_row = []
    # For every row, we calculate the average in sum and difference of every pair of values
    for row in range(frame_height):
        sum_avg_values = []
        diff_avg_values = []
        for col in range(0,frame_width-1, 2):
            sum_avg_values.append((np.float(y_component[row][col]) + np.float(y_component[row][col+1])) / 2)
            diff_avg_values.append((np.float(y_component[row][col]) - np.float(y_component[row][col+1])) / 2)

        output_row.append(sum_avg_values + diff_avg_values)

    transformed_data = np.array(output_row,dtype=np.float)
    transformed_data = transformed_data.transpose()

    # For every row, we calculate the average in sum and difference of every pair of values
    for row in range(frame_height/2):
        transform_row = transformed_data[row]
        diff_avg_values = []
        index = 0
        for col in range(0,frame_width-1, 2):
            transform_row[index] = (transform_row[col] + transform_row[col+1]) / 2
            diff_avg_values.append((transform_row[col] - transform_row[col+1]) / 2)
            index += 1
        for col in range(frame_width/2,frame_width):
            transform_row[col] = diff_avg_values[col-frame_width/2]

    # print transformed_data.transpose()
    saveToFile(frame_id,transformed_data, num_components)


def saveToFile(frame_id,transformed_info, length):

    global outputFilePath

    output_file = open(outputFilePath, 'a')

    rows,cols = transformed_info.shape
    index = 1
    turn = 0
    i = j = 0
    while i < rows and j < cols and index <= length:
        # print ("{0} -> ({1},{2})".format(transformed_info[i][j],i,j))
        stringToOutput = "{0},{1},{2} \n".format(frame_id,index,transformed_info[i][j])
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


def logPrinter(message):
    print message


def main():
    acceptInput()


if __name__ == '__main__':
    main()