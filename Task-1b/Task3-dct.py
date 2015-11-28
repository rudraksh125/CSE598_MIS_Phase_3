__author__ = 'kvivekan'

from sys import platform as _platform
import cv2
import math
from itertools import izip
import operator
import numpy

task_3_input_video_file = ""
task_1_input_bct_file = ""
num_frequency_components = 0
frame_id = 0
block_width = 8
block_height = 8
frame_width = 64
frame_height = 64
freq_comp_id_coord = {}

def calculate_dct_matrix():
    global block_width
    global block_height

    dct_matrix = [[0 for x in range(block_width)] for y in range(block_height)]

    for i in range(block_height):
        for j in range(block_width):
            if i == 0:
                dct_matrix[i][j] = 1.0 / (2 * math.sqrt(2))
            else:
                dct_matrix[i][j] = 0.5 * math.cos(((((2.0 * j) + 1.0) * i * math.pi) / 16.0))

    return dct_matrix

def dct_matrix_transpose(dct_matrix):
    global block_width
    global block_height

    dct_matrix_tran = [[0 for x in range(block_width)] for y in range(block_height)]

    for i in range(len(dct_matrix)):
        for j in range(len(dct_matrix[0])):
            dct_matrix_tran[j][i] = dct_matrix[i][j]

    return dct_matrix_tran

def init_freq_coord_zigzag(block_height, block_width):

    global freq_comp_id_coord

    current_x = 0
    current_y = 0
    comp_id = 0
    #printstr(current_x), str(current_y)
    freq_comp_id_coord[comp_id]= [current_x,current_y]
    comp_id += 1
    while current_x <block_width and current_y<block_height:
        if current_x==0 and current_y == block_height -1:
            break;
        current_x += 1
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        comp_id += 1
        if current_y == 0:
            while current_x > 0:
                current_x -= 1
                current_y += 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                comp_id += 1
            if current_y != block_height - 1:
                current_y += 1
            else:
                continue
            #printstr(current_x), str(current_y)
            freq_comp_id_coord[comp_id] = [current_x,current_y]
            comp_id += 1
            while current_y > 0:
                current_x += 1
                current_y -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                comp_id += 1

    while current_x <block_width and current_y<block_height:
        current_x += 1
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        comp_id += 1
        while current_x < block_width:
            current_x += 1
            if current_x < block_width:
                current_y -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                comp_id += 1

        current_x -= 1
        if current_y != block_height - 1:
            current_y += 1
        else:
             break
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        comp_id += 1

        while current_y < block_height:
            current_y += 1
            if current_y < block_height:
                current_x -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                comp_id += 1
        current_y -= 1
    #printfreq_comp_id_coord

def matrixmult(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print "Cannot multiply, dimensions incorrect"
        return

    C = [[0 for row in range(cols_B)] for col in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def read_input():
    global task_3_input_video_file
    global task_1_input_bct_file
    global num_frequency_components
    global frame_id
    global block_width
    global block_height

    task_3_input_video_file = raw_input("Enter the path to Task 3 video file: ")
    frame_id = int(raw_input("Enter frame num to compare (1 indexed): "))
    task_1_input_bct_file = raw_input("Enter .bct filename: ")
    num_frequency_components = int(raw_input("Enter value of n: "))

    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    if slash in task_3_input_video_file:
        input_video_filename = task_3_input_video_file.rsplit(slash, 1)[1].rsplit(".", 1)[0]
    else:
        input_video_filename = task_3_input_video_file.rsplit(".", 1)[0]

    frame_id_filename = "{0}_frame_{1}.jpg".format(input_video_filename, frame_id)

    frame = extract_save_frame(frame_id, frame_id_filename)

    frame_id_bct_filename = "{0}_blockdct_compare_{1}.bct".format(input_video_filename, num_frequency_components)

    DCT2D_Tranform(frame_id_bct_filename, frame,frame_id,block_height,block_width)

    compare(task_1_input_bct_file, frame_id_bct_filename)

def set_frame_value_by_line(frame, line):
    l = line.split(",")
    frame_id = int(l[0])
    block_id = int(l[1])
    comp_id = int(l[2])
    value = float(l[3])

    frame_x, frame_y = get_freq_comp_block_byid(block_id, comp_id)

    # print "about to set block id : "+ str(block_id) +", " +" comp id: "+ str(comp_id) +", " + str(frame_x) + "," + str(frame_y) + " with value: " + str(value)
    frame[frame_y][frame_x] = value

#block id
def get_freq_comp_block_byid(block_id, comp_id):
    block_x = block_id % (frame_width / block_width)
    # block_y = block_id / block_width
    block_y = block_id / (frame_width / block_width)
    frame_x,frame_y = get_freq_comp_frame_byid(block_x,block_y, comp_id)
    return frame_x, frame_y

#comp_id
def get_freq_comp_frame_byid(block_x, block_y, comp_id):
    coord = get_freqcomp_coord_byid(comp_id)
    frame_x = block_width * block_x + coord[0]
    frame_y = block_height * block_y + coord[1]
    return frame_x, frame_y

def get_freqcomp_coord_byid(comp_id):
    return freq_comp_id_coord[comp_id]


def recreate_frame(frame_id, filename):
     with open(filename,"r") as f:
        frame = [[0 for x in range(frame_width)] for y in range(frame_height)]
        for line in f:
            if int(line.split(",")[0]) == frame_id:
                set_frame_value_by_line(frame, line)
        return frame

def IDCT2D_Tranform(output_file, frame, frame_id):

    global top_n_components
    global num_frequency_components

    dct_matrix = calculate_dct_matrix()
    dct_matrix_tran = dct_matrix_transpose(dct_matrix)
    init_freq_coord_zigzag(block_height, block_width)

    with open(output_file,"wb") as f_output_file:
        print "frame_id: " + str(frame_id)
        # print_matrix(frame)
        block_id = 0
        block_x = 0
        block_y = 0
        x_current = 0
        y_current = 0
        block_matrix = [[0 for x in range(block_width)] for y in range(block_height)]
        while block_x < frame_height:
            while block_y < frame_width:
                # print "current block id: " + str(block_id)
                for i in range(x_current, x_current + block_height):
                    if i < frame_height:
                        for j in range(y_current, y_current + block_width):
                            if j <frame_width:
                                block_matrix[i-x_current][j-y_current] = frame[i][j]
                # print_matrix(block_matrix)
                TA = matrixmult(dct_matrix_tran, block_matrix)
                result_matrix_block = matrixmult(TA, dct_matrix)
                # print "frequency domain block:"
                # print_matrix(result_matrix_block)
                lines = zigzag(0,0,block_height,block_width,result_matrix_block,num_frequency_components,frame_id,block_id)
                for line in lines[:num_frequency_components]:
                    f_output_file.write(line +'\n')

                block_y = block_y + block_width
                y_current = block_y
                block_id += 1
            block_x = block_x + block_height
            block_y = 0
            x_current = block_x
    # print "saved idct file: " + output_file

def recreate_frames(filename):
    with open(filename,"r") as f:
        list_frames = []
        current_frame_id = 1
        frame = [[0 for x in range(frame_width)] for y in range(frame_height)]
        for line in f:
            if int(line.split(",")[0]) == current_frame_id:
                set_frame_value_by_line(frame, line)
            else:
                list_frames.append(frame)
                current_frame_id += 1
                frame = [[0 for x in range(frame_width)] for y in range(frame_height)]
                set_frame_value_by_line(frame, line)
        return list_frames

def compare(task_1_input_bct_file, frame_id_bct_filename):
    global frame_id
    input_frame = recreate_frame(frame_id, frame_id_bct_filename)
    IDCT2D_Tranform("input._idct",input_frame,frame_id)
    spacial_input_frame = recreate_frame(frame_id, "input._idct")

    target_frames = recreate_frames(task_1_input_bct_file)

    all_similar_frames = {}
    count = 1
    for f in target_frames:
        IDCT2D_Tranform("target_"+str(count)+"._idct", f, count)
        spacial_target_frame = recreate_frame(count, "target_"+str(count)+"._idct")
        pairs = izip(spacial_input_frame, spacial_target_frame)
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        total_components = frame_height * frame_width
        score = (dif / 255.0 * 100) / total_components
        print "Difference (percentage) with frame "+ str(count) +":", score
        all_similar_frames[count] = ["target_"+str(count)+"._idct",score]
        count += 1

    sorted_frames = sorted(all_similar_frames, key=lambda k: all_similar_frames[k][1])
    n = 1
    for k in sorted_frames[:11]:
        print all_similar_frames[k]
        filename = all_similar_frames[k][0]
        spacial_target_frame = recreate_frame(k, filename)
        save_frame_tofile(str(n)+"_recreated.jpg", numpy.array(spacial_target_frame,dtype=numpy.uint8))
        n += 1

def save_frame_tofile(name, frame):
    yframes = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(name, yframes)

def extract_save_frame(frame_id, frame_id_filename):
    cap = cv2.VideoCapture(task_3_input_video_file)

    frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    print frame_height, frame_width, frame_count

    yframe = None

    counter = 1
    while cap.isOpened():
        val, frame = cap.read()
        if counter ==  frame_id:
            if val is True:
                yuv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                yframe, u, v = cv2.split(yuv_image)
                cv2.imwrite(frame_id_filename, yframe)
                cap.release()
                break
        else:
            counter += 1
    return yframe

def converttostrline(f,b,c,v):
    l = str(f) + "," + str(b) + "," + str(c) + "," + str(v)
    return l

def getlistelement(block, x,y):
    return block[y][x]

def zigzag(x,y,height,width,block,n, frameid, blockid):
    lines = []
    global freq_comp_id_coord
    current_x = x
    current_y = y
    comp_id = 0
    #printstr(current_x), str(current_y)
    freq_comp_id_coord[comp_id]= [current_x,current_y]
    l = converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y))
    lines.append(l)
    comp_id += 1
    while current_x <width and current_y<height:
        if current_x==0 and current_y == height -1:
            break;
        current_x += 1
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
        comp_id += 1
        if current_y == 0:
            while current_x > 0:
                current_x -= 1
                current_y += 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
                comp_id += 1
            if current_y != height - 1:
                current_y += 1
            else:
                continue
            #printstr(current_x), str(current_y)
            freq_comp_id_coord[comp_id] = [current_x,current_y]
            lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
            comp_id += 1
            while current_y > 0:
                current_x += 1
                current_y -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
                comp_id += 1

    while current_x <width and current_y<height:
        current_x += 1
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
        comp_id += 1
        while current_x < width:
            current_x += 1
            if current_x < width:
                current_y -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
                comp_id += 1

        current_x -= 1
        if current_y != height - 1:
            current_y += 1
        else:
             break
        #printstr(current_x), str(current_y)
        freq_comp_id_coord[comp_id] = [current_x,current_y]
        lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
        comp_id += 1

        while current_y < height:
            current_y += 1
            if current_y < height:
                current_x -= 1
                #printstr(current_x), str(current_y)
                freq_comp_id_coord[comp_id] = [current_x,current_y]
                lines.append(converttostrline(frameid,blockid,comp_id,getlistelement(block,current_x,current_y)))
                comp_id += 1
        current_y -= 1
    #printfreq_comp_id_coord
    return lines

def DCT2D_Tranform(frame_id_bct_filename ,frame, frame_id, block_height, block_width):
    global frame_height
    global frame_width

    dct_matrix = calculate_dct_matrix()
    dct_matrix_tran = dct_matrix_transpose(dct_matrix)
    init_freq_coord_zigzag(block_height, block_width)

    with open(frame_id_bct_filename,"wb") as f_output_file:
        print "frame_id: " + str(frame_id)
        # print_matrix(frame)
        block_id = 0
        block_x = 0
        block_y = 0
        x_current = 0
        y_current = 0
        block_matrix = [[0 for x in range(block_width)] for y in range(block_height)]
        while block_x < frame_height:
            while block_y < frame_width:
                #print "current block id: " + str(block_id)
                for i in range(x_current, x_current + block_height):
                    if i < frame_height:
                        for j in range(y_current, y_current + block_width):
                            if j <frame_width:
                                block_matrix[i-x_current][j-y_current] = frame[i][j]
                #print_matrix(block_matix)
                TA = matrixmult(dct_matrix, block_matrix)
                result_matrix_block = matrixmult(TA, dct_matrix_tran)
                #print "frequency domain block:"
                #print_matrix(result_matrix_block)
                lines = zigzag(0,0,block_height,block_width,result_matrix_block,num_frequency_components,frame_id,block_id)
                for line in lines[:num_frequency_components]:
                    f_output_file.write(line +'\n')

                block_y = block_y + block_width
                y_current = block_y
                block_id += 1
            block_x = block_x + block_height
            block_y = 0
            x_current = block_x
    print "saved dct transform file: " + frame_id_bct_filename


read_input()