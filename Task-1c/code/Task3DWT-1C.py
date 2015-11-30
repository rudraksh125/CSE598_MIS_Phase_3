__author__ = 'rahulkrsna'


import cv2
import Task1c as t2
import numpy as np
import collections

compare_FrameID = 0
videoFileName = ""
selectedFrames = []
totalMatchFrames = 10

def acceptInput():
    global videoFileName
    global compare_FrameID

    videoFileName = raw_input('Enter the .bwt file path: ')
    compare_FrameID = int(raw_input("Enter FrameID for Comaprison: "))


# Compute Eucleadean Distance between every vector and the vector of the chosen frame
def computeEucleadean(input_file):
    global compare_FrameID
    global selectedFrames
    global totalMatchFrames

    FrameInfo = {}
    eucledeanInfo = {}

    # Read the input file(.dwt file) and deserailized the data line by line and save the dwt values to a dictionary, based on frames
    for line in input_file:
        frameId = int(line.split(',')[0])
        # blockCoor = line.split(',')[1] +','+line.split(',')[2]
        # data = np.array([int(line.split(',')[1]),float(line.split(',')[2])])
        data = float(line.split(',')[4])
        if frameId in FrameInfo.keys():
            FrameInfo[frameId].append(data)
        else :
            FrameInfo[frameId] = [data]

    # Take the compare frame to be the frameID chosen by the user.
    keyFrame = FrameInfo[compare_FrameID]

    # Calculate the Eucledean distance for every frame, based on the DWT values
    # Compute Similarity = 1 / (1+ eucledean_distance)
    for keys,values in FrameInfo.items():
        distance = np.linalg.norm(np.array(keyFrame) - np.array(values))
        similarity = 1. / (1. + distance) # Similarity = 1 / (1+eucledian_distance)
        if similarity in eucledeanInfo.keys():
            eucledeanInfo[similarity].append(keys)
        else:
            eucledeanInfo[similarity] = [keys]

    # Sort the values in descending order basing on their similarities
    od_Similarities = collections.OrderedDict(sorted(eucledeanInfo.items(),reverse=True))

    # Print the 10 most similar frames to the chosen frame
    count = 0
    print('Similarity :: 1 :: very high similarity')
    print('Similarity :: 0 :: very low similarity')
    print('Similarity     - FrameId')
    for keys,values in od_Similarities.items():
        for value in values:
            if compare_FrameID != value:
                print ("{0} - {1}".format(keys, value))
                print ""
                selectedFrames.append(value)
                count += 1

        if count == totalMatchFrames:
            break


def showFrames():
    global selectedFrames
    global totalMatchFrames

    print t2.videoFilePath
    cap = cv2.VideoCapture(t2.videoFilePath)

    frame_id = 0
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            frame_id += 1
            # If the current frame is the frame chosen display the frame
            if frame_id in selectedFrames:
                cv2.imshow(str(frame_id), frame)
                count += 1
        else:
            cap.release()

        # All the 10 frames chosen are displayed so we exit.
        if count == totalMatchFrames:
            cap.release()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    global videoFileName

    t2.main() # Call the main function of task-2

    acceptInput() # Accept User Input
    # Open the input file to read
    input_file = open(videoFileName, 'r')
    frameInfo = input_file.readline()
    rows = int(frameInfo.split(',')[0].split(':')[1].strip(' '))
    cols = int(frameInfo.split(',')[1].split(':')[1].strip(' '))
    wavelets = int(frameInfo.split((','))[2].split(':')[1].strip(' '))
    computeEucleadean(input_file) #Compute Eculedean Distnace and similarities
    input_file.close() #close the file

    # Output
    showFrames()


# /Users/rahulkrsna/Documents/ASU_Fall2015/MIS/HW-3/CSE598_MIS_Phase_3/Task-2/code/R1_framedwt_10.fwt
if __name__ == '__main__':
    main()
