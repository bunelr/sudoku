from iterative_projection.solver import solve_iterative_projection

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')

    return sudoku_tab


if __name__ == '__main__':
    sudokus_txt = load_sudokus_from_file('easy50.txt')
    for sudoku in sudokus_txt:
        solve_iterative_projection(sudoku)
