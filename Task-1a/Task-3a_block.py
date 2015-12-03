__author__ = 'ysun138'
import cv2
import numpy as np

def Histogram(bits, yuv):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0/hist_pieces

    gray_instance = []
    l_gray_instance = []
    for m in range(0, hist_pieces):
        gray_instance.append(0)
    rows, cols = yuv.shape
    block_row = int(rows/8)
    block_col = int(cols/8)
    for i in range(0, block_row):
        for j in range(0, block_col):
            gray_instance = []
            for m in range(0, hist_pieces):
                gray_instance.append(0)
            for k in range(0, 8):
                for l in range(0, 8):
                    value = int(yuv[i*8+k,j*8+l])
                    gray_index = int(value/interval)
                    if(gray_index == gray_instance.__len__()):
                        gray_index-=1
                    gray_instance[gray_index] = gray_instance[gray_index]+1
                    l_gray_instance.append(gray_instance)
    return  l_gray_instance

def Correlation(hist_1, hist_2):
    avg_1 = 0.0
    avg_2 = 0.0
    length = hist_1.__len__()
    for i in range (0, length):
        avg_1 += hist_1[i]
        avg_2 += hist_2[i]
    avg_1 = avg_1/float(length)
    avg_2 = avg_2/float(length)

    square_sum1 = 0.0
    square_sum2 = 0.0
    numerator = 0.0
    for i in range(0, length):
        square_sum1+=(float(hist_1[i]) - avg_1)*(float(hist_1[i]) - avg_1)
        square_sum2+=(float(hist_2[i]) - avg_2)*(float(hist_2[i]) - avg_2)
        numerator+=(float(hist_1[i]) - avg_1)*(float(hist_2[i] - avg_2))
    denominator = pow(square_sum1*square_sum2, 0.5)
    if(denominator == 0.0):
        return 0
    else:
        return numerator/denominator

def Retrieve(frame_id, bits, filename):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0/hist_pieces
    #list to store gray_instance_id
    hist_value = []
    for i in range(0, hist_pieces):
        hist_value.append(int(interval*i+interval/2.0))

    original_frame = None
    original_gray_instance = []
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    # calculate histogram of given frame
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            if(frame_index == frame_id):
                original_frame = frame
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[:,:,0]
                original_gray_instance = Histogram(bits, yuv)
                break
            else:
                frame_index+=1

    l_frame_id = []
    l_score = []
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    # calculate similarity
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            yuv = yuv[:,:,0]
            gray_instance = Histogram(bits, yuv)
            score = 0.0
            for i in range(0, gray_instance.__len__()):
                score += Correlation(gray_instance[i], original_gray_instance[i])
            score/=float(gray_instance.__len__())
            l_frame_id.append(frame_index)
            l_score.append(score)
            frame_index+=1
        else:
            break

    for i in range (0, l_frame_id.__len__()-1):
        for j in range (i+1, l_frame_id.__len__()):
            if(l_score[i]<l_score[j]):
                x = l_score[i]
                l_score[i] = l_score[j]
                l_score[j] = x
                y = l_frame_id[i]
                l_frame_id[i] = l_frame_id[j]
                l_frame_id[j] = y

    l_result_id = []
    l_result_score = []
    for i in range(0, l_frame_id.__len__()):
        if(l_frame_id[i] == frame_id):
            continue
        else:
            l_result_id.append(l_frame_id[i])
            l_result_score.append(l_score[i])
        if(l_result_id.__len__() == 10):
            break
    print "Best ten matches:\nRank\tFrame_id\tMatching score"
    for i in range(0, l_result_id.__len__()):
        print str.format("{0}\t{1}\t{2}", i+1, l_result_id[i], l_result_score[i])

    cap = cv2.VideoCapture(filename)
    frame_index = 0
    d_frame = {}
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            for i in range(0, l_result_id.__len__()):
                if(frame_index == l_result_id[i]):
                    d_frame[l_result_id[i]] = frame
            if(d_frame.__len__() == 10):
                break
            frame_index+=1
        else:
            break
    cv2.imshow("original",original_frame)
    for i in range (0, l_result_id.__len__()):
        cv2.imshow(str.format("{0}", i+1),d_frame[l_result_id[i]])
    cv2.waitKey()
    cv2.destroyAllWindows()

def main():
    filename = raw_input("Enter the make of the video file: ")
    frame_id = int(raw_input("Enter the frame id: "))
    bits = int(raw_input("Enter number of n: "))

    Retrieve(frame_id, bits, filename)

if __name__ == '__main__':
    main()