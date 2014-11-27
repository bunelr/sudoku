from sudoku import Sudoku, load_sudokus_from_file
import random
import math


sudokus = load_sudokus_from_file('easy50.txt')
sudo = sudokus[1]

def solve_sudoku(sudoku):
    # Generate initial state
    energy = sudoku.constraints_violation.sum()
    best_energy = energy
    best_solution = sudoku.sudoku_grid.copy()

    temperature = 1
    i =0
    try:
        while True:
            i = i+1
            new_solution, constraints_violation = sudoku.get_new_solution()
            new_energy = constraints_violation.sum()

            if should_do_transition(energy, new_energy, temperature):
                energy = new_energy
                sudoku.sudoku_grid = new_solution
                sudoku.constraints_violation = constraints_violation

                if energy < best_energy:
                    best_energy = energy
                    best_solution = new_solution.copy()
                if energy == 0:
                    break

            if i % 1000==0:
                print i, temperature, best_energy

            temperature = temperature * 0.99999

    except KeyboardInterrupt:
        pass

    sudoku.show_filled()


def should_do_transition(energy, new_energy, temperature):
    if new_energy < energy:
        return True
    barrier = math.exp((energy - new_energy)/ temperature)
    if random.random() < barrier:
        return True
    else:
        return False


solve_sudoku(sudo)
