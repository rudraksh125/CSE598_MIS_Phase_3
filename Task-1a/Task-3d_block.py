__author__ = 'ysun138'
import cv2
import numpy as np

def Histogram(bits, yuv):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0*2/hist_pieces

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

def GetMatchingScore(hist_1, hist_2):
    cos = 0.0
    numerator = 0.0
    denominator1 = 0.0
    denominator2 = 0.0
    for i in range(0, hist_1.__len__()):
        numerator+=hist_1[i]*hist_2[i]
        denominator1+=hist_1[i]*hist_1[i]
        denominator2+=hist_2[i]*hist_2[i]
    cos = numerator / (pow(denominator1,0.5)*pow(denominator2,0.5))
    return cos

def Retrieve(frame_id, bits, filename):
    #number of pieces of histogram
    hist_pieces = int(bits)
    #interval of the histogram
    interval = 255.0/hist_pieces*2
    #list to store gray_instance_id
    hist_value = []
    for i in range(0, hist_pieces):
        hist_value.append(int(interval*i+interval/2.0-255.0))

    # calculate features for given frame
    original_frame = None
    original_gray_instance = []
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    while(cap.isOpened):
        ret, frame = cap.read()
        if(ret):
            if(frame_index == frame_id):
                # current frame
                original_frame = frame
                original_yuv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2YUV)
                original_yuv = original_yuv[:,:,0]

                # next frame
                ret,frame = cap.read()
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yuv = yuv[:,:,0]

                rows, cols = yuv.shape
                diff = np.ndarray((rows,cols), dtype = float, order = 'F')
                for i in range (0, rows):
                    for j in range(0, cols):
                        diff[i, j] = float(yuv[i,j]) - float(original_yuv[i,j])
                original_gray_instance = Histogram(bits, diff)
                break
            else:
                frame_index+=1

    # calculate similarity
    l_frame_id = []
    l_score = []
    cap = cv2.VideoCapture(filename)
    frame_index = 0
    ret, current_frame = cap.read()
    frame_count = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    for index in range (0, frame_count-1):
        ret, frame = cap.read()
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        yuv = yuv[:,:,0]

        original_yuv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2YUV)
        original_yuv = original_yuv[:,:,0]

        rows, cols = yuv.shape

        diff = np.ndarray((rows,cols), dtype = float, order = 'F')
        for i in range (0, rows):
            for j in range(0, cols):
                diff[i, j] = float(yuv[i,j]) - float(original_yuv[i,j])
        gray_instance = Histogram(bits, diff)
        score = 0.0
        for i in range(0, gray_instance.__len__()):
            score+=GetMatchingScore(original_gray_instance[i], gray_instance[i])
        score/= float(gray_instance.__len__())
        l_frame_id.append(frame_index)
        l_score.append(score)
        frame_index+=1
        current_frame = frame

    # sort
    for i in range (0, l_frame_id.__len__()-1):
        for j in range (i+1, l_frame_id.__len__()):
            if(l_score[i]<l_score[j]):
                x = l_score[i]
                l_score[i] = l_score[j]
                l_score[j] = x
                y = l_frame_id[i]
                l_frame_id[i] = l_frame_id[j]
                l_frame_id[j] = y

    # store the best ten scores and ids
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

    # find the best ten frames in video and show them
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    filename = raw_input("Enter the make of the video file: ")
    frame_id = int(raw_input("Enter the frame id: "))
    bits = int(raw_input("Enter number of n: "))

    Retrieve(frame_id, bits, filename)

if __name__ == '__main__':
    main()