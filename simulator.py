"""
Simulator
"""

from othello import Othello
from othello_ai import AI_move

N = 1000

def main():
    simulate(11, 1, 1)


# This function simulates N games with 2 ai levels representing black and white, printing the number and percentage of wins, loses and draws
def simulate(N, level_black, level_white):
    win_black, win_white = 0, 0
    for i in range(N):
        print(f"Playing game {i+1} out of {N}...")
        ot = Othello(8, 8)
        ot.set_initial_position([(3, 3), (4, 4)], [(3, 4), (4, 3)])
        while True:
            moves = ot.get_possible_moves()
            ot.check_no_move(moves)
            if ot.check_victory() != 0: break
            if ot.turn == 1: ot.make_move(AI_move(ot, level_black, False))
            elif ot.turn == 2: ot.make_move(AI_move(ot, level_white, False))
        if ot.check_victory() == 1: win_black += 1
        elif ot.check_victory() == 2: win_white += 1
    print(f"Out of {N} games, black wins {win_black} times, white wins {win_white} times, and {N - win_black - win_white} draws.")
    win_rate_b, win_rate_w = round(win_black * 100 / N, 2), round(win_white * 100 / N, 2)
    print(f"Win rate: black {win_rate_b}%, white {win_rate_w}%, draw {abs(round(100 - win_rate_b - win_rate_w, 2))}%")


main()
