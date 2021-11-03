import time
# from typing import List
# import sympy.utilities.iterables
from sympy.utilities.iterables import multiset_permutations
# Lazor project
# 0: Free to place
# 1: Block A
# 2: Block B
# 3: Block C
# -1: Unable to place

time_start = time.time()
def read_file (file_name):
    A_num = 0 # Initialize the # of A, B and C blocks as 0
    B_num = 0
    C_num = 0
    L_list = [] 
    P_list = []
    board_list = []
    i = 0
    j = 0
    file_read_list = []
    with open (file_name, 'r') as file:
        for line in file.readlines():
            file_read_list.append(line)
            i += 1
            if (line == 'GRID START\n'):
                start_loc = i
            if (line[0] == 'A' and len(line) == 4):
                A_list_temp = line.strip().split(' ')
                A_list_temp.remove('A')
                A_num = int(A_list_temp[0])
            if (line[0] == 'B' and len(line) == 4):
                B_list_temp = line.strip().split(' ')
                B_list_temp.remove('B')
                B_num = int(B_list_temp[0])
            if (line[0] == 'C' and len(line) == 4):
                C_list_temp = line.strip().split(' ')
                C_list_temp.remove('C')
                C_num = int(C_list_temp[0])
            if (line[0] == 'L'):
                L_list_temp = line.strip().split(' ')
                L_list_temp.remove('L')
                L_list.append([int(L_list_temp[0]), int(L_list_temp[1]), int(L_list_temp[2]), int(L_list_temp[3])])
            if (line[0] == 'P'):
                P_list_temp = line.strip().split(' ')
                P_list_temp.remove('P')
                P_list.append([int(P_list_temp[0]), int(P_list_temp[1])])
        while (True):
            board_list_temp_row = []
            if (file_read_list[start_loc+j] == 'GRID STOP\n'):
                break
            else:
                board_list_temp = file_read_list[start_loc+j].split()
                for k in range(0, len(board_list_temp)):
                    board_list_temp_row.append(board_list_temp[k])
                board_list.append(board_list_temp_row)
            j += 1
        # Separating the L_list into two list which contains the lazor start points and directions.
        L_point = []
        L_direction = []
        for l in L_list:
            L_point.append([l[0], l[1]])
            L_direction.append([l[2], l[3]])

        # create matrices based on board size
        '''
        The column is the number of positions in a row, and the row is the number of row
        The size of the matrix will be (2 * column + 1) * (2 * row + 1)
        The square shape of each block consists of nine 3 by 3 points in this matrix
        fixed blocks or input blocks or unvailable positions can only be setted in the middle of the 3 by 3 square
        Available position for blocks will be presented by "o"
        The board matrix is the board for a level of this game.
        '''
        board = []
        row = len(board_list)
        column = len(board_list[0])
        for i in range(2 * row + 1):
            if i % 2 == 0:
                board.append(['0'] * (2 * column +1))
            else:
                row_list = []
                for j in range(2 * column + 1):
                    if j % 2 == 0:
                        row_list.append("0")
                    else:
                        row_list.append(board_list[(i - 1) // 2][(j - 1) // 2])
                board.append(row_list)
        # Mark the starting point and target end point lazor with "L" and "P", respectively.
        # for l in L_point:
        #     board[l[1]][l[0]] = "L"
        # for p in P_list:
        #     board[p[1]][p[0]] = "P"
        # Mark the four sides of the fixed block with "1","2","3","4".
        # for i in range(len(board)-1):
        #     for j in range(len(board[i])-1):
        #         if board[i][j] == "A" or board[i][j] == "B" or board[i][j] == "C":
        #             board[i - 1][j] = "1"  # top
        #             board[i + 1][j] = "2"  # bottom
        #             board[i][j - 1] = "3"  # left
        #             board[i][j + 1] = "4"  # right
        # print(A_num, B_num, C_num, L_list, P_list, board_list)
    return A_num, B_num, C_num, L_point, L_direction, P_list, board_list, board

class Block:
    '''
    This class is aimed to implement specific movement and functions of different blocks
    '''

    def __init__(self, position, b_type):
        self.position = position
        self.b_type = b_type

    def add_block(self, board):
        '''
        This function will allow users to move blocks to certain position
        input:
        The matrix of the board and the block type
        output:
        A matrix with specific blocks and each side of the block presenting as "1","2","3,"4".
        '''

        position = self.position
        pos_x = position[0]
        pos_y = position[1]
        if board[pos_y][pos_x] != "x":
            board[pos_y][pos_x] = self.b_type
            if board[pos_y][pos_x] != "C":
                board[pos_y - 1][pos_x] = "1"  # top
                board[pos_y + 1][pos_x] = "2"  # bottom
                board[pos_y][pos_x - 1] = "3"  # left
                board[pos_y][pos_x + 1] = "4"  # right
            else:
                if board[pos_y - 1][pos_x] != "2":
                    board[pos_y - 1][pos_x] = "1"  # top
                if board[pos_y + 1][pos_x] != "1":
                    board[pos_y + 1][pos_x] = "2"  # bottom
                if board[pos_y][pos_x - 1] != "4":
                    board[pos_y][pos_x - 1] = "3"  # left
                if board[pos_y][pos_x + 1] != "3":
                    board[pos_y][pos_x + 1] = "4"  # right
        return board

    def prop(self, lazor_x, lazor_y, face):
        '''
        This function is able to setting different properties of different kind of blocks.
        input:
        The x and y direction of the lazor and the face of lazor contacting with a block.
        output:
        The new x and y direction of lazor
        '''
        
        if self.b_type == "A":
            if face == "1" or face == "2":
                new_la_x1 = lazor_x
                new_la_y1 = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x1 = (-1) * lazor_x
                new_la_y1 = lazor_y
            new_la_x2 = 0
            new_la_y2 = 0
        elif self.b_type == "B":
            new_la_x1 = 0
            new_la_y1 = 0
            new_la_x2 = 0
            new_la_y2 = 0
        elif self.b_type == "C":
            if face == "1" or face == "2":
                new_la_x1 = lazor_x
                new_la_y1 = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x1 = (-1) * lazor_x
                new_la_y1 = lazor_y
            new_la_x2 = lazor_x
            new_la_y2 = lazor_y

        return new_la_x1, new_la_y1, new_la_x2, new_la_y2


class Lazor:
    '''
    This class wraps functions which are related to all the points and directions of lazors. It allows
    the laser beam to parse through the board and take suitable actions of contacting a particular type of block.
    '''

    def __init__(self, start_point, dir_x, dir_y):
        self.start_point = start_point
        self.dir_x = dir_x
        self.dir_y = dir_y

    def pos_chk(self, x, y, x_boundary, y_boundary):
        '''
        To check whether the current position of lazor is still within the grid or not.
        input:
        param x: The x direction of lazor
        param y: The y direction of lazor
        param boundary: The boundary of the board
        output:
        Ture or False
        '''

        return x >= 0 and x < x_boundary and y >= 0 and y < y_boundary

    # def out_block(self, pos_x, pos_y, newpos_x, newpos_y, board):
    #     '''
    #     This function is able to make sure that the lazor won't go through a block on the board.
    #     input:
    #     :param pos_x: The current x coordinate of lazor
    #     :param pos_y: The current y coordinate of lazor
    #     :param newpos_x: The new x coordinate of lazor
    #     :param newpos_y: The new y coordinate of lazor
    #     :param board: The board
    #     output:
    #     The result of whether lazors go through the block or not.
    #     '''
    #     return board[pos_y][pos_x] != "1" and "2" and "3" and "4" 
    #     and board[newpos_y][newpos_x] != "1" and "2" and "3" and "4"

    def check_out_block(self, x, y, board, pos_x, pos_y):
        '''
        This function is aimd to check whether the lazor is reflecting inside the block or not.
        input:
        :param x: The current x direction of lazor
        :param y: The current y direction of lazor
        :param board: The board
        :param pos_x: The current x position
        :param pos_y: The current y position
        output:
        :return: If the lazor is out of the block, return True
                 If the lazor is in the block, return False
        '''
        if board[pos_y][pos_x] == "1":
            result = (y > 0)
        if board[pos_y][pos_x] == "2":
            result = (y < 0)
        if board[pos_y][pos_x] == "3":
            result = (x > 0)
        if board[pos_y][pos_x] == "4":
            result = (x < 0)
        return result

    def lazor_path(self, board):
        '''
        This function is able to record all move position of the lazors and store in different lists.
        The lazor will reflect when it hit block A
        The lazor will be absorbed when it hit block B
        The lazor will reflect and refract when it hit block C
        This fucntion allow lazors to change direction when hit certain type of bolcks and record the new route.
        input:
        :param board: The board matrix
        output:
        :return: Lazor path list containing different route list of lazors.
        '''
        start = self.start_point
        path_list = [[start]]
        dir_x1 = self.dir_x
        dir_y1 = self.dir_y
        # The path_list only has one route at the beginning. It increases as lazor hitting block C which means
        # the reflection happen. Then each lazor route starts their own move loop.
        for p in path_list:
            while True:
                if p[-1] != "end":
                    # When a lazor hit the "C" block or move out of the board, the path list will be ended with "end"
                    curr_pos = p[-1]
                    if len(p) >= 2:
                        dir_x1 = p[-1][0] - p[-2][0]
                        dir_y1 = p[-1][1] - p[-2][1]
                    new_x = curr_pos[0] + dir_x1
                    new_y = curr_pos[1] + dir_y1
                    if self.pos_chk(new_x, new_y, len(board[0]), len(board)):
                        if board[curr_pos[1]][curr_pos[0]] == "0" or board[curr_pos[1]][curr_pos[0]] == "L" \
                                or board[curr_pos[1]][curr_pos[0]] == "P":
                            # if the current position of the lazor is not on the side of a block.
                            # the lazor can be longer for one step.
                            p.append([new_x, new_y])
                        else:
                            if self.check_out_block(dir_x1, dir_y1, board, curr_pos[0], curr_pos[1]):
                                block_type = 0
                                block_position = 0
                                if board[curr_pos[1]][curr_pos[0]] == "1":
                                    block_position = [curr_pos[0], curr_pos[1] + 1]
                                    block_type = board[block_position[1]][block_position[0]]
                                elif board[curr_pos[1]][curr_pos[0]] == "2":
                                    block_position = [curr_pos[0], curr_pos[1] - 1]
                                    block_type = board[block_position[1]][block_position[0]]
                                elif board[curr_pos[1]][curr_pos[0]] == "3":
                                    block_position = [curr_pos[0] + 1, curr_pos[1]]
                                    block_type = board[block_position[1]][block_position[0]]
                                elif board[curr_pos[1]][curr_pos[0]] == "4":
                                    block_position = [curr_pos[0] - 1, curr_pos[1]]
                                    block_type = board[block_position[1]][block_position[0]]
                                # Using the Block class to figure out the new direction of the lazor after striking.
                                new_dir_x, new_dir_y, pre_dir_x, pre_dir_y = Block(block_position, block_type).prop\
                                (dir_x1, dir_y1, board[curr_pos[1]][curr_pos[0]])
                                dir_x1 = new_dir_x
                                dir_y1 = new_dir_y
                                dir_x2 = pre_dir_x
                                dir_y2 = pre_dir_y
                                if dir_x1 != 0 and dir_y1 != 0:
                                    # The reflection lazor will go with the new direction.
                                    new_x1 = curr_pos[0] + dir_x1
                                    new_y1 = curr_pos[1] + dir_y1
                                    p.append([new_x1, new_y1])
                                else:
                                    p.append("end")
                                if dir_x2 != 0 and dir_y2 != 0:
                                    # After go through the "C" block, the refraction lazor path will be added to
                                    # a new path list in path_list.
                                    path_list.append([])
                                    path_list[-1].append([curr_pos[0], curr_pos[1]])
                                    # The refraction lazor will go with the previous direction.
                                    path_list[-1].append([new_x, new_y])
                            else:
                                # If lazors hit blocks from the inside of the block, the reflection won't happen
                                # Just go straight
                                p.append([new_x, new_y])
                    else:
                        # Lazors will stop when it reaching the boundary of the board.
                        p.append("end")
                else:
                    break
        return path_list


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


def possible_path(block_list, position_list, board):
    board_possible = []
    lazor_possible = []
    for i in range(len(block_list)):
        board1 = board.copy()
        for j in range(len(block_list[i])):
            Block(position_list[i][j], block_list[i][j]).add_block(board1)
        board_possible.append(board1)
        for l in range(len(start)):
            lazor_possible.append((Lazor(start[l], direction[l][0], direction[l][1]).lazor_path(board_possible[i])))
    return lazor_possible

test = 'mad_7.bff'
read_file(test)
start = read_file(test)[3]
direction = read_file(test)[4]

board1 = read_file(test)[7]
# print(read_file(test)[0])
# print(direction)
# print(start)
# Block([3, 1], "A").add_block(board1)
# Block([5, 3], "A").add_block(board1)
# Block([1, 5], "A").add_block(board1)
# Block([1, 3], "B").add_block(board1)
print(board1)
for i in range(len(start)):
    print(Lazor(start[i],direction[i][0], direction[i][1]).lazor_path(board1))
# read_file('tiny_5.bff')
# print(read_file('dark_1.bff'))

board = read_file(test)[7]
block_list, position_list = possible_boards(read_file(test)[6], read_file(test)[0], read_file(test)[1],
                                            read_file(test)[2])
possible = possible_path(block_list, position_list, board=read_file(test)[7])
print(possible)
time_end = time.time()
print(time_start - time_end)




