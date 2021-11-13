import time
import copy
from sympy.utilities.iterables import multiset_permutations

time_start = time.time()
def read_file (file_name):
    '''
    This function is for read and extract the information in .bff file.

    **Parameters**
        
        file_name: *file*
            The .bff file
    
    **Output**

         A_num, B_num, C_num: *int*
            The number of blocks of A, B and C
        L_point, L_direction: *list*
            The coordinate and directions of starts
        P_list: *list*
            The coordinate of destinations
        board_list: *list*
            The board condition include free positions, occupied positions and fixed blocks
        board: *list*
            The extended board matrix. i.e. extended every single "o" or "x" or fixed block to a 3x3 matrix
            e.g. "0" "0" "0"
                 "0" "o" "0"
                 "0" "0" "0"
    '''
    # Initialize the # of A, B and C blocks as 0
    A_num = 0 
    B_num = 0
    C_num = 0
    # Initialize the starting and destiation list as empty 
    L_list = [] 
    P_list = []
    board_list = []
    # Initialize the loop index (i and j)
    i = 0
    j = 0
    # Initialize the list for storing each line in .bff file
    file_read_list = []
    # Start to open file and read lines
    with open (file_name, 'r') as file:
        for line in file.readlines():
            # Store each line as a list
            file_read_list.append(line)
            # Locate the 'GRID START' line and store the location as start_loc
            # The board abstract process will start later out side this loop
            i += 1
            if (line == 'GRID START\n'):
                start_loc = i
            # If the line starts with a 'A', extract the number behind it in this line
            # The reason why we use len(line) == 4 is because when the grid starts with A, the grid will be
            # recognized as the number of A and lead to error
            if (line[0] == 'A' and len(line) == 4):
                # Strip and split the line
                A_list_temp = line.strip().split(' ')
                # Remove the string 'A' in the line and leaves only the number(string format)
                A_list_temp.remove('A')
                # Append the number(string format) as a int into the output variable
                A_num = int(A_list_temp[0])
            # If the line starts with a 'B', extract the number behind it in this line
            if (line[0] == 'B' and len(line) == 4):
                B_list_temp = line.strip().split(' ')
                B_list_temp.remove('B')
                B_num = int(B_list_temp[0])
            # If the line starts with a 'C', extract the number behind it in this line
            if (line[0] == 'C' and len(line) == 4):
                C_list_temp = line.strip().split(' ')
                C_list_temp.remove('C')
                C_num = int(C_list_temp[0])
            # If the line starts with a 'L', extract the number behind it in this line
            if (line[0] == 'L'):
                L_list_temp = line.strip().split(' ')
                L_list_temp.remove('L')
                # The four value includes two coordinates and two ditrctions
                L_list.append([int(L_list_temp[0]), int(L_list_temp[1]), int(L_list_temp[2]), int(L_list_temp[3])])
            # If the line starts with a 'P', extract the number behind it in this line
            if (line[0] == 'P'):
                P_list_temp = line.strip().split(' ')
                P_list_temp.remove('P')
                P_list.append([int(P_list_temp[0]), int(P_list_temp[1])])
        # This loop is for extract the board condition according to the location of 'GRID START'
        while (True):
            board_list_temp_row = []
            # If the grid ends, jump out of this infinity loop
            if (file_read_list[start_loc+j] == 'GRID STOP\n'):
                break
            # If the line is between 'grid start' and 'grid stop', store the board condition
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
    return A_num, B_num, C_num, L_point, L_direction, P_list, board_list, board

class Block:
    '''
    This class create a wrapper for functions which implement specific movement and functions of different blocks

    **Parameters**

        list and string: *position* and *b_type*
            The position and type of blocks that have to be wrapped
    '''
    def __init__(self, position, b_type):
        self.position = position
        self.b_type = b_type

    def add_block(self, board):
        '''
        This function will allow users to move blocks to certain position

        **Parameters**

            board: *string*
                The matrix of the board and the block type

        **Returns**

            *list*: A matrix with specific blocks and each side of the block presenting as "1","2","3,"4".
        '''

        position = self.position
        pos_x = position[0]
        pos_y = position[1]
        if board[pos_y][pos_x] != "x":
            board[pos_y][pos_x] = self.b_type
            if board[pos_y][pos_x] != "C":
                # If the block is C
                # make sure that the four face of the block is exactly "1", "2", "3" and "4"
                # So that the lazor won't recognize a wrong face of a block for further function of lazor
                board[pos_y - 1][pos_x] = "1"  # top
                board[pos_y + 1][pos_x] = "2"  # bottom
                board[pos_y][pos_x - 1] = "3"  # left
                board[pos_y][pos_x + 1] = "4"  # right
            else:
                # if the block is not C
                # The face number should keep unchanged if the block is put next to a existing block
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

        **Parameters**

            lazor_x: *int*
                The x direction of the lazor. i.e. 1 or -1
            lazor_y: *int*
                The y direction of the lazor. i.e. 1 or -1
            face: *int*
                The face of lazor contacting with a block. i.e. 1 or 2 or 3 or 4

        **Returns**

            *int*: The new x and y direction of lazor and the previous x and y direction of lazor.
        '''
        if self.b_type == "A":
            # A block have the property of reflection
            if face == "1" or face == "2":
                new_la_x1 = lazor_x
                new_la_y1 = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x1 = (-1) * lazor_x
                new_la_y1 = lazor_y
            # direction change after striking
            # the original direction disappear
            new_la_x2 = 0
            new_la_y2 = 0
        elif self.b_type == "B":
            # B block have the property of absorption
            # new direction and original direction both become 0
            new_la_x1 = 0
            new_la_y1 = 0
            new_la_x2 = 0
            new_la_y2 = 0
        elif self.b_type == "C":
            # A block have the property of refraction
            # direction change after striking
            if face == "1" or face == "2":
                new_la_x1 = lazor_x
                new_la_y1 = (-1) * lazor_y
            elif face == "3" or face == "4":
                new_la_x1 = (-1) * lazor_x
                new_la_y1 = lazor_y
            # the original direction keeps
            new_la_x2 = lazor_x
            new_la_y2 = lazor_y

        return new_la_x1, new_la_y1, new_la_x2, new_la_y2


class Lazor:
    '''
    This class create a wrapper for functions which implement lazor route and specific end condition for lazor

    **Parameters**

        list : *start_point*
            The coordinate of the lazor start point.
        int : *dir_x*
            The initial x direction of lazor
        int : *dir_y*
            The initial y direction of lazor
    '''
    def __init__(self, start_point, dir_x, dir_y):
        self.start_point = start_point
        self.dir_x = dir_x
        self.dir_y = dir_y

    def pos_chk(self, x, y, x_boundary, y_boundary):
        '''
        This function is able to check whether the current position of lazor is still within the grid or not.

        **Parameters**

            x: *int*
                The x coordinate to check if it resides within the board
            y: *int*
                The y coordinate check if it resides within the board
            x_boundary: *int*
                The x coordinate boundary of the board
            y_boundary: *int*
                The y coordinate boundary of the board

        **Returns**

            valid: *bool*
                Whether the coordiantes are valid (True) or not (False).
        '''
        return x >= 0 and x < x_boundary and y >= 0 and y < y_boundary

    def check_out_block(self, x, y, board, pos_x, pos_y):
        '''
        This function is able to check whether the current position of lazor is out of the block or not.

        **Parameters**

            x: *int*
                The current x direction of lazor
            y: *int*
                The current y direction of lazor
            board: *list*
                The board matrix
            pos_x: *int*
                The x coordinate of current position
            pos_y: *int*
                The y coordinate of current position

        **Returns**

            valid: *bool*
                Whether the direction is from out of the block (True) or not (False).
        '''
        if board[pos_y][pos_x] == "1":
            # if the lazor strikes the block at face "1" from outside
            # the y direction of the lazor should be positive
            result = (y > 0)
        if board[pos_y][pos_x] == "2":
            # if the lazor strikes the block at face "2" from outside
            # the y direction of the lazor should be negative
            result = (y < 0)
        if board[pos_y][pos_x] == "3":
            # if the lazor strikes the block at face "3" from outside
            # the x direction of the lazor should be positive
            result = (x > 0)
        if board[pos_y][pos_x] == "4":
            # if the lazor strikes the block at face "4" from outside
            # the x direction of the lazor should be negative
            result = (x < 0)
        return result

    def lazor_path(self, board):
        '''
        This function is able to record all move position of the lazors and store in different lists.
        The lazor will reflect when it hit block A
        The lazor will be absorbed when it hit block B
        The lazor will reflect and refract when it hit block C
        This fucntion allow lazors to change direction when hit certain type of bolcks and record the new route.

        **Parameters**

            board: *list*
                The board matrix

        **Returns**

            path_list: *list*
                Lazor path list containing different route list of lazors.
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
                            # if the current position of the lazor is on the side of a block.
                            if self.check_out_block(dir_x1, dir_y1, board, curr_pos[0], curr_pos[1]):
                                # If lazors hit blocks from the outside of the block
                                # find out which face the lazor strike at
                                # locate the corresponding block and read it's type
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
    '''
    This function will enumerate all possible boards for the given boards after inputting
    all blocks, such as A, B, C.

    **Parameters**

        board_list: *list*
            list consist lists of blocks, obtained from read_file function
        A_num: *int*
            numbers of moved A blocks
        B_num: *int*
            numbers of moved B blocks
        C_num: *int*
            numbers of moved C blocks

    **Returns**

        all_block_possible_list: *list*
            the possible block matrixes and all placement of blocks insdead of 'x' and 'o'.
        all_position_possible_list: *list*
            all the corresponding position coordinate of each block in each possible permutation.
    '''
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

    # get a format_list, format like board_list
    # below is to generate coordinate list
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
    # print(all_block_possible_list)
    return all_block_possible_list, all_position_possible_list


def possible_path(test, block_list, position_list):
    '''
    This function will list and store all the lazor route of each possible block setted board permutation.

    **Parameters**

        test: *string*
            the file name which users want to read
        block_list: *list*
            the possible block matrixes and all placement of blocks insdead of 'x' and 'o'.
            the first output we get from possible_board function
        position_list: *list*
            all the corresponding position coordinate of each block in each possible permutation.
            the second output we get from possible_board function

    **Returns**

        lazor_possible: *list*
            the possible block matrixes and all placement of blocks insdead of 'x' and 'o'.
        board_possible: *list*
            all the corresponding possible board Permutation.

    '''
    board_possible = []
    lazor_possible_temp = []
    start = read_file(test)[3]
    direction = read_file(test)[4]
    for i in range(len(block_list)):
        board = read_file(test)[7]
        board1 = board.copy()
        for j in range(len(block_list[i])):
            # Using Block class to set every blocks in one possible permutation into the board
            Block(position_list[i][j], block_list[i][j]).add_block(board1)
        # get every possible board permutations
        board_possible.append(board1)
        lazor_temp = []
        for l in range(len(start)):
            # To deal with lazors which have more than one start point
            # Using Lazor class to store every routes of lazors in each possible board permutation
            lazor_temp.append((Lazor(start[l], direction[l][0], direction[l][1]).lazor_path(board1)))
        lazor_possible_temp.append(lazor_temp)
    lazor_possible =[]
    # merge the two or more lazor routes which produced by corresponding start points
    for a in range(len(lazor_possible_temp)):
        lazor_temp_1 = []
        for b in range(len(lazor_possible_temp[a])):
            lazor_temp_1 += lazor_possible_temp[a][b]
        lazor_possible.append(lazor_temp_1)
    return lazor_possible, board_possible


def final_check(lazor_possible, P_list, board_possible):
    '''
    
    This function is for check all the probabilities and find the correct answer

    **Parameters**
        
        lazor_possible: *list*
            The list that store all the probablities of lazor coordinates
        P_list: *list*
            The list that store the destinations 
        board_possible: *list*
            The list that store all the board conditions

    **Returns**

        board_possible[i]: *list*
            The board condition of correct soltion

    '''
    # For each probability
    for i in range(len(lazor_possible)):
        # Copy the P_list as test_list
        test_list = copy.deepcopy(P_list)
        # For each lazer path in each probability
        for j in range(len(lazor_possible[i])):
            # For each point in each path in each probability
            for k in range(len(lazor_possible[i][j])):
                # Check if the point is inside the copied list
                if lazor_possible[i][j][k] in test_list:
                    # If so, remove the found point from the copied list
                    test_list.remove(lazor_possible[i][j][k])
        # If the copied list is empty, this is the correct solution, then return the corresponding board condition
        if test_list == []:
            return board_possible[i]

def out_put(result, test):
    '''
    This function is to output a .txt file with a readable solution

    ***Parameters***

        result: **list**
            The list storing the board condition of correct solution
        test: **str**
            The name of .bff file

    ***Returns***

        None
    '''
    # Write the file as solution.txt
    with open ('solution.txt','w+') as file:
        file.write('This is the solution of the board you choose:' + test)
        file.write('\n\n')
        # Extract the block information from the correct solution
        # The bolck exist in every even numbered position, so i and j is added 2 in each loop
        i = 1
        while i < len(result):
            j = 1
            while j < len(result[i]):
                print(result[i][j], end=' ')
                file.write(result[i][j])
                file.write(' ')
                j += 2
            print('\n')
            file.write('\n\n')
            i += 2


def solve_game(test):

    '''
    This function is to pack all the functions into one

    ***Parameters***

        test: **str**
            The name of .bff file

    ***Returns***

        None
    '''
    read_file(test)
    p_list = read_file(test)[5]
    # t : the first output of function possible_boards which is all_block_possible_list.
    # w : the second output of function  which is corresponding all_position_possible_list.
    t, w = possible_boards(read_file(test)[6], read_file(test)[0], read_file(test)[1], read_file(test)[2])
    # l: the first output of function possible_path which is lazor_possible, board_possible.
    # lazor_possible is all the lazor path point coordinate of each possible board.
    # b : the second output of function possible_path which is board_possible.
    # board_possible is all the corresponding possible board.
    l, b = possible_path(test, t, w)
    out_put(final_check(l, p_list, b), test)


if __name__ == "__main__":
    solve_game("mad_7.bff")
    time_end = time.time()
    print(time_end - time_start)

