from sudoku import Sudoku, load_sudokus_from_file
import random
import math

sudokus = load_sudokus_from_file('easy50.txt')

MAX_ITERATION = 50000

def solve_sudoku(sudoku):
    # Parameters of the problem
    state_len = len(sudoku.dispos)
    
    # Generate initial state
    solution = range(state_len)
    sudoku.fill_in_state(solution)
    energy = sudoku.count_constraint_violation()
    
    best_solution = solution[:]
    best_energy = energy
    temperature = 1

    for i in range(MAX_ITERATION):
        new_sol = get_new_solution(solution)

        sudoku.fill_in_state(new_sol)
        new_energy = sudoku.count_constraint_violation()

        if should_do_transition(energy, new_energy, i):
            energy = new_energy
            solution = new_sol
        
        if energy < best_energy:
            best_energy = energy
            best_solution = solution[:]
        
        if best_energy == 0:
            break
        if i % 100==0:
            print i, temperature, best_energy

        temperature = temperature * 0.9999
    sudoku.fill_in_state(best_solution)
    sudoku.show_filled()

def get_new_solution(solution):
    '''
    Randomly permut two elements of the solution
    This way, the two configuration should be close in terms of energy
    '''
    idx_range = len(solution)

    a = random.randint(0, idx_range -1)
    b = random.randint(0, idx_range -1)

    solution[a], solution[b] = solution[b], solution[a]
    return solution

def should_do_transition(energy, new_energy, temperature):
    if new_energy < energy:
        return True
    barrier = math.exp((energy - new_energy)/ temperature)
    if random.random() < barrier:
        return True
    else:
        return False
