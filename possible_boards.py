import copy
import time
from typing import List
import sympy.utilities.iterables
from sympy.utilities.iterables import multiset_permutations
start = time.time()

def possible_boards(board_list, A_num, B_num, C_num):
    moved_block = []  # get a list of ABC blocks, eg: ['A', 'B', 'C']
    for i in range(A_num):
        moved_block.append('A')
    for i in range(B_num):
        moved_block.append('B')
    for i in range(C_num):
        moved_block.append('C')

    long_block_list = []  # eg: ['o', 'o', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x', 'o', 'x', 'o']
    for i in board_list:
        for j in i:
            long_block_list.append(j)

    fixed_list = []
    fixed_position = []
    o_list = []

    for i in range(len(long_block_list)):
        if long_block_list[i] == 'x':
            fixed_list.append('x')
            fixed_position.append(i)
        elif long_block_list[i] == 'A':
            fixed_list.append('A')
            fixed_position.append(i)
        elif long_block_list[i] == 'B':
            fixed_list.append('B')
            fixed_position.append(i)
        elif long_block_list[i] == 'C':
            fixed_list.append('C')
            fixed_position.append(i)
        else:
            o_list.append(long_block_list[i])

    for i in moved_block:
        o_list.pop()
    for i in moved_block:
        o_list.append(i)

    moved_block_list = []    # the list with all possible arrangements of moved blocks
    for i in multiset_permutations(o_list):
        moved_block_list.append(i)



    if fixed_list is not None:
        for i in range(len(fixed_list)):
            for li in moved_block_list:
                li.insert(fixed_position[i], fixed_list[i])

    # get 'moved_block_list', but every board was a list
    # every list in moved_block_list need to return a coordinate
    # change the list into coordinate

    row = len(board_list)
    column = len(board_list[0])

    # format_list = []
    # for a_li in moved_block_list:
    #     new_li = []
    #     for i in range(0, len(li), column):
    #         new_li.append(li[i: i + 3])
    #     format_list.append(new_li)
    # print(format_list)
    # get a format_list, format like board_list
    # below is to generate coordinate list
    # for one_li in format_list:
    all_block_possible_list = []
    all_position_possible_list = []
    for ali in moved_block_list:
        b_l = []
        p_l = []
        for i in range(len(ali)):
            if ali[i] == 'A':
                b_l.append(ali[i])
                p_l.append(((i % column) * 2 + 1, (i // column) * 2 + 1))
            if ali[i] == 'B':
                b_l.append(ali[i])
                p_l.append(((i % column) * 2 + 1, (i // column) * 2 + 1))
            if ali[i] == 'C':
                b_l.append(ali[i])
                p_l.append(((i % column) * 2 + 1, (i // column) * 2 + 1))
        all_block_possible_list.append(b_l)
        all_position_possible_list.append(p_l)



    return all_block_possible_list, all_position_possible_list



if __name__ == '__main__':
    board = [['o','o','o'], ['o','o','x'],['o', 'B','o']]
    print(possible_boards(board, 1, 1, 1)[0])
    print(possible_boards(board, 1, 1, 1)[1])    
    end = time.time()
    print(end - start)



