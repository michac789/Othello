"""
All AI algorithms are handled in this file
"""

from copy import deepcopy
from random import choice
from time import sleep
from pickle import load
from othello import Othello


# Board score based on position used for heuristic function
val1 = [[10, -3, 2, 1, 1, 2, -3, 10],
       [-3, -5, 0, 0, 0, 0, -5, -3],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [2, 0, 0, 0, 0, 0, 0, 2],
       [-3, -5, 0, 0, 0, 0, -5, -3],
       [10, -3, 2, 1, 1, 2, -3, 10]]

val2 = [[10, -3, 2, 1, 1, 2, -3, 10],
       [-3, -5, -1, -1, -1, -1, -5, -3],
       [2, -1, 2, 0, 0, 2, -1, 2],
       [1, -1, 0, 0, 0, 0, -1, 1],
       [1, -1, 0, 0, 0, 0, -1, 1],
       [2, -1, 2, 0, 0, 2, -1, 2],
       [-3, -5, -1, -1, -1, -1, -5, -3],
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
    moves = ot.get_possible_moves()
    score_move = [-99999, []]
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax3(temp_ot, 2, -99999, 99999) * (1 if temp_ot.turn == 2 else -1)
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
            score += val1[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score

def heuristic_eval3(state):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val2[i][j] * (1 if state[i][j] == 1 else -1 if state[i][j] == 2 else 0)
    return score

def heuristic_eval2(state, turn):
    model = load(open("trial_model2.sav", 'rb'))
    prob_array = model.predict_proba([get_values(state, turn)])
    score = int(prob_array[0][2] * 20 - 10)
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

def negamax3(ot, depth, alpha, beta): #TESTED OKAY
    if depth == 0 or ot.check_victory() != 0:
        return heuristic_eval3(ot.board)
    moves = ot.get_possible_moves()
    ot.check_no_move(moves)
    score = -99999
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax3(temp_ot, depth - 1, -beta, -alpha) * (1 if ot.turn == 1 else -1)
        score = max(score, new_score)
        alpha = max(alpha, score)
        if beta <= alpha: break
    return score * (1 if ot.turn == 1 else -1)

def negamax2(ot, depth, alpha, beta):
    if depth == 0 or ot.check_victory() != 0:
        x = heuristic_eval2(ot.board, ot.turn)
        return x
    moves = ot.get_possible_moves()
    ot.check_no_move(moves)
    score = -99999
    for move in moves:
        temp_ot = deepcopy(ot)
        temp_ot.make_move(move)
        new_score = negamax2(temp_ot, depth - 1, -beta, -alpha) * (1 if ot.turn == 1 else -1)
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

# Returns the difference between the black pieces and white pieces
def heur_pieces(board):
    black_tiles, white_tiles = count_tiles(board)
    return black_tiles - white_tiles

# Returns a weighted score of a board state based on different tile weights
def heur_weight(board):
    score = 0
    for i in range(8):
        for j in range(8):
            score += val2[i][j] * (1 if board[i][j] == 1 else -1 if board[i][j] == 2 else 0)
    return score

# Returns the difference between the possible move that can be made by black and white on a certain state
def heur_mobility(board):
    temp_ot = Othello(8, 8)
    temp_ot.board = board
    temp_ot.turn = 1
    moves_black = len(temp_ot.get_possible_moves())
    temp_ot.turn = 2
    moves_white = len(temp_ot.get_possible_moves())
    return moves_black - moves_white

# Returns 1 if black is expected to make the last move in the game, otherwise returns -1
def heur_parity(board, turn):
    black_tiles, white_tiles = count_tiles(board)
    empty_tiles = 64 - black_tiles - white_tiles
    return (-1 * (1 if turn == 1 else -1) if empty_tiles % 2 == 0 else 1 * (1 if turn == 1 else -1))

# Returns the difference of lower bound of stable black and white tiles on the sides only
def heur_stablility(board):
    sides = [[board[0][i] for i in range(8)], [board[7][i] for i in range(8)], [board[i][0] for i in range(8)], [board[i][7] for i in range(8)]]
    score = sum(check_stable_side(side) for side in sides)
    score += sum((1 if board[x[0]][x[1]] == 1 else - 1) if board[x[0]][x[1]] != 0 else 0 for x in [(0, 0), (0, 7), (7, 0), (7, 7)])
    return score

# Returns the difference of stable black and white tiles on a side excluding the corner
def check_stable_side(tiles):
    if all(tile != 0 for tile in tiles):
        return sum((1 if tiles[i] == 1 else -1) for i in range(1, 7, 1))
    score = 0
    if tiles[0] != 0:
        for i in range(6):
            if tiles[1 + i] == tiles[0]:
                score += (1 if tiles[0] == 1 else -1)
            else: break
    if tiles[7] != 0:
        for i in range(6):
            if tiles[6 - i] == tiles[7]:
                score += (1 if tiles[7] == 1 else -1)
            else: break
    return score

# Given a board, returns the number of black tiles, number of white tiles
def count_tiles(board):
    black_tiles, white_tiles = 0, 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1: black_tiles += 1
            if board[i][j] == 2: white_tiles += 1
    return black_tiles, white_tiles

def get_values(board, turn):
    a, b, c, d, e, f, g, h, i, j = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for p in range(8):
        for q in range(8):
            mul = (1 if board[p][q] == 1 else -1 if board[p][q] == 2 else 0)
            if (p, q) in [(0, 0), (0, 7), (7, 0), (7, 7)]: a += 1 * mul
            if (p, q) in [(0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (6, 7), (7, 6)]: b += 1 * mul
            if (p, q) in [(0, 2), (2, 0), (0, 5), (2, 7), (5, 0), (7, 2), (5, 7), (7, 5)]: c += 1 * mul
            if (p, q) in [(0, 3), (3, 0), (0, 4), (3, 7), (4, 0), (7, 3), (4, 7), (7, 4)]: d += 1 * mul
            if (p, q) in [(1, 1), (1, 6), (6, 1), (6, 6)]: e += 1 * mul
            if (p, q) in [(1, 2), (2, 1), (1, 5), (2, 6), (5, 1), (6, 2), (5, 6), (6, 5)]: f += 1 * mul
            if (p, q) in [(1, 3), (3, 1), (1, 4), (3, 6), (4, 1), (6, 3), (4, 6), (6, 4)]: g += 1 * mul
            if (p, q) in [(2, 2), (2, 5), (5, 2), (5, 5)]: h += 1 * mul
            if (p, q) in [(2, 3), (2, 4), (3, 2), (3, 5), (4, 2), (4, 5), (5, 3), (5, 4)]: i += 1 * mul
            if (p, q) in [(3, 3), (4, 4), (4, 4), (3, 3)]: j += 1 * mul
    return [a, b, c, d, e, f, g, h, i, j, turn]

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
