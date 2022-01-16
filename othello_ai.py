"""
All AI algorithms are handled in this file
"""

from copy import deepcopy
from random import choice
from time import sleep

# Board score used for heuristic function
val = [[10, -3, 2, 1, 1, 2, -3, 10],
       [-3, -5, 0, 0, 0, 0, -5, -2],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [-3, -5, 0, 0, 0, 0, -5, -2],
       [10, -3, 2, 1, 1, 2, -3, 10]]

# Given an othello object and ai level, return the move made by the ai
def AI_move(othello, level, delay):
    if level == 1: return level1(othello, delay)
    if level == 2: return level2(othello, delay)
    if level == 3: return level3(othello, delay)
    if level == 4: return level4(othello, delay)
    if level == 5: return level5(othello, delay)
    if level == 6: return level6(othello, delay)

# Level 1 AI: make completely random moves
def level1(ot, delay):
    moves = ot.get_possible_moves()
    if delay: sleep(0.5)
    return choice(moves)

# Level 2 AI: the ai tries to maximize its piece count for every move
def level2(ot, delay):
    moves = ot.get_possible_moves()
    score_move = [0, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = (temp_ot.white_tiles if temp_ot.turn == 1 else temp_ot.black_tiles)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    if delay: sleep(0.5)
    return choice(score_move[1])

def level3(ot, delay):
    moves = ot.get_possible_moves()
    score_move = [-99999, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = heuristic_eval(temp_ot.board) * (1 if temp_ot.turn == 2 else -1)
        print(move, "  ", new_score)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
        print(score_move)
    if delay: sleep(0.5)
    return choice(score_move[1])

def level4(ot, delay):
    # Early game (move 1-10), Mid game (move 11-52), End game (move 53-60)
    raise NotImplementedError

def level5(ot, delay):
    raise NotImplementedError

def level6(ot, delay):
    raise NotImplementedError

# Given an othello object state, return the score of that state (max for black aka player 1, min for white)
def heuristic_eval(state):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score

def minimax(ot, depth, alpha, beta):
    pass


# def AI_1(ot):
#     pass
