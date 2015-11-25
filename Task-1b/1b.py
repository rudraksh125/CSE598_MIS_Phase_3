__author__ = 'kvivekan'

from sys import platform as _platform
import cv2
import time
import math

input_file = ""
input_video_filename = ""
output_file = ""
num_frequency_components = 0
block_width = 8
block_height = 8
frame_width = 0
frame_height = 0
dct_matrix = [[0 for x in range(block_width)] for y in range(block_height)]
dct_matrix_tran = [[0 for x in range(block_width)] for y in range(block_height)]


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


def print_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print '\n'.join(table)


def calculate_dct_matrix():
    global block_width
    global block_height
    global dct_matrix

    x_current = 0
    y_current = 0

    for i in range(x_current, x_current + block_height):
        for j in range(y_current, y_current + block_width):
            if i == 0:
                dct_matrix[i - x_current][j - y_current] = 1.0 / 2 * math.sqrt(2)
            else:
                dct_matrix[i - x_current][j - y_current] = 0.5 * math.cos(((2 * j + 1) * i * math.pi) / 16.0)
    print print_matrix(dct_matrix)

    dct_matrix_transpose()
    print_matrix(dct_matrix_tran)

def dct_matrix_transpose():
    global dct_matrix_tran
    global dct_matrix
    for i in range(len(dct_matrix)):
        for j in range(len(dct_matrix[0])):
            dct_matrix_tran[j][i] = dct_matrix[i][j]

def DCT2D_Tranform(frame, frame_id):
    print "frame_id: " + str(frame_id)
    print_matrix(frame)
    block_id = 1
    block_x = 0
    block_y = 0
    list_block = []
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
            print_matrix(block_matrix)
            print "\n"
            block_y = block_y + block_width
            y_current = block_y
            block_id += 1
        block_x = block_x + block_height
        block_y = 0
        x_current = block_x


def matrixmult(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print "Cannot multiply the two matrices. Incorrect dimensions."
        return

    # Create the result matrix
    # Dimensions would be rows_A x cols_B
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    print C

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C


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

    frame_id = 1
    while cap.isOpened():
        val, frame = cap.read()
        if val is True and frame_id < 2:
            frame_id += 1
            yuv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            y, u, v = cv2.split(yuv_image)
            DCT2D_Tranform(y, frame_id)
        else:
            cap.release()


def main():
    read_input()
    extract_frames()


main()
