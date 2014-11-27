import numpy as np
import random

SMALL = 3
SIZE = 9

class Sudoku:

    def __init__(self, sudoku_txt):
        sudoku_grid = np.zeros((SIZE,SIZE))
        empty_cases = []
        lines = sudoku_txt.split()

        available_for_line = []

        # Read the sudoku
        for i, line in enumerate(lines):
            line_possibility = set(range(1,SIZE+1))
            for j, char in enumerate(line):
                if char!='0':
                    line_possibility.discard(int(char))
                    sudoku_grid[i,j]  = int(char)
                else:
                    empty_cases.append((i,j))
            available_for_line.append(line_possibility)

        # Parameters of the problem
        self.size = SIZE
        self.sudoku_grid_empty = np.copy(sudoku_grid)
        self.empty_cases = empty_cases

        # Generate initial solution
        for i,line in enumerate(available_for_line):
            for j in range(SIZE):
                if sudoku_grid[i,j] == 0:
                    sudoku_grid[i,j] = line.pop()
            assert len(line)==0
        self.sudoku_grid = sudoku_grid

        # Get numbers of constraint by elements
        self.constraints_violation = self.count_constraint_violation(self.sudoku_grid)



    def __repr__(self):
        return str(self.sudoku_grid_empty)

    def show_filled(self):
        print self.sudoku_grid

    def count_constraint_violation(self, solution):
        constraints_violation = np.zeros((len(self.empty_cases),1))

        for k, (i, j)  in enumerate(self.empty_cases):
            a = SMALL* (i / SMALL)
            b = SMALL* (j / SMALL)
            value = solution[i,j]
            constraints_violation[k] = np.sum(solution[i,:]==value) + \
                                       np.sum(solution[:,j]==value) + \
                                       np.sum(solution[a:a+3,b:b+3]==value) - 3
            # The -3 is there because there should be a value everytime
            # -> the one we're considering


        return constraints_violation

    def get_new_solution(self):
        solution = np.copy(self.sudoku_grid)
        probabilities = np.exp(self.constraints_violation).cumsum()

        mult = probabilities[-1]
        pos1 = probabilities.searchsorted(mult*random.random())
        pos2 = probabilities.searchsorted(mult*random.random())

        idx1 = self.empty_cases[pos1]
        idx2 = self.empty_cases[pos2]

        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

        return solution, self.count_constraint_violation(solution)


def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')
    sudokus = []

    for sudoku_txt in sudoku_tab:
        sudokus.append(Sudoku(sudoku_txt))

    return sudokus
