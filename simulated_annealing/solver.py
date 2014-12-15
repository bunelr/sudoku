from sudoku import Sudoku
import random
import math


def solve_sudoku(sudoku):
    # Generate initial state
    energy = sudoku.get_cost()
    best_energy = energy
    best_solution = sudoku.sudoku_grid.copy()

    temperature = 1
    i =0
    while True:
        i = i+1
        new_solution, (constraints_violation, new_energy) = sudoku.get_new_solution()

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

    sudoku.show_filled()


def should_do_transition(energy, new_energy, temperature):
    if new_energy < energy:
        return True
    barrier = math.exp((energy - new_energy)/ temperature)
    if random.random() < barrier:
        return True
    else:
        return False

def solve_simulated_annealing(sudo_txt):
    sudoku = Sudoku(sudo_txt)
    solve_sudoku(sudoku)
