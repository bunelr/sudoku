from sudoku import Sudoku, load_sudokus_from_file
import random
import math
import pdb

sudokus = load_sudokus_from_file('easy50.txt')
sudo = sudokus[0]

def solve_sudoku(sudoku):
    # Generate initial state
    solution = [elt  for line in sudoku.available_for_line for elt in line]
    sudoku.fill_in_state(solution)
    energy = sudoku.count_constraint_violation()
    
    best_solution = solution[:]
    best_energy = energy
    temperature = 1
    i =0
    try:
        while True:
            i = i+1
            new_sol = get_new_solution(solution, sudoku)

            sudoku.fill_in_state(new_sol)
            new_energy = sudoku.count_constraint_violation()

            if should_do_transition(energy, new_energy, temperature):
                energy = new_energy
                solution = new_sol
        
                if energy < best_energy:
                    best_energy = energy
                    best_solution = solution[:]
        
            if best_energy == 0:
                break
            if i % 1000==0:
                print i, temperature, best_energy

            temperature = temperature * 0.99999
    except KeyboardInterrupt:
        pass

    sudoku.fill_in_state(best_solution)

    sudoku.show_filled()

def get_new_solution(solution, sudoku):
    '''
    Randomly permut two elements of the solution
    This way, the two configuration should be close in terms of energy
    '''
    line = random.randint(0,sudoku.size-1)

    cases = [idx  for (idx, case) in enumerate(sudoku.empty_cases) if case[0]==line]

    a = random.randint(0, len(cases) -1)
    b = random.randint(0, len(cases) -1)

    solution[cases[a]], solution[cases[b]] = solution[cases[b]], solution[cases[a]]

    return solution

def should_do_transition(energy, new_energy, temperature):
    if new_energy < energy:
        return True
    barrier = math.exp((energy - new_energy)/ temperature)
    if random.random() < barrier:
        return True
    else:
        return False


solve_sudoku(sudo)
