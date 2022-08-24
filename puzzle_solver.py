#############################################################
# FILE : puzzle_solver.py
# WRITER : Ilan Vysokovsky, ilan.vys, 207375528
# EXERCISE : intro2cs1 ex8 2021
# DESCRIPTION: A program for solving a Nonogram type game
# using backtracking
#############################################################

from typing import Generator, List, Tuple, Set, Optional, Any

BLACK = 0
WHITE = 1
EMPTY = -1

# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]

def init_picture(n: int, m: int) -> Optional[Picture]: 
    '''
    Recieves two numbers representing row size and
    column size and creates an empty game borad (Picture)
    :param n: number of rows
    :param m: number of columns
    :return: an empty Picture
    '''
    picture = [[]] * n
    for i in range(0, len(picture)):
        picture[i] = [EMPTY] * m
        
    return picture

def valid_to_place(picture: Picture, constraints_set: Set[Constraint],
                   n: int, m: int) -> List[int]:
    '''
    Recieves a picture, a list of constraints and and a row and col index,
    and builds a list of all the valid values that can be put in that index.
    :param picture: the picture we want to check
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :param n: row index
    :param m: column index
    :return: a list of valid options for the index recieved.
    '''
    valid_values = []
    original_value = picture[n][m]
    for color in [BLACK, WHITE]:
        picture[n][m] = color

        if check_constraints(picture, constraints_set) != 0:
            valid_values.append(color)
        picture[n][m] = original_value
        
    return valid_values

def is_picture_filled(picture: Picture) -> bool:
    '''
    Recieves picture and checks if all the cells in it are 
    filled with a value.
    :param picture: the picture we want to check
    :return: True if picture is filled, otherwise False
    '''
    for i in range(0, len(picture)):
        if EMPTY in picture[i]:
            return False
    return True

def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''
    Recieves a partial picture, row and column indexes, and calcualtes
    the maximal amount of cells "seen" from the current cell.
    Returns the number of cells if all the unknown ones were to be 
    counted as white.
    :param picture: the picture we want to check
    :param row: row index
    :param col: column index
    :return: maximal number of seen cells
    '''
    count = 0
    if picture[row][col] == BLACK:
        return 0
    if picture[row][col] in [EMPTY, WHITE]:
        count+=1
        
    # check right
    for i in range(col+1, len(picture[0])):
        if picture[row][i] == 0:
            break
        if  picture[row][i] in [EMPTY, WHITE]:
            count+=1
            
    # check left
    for i in range(col-1, -1, -1):
        if picture[row][i] == BLACK:
            break
        if picture[row][i] in [EMPTY, WHITE]:
            count+=1
            
    # check downward
    for j in range(row+1, len(picture)):
        if picture[j][col] == BLACK:
            break
        if picture[j][col] in [EMPTY, WHITE]:
            count+=1
            
    # check upward
    for j in range(row-1, -1, -1):
        if picture[j][col] == BLACK:
            break
        if picture[j][col] in [EMPTY, WHITE]:
            count+=1
    
    return count
                
def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''
    Recieves a partial picture, row and column indexes, and calcualtes
    the minimal amount of cells "seen" from the current cell.
    Returns the number of cells if all the unknown ones were to be 
    counted as black.
    :param picture: the picture we want to check
    :param row: row index
    :param col: column index
    :return: minimal number of seen cells
    '''
    count = 0
    if picture[row][col] in [BLACK, EMPTY]:
        return 0
    if picture[row][col] == WHITE:
        count+=1
        
    # check right
    for i in range(col+1, len(picture[0])):
        if picture[row][i] in [BLACK, EMPTY]:
            break
        if picture[row][i] == WHITE:
            count+=1
            
    # check left
    for i in range(col-1, -1, -1):
        if picture[row][i] in [BLACK, EMPTY]:
            break
        if picture[row][i] == WHITE:
            count+=1
            
    # check downward
    for j in range(row+1, len(picture)):
        if picture[j][col] in [BLACK, EMPTY]:
            break
        if picture[j][col] == WHITE:
            count+=1
            
    # check upward
    for j in range(row-1, -1, -1):
        if picture[j][col] in [BLACK, EMPTY]:
            break
        if picture[j][col] == WHITE:
            count+=1
    
    return count

def check_constraints(picture: Picture, 
                      constraints_set: Set[Constraint]) -> int:
    '''
    Recieves a partial picture, and a constraint list,
    and returns a number for indicating weather the constrins were met.
    :param picture: the picture we want to check
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :return: 0 for illegal picture, 1 for a picture with all constraints 
    met exactly, and 2 for a picture with all the constraints met partially.
    '''
    value_to_return = 1
    for constraint in constraints_set:
        max_seen = max_seen_cells(picture, constraint[0], constraint[1])
        min_seen = min_seen_cells(picture, constraint[0], constraint[1])
        seen = constraint[2]
        
        if seen >= min_seen and seen <= max_seen and \
            max_seen != min_seen and value_to_return != 0:
            value_to_return = 2
            
        if seen < min_seen or seen > max_seen:
            return 0
    
    return value_to_return

def solve_puzzle_helper(picture: Picture, constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    '''
    Helper function for `solve_puzzle`. We use backtracking for
    checking all the possible values for all possible cells.
    :param picture: the picture we want to fill
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :param n: row index
    :param m: column index
    :return: a solved picture puzzle painted in black and white,
             represented by 1 for white and 0 for black
    '''
    if is_picture_filled(picture):
        return picture
    
    if m == len(picture[0]) and n < len(picture):
        m = 0
        n += 1
        
    for i in valid_to_place(picture, constraints_set, n, m):
        picture[n][m] = i
        if solve_puzzle_helper(picture, constraints_set, n, m + 1):
            return picture
    
    picture[n][m] = EMPTY
    
def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    '''
    Recieves a constraint list and a picture size and returns one 
    possible solution to the puzzle.
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :param n: number of rows for the picture
    :param m: number of columns for the picture
    :return: a solved picture puzzle painted in black and white,
             represented by 1 for white and 0 for black
    '''
    picture = init_picture(n, m)
    return solve_puzzle_helper(picture, constraints_set, 0, 0)

def how_many_solutions_helper(picture: Picture, 
                              constraints_set: Set[Constraint], 
                              n: int, m: int, lst: List) -> int:
    '''
    Helper function for `how_many_solutions`. We use backtracking for
    checking all the possible values for all possible cells.
    :param picture: the picture we want to fill
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :param n: row index
    :param m: column index
    :param l: a list with the length of all the solutions found
    :return: the number of all the possible solutions to the puzzle.
    '''
    if is_picture_filled(picture): 
        if check_constraints(picture, constraints_set) == 1:
            lst[0] += 1
            return True
        return False
    
    if m == len(picture[0]) and n < len(picture):
        m = 0
        n += 1
        
    for i in valid_to_place(picture, constraints_set, n, m):
        picture[n][m] = i
        how_many_solutions_helper(picture, constraints_set, n, m + 1, lst)
    picture[n][m] = EMPTY
    
    return lst[0]

def how_many_solutions(constraints_set: Set[Constraint], 
                       n: int, m: int) -> int:
    '''
    Recieves a constraint list and a picture size and calculates the 
    number of all the possible solutions to the puzzle.
    :param constraints_set: a set of constrints for the game picture 
                            with indexes for the location and their value.
    :param n: number of rows for the picture
    :param m: number of columns for the picture
    :return: the number of all the possible solutions to the puzzle.
    '''
    picture = init_picture(n, m)
    return how_many_solutions_helper(picture, constraints_set, 0, 0, [0])

def power_set(items: list[Any]) -> list[Any]:
    '''
    Recieves a list of items and returns all the permutations
    of items from that list.
    :param items: list of items we want to explore.
    :param m: number of columns for the picture
    :return: the number of all the possible solutions to the puzzle.
    '''
    if len(items) == 0:
        return [[]]
    
    without_x_n = items[:]
    x_n = without_x_n.pop()
    all_subsets = []
    
    for subset in power_set(without_x_n):
        all_subsets.append(subset)
        all_subsets.append(subset + [x_n])
        
    return all_subsets

def setify_constraints(constraints_list: list[list[int]]) -> Set[Constraint]:
    '''
    Recieves a list of constraints represented as a list,
    and creates a set containing those constraints.
    :param constraints_list: list of constraints.
    :return: the number of all the possible solutions to the puzzle.
    '''
    constraints_set = set()
    for constraint in constraints_list:
        constraints_set.add((constraint[0], constraint[1], constraint[2]))
    
    return constraints_set
 
def generate_puzzle_helper(picture: Picture, constraints_list: List[List[int]]) -> Set[Constraint]:
    '''
    Helper function to `generate_puzzle` .Receives a list of constraints
    represented as a list, and a solved puzzle, and finds a minimal
    nmber of constrints for solving that puzzle. 
    :param constraints_list: list of all possible constraints.
    :return: a minimal set of constraints for a single solution.
    '''
    all_possible_sets = power_set(constraints_list)
    all_possible_sets.sort(key=len)
    
    for i in range(0, len(all_possible_sets)):
        constraints_set = setify_constraints(all_possible_sets[i])
        
        if how_many_solutions(constraints_set, len(picture), len(picture[0])) == 1 \
            and solve_puzzle(constraints_set, len(picture), len(picture[0])) == picture:
            return constraints_set
                
def generate_puzzle(picture: Picture) -> Set[Constraint]:
    '''
    Recieves a solved puzzle and retruns a minimal set of constraints
    that is limiting the solution to be only one.
    :param picture: a solved puzzle.
    :return: a minimal set of constraints for a single solution.
    '''
    constraints_list = []
    for i in range(0, len(picture)):
        for j in range(0, len(picture[0])):
            constraints_list.append([i, j, max_seen_cells(picture, i, j)])
                
    return generate_puzzle_helper(picture, constraints_list)
