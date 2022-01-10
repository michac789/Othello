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
        self.surrounding_tiles = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i != 0 or j != 0]
        
        self.tiles_corner = [(0, 0), (0, self.width - 1), (self.height - 1, 0), (self.height - 1, self.width - 1)]
        self.tiles_near_corner = [(0, 1), (1, 0), (1, 1), (0, self.width - 2), (1, self.width - 2), (1, self.width - 1), (self.height - 2, 0), (self.height - 1, 1), (self.height - 2, 1), (self.height - 2, self.width - 1), (self.height - 1, self.width - 2), (self.height - 2, self.width - 2)]
        self.tiles_edge = [(i, j) for i in range(self.height) for j in range(self.width) if i == 0 or i != self.height - 1 or j != 0 or j != self.width - 1]
    
    # Accepts a list of initial white and black tiles to be filled with its respective colors, clear previous board
    def set_initial_position(self, initial_white, initial_black):
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.white_tiles, self.black_tiles = 0, 0
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
        self.update_piece_count()
    
    # Check for a certain board state, return 2 if white wins, 1 if black wins, 3 if draw, 0 if neither wins
    def check_victory(self):
        if self.black_tiles + self.white_tiles == self.height * self.width or self.skip_turn == 2:
            return (2 if self.white_tiles > self.black_tiles else 1 if self.white_tiles < self.black_tiles else 3)
        return 0
    
    # Level 1 AI: return random move
    def level1(self):
        return random.choice(self.get_possible_moves())
    
    # Level 2 AI: minimax algorithm with depth 2
    def level2(self):
        pass
    
    # Level 3 AI: minimax algorithm with depth 4
    def level3(self):
        pass
    
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
    
    # Initialize the game (apply standard game settings)
    ot = Othello(8, 8)
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    # Loop through while the game is not ended
    while(True):
        color = ("White" if ot.turn == 2 else "Black")
        print(f"It is player {color}'s turn.")
        
        # Ensure a valid move is given by the user
        moves = ot.get_possible_moves()
        while(True):
            if len(moves) == 0:
                print("No moves possible")
                ot.skip_turn = 1
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
    
    # Display the winner when someone wins
    winner = ("White" if ot.check_victory() == 2 else "Black")
    print(f"Congratulations! {winner} wins the game!")

def check_int(input):
    try:
        x = int(input)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
