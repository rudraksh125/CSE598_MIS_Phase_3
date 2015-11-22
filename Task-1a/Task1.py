__author__ = 'ysun138'

import cv2
import numpy as np

def Quantizing(cap, bits, filename):
    outfile = open("{0}_hist_{1}.hst".format(filename.split(".")[0], bits),'w')
    hist_pieces = int(pow(2, bits))
    interval = 255.0/hist_pieces
    print interval
    hist_value = []
    for i in range(0, hist_pieces):
        hist_value.append(int(interval*i+interval/2.0))
    frame_index = 1
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            yuv = yuv[:,:,0]
            rows, cols = yuv.shape
            block_row = int(rows/8)
            block_col = int(cols/8)
            print block_row
            print block_col
            for i in range(0, block_row):
                for j in range(0, block_col):
                    gray_instance = []
                    for m in range(0, hist_pieces):
                        gray_instance.append(0)
                    for k in range(0, 8):
                        for l in range(0, 8):
                            value = int(yuv[i*8+k,j*8+l])
                            gray_index = int(value/interval)
                            gray_instance[gray_index] = gray_instance[gray_index]+1
                    block_index = i*block_col+j
                    for m in range(0, hist_pieces):
                        outfile.write("{0},{1},{2},{3}\n".format(frame_index, block_index, hist_value[m], gray_instance[m]))
            frame_index+=1
        else:
            break
    outfile.close()

def main():
    filename = raw_input("Enter the make of the video file: ")
    bits = int(raw_input("Enter number of n:"))
    videoFile = filename
    cap = cv2.VideoCapture(videoFile)

    Quantizing(cap, bits, filename)

if __name__ == '__main__':
    main()