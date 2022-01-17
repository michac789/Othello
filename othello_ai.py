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
    if level == 3: return level3(othello)
    if level == 4: return level4(othello)
    if level == 5: return level5(othello)
    if level == 6: return level6(othello)

# Level 1 AI: make completely random moves
def level1(ot, delay):
    moves = ot.get_possible_moves()
    if delay: sleep(0.5)
    return choice(moves)

# Level 2 AI: the ai tries to capture corners and prevent capturing buffer pieces
def level2(ot, delay):
    moves = ot.get_possible_moves()
    score_move = [-99999, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = heuristic_eval(temp_ot.board) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    if delay: sleep(0.5)
    return choice(score_move[1])

# Level 3 AI: looks 3 move ahead, focus on capturing corner and important tiles, prevent from capturing buffer zones
def level3(ot):
    moves = ot.get_possible_moves()
    score_move = [-99999, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax(temp_ot, 2, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return choice(score_move[1])

def level4(ot):
    # Early game (move 1-10), Mid game (move 11-51), End game (move 52-60)
    moves = ot.get_possible_moves()
    score_move = [-99999, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        if ot.move_no < 51:
            new_score = negamax(temp_ot, 2, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        else:
            new_score = negamax_late(temp_ot, 10, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return choice(score_move[1])

def level5(ot, delay):
    moves = ot.get_possible_moves()
    score_move = [-99999, [None]]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax_late(temp_ot, 0, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return choice(score_move[1])

def level6(ot, delay):
    raise NotImplementedError

# Given an othello object state, return the score of that state based on some tile score (max for black aka player 1, min for white)
def heuristic_eval(state):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score


def negamax(ot, depth, alpha, beta):
    if depth == 0 or ot.check_victory() != 0:
        return heuristic_eval(ot.board)
    moves = ot.get_possible_moves()
    ot.check_no_move(moves)
    score = -99999
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax(temp_ot, depth - 1, -beta, -alpha) * (1 if ot.turn == 1 else -1)
        score = max(score, new_score)
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return score * (1 if ot.turn == 1 else -1)


def negamax_late(ot, depth, alpha, beta):
    if depth == 0 or ot.check_victory() != 0:
        return heur_pieces(ot.black_tiles, ot.white_tiles)
    moves = ot.get_possible_moves()
    ot.check_no_move(moves)
    score = -99999
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax_late(temp_ot, depth - 1, -beta, -alpha) * (1 if ot.turn == 1 else -1)
        score = max(score, new_score)
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return score * (1 if ot.turn == 1 else -1)

# Given a board, this function will return the difference of black pieces and white pieces
def heur_pieces(ot_black, ot_white):
    return ot_black - ot_white





# This AI picks the move that maximizes its piece in the next state; it is bad, as it loses quite frequently even with level 1 ai
def extra_ai1(ot, delay):
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

# def AI_1(ot):
#     pass
