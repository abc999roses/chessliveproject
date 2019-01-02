# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 08:58:02 2018

@author: CHU TIEN THANH
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:02:51 2018

@author: CHU TIEN THANH
"""

# this file is the main and the only file that needs to run on server
# nhận diện quân cờ, đưa ra vị trí quân cờ dạng list
# status: nhận diện quân cờ có lúc sai => không detect được nước tiếp theo.
# cần sửa thêm file move_tools4.py
import os, sys
import math
from keras.models import load_model
from time import gmtime, strftime, sleep
import inspect
from datetime import datetime
import logging
import time
import cv2
# user defined libraries
from server_tools import *
from move_tools5 import *

frame = inspect.currentframe()
fileName  =  ' ' + __file__ + ' '
logging.basicConfig(filename='example.log',level=logging.INFO)


def out_log(mode, *agrs):
  output_text = datetime.now().strftime("%H:%M:%S.%f") + fileName + (', '.join(agrs))
  if (mode == 2): # INFO
    logging.info(output_text)
  elif (mode == 1): # DEBUG
    logging.debug(output_text)
  return 0

# constant
n_col = 9
n_row = 10
n_col_inp = n_row
n_row_inp = n_col
#initial_color_label = [
#    [2, 2, 2, 2, 2, 2, 2, 2, 2],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 2, 0, 0, 0, 0, 0, 2, 0],
#    [2, 0, 2, 0, 2, 0, 2, 0, 2],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [1, 0, 1, 0, 1, 0, 1, 0, 1],
#    [0, 1, 0, 0, 0, 0, 0, 1, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [1, 1, 1, 1, 1, 1, 1, 1, 1]
#    ]
initial_piece_label = [
    [14, 9, 12, 11, 13, 11, 12, 9, 14],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 0, 0, 0, 0, 10, 0],
    [8, 0, 8, 0, 8, 0, 8, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 3, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 5, 4, 6, 4, 5, 2, 7]
    ]
# image parameters
img_width, img_height = 80, 80
cwd = os.getcwd()
last_piece_label_path   = cwd + '/src/last_piece_label.txt'
new_color_label_path    = cwd + '/src/new_color_label.txt'
# board_image_folder_path = cwd + '/destination'  # use these paths on Duc's Macbook
# piece_image_folder_path = cwd + '/piece_image'
board_image_folder_path        = '/data/project/lotuschess/rtmp/HLS/image/boardImage'  # use these path on server
piece_image_folder_path = '/data/project/lotuschess/rtmp/HLS/image/pieceImage'
piece_blue_folder_path = cwd + '/src/chess_piece/blue_piece'
piece_red_folder_path = cwd + '/src/chess_piece/red_piece'
run_file_path           = cwd + '/src/gen_piece_image_2.sh'
color_model_path        = cwd + '/models/80_color_model2.h5'
color_weights_path      = cwd + '/models/80_color_weights2.h5'
# db info
user = 'root'  # username on local host
password = 'secret'
db_name = 'lotuschess'
# give authorization
cmd = 'chmod -R 777 ' + run_file_path
os.system(cmd)
sleep_time = 0.01

# load model
color_model = load_model(color_model_path)
color_model.load_weights(color_weights_path)

# initialize
n_board_image_resolved = 0  # total of files that have been resolved
board_image_resolved_path = ''

if os.path.isfile(last_piece_label_path):
    os.remove(last_piece_label_path)

while 1:
    #print('new loop starts here !')
    out_log(2, ' line#: ', str(frame.f_lineno), ' start new transaction')
    # in each loop, read all files in folder
    # execute only new files
    files = sorted(os.listdir(board_image_folder_path))
    n_files = len(files)
    # print('board images: ', files)
    n_new_files = n_files - n_board_image_resolved
    if n_new_files == 0:
        #print('there is no new files, this loop ends here')
        out_log(2, ' line#: ', str(frame.f_lineno), ' no images, end new transaction')
        sleep(sleep_time)
        continue
    time_start = time.time()
    # loop through all files in this transaction
    for cnt in range(n_board_image_resolved, n_files):
        out_log(2, ' line#: ', str(frame.f_lineno), ' before for one image')
        # delete all old piece images
        
        board_image_path = board_image_folder_path + '/' + files[cnt]
        print(board_image_path)
        if board_image_resolved_path and compare_image(board_image_path, board_image_resolved_path)==1:
            print('there is no change in chessboard')
            time_end = time.time()
            print('time_compare:',time_end-time_start)
            continue
        # gán lại ảnh đã xử lý
        #board_image_resolved_path = board_image_path
        delete_images(piece_image_folder_path)
        # crop board image into piece images
        gen_piece_image(run_file_path, board_image_path, piece_image_folder_path)
        piece_files = sorted(os.listdir(piece_image_folder_path))
        # print('number of images, expected 90 to be found: ', len(piece_files))

        # loop through all piece images
        # color recognition, save results in new_color_label_inp
        cnt1 = 0
        new_color_label_inp = gen_2d_list(n_row_inp, n_col_inp)  # chess board input format, storing all colors
        new_piece_label_inp = gen_2d_list(n_row_inp, n_col_inp)
        for file in piece_files:
            file_path = piece_image_folder_path + '/' + file
            if file.find('.jpg') != -1:
                row = int(math.floor(cnt1 / n_col_inp))
                col = int(math.floor(cnt1 - row * n_col_inp))
                # tim manh co hinh tron
                img = cv2.imread(file_path, 0)
                circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,22,
                             param1=100,param2=25,minRadius=20, maxRadius=28)
                if circles is None:
                    #print ('khong phai quan co')
                    new_color_label_inp[row][col] = 0
                else:    
                    color_label = predict(file_path, img_height=img_height, img_width=img_width, model=color_model)
                    # print('row and col: ', row, col)
                    if color_label == 1:
                        new_color_label_inp[row][col] = 2  # black = blue = 2
                        compare_one_folder(file_path, piece_blue_folder_path,new_piece_label_inp)
                    elif color_label == 2:
                        new_color_label_inp[row][col] = 1  # red = 1
                        compare_one_folder(file_path, piece_red_folder_path,new_piece_label_inp)
                    else:
                        new_color_label_inp[row][col] = 0  # blank = 0
            cnt1 += 1
        new_color_label = rotate(new_color_label_inp, 270)
        new_piece_label = rotate(new_piece_label_inp, 270)
        print('new color label: ',new_color_label)
        # time new color label
        time_end = time.time()
        print('time_newcolorlabel:',(time_end-time_start))
        print('new piece label: ', new_piece_label)
        # find verdict
        if not os.path.isfile(last_piece_label_path):  # there is no file last_piece_label
            print('the game has not started yet')
            if new_piece_label != initial_piece_label:
                # verdict: the board is not ready, continue to next image
                print('the board is not ready, please arrange your pieces')
                out_log(2, ' line#: ', str(frame.f_lineno), ' the board is not ready, please arrange your pieces')
                time_end = time.time()
                print('time_boardnotready:',(time_end-time_start))
                board_image_resolved_path = board_image_path
                continue
            else:  # initial labels detected
                # verdict: the board is ready. execute the 1st step: initialization for file and db
                print('the board is ready. waiting for initialization')
                print('initialize last_piece_label and database')
                out_log(2, ' line#: ', str(frame.f_lineno), 'initialize last_piece_label and database')
                last_piece_label = initial_piece_label
                print_list_2d_to_txt(last_piece_label, last_piece_label_path)
                query = gen_insert_query(last_piece_label, 'Start', '')
                out_log(2, ' line#: ', str(frame.f_lineno), ' before exe_query')
                exe_query(user, password, db_name, query)
                out_log(2, ' line#: ', str(frame.f_lineno), ' after exe_query')
                # time after exe_query
                time_end = time.time()
                print('time_afterexe_query:',(time_end-time_start))
                board_image_resolved_path = board_image_path
                continue
        else:
            # file exists
            print('the game has started')
            # read the last label
            last_piece_label = read_txt_to_list_2d(last_piece_label_path)
            n_change, capture, new_move, new_move_2 = gen_new_change(last_piece_label, new_piece_label)

            print('n_change: ', n_change, ' capture: ', capture, ' new move: ', new_move, ' new move 2', new_move_2)
            if n_change == 0 or capture > 1:
                # verdict: no change, or something bad happens, move to next image
                out_log(2, ' line#: ', str(frame.f_lineno), 'no change, or something bad happens, move to next image')
                # time no change, move next image
                time_end = time.time()
                print('time_movenextimage:',(time_end-time_start))
                board_image_resolved_path = board_image_path
                continue
            else:
                # verdict: new move detected
                out_log(2, ' line#: ', str(frame.f_lineno), 'new move detected')
                print_list_2d_to_txt(new_piece_label, last_piece_label_path)
                query = gen_insert_query(new_piece_label, new_move, new_move_2)
                print(query)
                out_log(2, ' line#: ', str(frame.f_lineno), ' before exe_query')
                exe_query(user, password, db_name, query)
                out_log(2, ' line#: ', str(frame.f_lineno), ' after exe_query')
                # time after exe_query
                time_end = time.time()
                print('time_afterexe_query:',(time_end-time_start))
                # gán lại ảnh đã xử lý
                board_image_resolved_path = board_image_path
        out_log(2, ' line#: ', str(frame.f_lineno), ' after for one image')
        time_end = time.time()
        print('time_afterforoneimage:',(time_end-time_start))
    # update index
    n_board_image_resolved = n_files
    # sleep for 0.1 seconds before next loop
    out_log(2, ' line#: ', str(frame.f_lineno), 'this loop ends here !')
    #print('this loop ends here !')
    sleep(sleep_time)




# piece recognition

# red_model_path      = cwd + '/models/80_red_model.h5'
# red_weights_path    = cwd + '/models/80_red_weights.h5'
# green_model_path    = cwd + '/models/80_green_model.h5'
# green_weights_path  = cwd + '/models/80_green_weights.h5'

# red_model = load_model(red_model_path)
# red_model.load_weights(red_weights_path)
# green_model = load_model(green_model_path)
# green_model.load_weights(green_weights_path)

# cnt = 0
# for file in files:
#     file_path = dir_inp + '/' + file
#     if file.find('.jpg') != -1:
#         color_label = predict(file_path, img_height=img_height, img_width=img_width, model=color_model)
#         row_index = int(math.floor(cnt/n_col_inp))
#         col_index = int(math.floor(cnt - row_index*n_col_inp))
#         print('check', cnt, row_index, col_index)
#         if color_label == 1:  # green
#             print(row_index, col_index)
#             piece_label_inp[row_index][col_index] = predict(file_path, img_height=img_height, img_width=img_width,
#                                                             model=green_model) + 1
#         elif color_label == 2:  # red
#             piece_label_inp[row_index][col_index] = predict(file_path, img_height=img_height, img_width=img_width,
#                                                             model=red_model) + 8
#         cnt += 1

# piece_label_out = rotate(piece_label_inp, 270)
# print('output: ', piece_label_out)
