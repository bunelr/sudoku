import numpy as np
import random

'''
Implementation of a sudoku solver using Elser's map and iterative projection
as described in Jason Schaad's paper:

Modeling the 8-queens problem and sudoku using an algorithm
based on projections onto nonconvex sets
'''

def make_unit(pos, size):
    v = np.zeros((size,))
    pos = round(pos)
    v[pos] = 1
    assert v.sum()==1
    return v

def unit_proj(arr):
    amax = arr.argmax()
    size = len(arr)
    unit = make_unit(amax, size)
    return unit

def column_proj(sudo):
    newsudo = sudo.copy()
    size = sudo.shape[0]
    for j in range(size):
        for k in range(size):
            newsudo[:,j,k] = unit_proj(sudo[:,j,k])
    return newsudo

def row_proj(sudo):
    newsudo = sudo.copy()
    size = sudo.shape[0]
    for i in range(size):
        for k in range(size):
            newsudo[i,:,k] = unit_proj(sudo[i,:,k])
    return newsudo

def cube_proj(sudo):
    newsudo = sudo.copy()
    size = sudo.shape[0]
    inner_size = int(np.sqrt(size))
    for a in range(inner_size):
        for b in range(inner_size):
            for k in range(size):
                temp = newsudo[inner_size*a:inner_size*(a+1),inner_size*b:inner_size*(b+1),k].ravel()
                temp = unit_proj(temp)
                temp = temp.reshape((inner_size,inner_size))
                newsudo[inner_size*a:inner_size*(a+1),inner_size*b:inner_size*(b+1),k] = temp
    return newsudo

def given_proj(sudo, given):
    newsudo = sudo.copy()
    size = sudo.shape[0]
    for i in range(size):
        for j in range(size):
            if given[i,j]!=0:
                newsudo[i,j,:] = make_unit(given[i,j]-1, size)
            else:
                newsudo[i,j,:] = unit_proj(newsudo[i,j,:])
    return newsudo

def represent_cube(sudo):
    size = sudo.shape[0]
    sudoku = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            sudoku[i,j]=1
            val = sudo[i,j,0]
            for k in range(1,size):
                if sudo[i,j,k] > val:
                    val = sudo[i,j,k]
                    sudoku[i,j] = k+1
    return sudoku

def diag_proj(sudo1, sudo2, sudo3, sudo4):
    return (sudo1+sudo2+sudo3+sudo4)/4.0

def col_cube(sudo1, sudo2, sudo3, sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    return column_proj(2*PD - sudo1) + sudo1 - PD;

def row_cube(sudo1,sudo2,sudo3,sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    return row_proj(2*PD-sudo2) + sudo2 - PD;

def cube_cube(sudo1, sudo2,sudo3, sudo4):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    return cube_proj(2*PD-sudo3) + sudo3 - PD;

def given_cube(sudo1, sudo2, sudo3, sudo4, given):
    PD = diag_proj(sudo1,sudo2,sudo3,sudo4)
    return given_proj(2*PD-sudo4,given) + sudo4 - PD;

def check_sudoku(sudoku, given):
    size = sudoku.shape[0]
    inner_size = int(np.sqrt(size))
    #Rows
    for i in range(size):
        if len(np.unique(sudoku[i,:]))!=size:
            return False
    #Cols
    for j in range(size):
        if len(np.unique(sudoku[:,j]))!=size:
            return False
    #Cubes
    for a in range(inner_size):
        for b in range(inner_size):
            cube = sudoku[inner_size*a:inner_size*(a+1),inner_size*b:inner_size*b+inner_size].ravel()
            if len(np.unique(cube))!=size:
                return False
    #Constraints
    for i in range(size):
        for j in range(size):
            if given[i,j]!=0:
                if sudoku[i,j]!=given[i,j]:
                    return False
    return True

def generate_initial_solution(given):
    size = given.shape[0]
    sudo = np.zeros((size,size,size))
    for i in range(size):
        for j in range(size):
            if given[i,j]!=0:
                sudo[i,j,:] = make_unit(given[i,j]-1, size)
    return sudo


def solve_sudoku(given):

    sudo = generate_initial_solution(given)

    sudo1_old = sudo
    sudo2_old = sudo
    sudo3_old = sudo
    sudo4_old = sudo
    to_comp = represent_cube(sudo)

    i = 0
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


    return to_comp

def sudo_from_text(sudo_txt):
    lines = sudo_txt.split()
    size = len(lines)
    given = np.zeros((size,size))
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char!='0':
                given[i,j] = int(char)
    return given

def solve_iterative_projection(sudo_txt):
    given = sudo_from_text(sudo_txt)
    solution = solve_sudoku(given)
    print solution
