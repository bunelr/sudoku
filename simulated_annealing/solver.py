from sudoku import Sudoku
import sudoku as other_file
from collections import deque
import random
import math


def solve_sudoku(sudoku):
    '''
    Print the solution to a sudoku if it is found
    and return a boolean indicating whether or not a solution
    has been found
    '''
    # Generate initial state
    energy = sudoku.get_cost()
    best_energy = energy
    best_solution = sudoku.sudoku_grid.copy()

    temperature = 1
    # cooling factor
    alpha = 0.999
    # reheating factor
    beta = 0.9
    # reheating scheduler parameter
    nb_identique = 1000

    cooling = True
    last_energies = deque(maxlen=nb_identique)
    sum_energies = 0

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

        if cooling:
            # Cooling
            if len(last_energies)==nb_identique:
                old = last_energies.popleft()
                sum_energies -= old
            last_energies.append(energy)
            sum_energies += energy
            if sum_energies == energy*nb_identique:
                cooling = False
                local_minima_energy = energy
                last_energies = deque(maxlen=nb_identique)
                sum_energies = 0
            temperature = temperature * alpha
            other_file.ALPHA = max(temperature,1)
        else:
            # Reheating
            if energy==local_minima_energy:
                temperature = min(temperature / beta,100)
            else:
                cooling = True
        if i % 1000==0:
            print i, temperature, energy, best_energy, "Cooling" if cooling else "Reheating"
            if i> 500000:
                print "No solution found, giving up"
                return False


    sudoku.show_filled()
    return True


def should_do_transition(energy, new_energy, temperature):
    if new_energy < energy:
        return True
    barrier = math.exp((energy - new_energy)/ temperature)
    if random.random() < barrier:
        return True
    else:
        return False

def solve_simulated_annealing(given):
    sudoku = Sudoku(given)
    return solve_sudoku(sudoku)
