"""
Simulator
"""

from sre_parse import State
from othello import Othello
from othello_ai import AI_move
from csv import writer


# Modify this function
def main():
    #simulate(100, 3, 4)
    #export_data(20, 4, 5)
    export_tile_heur(10, 1, 1)

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
            moves = ot.get_possible_moves()
            if ot.check_victory() != 0: break
            if ot.turn == 1: ot.make_move(AI_move(ot, level_black, False))
            elif ot.turn == 2: ot.make_move(AI_move(ot, level_white, False))
        if ot.check_victory() == 1: win_black += 1
        elif ot.check_victory() == 2: win_white += 1
    print(f"Out of {N} games, black wins {win_black} times, white wins {win_white} times, and {N - win_black - win_white} draws.")
    win_rate_b, win_rate_w = round(win_black * 100 / N, 2), round(win_white * 100 / N, 2)
    print(f"Win rate: black {win_rate_b}%, white {win_rate_w}%, draw {abs(round(100 - win_rate_b - win_rate_w, 2))}%")

# Write the data to a csv file containing tile heuristic
#  a  b  c  d
#  b  e  f  g
#  c  f  h  i
#  d  g  i  j  (x4 quadrants; only applies for 8x8 board)
# csv writer order: turn,a,b,c,d,e,f,g,h,i,j,outcome
def export_tile_heur(N, level_black, level_white):
    win_black, win_white = 0, 0
    games_data = []
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
        winner = ot.check_victory()
        if winner == 1: win_black += 1
        elif winner == 2: win_white += 1
        
        with open("data.csv", "a", newline = "") as infile:
            csv_writer = writer(infile)
            move_no = 0
            for key in ot.moves_made.keys():
                row = get_values(ot.moves_made[key][0])
                row.append(move_no)
                move_no += 1
                if winner == 3: row.append(0)
                elif winner == ot.moves_made[key][1]: row.append(1)
                else: row.append(-1)
                csv_writer.writerow(row)
                
    print(f"Out of {N} games, black wins {win_black} times, white wins {win_white} times, and {N - win_black - win_white} draws.")
    win_rate_b, win_rate_w = round(win_black * 100 / N, 2), round(win_white * 100 / N, 2)
    print(f"Win rate: black {win_rate_b}%, white {win_rate_w}%, draw {abs(round(100 - win_rate_b - win_rate_w, 2))}%")

# Return a list containing 10 values of a certain board state; see above comments for more detail
def get_values(board):
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
    return [a, b, c, d, e, f, g, h, i, j]

# Simulates N game played by 2 ai levels, exporting necessary information to an external csv file for learning purpose
def export_data(N, level_black, level_white):
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
        
        with open("data.csv", "w", newline = "") as infile:
            csv_writer = writer(infile)
            for key in ot.moves_made.keys():
                row = []
                row.append(ot.moves_made[key][0])
                row.append(ot.moves_made[key][1])
                row.append(ot.moves_made[key][2])
                csv_writer.writerow(row)
            
    print(f"Out of {N} games, black wins {win_black} times, white wins {win_white} times, and {N - win_black - win_white} draws.")
    win_rate_b, win_rate_w = round(win_black * 100 / N, 2), round(win_white * 100 / N, 2)
    print(f"Win rate: black {win_rate_b}%, white {win_rate_w}%, draw {abs(round(100 - win_rate_b - win_rate_w, 2))}%")


main()
