"""
All AI algorithms are handled in this file
"""

from copy import deepcopy
from random import choice
from time import sleep


def AI_move(othello, level):
    if level == 1: return level1(deepcopy(othello))
    if level == 2: return level2(deepcopy(othello))
    if level == 3: return level3(deepcopy(othello))

def level1(ot):
    moves = ot.get_possible_moves()
    sleep(0.5)
    return choice(moves)

def level2(ot):
    pass

def level3(ot):
    pass

