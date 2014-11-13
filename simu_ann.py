from sudoku import Sudoku, load_sudokus_from_file

sudokus = load_sudokus_from_file('easy50.txt')

MAX_ITERATION = 5000

def solve_sudoku(sudoku):
    # Parameters of the problem
    state_len = len(sudoku.dispos)
    
    # Generate initial state
    solution = range[state_len]
    sudoku.fill_in_state(solution)
    energy = sudoku.count_constraint_violation()
    
    best_solution = solution[:]
    best_energy = energy

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
