"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from re import L
from telnetlib import X3PAD


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numEmpty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                numEmpty += 1
    if numEmpty % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    newBoard = deepcopy(board)
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")
    newBoard[i][j] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    # Check vertical
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]
    # Check diagonal kek this is some smoothbrain code
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[1][1]
    elif board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    numEmpty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                numEmpty += 1
    return numEmpty == 0 or winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    for action in actions(board):
        if player(board) == X:
            if max_value(board) == min_value(result(board, action)):
                return action
        else:
            if min_value(board) == max_value(result(board, action)):
                return action

# # testing stuff
# board = [[EMPTY, X, O],
#         [O, X, EMPTY],
#         [X, EMPTY, O]]

# print(minimax(board))

# board = [[X, X, X],
#         [O, X, EMPTY],
#         [X, EMPTY, O]]
# print(winner(board))
