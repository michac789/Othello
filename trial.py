# from simulator import get_values

board = [[1,1,2,0,0,0,0,0],[1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,1,0,0,0],
         [0,0,0,1,2,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
# x = get_values(board)
# print(x)

from othello_ai import *

x = heuristic_eval2(board, 50)


