import time
import json
import numpy as np
import os

from simulated_annealing.solver import solve_simulated_annealing
from iterative_projection.solver import solve_iterative_projection

DATASETS = ['easy', 'medium', 'hard', '16_wide', '25_wide']

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.splitlines()

    sudokus_np = []
    for sudo_txt in sudoku_tab:
        sudokus_np.append(sudo_from_text(sudo_txt))

    return sudokus_np


def sudo_from_text(sudo_txt):
    '''
    Convert a sudoku under string form to
    its usual form (size*size matrix)
    '''
    values = sudo_txt.split('.')
    size_2 = len(values)
    size = int(np.sqrt(size_2))

    given = np.zeros((size,size))
    for idx, val in enumerate(values):
        i = idx / size
        j = idx - (i*size)
        given[i,j] = int(val)
    assert (idx+1) == size*size
    return given



def main():
    for dataset in DATASETS:
        sudokus = load_sudokus_from_file(os.path.join('data',dataset))

        solved_sa = dict()
        solved_pr = dict()
        timing_sa = dict()
        timing_pr = dict()

        for index, sudoku in enumerate(sudokus):
            print sudoku

            print "Solving by Iterative Projection"
            start = time.clock()
            solved = solve_iterative_projection(sudoku)
            end = time.clock()
            solved_pr[index] = solved
            timing_pr[index] = end - start

            print "Solving by simulated Annealing"
            start = time.clock()
            solved = solve_simulated_annealing(sudoku)
            end = time.clock()
            solved_sa[index] = solved
            timing_sa[index] = end -start

            with open(dataset+'_SA_timing.json','w') as f:
                json.dump(timing_sa,f)

            with open(dataset+'_PR_timing.json','w') as f:
                json.dump(timing_pr,f)

            with open(dataset+'_SA_solved.json','w') as f:
                json.dump(solved_sa,f)

            with open(dataset+'_PR_solved.json','w') as f:
                json.dump(solved_pr,f)

            print "\n\n"


if __name__ == '__main__':
    main()
