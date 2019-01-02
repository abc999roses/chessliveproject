# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:54:02 2018

@author: CHU TIEN THANH
"""

# this file contains all tools for detecting new move
# from chess_tools import *


def gen_new_change(last_piece_label, new_piece_label):
    n_row, n_col = 10, 9
    # first we need to check if there is a move that have been made
    # knowing the side to make the latest move
    capture = 0
    pos_change = []
    for row in range (n_row):
        for col in range(n_col):
            x_old = last_piece_label[row][col]
            x_new = new_piece_label[row][col]
            if x_old == 0 and x_new != 0:
                pos_change.append([row, col])
            elif x_old != 0 and x_new == 0:
                pos_change.append([row, col])
            elif x_old != 0 and x_new != 0 and x_old != x_new:
                if (x_old in range(1, 8) and x_new in range(8, 15) or (x_old in range(8, 15) and x_new in range(1,8))):
                    pos_change.append([row, col])
                    if capture == 0:
                        capture = 1
                    else:
                        print('what ??? more than 1 capture ??? DO IT AGAIN !')
                        return 0, 0, '', ''
                elif (x_old in range(1, 8) and x_new in range(1, 8) or (x_old in range(8, 15) and x_new in range(8,15))): 
                    print('Wrong move')
                    print(row , col)
                    print(x_old, x_new)
                    return 0,0,'',''
            
    n_change = len(pos_change)
    print(pos_change)
    if n_change == 0:
        print('no move, do nothing')
        return 0, 0, '', ''
    if n_change == 1:
        print('1 change ? weird ! DO IT AGAIN !')
        return 0, 0, '', ''
    if n_change > 2:
        print('more than 2 changes, something wrong here ! DO IT AGAIN !')
        return 0, 0, '', ''
    if n_change == 2:
        print('FIND ONE MOVE !')
    x1 =  last_piece_label[pos_change[0][0]][pos_change[0][1]]
    x2 =  new_piece_label[pos_change[1][0]][pos_change[1][1]]
    print(x1, x2)      
    if (x1 in range(1, 8) and x2 in range(8, 15)) or (x1 in range(8, 15) and x2 in range(1, 8)):
        print('Wrong move, detect nham mau')
        return 0, 0, '', ''
    # print(pos_change)
    if new_piece_label[pos_change[0][0]][pos_change[0][1]] == 0:
        if new_piece_label[pos_change[1][0]][pos_change[1][1]] == 0:
            print('Wrong move, two piece lost')
            print(pos_change[0][0],pos_change[0][1],pos_change[1][0],pos_change[1][1])
            return 0, 0, '', ''
        else:
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
    
    move_str = gen_move(last_piece_label[new_pos[0]][new_pos[1]], old_pos, new_pos, last_piece_label)
    # check cản mã, cản xe, ngòi pháo.
    # Todo mã
    # Todo xe
    # Todo pháo
    if move_str == '':
        print('failed to detect new move, the move seems to be wrong. DO IT AGAIN !')
        return 0, 0, '', ''
    else:
        return 2, capture, move_str, move_str_2


def gen_move(piece_label, old_pos, new_pos, last_piece_label):
    res = ''
    pl = piece_label
    # use this convention: http://cotuong.vn/tong-hop-cach-ghi-ban-co-tuong-chuan-viet-nam-va-quoc-te.html
    ps = ['', 'B', 'M', 'P', 'S', 'T', 'Tg', 'X', 'B', 'M', 'P', 'S', 'T', 'Tg', 'X']

    if pl in range(1, 8):
        r1, c1, r2, c2 = 10 - old_pos[0], 9 - old_pos[1], 10 - new_pos[0], 9 - new_pos[1]
    else:
        r1, c1, r2, c2 =  1 + old_pos[0], 1 + old_pos[1],  1 + new_pos[0], 1 + new_pos[1]
    
    if pl in [2, 9, 4, 11, 5, 12]:  # ma, si, tinh
        if pl in [4, 11]:
            if (((r2,c2) not in [(r1+1, c1+1), (r1+1, c1-1), (r1-1, c1+1), (r1-1, c1-1)])
            or (r2>3) or (c2 not in [4,5,6])):
                print('sy di sai')
                return ''
        if pl in [5, 12]:
            print(last_piece_label[old_pos[0]-3][old_pos[1]])
            if ((r2,c2) not in [(r1+2, c1+2), (r1+2, c1-2), (r1-2, c1+2), (r1-2, c1-2)]) or (r2>5):
                #print(str(r2)+'/'+str(c2)+'/'+str(r1)+'/'+str(c1))
                print('tinh di sai')
                return ''
        if pl in [2, 9]:
            if (pl == 2):
                 r1, c1, r2, c2 = 10 - r1, 9 - c1, 10 - r2, 9 - c2
            else:
                r1, c1, r2, c2 =  r1 - 1, c1 - 1,  r2 - 1, c2 - 1
            # check can ma
            if((r1 >=1) and (r1<=9) and (c1>=1) and (c1<=8)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2)) or 
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return ''
            elif((r1==0) and (c1>=1) and (c1 <=8)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2)) or 
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return ''
            elif((r1==0) and (c1==9)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return ''
            elif((r1>=1) and (r1<=9) and (c1 ==0)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2))) :
                    print('ma bi can')
                    return ''
            elif((r1>=1) and (r1<=9) and (c1 ==9)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return ''
            elif((r1==10) and (c1==0)):
                if (((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2))):
                    print('ma bi can')
                    return ''
            elif((r1==10)and (c1>=1) and (c1<=8)):
                if (((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2)) or 
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return
            elif((r1==10) and (c1 ==9)):
                if (((last_piece_label[r1-1][c1] != 0) and (r2 == r1-2)) or
                    ((last_piece_label[r1][c1-1] != 0) and (c2 == c1-2))):
                    print('ma bi can')
                    return ''
            elif((r1==0) and (c1==0)):
                if (((last_piece_label[r1+1][c1] != 0) and (r2 == r1+2)) or
                    ((last_piece_label[r1][c1+1] != 0) and (c2 == c1+2))):
                    print('ma bi can')
                    return ''
            
            if((r2,c2) not in [(r1+1, c1+2), (r1+1, c1-2), (r1+2, c1+1), (r1+2, c1-1),
                (r1-1, c1+2), (r1-1, c1-2), (r1-2, c1+1), (r1-2, c1-1)]):
                print('ma di sai')
                return ''
        if pl in range(1, 8):
            r1, c1, r2, c2 = 10 - old_pos[0], 9 - old_pos[1], 10 - new_pos[0], 9 - new_pos[1]
        else:
            r1, c1, r2, c2 =  1 + old_pos[0], 1 + old_pos[1],  1 + new_pos[0], 1 + new_pos[1]
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + str(c2)
        if r2 < r1:
            res = ps[pl] + str(c1) + '/' + str(c2)
    if pl in [3, 10, 6, 13, 7, 14]:  # phao, tuong, xe
        if pl in [6, 13]:
            if(((r2,c2) not in [(r1, c1+1), (r1, c1-1), (r1+1, c1), (r1-1, c1)]) or (r2 >3) or (c2 not in [4,5,6])):
                print('tuong di sai')
                return ''
        if pl in [7,14]:
            if ((r2 != r1) and (c2 != c1)):
                print('xe di sai')
                return ''
        
            #check xe bi can
            if (pl == 7):
                 r1, c1, r2, c2 = 10 - r1, 9 - c1, 10 - r2, 9 - c2
            else:
                r1, c1, r2, c2 =  r1 - 1, c1 - 1,  r2 - 1, c2 - 1
            if (r2 == r1):
                if (c2 > c1):
                    for c in range(c1,c2):
                        if last_piece_label[r1][c] != 0: 
                            print('xe bi can')
                            return ''
                else :
                    for c in range(c2,c1):
                        if last_piece_label[r1][c] != 0: 
                            print('xe bi can')
                            return ''
            else :
                if (r2 > r1):
                    for r in range(r1,r2):
                        if last_piece_label[r][c1] != 0: 
                            print('xe bi can')
                            return ''
                else :
                    for r in range(r2,r1):
                        if last_piece_label[r][c1] != 0: 
                            print('xe bi can')
                            return ''
                            
        if pl in [3,10]:
            if ((r2 != r1) and (c2 != c1)):
                print('phao di sai')
                return ''
            
            if (pl == 3):
                r1, c1, r2, c2 = 10 - r1, 9 - c1, 10 - r2, 9 - c2
            else :
                r1, c1, r2, c2 =  r1 - 1, c1 - 1,  r2 - 1, c2 - 1
            if (r2 == r1):
                if (c2 > c1):
                    #check can phao
                    if(last_piece_label[r2][c2] == 0):
                        for c in range(c1,c2):
                            if last_piece_label[r1][c] != 0: 
                                print('phao bi can')
                                return ''
                    #check ngoi phao
                    else:
                        count = 0
                        for c in range(c1,c2):
                            if last_piece_label[r1][c] != 0:
                                count = count + 1
                        if (count == 0):
                            print('phao khong co ngoi')
                            return ''
                        if (count > 1):
                            print('phao nhay coc')
                            return ''
                                
                        
                else :
                    if(last_piece_label[r2][c2] == 0):
                        for c in range(c2,c1):
                            if last_piece_label[r1][c] != 0: 
                                print('phao bi can')
                                return ''
                    #check ngoi phao
                    else:
                        count = 0
                        for c in range(c2,c1):
                            if last_piece_label[r1][c] != 0:
                                count = count + 1
                        if (count == 0):
                            print('phao khong co ngoi')
                            return ''
                        if (count > 1):
                            print('phao nhay coc')
                            return ''
            # c2 == c1
            else :
                if (r2 > r1):
                    #check can phao
                    if(last_piece_label[r2][c2] == 0):
                        for r in range(r1,r2):
                            if last_piece_label[r][c1] != 0: 
                                print('phao bi can')
                                return ''
                    #check ngoi phao
                    else:
                        count = 0
                        for r in range(r1,r2):
                            if last_piece_label[r][c1] != 0:
                                count = count + 1
                        if (count == 0):
                            print('phao khong co ngoi')
                            return ''
                        if (count > 1):
                            print('phao nhay coc')
                            return ''
                                
                        
                else :
                    # check can phao
                    if(last_piece_label[r2][c2] == 0):
                        for r in range(r2,r1):
                            if last_piece_label[r][c1] != 0: 
                                print('phao bi can')
                                return ''
                    #check ngoi phao
                    else:
                        count = 0
                        for r in range(r2,r1):
                            if last_piece_label[r][c1] != 0:
                                count = count + 1
                        if (count == 0):
                            print('phao khong co ngoi')
                            return ''
                        if (count > 1):
                            print('phao nhay coc')
                            return ''
                                
                
        if pl in range(1, 8):
            r1, c1, r2, c2 = 10 - old_pos[0], 9 - old_pos[1], 10 - new_pos[0], 9 - new_pos[1]
        else:
            r1, c1, r2, c2 =  1 + old_pos[0], 1 + old_pos[1],  1 + new_pos[0], 1 + new_pos[1]            
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + str(r2 - r1)
        elif r2 < r1:
            res = ps[pl] + str(c1) + '/' + str(r1 - r2)
        else:  # r2 == r1
            res = ps[pl] + str(c1) + '-' + str(c2)
    if pl in [1, 8]:  # tot
        if (r1 < 5):
            if r2 != (r1+1):
                print ('tot di sai')
                return ''
        else:
            if (r2, c2) not in [(r1,c1+1), (r1, c1-1), (r1+1, c1)]:
                print ('tot di sai')
        if r2 > r1:
            res = ps[pl] + str(c1) + '.' + '1'
        if r2 == r1:
            res = ps[pl] + str(c1) + '-' + str(c2)

    return res
