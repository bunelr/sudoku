import numpy as np
import random
import pdb

def make_unit(pos):
    v = np.zeros((9,))
    pos = round(pos)
    v[pos] = 1
    assert v.sum()==1
    return v

def unit_proj(arr):
    amax = arr.argmax()
    unit = make_unit(amax)
    return unit

def column_proj(sudo):
    newsudo = sudo.copy()
    for j in range(9):
        for k in range(9):
            newsudo[:,j,k] = unit_proj(sudo[:,j,k])
    return newsudo

def row_proj(sudo):
    newsudo = sudo.copy()
    for i in range(9):
        for k in range(9):
            newsudo[i,:,k] = unit_proj(sudo[i,:,k])
    return newsudo

def cube_proj(sudo):
    newsudo = sudo.copy()
    for a in range(3):
        for b in range(3):

            for k in range(9):
                temp = newsudo[a:a+3,b:b+3,k].ravel()
                temp = unit_proj(temp)
                temp = temp.reshape((3,3))
                newsudo[a:a+3,b:b+3,k] = temp
    return newsudo

def given_proj(sudo, given):
    newsudo = sudo.copy()
    for i in range(9):
        for j in range(9):
            if given[i,j]!=0:
                newsudo[i,j,:] = make_unit(given[i,j]-1)
            else:
                newsudo[i,j,:] = unit_proj(newsudo[i,j,:])
    return newsudo

def represent_cube(sudo):
    sudoku = np.zeros((9,9))
    for i in range(9):
        for j in range(9):
            sudoku[i,j]=1
            val = sudo[i,j,0]
            for k in range(1,9):
                if sudo[i,j,k] > val:
                    val = sudo[i,j,k]
                    sudoku[i,j] = k+1
    return sudoku

def diag_proj(sudo1, sudo2, sudo3, sudo4):
    return (sudo1+sudo2+sudo3+sudo4)/4.0

def col_cube(sudo1, sudo2, sudo3, sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    r_delta = 2 * PD - sudo1
    return (2*column_proj(r_delta) - r_delta + sudo1)/2

def row_cube(sudo1,sudo2,sudo3,sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    r_delta = 2 * PD - sudo2
    return (2*row_proj(r_delta) -r_delta + sudo2)/2

def cube_cube(sudo1, sudo2,sudo3, sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    r_delta = 2 * PD - sudo3
    return (2*cube_proj(r_delta) -r_delta + sudo3)/2

def given_cube(sudo1, sudo2, sudo3, sudo4, given):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    r_delta = 2 * PD - sudo4
    return (2*given_proj(r_delta,given) -r_delta + sudo4)/2

def check_sudoku(sudoku, given):
    #Rows
    for i in range(9):
        if len(np.unique(sudoku[i,:]))!=9:
            return False
    #Cols
    for j in range(9):
        if len(np.unique(sudoku[:,j]))!=9:
            return False
    #Cubes
    for a in range(3):
        for b in range(3):
            cube = sudoku[3*a:3*(a+1),3*b:3*b+3].unravel()
            if len(np.unique(cube))!=9:
                return False
    #Constraints
    for i in range(9):
        for j in range(9):
            if given[i,j]!=0:
                if sudoku[i,j]!=given[i,j]:
                    return False
    return True

def generate_initial_solution(given):
    sudo = np.zeros((9,9,9))
    for i in range(9):
        for j in range(9):
            if given[i,j]!=0:
                sudo[i,j,:] = make_unit(given[i,j]-1)
    return sudo


def solve_sudoku(given):

    sudo = generate_initial_solution(given)

    sudo1_old = sudo
    sudo2_old = sudo
    sudo3_old = sudo
    sudo4_old = sudo
    to_comp = represent_cube(sudo)

    i = 0
    print to_comp
    print

    while not check_sudoku(to_comp, given):
        sudo1 = col_cube(sudo1_old, sudo2_old, sudo3_old, sudo4_old)
        sudo2 = row_cube(sudo1_old, sudo2_old, sudo3_old, sudo4_old)
        sudo3 = cube_cube(sudo1_old, sudo2_old, sudo3_old, sudo4_old)
        sudo4 = given_cube(sudo1_old, sudo2_old, sudo3_old, sudo4_old, given)

        sudoada = diag_proj(sudo1, sudo2, sudo3, sudo4)

        sudo1_old = sudo1
        sudo2_old = sudo2
        sudo3_old = sudo3
        sudo4_old = sudo4

        to_comp = represent_cube(sudoada)
        i += 1


        print to_comp
        print

        if i>10:
            break

def load_sudokus_from_file(path_to_file):
    with open(path_to_file, 'r') as sudoku_file:
        sudokus = sudoku_file.read()
    sudoku_tab = sudokus.split('========')
    sudokus = []

    for sudoku_txt in sudoku_tab:
        sudokus.append(sudo_from_text(sudoku_txt))

    return sudokus

def sudo_from_text(sudo_txt):
    given = np.zeros((9,9))
    lines = sudo_txt.split()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char!='0':
                given[i,j] = int(char)
    return given

sudokus = load_sudokus_from_file('easy50.txt')
sudok = sudokus[0]

solve_sudoku(sudok)
