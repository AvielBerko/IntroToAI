import random
import numpy as np

columns = [] # columns is the locations for each of the queens

def display():
    for row in range(len(columns)):
        for column in range(len(columns)):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()


def place_n_queens(size):
    columns.clear()
    row = 0
    while row < size:
        column=random.randrange(0,size)
        columns.append(column)
        row += 1

########### British Museum Solution ###########

def solution_found():
    '''
    checks if the n queens are placed so that no queen threatens another queen
    '''
    global columns
    # save the columns in a temporary list
    temp_cols = list(columns)
    # reset columns to the first queen only
    columns = [temp_cols[0]]
    # checks for each row if the queens are safe
    for col in temp_cols[1:]:
        if not next_row_is_safe(col, len(temp_cols)):
            # found a queen that is not safe
            columns = temp_cols
            return False
        columns.append(col)
    # the solution was found, all queens are safe
    return True

def british_museum_solution(size):
    num_of_checks = 0
    # places n queens randomaly until a solution was found
    place_n_queens(size)
    while not solution_found():
        place_n_queens(size)
        num_of_checks += 1
        
    print("\nSolution found! Here it is:")
    display()
    print(columns)
    print ("Number of checks:", num_of_checks)
    return num_of_checks


def average_british_museums(size, times):
    sum_of_checks = 0
    for _ in range(times):
        sum_of_checks += british_museum_solution(size)

    avg = sum_of_checks / times
    print("\nAverage number of checks:", avg )
    return avg


########### DFS Solution ###########

def dfs_solution(size):
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0  
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        while column < size:
            number_of_iterations+=1
            if next_row_is_safe(column, size):
                place_in_next_row(column)
                number_of_moves += 1
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:
                print("Solution found! Here it is:")
                display()
                print("Number of iterations:",number_of_iterations)
                print("Number of queens placed + backtracks:",number_of_moves)
                return number_of_iterations, number_of_moves
            
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column
            number_of_moves += 1
            
def place_in_next_row(column):
    columns.append(column)
 
def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1
 
def next_row_is_safe(column, size):
    row = len(columns) 
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False
 
    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False
 
    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True


########### Forward Tracking Solution ###########

def forward_tracking_solution(size):
    columns.clear()
    # creates a matrix sizeXsize
    board = np.zeros((size,size))
    number_of_moves = 0
    number_of_iterations = 0 
    row = 0
    prev_col = -1
    backtraking = False

    while row < size:   
        col = prev_col + 1
        while col < size:
            number_of_iterations += 1
            # checks if at row and col the position is unsafe
            if board[row][col] != 0:
                col += 1
                continue
            
            # the position at row and col is safe
            columns.append(col)
            number_of_moves += 1
            # mark next rows' unsafe positions
            _update_possible_positions(board, row, col, MARK)
            prev_col = -1
            
            # checks if a row with no safe positions exists
            if is_dead_end(board, row):
                backtraking = True
            else:
                row += 1
                
            break

        # checks if got to the end of the row without finding a position for a queen
        if col == size:
            if row == 0:
                print("No solution found :(")
                return number_of_iterations, number_of_moves
            row -= 1
            backtraking = True

        if backtraking:
            number_of_moves += 1
            prev_col = columns[row]
            # unmark the removed queen's unsafe positions
            _update_possible_positions(board, row, prev_col, UNMARK)
            columns.pop()
            backtraking = False
            
    print("\nSolution found! Here it is:")
    display()
    print("Number of iterations:",number_of_iterations)
    print("Number of queens placed + backtracks:",number_of_moves)
    return number_of_iterations, number_of_moves

MARK = 1
UNMARK = -1

def _update_possible_positions(board, row, col, mark_or_unmark):
    '''
    marks or unmarks unsafe positions for a given position (row, col) on a given board
    '''
    size = len(board)
    # marks or unmarks the column
    for i in range(row + 1, size):
        board[i][col] += mark_or_unmark
        
    rem_cols = size - col
    rem_rows = size - row
    
    # marks or unmarks the right diagonal
    for i in range(1, min(rem_cols, rem_rows)):
        board[row + i][col + i] += mark_or_unmark
        
    # marks or unmarks the left diagonal
    for i in range(1, min(col + 1, rem_rows)):
        board[row + i][col - i] += mark_or_unmark


def is_dead_end(board, row):
    '''
    checks if after a given row, exists a row with no safe position
    '''
    for i in range(row + 1, len(board)):
        if all(board[i]):
            return True


########### Stochastic Solution ###########

def stochastic_solution(size):
    columns.clear()
    # creates a matrix sizeXsize
    board = np.zeros((size,size))
    number_of_moves = 0
    number_of_iterations = 0 
    row = 0
    backtraking = False
    
    while row < size:   
        col = random_possible_col(board, row)
        while col != -1:
            number_of_iterations += 1
            # checks if at row and col the position is unsafe
            if board[row][col] != 0:
                col = random_possible_col(board, row)
                continue
            
            # the position at row and col is safe
            columns.append(col)
            number_of_moves += 1
            # mark next rows' unsafe positions and mark the columns as already checked
            update_possible_positions(board, row, col, MARK)
            
            # checks if a row with no safe positions exists
            if is_dead_end(board, row):
                backtraking = True
            else:
                row += 1
                
            break
            
        # checks if got to the end of the row without finding a position for a queen
        if col == -1:
            if row == 0:
                print("No solution found :(")
                return number_of_iterations, number_of_moves
            
            # remove all "already checked" positions from the current row
            for i in range(size):
                if board[row][i] == -1:
                    board[row][i] = 0
            row -= 1
            backtraking = True
            
        if backtraking:
            number_of_moves += 1
            # unmark the removed queen's unsafe positions
            update_possible_positions(board, row, columns[row], UNMARK)
            columns.pop()
            backtraking = False
            
            
    print("\nSolution found! Here it is:")
    display()
    print("Number of iterations:",number_of_iterations)
    print("Number of queens placed + backtracks:",number_of_moves)
    return number_of_iterations, number_of_moves

MARK = 1
UNMARK = -1

def update_possible_positions(board, row, col, mark_or_unmark):
    '''
    marks or unmarks unsafe positions for a given position (row, col) on a given board
    also, if set to MARK, marks the position (row, col) as checked position (-1)
    '''
    size = len(board)
    # marks or unmarks the column
    for i in range(row + 1, size):
        board[i][col] += mark_or_unmark
        
    rem_cols = size - col
    rem_rows = size - row
    
    # marks or unmarks the right diagonal
    for i in range(1, min(rem_cols, rem_rows)):
        board[row + i][col + i] += mark_or_unmark

    # marks or unmarks the left diagonal
    for i in range(1, min(col + 1, rem_rows)):
        board[row + i][col - i] += mark_or_unmark

    # marks the position (row, col) as checked position
    if mark_or_unmark == 1:
        board[row][col] = -1


def random_possible_col(board, row):
    '''
    returns randomly a safe and unchecked column at a given row
    if a row doens't have a possible column, returns -1
    '''
    possible_cols = []
    for col,val in enumerate(board[row]):
        if val == 0:
            possible_cols.append(col)
    
    if not possible_cols:
        return -1
        
    return random.choice(possible_cols)
    
def average_stochastic(size, times):
    sum_of_iterations = 0
    sum_of_moves = 0
    for _ in range(times):
        iterations, moves = stochastic_solution(size)
        sum_of_iterations += iterations
        sum_of_moves += moves
        
    avg_iterations = sum_of_iterations / times
    avg_moves = sum_of_moves / times

    print("\nAverage number of iterations:", avg_iterations)
    print("Average number of moves:", avg_moves)
    return avg_iterations, avg_moves
    
if __name__ == "__main__":
    # british_museum_solution(8)
    # average_british_museums(6, 20)
    # dfs_solution(8)
    # forward_tracking_solution(28)
    # stochastic_solution(24)
    average_stochastic(28, 20)
    
