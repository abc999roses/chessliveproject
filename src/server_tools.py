# this file contains all tools for running run_server.py
import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
import MySQLdb
import json
from skimage.measure import compare_ssim
import cv2


def gen_2d_list(n_row, n_col):
    return [[0] * n_col for _ in range(n_row)]


def print_list_2d_to_txt(list_2d, file_name):
    n_row = len(list_2d)
    n_col = len(list_2d[0])
    f = open(file_name, 'w+')
    for row in range(0, n_row):
        for col in range(0, n_col):
            f.write(str(list_2d[row][col]) + ' ')
    f.close()


def read_txt_to_list_2d(file_name):
    n_row, n_col = 10, 9
    list_2d = [[0] * n_col for _ in range(n_row)]
    f = open(file_name, 'r')
    content = f.readline().split()
    f.close()
    cnt = 0
    for row in range(0, n_row):
        for col in range(0, n_col):
            list_2d[row][col] = int(content[cnt])
            cnt += 1
    return list_2d


def predict(file, img_width, img_height, model):
    x = load_img(file, target_size=(img_width,img_height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = model.predict(x)
    result = array[0]
    answer = np.argmax(result)
    return answer


# rotate a 2D list 90 degree counterclockwise
def rotate90(inp_board):
    n_row = len(inp_board)
    n_col = len(inp_board[0])
    res = [[0]*n_row for _ in range(n_col)]  # create separate lists
    for cnt in range(n_col):
        for cnt1 in range(n_row):
            # print(inp_board[n_row - cnt1 - 1][cnt])
            res[cnt][cnt1] = inp_board[n_row - cnt1 - 1][cnt]
            # print(res)
    return res


def rotate(inp_board, angle):
    if angle == 0:
        return inp_board
    elif angle == 90:
        return rotate90(inp_board)
    elif angle == 180:
        return rotate90(rotate90(inp_board))
    elif angle == 270:
        return rotate90(rotate90(rotate90(inp_board)))
    else:
        print('stupid angle')
        return -1


def delete_images(folder_path):
    print('folder_path: ', folder_path)
    files = sorted(os.listdir(folder_path))
    print('number of file: ', len(files))
    for file in files:
        file_path = folder_path + '/' + file
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)  # this is to remove subdirectories too
        except Exception as e:
            print(e)


def gen_insert_query(new_piece_label, new_move, new_move_2):
    n_row, n_col = 10, 9
    piece_names = [
        '',
        'do-tot',
        'do-ma',
        'do-phao',
        'do-si',
        'do-tinh',
        'do-tuong',
        'do-xe',
        'den-tot',
        'den-ma',
        'den-phao',
        'den-si',
        'den-tinh',
        'den-tuong',
        'den-xe',
    ]

    # save board status as a dictionary for printing out
    new_piece_label_dict = {}
    for row in range(n_row):
        for col in range(n_col):
            new_piece_label_dict[str(row + 1) + '-' + str(col + 1)] = piece_names[new_piece_label[row][col]]

    new_piece_label_dump = json.dumps(new_piece_label_dict)
    print(new_piece_label_dump)

    query = "INSERT INTO chess_boards(game_id, step, state, move) VALUES (1, '%s', '%s', '%s')" % (new_move, new_piece_label_dump, new_move_2)
    print(query)
    return query


def exe_query(user, password, db_name, query):
    # parameters
    # connect to an existing db on local
    db = MySQLdb.connect('localhost', user, password, db_name)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute the insert query
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


def gen_piece_image(run_file_path, board_image_path, piece_image_folder_path):
    cmd = run_file_path + ' ' + board_image_path + ' ' + piece_image_folder_path
    os.system(cmd)


def execute_image(image_name):


    return 0
	
def compare_image(img1, img2):
    
    imageA = cv2.imread(img1, 0)
    imageB = cv2.imread(img2, 0)
    
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(imageA, imageB, win_size = 51, full = True)
    # diff = (diff * 255).astype("uint8")
    print(img1 +'/'+ img2)
    #print("SSIM: {}".format(score))
    # 0.93 la nguong bat dau giong nhau
    if (score>0.93):
        return 1
    else : 
        print("SSIM: {}".format(score))
        return 0
    
def compare(file1, des2):
    #MIN_MATCH_COUNT = 10
    
    img1 = cv2.imread(file1,0) # queryImage
    #img2 = cv2.imread(file2,0) # trainImage
    
    # Initiate SIFT detector
    #sift = cv2.SIFT()
    sift = cv2.xfeatures2d.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    #kp2, des2 = sift.detectAndCompute(img2,None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1, des2, k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    return len(good)
def compare_one_folder(file2, test_path1,list2d_piece_label):
    file1s = sorted(os.listdir(test_path1))
    sift = cv2.xfeatures2d.SIFT_create()
    if file2.find('jpg') != -1:
            img2 = cv2.imread(file2, 0) # trainImage
            kp2, des = sift.detectAndCompute(img2,None)
            max = 0
            result = 0
            label = 0
            for file1 in file1s:
                if file1.find('.jpg') != -1:  # filter all image files
                    #result = compare(test_path + '/'+ file, file2)
                    img1 = test_path1 +'/'+file1
                    result = compare(img1, des)
                    if max <= result:
                        max = result
                        label = int(file1.split('.')[0])
            i = int(file2[-6])
            j = int(file2[-5])
            list2d_piece_label[i][j] = label

def compare_folder(test_path2, test_path1, list2d_piece_label):
    file2s = sorted(os.listdir(test_path2))
    file1s = sorted(os.listdir(test_path1))
    sift = cv2.xfeatures2d.SIFT_create()
    for file2 in file2s:
        if file2.find('jpg') != -1:
            img2 = cv2.imread(test_path2 + '/'+ file2, 0) # trainImage
            kp2, des = sift.detectAndCompute(img2,None)
            max = 0
            result = 0
            label = 0
            for file1 in file1s:
                if file1.find('.jpg') != -1:  # filter all image files
                    #result = compare(test_path + '/'+ file, file2)
                    img1 = test_path1 +'/'+file1
                    result = compare(img1, des)
                    if max <= result:
                        max = result
                        label = int(file1.split('.')[0])
            i = int(file2[-6])
            j = int(file2[-5])
            list2d_piece_label[i][j] = label