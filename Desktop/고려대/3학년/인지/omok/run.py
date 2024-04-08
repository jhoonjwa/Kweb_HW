import copy
import math
import time

# Constants
EMPTY = 0
BLACK = 1  # Computer
WHITE = 2  # Human
BOARD_SIZE = 19
DEPTH_LIMIT = 2

# Directions for checking lines on the board
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

def init_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY

def make_move(board, row, col, player):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False



def heuristic(board, player):
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player:
                for dx, dy in DIRECTIONS:
                    for direction in [1, -1]:  # Check both directions for open ends
                        line_score = 0
                        open_ends = 0
                        step = 0
                        while step < 5:  # Look for continuous stones in one direction
                            new_row = row + step * dx * direction
                            new_col = col + step * dy * direction
                            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and board[new_row][new_col] == player:
                                line_score += 1
                            else:
                                break  # Break if the line is interrupted
                            step += 1
                        
                        # Check for open end after the line
                        if step > 0:  # Ensure that we moved at least one step
                            end_row = row + step * dx * direction
                            end_col = col + step * dy * direction
                            start_row = row - dx * direction
                            start_col = col - dx * direction
                            if 0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE and board[end_row][end_col] == EMPTY:
                                open_ends += 1
                            if 0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE and board[start_row][start_col] == EMPTY:
                                open_ends += 1

                        score += line_score + open_ends * 2  # Adjust score based on line_score and open ends

    return score


###heuristic definition: limit search space based on open ends and 

def alpha_beta(board, depth, alpha, beta, maximizingPlayer, time_set, start_time, user_move):
    # Check time constraint to terminate the search early if necessary
    print('depth left to search', depth)
    if (time.time() - start_time) >= (time_set - 0.05):
        return heuristic(board, BLACK) - heuristic(board, WHITE), user_move[0], user_move[1]

    if depth == 0 or check_win(board, BLACK, user_move) or check_win(board, WHITE, user_move):
        return heuristic(board, BLACK) - heuristic(board, WHITE), user_move[0], user_move[0]

    if maximizingPlayer:
        maxEval = -math.inf
        best_move = (None, None)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if is_valid_move(board, row, col):
                    print('exploring coords:', row, col)
                    board[row][col] = BLACK  # Make move for BLACK
                    user_move = (row, col)
                    eval, _, _ = alpha_beta(board, depth-1, alpha, beta, False, time_set, start_time, user_move)
                    board[row][col] = EMPTY  # Undo move
                    
                    if eval > maxEval:
                        maxEval = eval
                        best_move = (row, col)
                        alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
        return maxEval, best_move[0], best_move[1]
    else:  # Minimizing player
        minEval = math.inf
        best_move = (None, None)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if is_valid_move(board, row, col):
                    print('exploring coords:', row, col)
                    board[row][col] = WHITE  # Make move for WHITE
                    user_move = (row, col)
                    eval, _, _ = alpha_beta(board, depth-1, alpha, beta, True, time_set, start_time, user_move)
                    board[row][col] = EMPTY  # Undo move
                    
                    if eval < minEval:
                        minEval = eval
                        best_move = (row, col)
                        beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
        return minEval, best_move[0], best_move[1]
    

def check(row, col):
    row_list, col_list = [], []
    boards = range(0, 19)

    row_start = max(row-5, 0)
    row_end = min(18, row+5)
    col_start = max(col-5, 0)
    col_end = min(col+5, 18)

    row_list = boards[row_start:row_end+1]
    col_list = boards[col_start:col_end+1]
    return row_list, col_list
    
    
def check_win(board, player, last_move):
    row, col = last_move[0], last_move[1]
    row_list, col_list = check(row, col)
    for row in row_list:
        for col in col_list:
            if board[row][col] == player:   ##two players are denoted as 1 or 2
                for dx, dy in DIRECTIONS:
                    count = 1
                    for step in range(1, 5):
                        new_row, new_col = row + step*dx, col + step*dy
                        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and board[new_row][new_col] == player:
                            count += 1
                        else:
                            break
                    if count == 5:
                        return True
    return False

def play_game():
    board = init_board()
    print("Omok Game Start! The computer is black, and the player is white.")
    print_board(board)

    time_set = float(input('Set your time per turn. It is recommended to take more than 4 seconds per turn'))
    row, col = None, None
    while True:
        # Computer's turn
        row = int(input("Enter your move's row: "))
        col = int(input("Enter your move's col: "))
        if make_move(board, row, col, WHITE):
            print_board(board)
            check_win(board, 1, (row, col))
        else:
            print("Invalid move. Try again.")
        user_move = (row, col)

        print("Computer's turn:")
        start_time = time.time()
        attack_eval, row1, col1 = alpha_beta(board, DEPTH_LIMIT, -math.inf, math.inf, True, time_set, start_time, user_move)
        defense_eval, row2, col2 = alpha_beta(board, DEPTH_LIMIT, -math.inf, math.inf, True, time_set, start_time, user_move)

        print('predicted_move:', row2, col2)
        if attack_eval > defense_eval:
            row, col = row1, col
        else:
            row, col = row2, col2
            
        make_move(board, row, col, BLACK)
        check_win(board, 2, (row, col))
        print_board(board)
        
        # Check for end of game or continue to human's move
        
        # Human's turn
        

# Uncomment below to start the game
play_game()
