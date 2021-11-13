'''
This file test the main function and functions in Class of the lazor file
'''
import unittest
import Lazor_project

class TestStringMethods(unittest.TestCase):

    def test_read_file(self):
        '''
        This function will check whether the function have read the .bff file properly
        and save the essential parameters correctly.
        '''
        A_num = 2
        B_num = 0
        C_num = 1
        L_point = [[2, 7]]
        L_direction = [[1, -1]]
        P_list = [[3, 0], [4, 3], [2, 5], [4, 7]]
        board_list = [['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'],['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
        board = [['0','0','0','0','0','0','0','0','0'],
                ['0','o','0','o','0','o','0','o','0'],
                ['0','0','0','0','0','0','0','0','0'],
                ['0','o','0','o','0','o','0','o','0'],
                ['0','0','0','0','0','0','0','0','0'],
                ['0','o','0','o','0','o','0','o','0'],
                ['0','0','0','0','0','0','0','0','0'],
                ['0','o','0','o','0','o','0','o','0'],
                ['0','0','0','0','0','0','0','0','0']]
        self.assertEqual(Lazor_project.read_file('mad_1.bff'),(A_num, B_num, C_num, L_point, L_direction, P_list, board_list, board))


    def test_add_block(self):
        '''
        This function will test add_block of Block Class. we need to check whether the funciton 
        could change the point around the block correctly.
        '''
        board_test = [['0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'C', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '0', 'A', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'A', '0', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0']]
        
        position = [[5, 1], [7, 3], [1, 5]]
        b_type = ['C','A','A']
        for i in range(len(position)):
            Lazor_project.Block(position[i], b_type[i]).add_block(board_test)

        solution = [['0', '0', '0', '0', '0', '1', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '3', 'C', '4', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '2', '0', '1', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '3', 'A', '4'], 
                    ['0', '1', '0', '0', '0', '0', '0', '2', '0'], 
                    ['3', 'A', '4', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '2', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0']]
        
        self.assertEqual(board_test, solution)
        

    def test_lazor_path(self):
        '''
        this function will test if the lazor_path in Lzaor class could get correct lazor path
        of the given board
        '''
        start_point = [2, 7]
        dir_x = 1
        dir_y = -1
        test_board = [['0', '0', '0', '0', '0', '1', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '3', 'C', '4', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '2', '0', '1', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '3', 'A', '4'], 
                    ['0', '1', '0', '0', '0', '0', '0', '2', '0'], 
                    ['3', 'A', '4', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '2', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0']]
        test_solution = Lazor_project.Lazor(start_point, dir_x, dir_y).lazor_path(test_board)
        solution = [[[2, 7], [3, 6], [4, 5], [5, 4], [6, 3], [5, 2], [4, 3], [3, 4], [2, 5], [3, 6], [4, 7], [5, 8], 'end'], 
                    [[5, 2], [4, 1], [3, 0], 'end']]
        self.assertEqual(test_solution, solution)


    def test_solve_game(self):
        '''
        this function will check if we can slove the lazor correctly
        '''
        Lazor_project.read_file('mad_1.bff')
        start = Lazor_project.read_file('mad_1.bff')[3]
        direction = Lazor_project.read_file('mad_1.bff')[4]
        p_list = Lazor_project.read_file('mad_1.bff')[5]
        T, W = Lazor_project.possible_boards(Lazor_project.read_file('mad_1.bff')[6], Lazor_project.read_file('mad_1.bff')[0], Lazor_project.read_file('mad_1.bff')[1], Lazor_project.read_file('mad_1.bff')[2])
        L, B = Lazor_project.possible_path('mad_1.bff', T, W)
        solution = [['0', '0', '0', '0', '0', '1', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '3', 'C', '4', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '2', '0', '1', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '3', 'A', '4'], 
                    ['0', '1', '0', '0', '0', '0', '0', '2', '0'], 
                    ['3', 'A', '4', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '2', '0', '0', '0', '0', '0', '0', '0'], 
                    ['0', 'o', '0', 'o', '0', 'o', '0', 'o', '0'], 
                    ['0', '0', '0', '0', '0', '0', '0', '0', '0']]
        self.assertEqual(Lazor_project.final_check(L, p_list, B),solution)

if __name__ == '__main__':

    unittest.main()

