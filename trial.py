from othello import Othello
from othello_ai import *

ot = Othello(8, 8)
ot.board = [[1,1,2,0,0,0,0,0],[1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,1,0,0,0],
         [0,0,0,1,2,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
# x = get_values(board)
# print(x)

print(heur_pieces(ot))
print(heur_weight(ot))
print(heur_mobility(ot))

list = [1,1,0,1,2,2,2,2]
print(check_stable_side(list))




