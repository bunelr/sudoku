import numpy as np
import pdb

SMALL = 3
SIZE = 9

class Sudoku:
     
    def __init__(self, sudoku_txt):
        sudoku_grid = np.zeros((SIZE,SIZE,SIZE))
        empty_cases = []
        lines = sudoku_txt.split()
        missing_values = [SIZE for _ in range(SIZE)]

        available_for_line = []

        for i, line in enumerate(lines):
            line_possibility = set(range(1,SIZE+1))
            for j, char in enumerate(line):
                if char!='0':
                    line_possibility.discard(int(char))
                    idx_char = int(char)-1
                    sudoku_grid[i,j,idx_char]  = 1
                    missing_values[idx_char] -= 1
                else:
                    empty_cases.append((i,j))
            available_for_line.append(line_possibility)
        dispos = []
        for i,count in enumerate(missing_values):
            dispos.extend([i+1 for _ in range(count)])
        
        assert len(dispos) == len(empty_cases)
        self.size = SIZE
        self.dispos = dispos
        self.sudoku_grid_empty = np.copy(sudoku_grid)
        self.sudoku_grid = sudoku_grid
        self.empty_cases = empty_cases
        self.available_for_line = available_for_line
        
    def __repr__(self):
        return Sudoku.visualise_sudoku(self.sudoku_grid_empty)

    def show_filled(self):
        print Sudoku.visualise_sudoku(self.sudoku_grid)

    @staticmethod
    def visualise_sudoku(sudoku):
        human_sudoku = np.zeros((SIZE,SIZE))
        for i in range(SIZE):
            human_sudoku=human_sudoku + (i+1) * sudoku[...,i]
        return str(human_sudoku)
        
    def count_constraint_violation(self):
        sudoku = self.sudoku_grid
        nb_constraint = 0
        obj = np.ones((1,SIZE))

        # Rows constraint
        for i in range(SIZE):
            # np.sum(sudo[i,...], axis=0) gives us an array of the number of times
            # a number is represented in the row i
            nb_constraint += np.sum(np.sum(sudoku[i,...], axis=0)!=obj)

        # Columns constraint
        for j in range(SIZE):
            # np.sum(sudo[...,j,...], axis=0) gives us an array of the number of times
            # a number is represented in the column j         
            nb_constraint += np.sum(np.sum(sudoku[...,j,...], axis=0)!=obj)

        # Box constraint
        for k in range(SIZE):
            a = k / SMALL
            b = k - a * SMALL
            # np.sum(sudo[a:a+3,b:b+3...], axis=(0,1)) gives us an array of the number 
            # of times a number is represented in the box of index a,b
            nb_constraint += np.sum(np.sum(sudoku[a:a+3,b:b+3,...], axis=(0,1)) != obj)

        return nb_constraint
    
    def fill_in_state(self, state):
        assert len(state) == len(self.dispos), "%s state != %s dispos" % (len(state),len(self.dispos))

        self.sudoku_grid = np.copy(self.sudoku_grid_empty)
        for value, pos in zip(state, self.empty_cases):
            row, col = pos
            self.sudoku_grid[row, col, value-1] = 1

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')
    sudokus = []

    for sudoku_txt in sudoku_tab:
        sudokus.append(Sudoku(sudoku_txt))

    return sudokus
