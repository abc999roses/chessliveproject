# this file contains all tools for detecting new move
# from chess_tools import *


def gen_new_piece_label(last_piece_label, new_color_label):
    n_row, n_col = 10, 9
    # first we need to check if there is a move that have been made
    # knowing the side to make the latest move
    capture = 0
    pos_change = []
    for row in range (n_row):
        for col in range(n_col):
            x_old = last_piece_label[row][col]
            x_new = new_color_label[row][col]
            if x_old == 0 and x_new != 0:
                pos_change.append([row, col])
            elif x_old != 0 and x_new == 0:
                pos_change.append([row, col])
            elif last_piece_label[row][col] != 0 and new_color_label[row][col] != 0:
                if (x_old in range(1, 8) and x_new == 2) or (x_old in range(8, 15) and x_new == 1):
                    pos_change.append([row, col])
                    if capture == 0:
                        capture = 1
                    else:
                        print('what ??? more than 1 capture ??? DO IT AGAIN !')
                        return last_piece_label, 0, 0, '', ''

    n_change = len(pos_change)
    print(pos_change)
    if n_change == 0:
        print('no move, do nothing')
        return last_piece_label, 0, 0, '', ''
    if n_change == 1:
        print('1 change ? weird ! DO IT AGAIN !')
        return last_piece_label, 0, 0, '', ''
    if n_change > 2:
        print('more than 2 changes, something wrong here ! DO IT AGAIN !')
        return last_piece_label, 0, 0, '', ''
    if n_change == 2:
        print('FIND ONE MOVE !')

    # print(pos_change)

    if new_color_label[pos_change[0][0]][pos_change[0][1]] == 0:
        old_pos = [pos_change[0][0], pos_change[0][1]]
        new_pos = [pos_change[1][0], pos_change[1][1]]
    else:
        new_pos = [pos_change[0][0], pos_change[0][1]]
        old_pos = [pos_change[1][0], pos_change[1][1]]

    all_col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    all_row = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
    move_str_2 = all_col[old_pos[1]] + all_row[old_pos[0]] + all_col[new_pos[1]] + all_row[new_pos[0]]
    print('move_str_2: ', move_str_2)

    last_piece_label[new_pos[0]][new_pos[1]] = last_piece_label[old_pos[0]][old_pos[1]]
    last_piece_label[old_pos[0]][old_pos[1]] = 0
    # print(last_piece_label[new_pos[0]][new_pos[1]], old_pos, new_pos)

    move_str = gen_move(last_piece_label[new_pos[0]][new_pos[1]], old_pos, new_pos)
    if move_str == '':
        print('failed to detect new move, the move seems to be wrong. DO IT AGAIN !')
        return last_piece_label, 0, 0, '', ''
    else:
        return last_piece_label, 2, capture, move_str, move_str_2


def gen_move(piece_label, old_pos, new_pos):
    res = ''
    pl = piece_label
    # use this convention: http://cotuong.vn/tong-hop-cach-ghi-ban-co-tuong-chuan-viet-nam-va-quoc-te.html
    ps = ['', 'B', 'M', 'P', 'S', 'T', 'Tg', 'X', 'B', 'M', 'P', 'S', 'T', 'Tg', 'X']

    if pl in range(1, 8):
        r1, c1, r2, c2 = 10 - old_pos[0], 9 - old_pos[1], 10 - new_pos[0], 9 - new_pos[1]
    else:
        r1, c1, r2, c2 =  1 + old_pos[0], 1 + old_pos[1],  1 + new_pos[0], 1 + new_pos[1]

    if pl in [2, 9, 4, 11, 5, 12]:  # ma, si, tinh
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + str(c2)
        if r2 < r1:
            res = ps[pl] + str(c1) + '/' + str(c2)
    if pl in [3, 10, 6, 13, 7, 14]:  # phao, tuong, xe
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + str(r2 - r1)
        elif r2 < r1:
            res = ps[pl] + str(c1) + '/' + str(r1 - r2)
        else:  # r2 == r1
            res = ps[pl] + str(c1) + '-' + str(c2)
    if pl in [1, 8]:  # tot
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + '1'
        if r2 == r1:
            res = ps[pl] + str(c1) + '-' + str(c2)

    return res
