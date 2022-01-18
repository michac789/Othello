"""
Simulator
"""

from turtle import window_width
from othello import Othello
from othello_ai import AI_move

N = 1000

def main():
    win_black = 0
    win_white = 0
    for i in range(N):
        print(f"Playing game {i+1} out of {N}...")
        ot = Othello(8, 8)
        ot.set_initial_position([(3, 3), (4, 4)], [(3, 4), (4, 3)])
        while True:
            moves = ot.get_possible_moves()
            ot.check_no_move(moves)
            if ot.check_victory() != 0:
                break
            if ot.turn == 1:
                ot.make_move(AI_move(ot, 1, False))
            elif ot.turn == 2:
                ot.make_move(AI_move(ot, 1, False))
        print(ot.moves_made) #TODO - IMPORT CSV FILE
        if ot.check_victory() == 1:
            win_black += 1
        elif ot.check_victory() == 2:
            win_white += 1
    print(f"Out of {N} games, black wins {win_black} times, white wins {win_white} times, and {N - win_black - win_white} draws.")


main()
