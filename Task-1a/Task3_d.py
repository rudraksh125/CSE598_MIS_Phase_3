__author__ = 'ysun138'
import cv2
import numpy as np

def Histogram(bits, yuv):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0*2/hist_pieces

    gray_instance = []
    for m in range(0, hist_pieces):
        gray_instance.append(0)
    rows, cols = yuv.shape
    for k in range(0, rows):
            for l in range(0, cols):
                value = int(yuv[k,l])
                gray_index = int((value+255.5)/interval)
                gray_instance[gray_index] = gray_instance[gray_index]+1
    return  gray_instance

def GetMatchingScore(hist_value, gray_instance):
    score = 0.0
    for i in range (0, hist_value.__len__()):
        score+=abs(hist_value[i]*gray_instance[i])
    return score

def Retrieve(frame_id, bits, filename):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0/hist_pieces*2
    #list to store gray_instance_id
    hist_value = []
    for i in range(0, hist_pieces):
        hist_value.append(int(interval*i+interval/2.0-255.0))

    original_frame = None
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            if(frame_index == frame_id):
                original_frame = frame
                break
            else:
                frame_index+=1

    l_frame_id = []
    l_score = []
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            if(frame_index == frame_id):
                l_frame_id.append(frame_index)
                l_score.append(0)
            else:
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[:,:,0]

                original_yuv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2YUV)
                original_yuv = original_yuv[:,:,0]

                rows, cols = yuv.shape

                diff = np.ndarray((rows,cols), dtype = float, order = 'F')
                for i in range (0, rows):
                    for j in range(0, cols):
                        diff[i, j] = float(yuv[i,j]) - float(original_yuv[i,j])
                gray_instance = Histogram(bits, diff)
                score = GetMatchingScore(hist_value,gray_instance)
                l_frame_id.append(frame_index)
                l_score.append(score)
            frame_index+=1
        else:
            break

    for i in range (0, l_frame_id.__len__()-1):
        for j in range (i+1, l_frame_id.__len__()):
            if(l_score[i]>l_score[j]):
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
    for i in range (0, l_result_id.__len__()):
        cv2.imshow(str.format("{0}", i+1),d_frame[l_result_id[i]])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    filename = raw_input("Enter the make of the video file: ")
    frame_id = int(raw_input("Enter the frame id: "))
    bits = int(raw_input("Enter number of n:"))

    Retrieve(frame_id, bits, filename)

if __name__ == '__main__':
    main()