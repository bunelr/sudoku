import numpy as np
import pdb

SMALL = 3
SIZE = 9

class Sudoku:
     
    def __init__(self, sudoku_txt):
        sudoku_grid = np.zeros((SIZE,SIZE,SIZE))
        empty_cases = []
        lines = sudoku_txt.split()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char!='0':
                    sudoku_grid[i,j,int(char)-1]  = 1
                else:
                    empty_cases.append((i,j))
        
        self.sudoku_grid = sudoku_grid
        self.empty_cases = empty_cases
        
    def __repr__(self):
        return self.visualise_sudoku()
        
    def visualise_sudoku(self):
        human_sudoku = np.zeros((SIZE,SIZE))
        for i in range(SIZE):
            human_sudoku=human_sudoku + (i+1) * self.sudoku_grid[...,i]
        return str(human_sudoku)
        
    @staticmethod
    def count_constraint_violation(sudoku):
        nb_constraint = 0
        obj = np.ones((1,SIZE))

        # Rows constraint
        for i in range(SIZE):
            # np.sum(sudo[i,...], axis=0) gives us an array of the number of times
            # a number is represented in the row i
            nb_constraint += np.sum(np.sum(sudo[i,...], axis=0)!=obj)

        # Columns constraint
        for j in range(SIZE):
            # np.sum(sudo[...,j,...], axis=0) gives us an array of the number of times
            # a number is represented in the column j         
            nb_constraint += np.sum(np.sum(sudo[...,j,...], axis=0)!=obj)

        # Box constraint
        for k in range(SIZE):
            a = k / SMALL
            b = k - a * SMALL
            # np.sum(sudo[a:a+3,b:b+3...], axis=(0,1)) gives us an array of the number 
            # of times a number is represented in the box of index a,b
            nb_constraint += np.sum(np.sum(sudo[a:a+3,b:b+3,...], axis=(0,1)) != obj)

        return nb_constraint
    

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')
    sudokus = []

    for sudoku_txt in sudoku_tab:
        sudokus.append(Sudoku(sudoku_txt))

    return sudokus

sudokus = load_sudokus_from_file('easy50.txt')
