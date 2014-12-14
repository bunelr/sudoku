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
        self.constraints_violation, _ = self.count_constraint_violation(self.sudoku_grid)

    def get_cost(self):
        return np.ma.masked_invalid(self.constraints_violation).sum()

    def __repr__(self):
        return str(self.sudoku_grid_empty)

    def show_filled(self):
        print self.sudoku_grid

    def count_constraint_violation(self, solution):
        constraints_violation =-np.inf * np.ones((self.size,self.size))

        for i, j  in self.empty_cases:
            a = SMALL* (i / SMALL)
            b = SMALL* (j / SMALL)
            value = solution[i,j]
            constraints_violation[i,j] = np.sum(solution[i,:]==value) + \
                                       np.sum(solution[:,j]==value) + \
                                       np.sum(solution[a:a+SMALL,b:b+SMALL]==value) - 3
            # The -3 is there because there should be a value on each constraints
            # -> the one we're considering
        cost = np.ma.masked_invalid(constraints_violation).sum()

        return constraints_violation, cost

    def get_new_solution(self):
        solution = np.copy(self.sudoku_grid)
        probabilities = np.exp(self.constraints_violation).cumsum(axis=1)

        line = discrete_sample(probabilities[:,-1].cumsum())


        col1 = discrete_sample(probabilities[line,:])
        col2 = discrete_sample(probabilities[line,:])

        idx1 = (line, col1)
        idx2 = (line, col2)

        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

        return solution, self.count_constraint_violation(solution)


def discrete_sample(cum):
    '''
    Return an index corresponding to a sample of the distribution defined by the
    unnormalized distribution function in cum
    '''
    return cum.searchsorted(cum[-1]*random.random())

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')
    sudokus = []

    for sudoku_txt in sudoku_tab:
        sudokus.append(Sudoku(sudoku_txt))

    return sudokus
