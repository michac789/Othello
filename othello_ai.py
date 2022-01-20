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

val2 = [[5, -3, 2, 1, 1, 2, -3, 5],
       [-3, -5, 0, 0, 0, 0, -5, -2],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [-3, -5, 0, 0, 0, 0, -5, -2],
       [5, -3, 2, 1, 1, 2, -3, 5]]

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
    score_move = [-99999, []]
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
    score_move = [-99999, []]
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
    score_move = [-99999, []]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        if ot.move_no < 53: # <51 for better
            new_score = negamax(temp_ot, 2, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        else:
            new_score = negamax_late(temp_ot, 10, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return choice(score_move[1])

def level5(ot):
    moves = ot.get_possible_moves()
    score_move = [-99999, []]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        if ot.move_no < 53:
            new_score = negamax2(temp_ot, 2, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        else:
            new_score = negamax_late(temp_ot, 10, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return choice(score_move[1])

def level6(ot):
    raise NotImplementedError

# Given an othello object state, return the score of that state based on some tile score (max for black aka player 1, min for white)
def heuristic_eval(state):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score

def heuristic_eval2(state):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val2[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score

def negamax(ot, depth, alpha, beta): #TESTED OKAY
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
        if beta <= alpha: break
    return score * (1 if ot.turn == 1 else -1)

def negamax2(ot, depth, alpha, beta):
    if depth == 0 or ot.check_victory() != 0:
        return heuristic_eval2(ot.board)
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

def negamax_late(ot, depth, alpha, beta): #BUGGY
    if depth == 0 or ot.check_victory() != 0:
        return heur_pieces(ot)
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

def heuristic_trial(ot):
    pass

# Given an othello object, this function will return the difference of black pieces and white pieces
def heur_pieces(ot):
    return ot.black_tiles - ot.white_tiles

# Given an othello object, this function will return the number of moves possible to be made
def heur_mobiity(ot):
    moves = ot.get_possible_moves()
    return len(moves)

# Given an othello object, this function .. #TODO
def heur_stable_pieces(ot):
    all_tiles = [(i, j) for i in range(ot.height) for j in range(ot.width)]
    stable_black, stable_white = 0, 0
    for tile in all_tiles:
        tile_color = ot.board[tile[0]][tile[1]]
        if tile_color != 0:
            for t in ot.surrounding_tiles:
                if ot.is_valid_tile((tile[0] + t[0], tile[1] + t[1])):
                    if ot.board[tile[0] + t[0]][tile[1] + t[1]] == tile_color % 2 + 1:
                        pass
                    elif ot.board[tile[0] + t[0]][tile[1] + t[1]] == tile_color: continue
                    elif ot.board[tile[0] + t[0]][tile[1] + t[1]] == 0: break
    raise NotImplementedError

    # def get_possible_moves(self):
    #     possible_moves = set()
    #     all_tiles = [(i, j) for i in range(self.height) for j in range(self.width)]
    #     for tile in all_tiles:
    #         if self.board[tile[0]][tile[1]] == 0:
    #             for t in self.surrounding_tiles:
    #                 if self.is_valid_tile((tile[0] + t[0], tile[1] + t[1])):
    #                     if self.board[tile[0] + t[0]][tile[1] + t[1]] == self.turn % 2 + 1:
    #                         k = 1
    #                         while True:
    #                             k += 1
    #                             if not self.is_valid_tile((tile[0] + t[0] * k, tile[1] + t[1] * k)): break
    #                             if self.board[tile[0] + t[0] * k][tile[1] + t[1] * k] == 0: break
    #                             if self.board[tile[0] + t[0] * k][tile[1] + t[1] * k] == self.turn:
    #                                 possible_moves.add(tile)
    #     return list(possible_moves)

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
