import copy
import sys
import operator
import random


class Othello():
    
    # Initialize an empty board and variables needed; 0: empty, 1: black, 2: white
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        
        # By default, black goes first; keep track for number of white and black tiles
        self.turn = 1
        self.white_tiles = 0
        self.black_tiles = 0
        self.skip_turn = 0
        self.move_no = 0
        self.surrounding_tiles = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i != 0 or j != 0]
        # Used when time runs out in runner.py file to force a certain player to win
        self.force_win = -1 
        # Dictionary mapping move[i] to be made with tuple (current board state, self.skip_turn, move made) for tracking purpose & undo functionality
        self.moves_made = {}
        
        self.tiles_corner = [(0, 0), (0, self.width - 1), (self.height - 1, 0), (self.height - 1, self.width - 1)]
        self.tiles_near_corner = [(0, 1), (1, 0), (1, 1), (0, self.width - 2), (1, self.width - 2), (1, self.width - 1), (self.height - 2, 0), (self.height - 1, 1), (self.height - 2, 1), (self.height - 2, self.width - 1), (self.height - 1, self.width - 2), (self.height - 2, self.width - 2)]
        self.tiles_edge = [(i, j) for i in range(self.height) for j in range(self.width) if i == 0 or i != self.height - 1 or j != 0 or j != self.width - 1]
    
    # Accepts a list of initial white and black tiles to be filled with its respective colors, clear previous board
    def set_initial_position(self, initial_white, initial_black):
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.white_tiles, self.black_tiles, self.move_no = 0, 0, 0
        for tile in initial_white:
            self.board[tile[0]][tile[1]] = 2
            self.white_tiles += 1
        for tile in initial_black:
            self.board[tile[0]][tile[1]] = 1
            self.black_tiles += 1
    
    # Prints the state of the board in the terminal
    def terminal_print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j], end="   ")
            print("")
        print("")
    
    # Return the color given the turn number
    def get_color(self, turn):
        return ("Black" if turn == 1 else "White")
    
    # Returns True if 'tile' is a valid tile on the board, otherwise False
    def is_valid_tile(self, tile):
        return (True if 0 <= tile[0] < self.height and 0 <= tile[1] < self.width else False)

    # Returns a list of all possible valid moves (tiles that can be clicked) in a certain state
    def get_possible_moves(self):
        possible_moves = set()
        all_tiles = [(i, j) for i in range(self.height) for j in range(self.width)]
        for tile in all_tiles:
            if self.board[tile[0]][tile[1]] == 0:
                for t in self.surrounding_tiles:
                    if self.is_valid_tile((tile[0] + t[0], tile[1] + t[1])):
                        if self.board[tile[0] + t[0]][tile[1] + t[1]] == self.turn % 2 + 1:
                            k = 1
                            while True:
                                k += 1
                                if not self.is_valid_tile((tile[0] + t[0] * k, tile[1] + t[1] * k)): break
                                if self.board[tile[0] + t[0] * k][tile[1] + t[1] * k] == 0: break
                                if self.board[tile[0] + t[0] * k][tile[1] + t[1] * k] == self.turn:
                                    possible_moves.add(tile)
        return list(possible_moves)
    
    # Updates the black and white piece count based on the current state of the board
    def update_piece_count(self):
        self.white_tiles, self.black_tiles = 0, 0
        for row in self.board:
            for piece in row:
                if piece == 1: self.black_tiles += 1
                if piece == 2: self.white_tiles += 1
    
    # Updates the board with the current move, assuming that the 'move' parameter should already be valid
    def make_move(self, move):
        self.moves_made[self.move_no] = (copy.deepcopy(self.board), self.skip_turn, move)
        for t in self.surrounding_tiles:
            if self.is_valid_tile((move[0] + t[0], move[1] + t[1])):
                if self.board[move[0] + t[0]][move[1] + t[1]] == self.turn % 2 + 1:
                    k, change = 1, False
                    while(True):
                        k += 1
                        if not self.is_valid_tile((move[0] + t[0] * k, move[1] + t[1] * k)): break
                        if self.board[move[0] + t[0] * k][move[1] + t[1] * k] == 0: break
                        if self.board[move[0] + t[0] * k][move[1] + t[1] * k] == self.turn:
                            change = True
                            break
                    if change:
                        for m in range(k):
                            self.board[move[0] + t[0] * m][move[1] + t[1] * m] = self.turn
        self.turn = self.turn % 2 + 1
        self.move_no += 1
        self.update_piece_count()
    
    # Check for a certain board state, return 2 if white wins, 1 if black wins, 3 if draw, 0 if neither wins
    def check_victory(self):
        if self.force_win != -1: return (self.force_win)
        if self.black_tiles + self.white_tiles == self.height * self.width or self.skip_turn == 2:
            self.moves_made[self.move_no] = (copy.deepcopy(self.board), self.skip_turn, None)
            return (2 if self.white_tiles > self.black_tiles else 1 if self.white_tiles < self.black_tiles else 3)
        return 0
    
    # Undo last move made, revert all self properties to previous state, returns False if no more undo possible, otherwise True
    def undo_move(self):
        if self.move_no != 0:
            self.board = self.moves_made[self.move_no - 1][0]
            self.skip_turn = self.moves_made[self.move_no - 1][1]
            self.move_no -= 1
            self.turn = self.turn % 2 + 1
            self.update_piece_count()
            return True
        return False
    
    # Returns True and create computer move where possible, otherwise returns False
    def make_computer_move(self, level):
        moves = self.get_possible_moves()
        if len(moves) == 0: return False
        if level == 1: move = self.level1(moves)
        if level == 2: move = self.level2(moves)
        if level == 3: move = self.level3(moves)
        self.make_move(move)
        return True
    
    # Level 1 AI: return random move
    def level1(self, moves):
        return random.choice(moves)
    
    # Level 2 AI: minimax algorithm with depth 2
    def level2(self):
        raise NotImplementedError
    
    # Level 3 AI: minimax algorithm with depth 4
    def level3(self):
        raise NotImplementedError
    
    # Return the point of a tile (for minimax algorithm)
    def tile_point(self, tile):
        return (4 if tile in self.tiles_corner else 3 if tile in self.tiles_near_corner else 2 if tile in self.tiles_edge else 1)
    
    # Return the score of a board position
    def heuristic_eval(self):
        score = 0
        for i in range(self.height):
            for j in range(self.width):
                tile_point = self.tile_point((i, j))
                if self.board[i][j] == 1:
                    score += tile_point
                elif self.board[i][j] == 2:
                    score -= tile_point
        return score
    
    # Return move with greatest minimax value (white max, black min)
    def minimax(self):
        pass


# This is used only for initial testing purposes using the terminal
def main():
    
    # Initialize the game (apply standard game settings; can be customized here)
    ot = Othello(8, 8)
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    # Testing purpose
    ot = Othello(4, 4)
    init_white = [(1, 1), (2, 2)]
    init_black = [(1, 2), (2, 1)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    # Prompt for game mode
    while True:
        print("1: human vs human")
        print("2: human vs ai")
        mode = input("Enter mode here: ")
        if mode in ["1", "2"]:
            break
    if mode == "1":
        human_vs_human(ot)
    else:
        while True:
            level = input("Choose AI level (between 1 to 5): ")
            if check_int(level) and 1 <= int(level) <= 5:
                break
        human_vs_ai(ot, int(level))
    
def human_vs_human(ot):
    # Loop through while the game is not ended
    while(True):
        print(f"It is {ot.get_color(ot.turn)}'s turn (Player {ot.turn})")
        
        # Ensure a valid move is given by the user
        moves = ot.get_possible_moves()
        while(True):
            if len(moves) == 0:
                print("No move possible.")
                ot.skip_turn = 1
                ot.turn = ot.turn % 2 + 1
                if ot.skip_turn == 1: ot.skip_turn += 1
                break
            move_y = input("Enter tile's height: ")
            move_x = input("Enter tile's width: ")
            if check_int(move_y) and check_int(move_x) and (int(move_y), int(move_x)) in moves:
                break
            print("Invalid move!")
        
        # Make move, print the board, end the game if someone wins
        if len(moves) != 0:
            ot.make_move((int(move_y), int(move_x)))
            ot.terminal_print()
            if ot.check_victory() != 0:
                break
    
    # Display the winner or draw when game is over
    if ot.check_victory() == 3:
        print("Game Draw.")
    else:
        winner = ("White" if ot.check_victory() == 2 else "Black")
        print(f"Congratulations! {winner} wins the game!")

def human_vs_ai(ot, level):
    # Loop through while the game is not ended; human is player 1 (goes first)
    while(True):
        print(f"It is your turn")
        
        # Ensure a valid move is given by the user
        moves = ot.get_possible_moves()
        while(True):
            if len(moves) == 0:
                print("No move possible.")
                ot.skip_turn = 1
                ot.turn = ot.turn % 2 + 1
                if ot.skip_turn == 1: ot.skip_turn += 1
                break
            move_y = input("Enter tile's height: ")
            move_x = input("Enter tile's width: ")
            if check_int(move_y) and check_int(move_x) and (int(move_y), int(move_x)) in moves:
                break
            print("Invalid move!")
        
        # Make move, print the board, end the game if someone wins
        if len(moves) != 0:
            ot.make_move((int(move_y), int(move_x)))
            ot.terminal_print()
            if ot.check_victory() != 0:
                break
            
        # Make computer move
        if ot.make_computer_move(level):
            ot.terminal_print()
        if ot.check_victory() != 0:
            break
    
    # Display the winner or draw when game is over
    if ot.check_victory() == 3:
        print("Game Draw.")
    elif ot.check_victory() == 1:
        print(f"Congratulations, you win against computer level {level}.")
    elif ot.check_victory() == 2:
        print(f"Computer level {level} wins, try again!")

def check_int(input):
    try:
        x = int(input)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
