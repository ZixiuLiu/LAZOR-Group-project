# Lazor project
# 0: Free to place
# 1: Block A
# 2: Block B
# 3: Block C
# -1: Unable to place

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
                board.append([0] * (2 * column +1))
            else:
                row_list = []
                for j in range(2 * column + 1):
                    if j % 2 == 0:
                        row_list.append("0")
                    else:
                        row_list.append(board_list[(i - 1) // 2][(j - 1) // 2])
                board.append(row_list)
        # Mark the starting point and target end point lazor with "L" and "P", respectively.
        for l in L_point:
            board[l[1]][l[0]] = "L"
        for p in P_list:
            board[p[1]][p[0]] = "P"
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
            board[pos_y - 1][pos_x] = "1"  # top
            board[pos_y + 1][pos_x] = "2"  # bottom
            board[pos_y][pos_x - 1] = "3"  # left
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
        new_la_x = 0
        new_la_y = 0
        if self.b_type == "A":
            if face == "1" or face == "2":
                new_la_x = lazor_x
                new_la_y = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x = (-1) * lazor_x
                new_la_y = lazor_y
        elif self.b_type == "B":
            new_la_x = 0
            new_la_y = 0
        elif self.b_type == "C":
            if face == "1" or face == "2":
                new_la_x = lazor_x
                new_la_y = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x = (-1) * lazor_x
                new_la_y = lazor_y
        return new_la_x, new_la_y


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
    #     return board[pos_y][pos_x] != "1" and "2" and "3" and "4" \
    # and board[newpos_y][newpos_x] != "1" and "2" and "3" and "4"

    def lazor_path(self, board):
        start = self.start_point
        path = [start]
        dir_x = self.dir_x
        dir_y = self.dir_x
        dir_x1 = dir_x
        dir_y1 = dir_y
        while True:
            curr_pos = path[-1]
            new_x = curr_pos[0] + dir_x1
            new_y = curr_pos[1] + dir_y1
            if self.pos_chk(new_x, new_y, len(board[0]), len(board)):
                if board[new_y][new_x] != "P":
                    if board[curr_pos[1]][curr_pos[0]] == "0" or board[curr_pos[1]][curr_pos[0]] == "L" \
                            or board[curr_pos[1]][curr_pos[0]] == 0:
                        # if the current position of the lazor is not on the side of a block.
                        # the lazor can be longer for one step.
                        path.append([new_x, new_y])
                    else:
                        block_type = 0
                        block_position = 0
                        # if self.out_block(curr_pos[0], curr_pos[1], new_x, new_y, board):
                        if board[curr_pos[1]][curr_pos[0]] == "1":
                            block_position = [curr_pos[0], curr_pos[1] + 1]
                            block_type = board[curr_pos[1] + 1][curr_pos[0]]
                        elif board[curr_pos[1]][curr_pos[0]] == "2":
                            block_position = [curr_pos[0], curr_pos[1] - 1]
                            block_type = board[curr_pos[1] - 1][curr_pos[0]]
                        elif board[curr_pos[1]][curr_pos[0]] == "3":
                            block_position = [curr_pos[0] + 1, curr_pos[1]]
                            block_type = board[curr_pos[1]][curr_pos[0] + 1]
                        elif board[curr_pos[1]][curr_pos[0]] == "4":
                            block_position = [curr_pos[0] - 1, curr_pos[1]]
                            block_type = board[curr_pos[1]][curr_pos[0] - 1]
                        # else:
                        #     # If the lazor will go through a block, then the lazor will stop.
                        #     break
                        # Using the Block class to figure out the new direction of the lazor after striking.
                        new_dir_x, new_dir_y = Block(block_position, block_type).prop(dir_x1, dir_y1, board[curr_pos[1]][curr_pos[0]])
                        dir_x1 = new_dir_x
                        dir_y1 = new_dir_y
                        if dir_x1 != 0 and dir_y1 != 0:
                            new_x = curr_pos[0] + dir_x1
                            new_y = curr_pos[1] + dir_y1
                            path.append([new_x, new_y])
                        else:
                            break
                else:
                    path.append([new_x, new_y])
                    # Lazors will stop when it reaching the target positions.
                    break
            else:
                # Lazors will stop when it reaching the boundary of the board.
                break

        return path


read_file('yarn_5.bff')
start = read_file('yarn_5.bff')[3]
direction = read_file('yarn_5.bff')[4]
board1 = read_file('yarn_5.bff')[7]

# print(direction)
# print(start)
Block([7,3], "B").add_block(board1)
print(board1)
print(Lazor(start[0], direction[0][0], direction[0][1]).lazor_path(board1))
# read_file('tiny_5.bff')
# print(read_file('dark_1.bff'))