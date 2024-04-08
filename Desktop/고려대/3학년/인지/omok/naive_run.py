import copy
import math
import time

# Constants
EMPTY = 0
BLACK = 1  # Computer
WHITE = 2  # Human
BOARD_SIZE = 19
DEPTH_LIMIT = 4

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
    # Score based on number of continuous pieces and open ends
    # This is a simple heuristic function for demonstration
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player:
                for dx, dy in DIRECTIONS:
                    line_score = 1
                    for step in range(1, 5):
                        new_row, new_col = row + step*dx, col + step*dy
                        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and board[new_row][new_col] == player:
                            line_score += 1
                        else:
                            break
                    score += line_score**2
    return score

def alpha_beta(board, depth, alpha, beta, maximizingPlayer, time_set, start_time, user_move):
    #start_time = time.time()
    print('depth left to explore: ', depth, 'elapsed time: ', time.time()-start_time)

    if (time.time() - start_time) >= (time_set - 0.05):  # If time limit is approached
        # Return a heuristic evaluation and no specific move if at the root call
        # This will trigger when the algorithm runs out of time at the root of the search tree
        return heuristic(board, BLACK) - heuristic(board, WHITE), None, None
    if depth == 0:
        return heuristic(board, BLACK) - heuristic(board, WHITE), None, None

    if maximizingPlayer:
        maxEval = -math.inf
        best_move = (None, None)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY:
                    board_copy = copy.deepcopy(board)
                    board_copy[row][col] = BLACK
                    eval, _, _ = alpha_beta(board_copy, depth-1, alpha, beta, False, time_set, start_time, user_move)
                    if eval > maxEval:
                        maxEval = eval
                        best_move = (row, col)
                        alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return maxEval, best_move[0], best_move[1]
    else:
        minEval = math.inf
        best_move = (None, None)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY:
                    board_copy = copy.deepcopy(board)
                    board_copy[row][col] = WHITE
                    eval, _, _ = alpha_beta(board_copy, depth-1, alpha, beta, True, time_set, start_time, user_move)
                    if eval < minEval:
                        minEval = eval
                        best_move = (row, col)
                        beta = min(beta, eval)
                    if beta <= alpha:
                        break
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
        _, row, col = alpha_beta(board, DEPTH_LIMIT, -math.inf, math.inf, True, time_set, start_time, user_move)
        make_move(board, row, col, BLACK)
        check_win(board, 2, (row, col))
        print_board(board)
        
        # Check for end of game or continue to human's move
        
        # Human's turn
        

# Uncomment below to start the game
play_game()
