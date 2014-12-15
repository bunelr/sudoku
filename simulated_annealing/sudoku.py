import numpy as np
import random

ALPHA = 0.7

class Sudoku:

    def __init__(self, sudoku_grid):
        sudoku_grid = sudoku

        empty_cases = []
        available_for_line = []

        size = sudoku.shape[0]
        # Read the sudoku
        for i in range(size):
            line_possibility = set(range(1,size+1))
            for j in range(size):
                if sudoku_grid[i,j]!=0:
                    line_possibility.discard(sudoku_grid[i,j])
                else:
                    empty_cases.append((i,j))
            available_for_line.append(line_possibility)

        # Parameters of the problem
        self.size = size
        self.small_size = int(np.sqrt(size))
        self.sudoku_grid_empty = np.copy(sudoku_grid)
        self.empty_cases = empty_cases

        # Generate initial solution
        for i,line in enumerate(available_for_line):
            for j in range(size):
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

        small = self.small_size
        for i, j  in self.empty_cases:
            a = small* (i / small)
            b = small* (j / small)
            value = solution[i,j]
            constraints_violation[i,j] = np.sum(solution[i,:]==value) + \
                                       np.sum(solution[:,j]==value) + \
                                       np.sum(solution[a:a+small,b:b+small]==value) - 3
            # The -3 is there because there should be a value on each constraints
            # -> the one we're considering
        cost = np.ma.masked_invalid(constraints_violation).sum()

        return constraints_violation, cost

    def get_new_solution(self):
        solution = np.copy(self.sudoku_grid)
        constraints_score = np.exp(self.constraints_violation)

        line_proba = constraints_score.sum(axis=1)
        line = discrete_sample(line_proba)


        col1 = discrete_sample(constraints_score[line,:])
        col2 = discrete_sample(constraints_score[line,:])

        idx1 = (line, col1)
        idx2 = (line, col2)

        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

        return solution, self.count_constraint_violation(solution)


def discrete_sample(density):
    '''
    Return an index corresponding to a sample of the distribution
    defined by the unnormalized discrete distribution
    Use constant alpha to allow exploration
    '''
    possible = (density!=0)
    density = ALPHA * (density/density.sum()) + ((1-ALPHA)*possible/possible.sum())

    distribution = density.cumsum()
    return distribution.searchsorted(random.random())
