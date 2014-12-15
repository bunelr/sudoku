import numpy as np
import random

'''
Implementation of a sudoku solver using Elser's map and iterative projection
as described in Jason Schaad's paper:

Modeling the 8-queens problem and sudoku using an algorithm
based on projections onto nonconvex sets
'''

def make_unit(pos, size):
    '''
    Make a Unit vector of size `size` and with a one
    on the `pos` coordinates
    '''
    v = np.zeros((size,))
    pos = round(pos)
    v[pos] = 1
    assert v.sum()==1
    return v

def unit_proj(arr):
    '''
    Project a vector to the closest unit vector of the basis
    Example: [0.2 0.3 0.6 0.1 0.2] will be projected to
             [0   0   1   0   0  ]
    '''
    amax = arr.argmax()
    size = len(arr)
    unit = make_unit(amax, size)
    return unit

def column_proj(sudo):
    '''
    Make all the columns vector unit vectors
    '''
    newsudo = sudo.copy()
    size = sudo.shape[0]
    for j in range(size):
        for k in range(size):
            newsudo[:,j,k] = unit_proj(sudo[:,j,k])
    return newsudo

def row_proj(sudo):
    '''
    Make all the rows vectors unit vectors
    '''
    newsudo = sudo.copy()
    size = sudo.shape[0]
    for i in range(size):
        for k in range(size):
            newsudo[i,:,k] = unit_proj(sudo[i,:,k])
    return newsudo

def cube_proj(sudo):
    '''
    Make all the cube vectors (The inner squares unraveled)
    unit vectors
    '''
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
    '''
    For all the position (row,col), make the value vector an unit vector
    (=> enforcing the 1 value per case condition )
    If the value is known for this point, enforce it, regardless of
    the current weights
    '''
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
    '''
    From the (size*size*size) matrix used internallt by the algorithm
    Extract a (size*size) matrix representing the sudoku's usual form
    '''
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

def check_sudoku(sudoku, given):
    '''
    Check if we reached the solution of the problem by
    validating all the constraints in succession
    '''
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
    '''
    From the sudoku's usual form (size*size matrix)
    Generate the one used by the algorithm (size*size*size matrix)
    '''
    size = given.shape[0]
    sudo = np.zeros((size,size,size))
    for i in range(size):
        for j in range(size):
            if given[i,j]!=0:
                sudo[i,j,:] = make_unit(given[i,j]-1, size)
    return sudo


def solve_sudoku(given):
    '''
    Taking as an input a sudoku in its usual form with 0 denoting
    empty cases, returns a filled sudoku
    '''

    found_solution = True

    sudo = generate_initial_solution(given)

    sudo1_old = sudo
    sudo2_old = sudo
    sudo3_old = sudo
    sudo4_old = sudo
    to_comp = represent_cube(sudo)

    i = 0
    while not check_sudoku(to_comp, given):
        sudo_diag = (sudo1_old + sudo2_old + sudo3_old + sudo4_old)/4.0
        sudo1 = column_proj(2*sudo_diag - sudo1_old) + sudo1_old - sudo_diag
        sudo2 = row_proj(2*sudo_diag - sudo2_old) + sudo2_old - sudo_diag
        sudo3 = cube_proj(2*sudo_diag - sudo3_old) + sudo3_old - sudo_diag
        sudo4 = given_proj(2*sudo_diag - sudo4_old,given) + sudo4_old - sudo_diag

        sudo1_old = sudo1
        sudo2_old = sudo2
        sudo3_old = sudo3
        sudo4_old = sudo4

        to_comp = represent_cube(sudo_diag)
        i += 1
        if i % 1000 ==0:
            print "%s iteration done"
            if i>10000:
                # Give up after too many operations
                found_solution=False

    return found_solution, to_comp

def solve_iterative_projection(given):
    '''
    Solve a sudoku given under text form
    '''
    found_solution, solution = solve_sudoku(given)
    if found_solution:
        print solution
    else:
        print "No solution found, giving up"
    return found_solution
