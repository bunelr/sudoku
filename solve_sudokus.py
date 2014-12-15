import time
import json

from simulated_annealing.solver import solve_simulated_annealing
from iterative_projection.solver import solve_iterative_projection

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')

    return sudoku_tab


def main():
    sudokus_txt = load_sudokus_from_file('easy50.txt')

    solved_sa = dict()
    solved_pr = dict()
    timing_sa = dict()
    timing_pr = dict()

    for index, sudoku in enumerate(sudokus_txt):

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

    with open('SA_timing.json','w') as f:
        json.dump(timing_sa,f)

    with open('PR_timing.json','w') as f:
        json.dump(timing_pr,f)

    with open('SA_solved.json','w') as f:
        json.dump(solved_sa,f)

    with open('PR_solved.json','w') as f:
        json.dump(solved_pr,f)


if __name__ == '__main__':
    main()
