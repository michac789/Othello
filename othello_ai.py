"""
All AI algorithms are handled in this file
"""

from copy import deepcopy
from random import choice
from time import sleep

# Given an othello object and ai level, return the move made by the ai
def AI_move(othello, level):
    if level == 1: return level1(othello)
    if level == 2: return level2(othello)
    if level == 3: return level3(othello)
    if level == 4: return level4(othello)
    if level == 5: return level5(othello)
    if level == 6: return level6(othello)

# Level 1 AI: make completely random moves
def level1(ot):
    moves = ot.get_possible_moves()
    sleep(0.5)
    return choice(moves)

# Level 2 AI: the ai tries to maximize its piece count for every move
def level2(ot):
    moves = ot.get_possible_moves()
    score_move = [0, None]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = (temp_ot.white_tiles if temp_ot.turn == 1 else temp_ot.black_tiles)
        if new_score > score_move[0]: score_move = [new_score, move]
    sleep(0.5)
    return score_move[1]

def level3(ot):
    raise NotImplementedError

def level4(ot):
    raise NotImplementedError

def level5(ot):
    raise NotImplementedError

def level6(ot):
    raise NotImplementedError

# def AI_1(ot):
#     pass
