__author__ = 'kvivekan'

from sys import platform as _platform
import cv2
import math
import numpy

input_file = ""
input_video_filename = ""
output_file = ""
num_frequency_components = 0
block_width = 8
block_height = 8
frame_width = 512
frame_height = 512
dct_matrix = [[0 for x in range(block_width)] for y in range(block_height)]
dct_matrix_tran = [[0 for x in range(block_width)] for y in range(block_height)]
top_n_components = []
freq_comp_id_coord = {}

def read_input():
    global input_file
    global output_file
    global num_frequency_components
    global input_video_filename

    path = raw_input("Enter the path to video file: ")
    num_frequency_components = int(raw_input("Enter number of significant frequency components: "))

    if _platform == "linux" or _platform == "linux2":
        slash = '/'
    elif _platform == "darwin":
        slash = '/'
    elif _platform == "win32":
        slash = '\\'

    if slash in path:
        input_video_filename = path.rsplit(slash, 1)[1].rsplit(".", 1)[0]
    else:
        input_video_filename = path.rsplit(".", 1)[0]

    input_file = path
    output_file = "{0}_blockdct_{1}.bct".format(input_video_filename, num_frequency_components)

def recreate_frame(frame_id, filename):
     with open(filename,"r") as f:
        frame = [[0 for x in range(frame_width)] for y in range(frame_height)]
        for line in f:
            if int(line.split(",")[0]) == frame_id:
                set_frame_value_by_line(frame, line)
        return frame

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

def set_frame_value_by_line(frame, line):
    l = line.split(",")
    frame_id = int(l[0])
    block_id = int(l[1])
    comp_id = int(l[2])
    value = float(l[3])
    if block_id == 512:
        print "block 512"
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

def print_matrix(matrix):
    print('\n'.join([''.join(['{:15}'.format(item) for item in row])
      for row in matrix]))


def calculate_dct_matrix():
    global block_width
    global block_height
    global dct_matrix

    for i in range(block_height):
        for j in range(block_width):
            if i == 0:
                dct_matrix[i][j] = 1.0 / (2 * math.sqrt(2))
            else:
                dct_matrix[i][j] = 0.5 * math.cos(((((2.0 * j) + 1.0) * i * math.pi) / 16.0))
    print_matrix(dct_matrix)

    dct_matrix_transpose()
    print "inverse:"
    print_matrix(dct_matrix_tran)

def dct_matrix_transpose():
    global dct_matrix_tran
    global dct_matrix
    for i in range(len(dct_matrix)):
        for j in range(len(dct_matrix[0])):
            dct_matrix_tran[j][i] = dct_matrix[i][j]

def DCT2D_Tranform(frame, frame_id):
    global output_file
    global top_n_components
    global num_frequency_components

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
                #print "current block id: " + str(block_id)
                for i in range(x_current, x_current + block_height):
                    if i < frame_height:
                        for j in range(y_current, y_current + block_width):
                            if j <frame_width:
                                block_matrix[i-x_current][j-y_current] = frame[i][j]
                #print_matrix(block_matrix)
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

def convert_to_int_matrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            mat[i][j] = int(mat[i][j])
    return mat

def IDCT2D_Tranform(frame, frame_id):
    global output_file
    global top_n_components
    global num_frequency_components

    with open(output_file+"_idct","wb") as f_output_file:
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
                print "current block id: " + str(block_id)
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

def init_list_top_n():
    global top_n_components
    global frame_height
    global frame_width
    global block_width
    global block_height
    max_num_comp = (frame_height * frame_width) / (block_width * block_height)
    top_n_components = [0 for x in range(max_num_comp)]
    #printlen(top_n_components)

def extract_frames():
    global input_file
    global frame_width
    global frame_height

    cap = cv2.VideoCapture(input_file)
    frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    print frame_height, frame_width, frame_count

    calculate_dct_matrix()
    init_list_top_n()

    frame_id = 1
    while cap.isOpened() and frame_id < 2:
        val, frame = cap.read()
        if val is True:
            f = '{:04}'.format(frame_id)
            nameBGR = "BGRframe"+f+".jpg"
            cv2.imwrite(nameBGR, frame)
            yuv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            y, u, v = cv2.split(yuv_image)
            nameYUV = "YUVframe"+f+".jpg"
            # yframes = cv2.cvtColor(y, cv2.COLOR_YUV2BGR)
            cv2.imwrite(nameYUV, y)
            DCT2D_Tranform(y, frame_id)
            frame_id += 1
        else:
            cap.release()

def save_frame_tofile(name, frame):
    yframes = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(name, yframes)

def test(num_comp):
    global input_file
    global output_file
    global num_frequency_components
    global input_video_filename
    global frame_width
    global frame_height


    input_file = "lenna.png"

    num_frequency_components = num_comp
    # input_file = "BGRframe0001.jpg"
    output_file = input_file + "_" + str(num_frequency_components) +"_output.bct"


    input_video_filename = "lenna"

    calculate_dct_matrix()
    init_list_top_n()

    ff = cv2.imread(input_file)


    frame_height, frame_width, frame_channels = ff.shape

    yuv_image = cv2.cvtColor(ff, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv_image)
    DCT2D_Tranform(y, 1)

    print "\n\n\n\n recreated:\n\n\n"
    freq_frame = recreate_frame(1, output_file)
    # print_matrix(freq_frame)
    IDCT2D_Tranform(freq_frame,1)
    spacial_frame = recreate_frame(1, output_file+"_idct")


    print "\n\nfloat:"
    # print_matrix(spacial_frame)
    print "\n\n\n\n spacial recreated:\n\n\n"
    int_sp_frame = convert_to_int_matrix(spacial_frame)
    # print_matrix(int_sp_frame)
    save_frame_tofile(output_file+"recreated_" +str(num_frequency_components)+".jpg", numpy.array(int_sp_frame,dtype=numpy.uint8))

def main():

    # read_input()
    # extract_frames()
    test(5)
    test(10)
    test(25)
    test(50)
    test(64)

main()
