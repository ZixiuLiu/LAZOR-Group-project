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
            else:
                new_la_x = (-1) * lazor_x
                new_la_y = lazor_y
        elif self.b_type == "B":
            new_la_x = 0
            new_la_y = 0
        elif self.b_type == "C":
            if face == "1" or face == "2":
                new_la_x = lazor_x
                new_la_y = (-1) * lazor_y
            else:
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

    def out_block(self, pos_x, pos_y, newpos_x, newpos_y, board):
        '''
        This function is able to make sure that the lazor won't go through a block on the board.
        input:
        :param pos_x: The current x coordinate of lazor
        :param pos_y: The current y coordinate of lazor
        :param newpos_x: The new x coordinate of lazor
        :param newpos_y: The new y coordinate of lazor
        :param board: The board
        output:
        The result of whether lazors go through the block or not.
        '''
        return board[pos_y][pos_x] != "1" and "2" and "3" and "4" \
    and board[newpos_y][newpos_x] != "1" and "2" and "3" and "4"

    def lazor_path(self, board):
        start = self.start_point
        path = [start]
        dir_x = self.dir_x
        dir_y = self.dir_x
        while True:
            curr_pos = path[-1]
            new_x = curr_pos[0] + dir_x
            new_y = curr_pos[1] + dir_y
            if board[curr_pos[1]][curr_pos[0]] != "P":
                if self.pos_chk(new_x, new_y, len(board[0]), len(board)):
                    if board[curr_pos[1]][curr_pos[0]] == "0" or "L":
                        # if the current position of the lazor is not on the side of a block.
                        # the lazor can be longer for one step.
                        path.append([new_x,new_y])
                    else:
                        block_type = 0
                        block_position = 0
                        if self.out_block(curr_pos[0], curr_pos[1], new_x, new_y, board):
                            if board[new_y][new_x] == "1":
                                block_position = [new_y + 1, new_x]
                                block_type = board[new_y + 1][new_x]
                            elif board[new_y][new_x] == "2":
                                block_position = [new_y - 1, new_x]
                                block_type = board[new_y - 1][new_x]
                            elif board[new_y][new_x] == "3":
                                block_position = [new_y, new_x + 1]
                                block_type = board[new_y][new_x + 1]
                            elif board[new_y][new_x] == "3":
                                block_position = [new_y, new_x - 1]
                                block_type = board[new_y][new_x - 1]
                        else:
                            # If the lazor will go through a block, then the lazor will stop.
                            break
                        # Using the Block class to figure out the new direction of the lazor after striking.
                        dir_x, dir_y = Block(block_position, block_type).prop(dir_x, dir_y, board[new_y][new_x])
                else:
                    # Lazors will stop when it reaching the boundary of the board.
                    break
            else:
                # Lazors will stop when it reaching the target positions.
                break
        return path






























