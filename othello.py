import sys
import operator


class Othello():
    
    # Initialize an empty board and variables needed; 0: empty, 1: white, 2: black
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.turn = 2
        self.white_tiles = 0
        self.black_tiles = 0
        
        self.surrounding_tiles = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i != 0 or j != 0]
        self.tiles_corner = [(0, 0), (0, self.width - 1), (self.height - 1, 0), (self.height - 1, self.width - 1)]
        self.tiles_near_corner = [(0, 1), (1, 0), (1, 1), (0, self.width - 2), (1, self.width - 2), (1, self.width - 1), (self.height - 2, 0), (self.height - 1, 1), (self.height - 2, 1), (self.height - 2, self.width - 1), (self.height - 1, self.width - 2), (self.height - 2, self.width - 2)]
        self.tiles_edge = [(i, j) for i in range(self.height) for j in range(self.width) if i == 0 or i != self.height - 1 or j != 0 or j != self.width - 1]
    
    # Accepts a list of initial white and black tiles to be filled with its respective colors, clear previous board
    def set_initial_position(self, initial_white, initial_black):
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        for tile in initial_white:
            self.board[tile[0]][tile[1]] = 1
            self.white_tiles += 1
        for tile in initial_black:
            self.board[tile[0]][tile[1]] = 2
            self.black_tiles += 1
    
    # Prints the state of the board in the terminal
    def terminal_print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j], end="   ")
            print("")
        print("")
    
    # Returns True if 'tile' is a valid tile on the board, otherwise False
    def is_valid_tile(self, tile):
        return (True if 0 <= tile[0] < self.height and 0 <= tile[1] < self.width else False)
    
    # Returns a list of all surrounding valid tiles, given a single tile
    def get_surrounding_tiles(self, tile):
        tiles = [tuple(map(operator.add, tile, s_tile)) for s_tile in self.surrounding_tiles]
        return [tile for tile in tiles if self.is_valid_tile(tile)]

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

    # Updates the board with the current move, assuming that the 'move' parameter should already be valid
    def make_move(self, move):
        for t in self.surrounding_tiles:
            if self.is_valid_tile(move[0] + t[0], move[0] + t[1]):
                if self.board[move[0] + t[0]][move[1] + t[1]] == self.turn % 2 + 1:
                    k, change = 1, False
                    while(True):
                        k += 1
                        if not self.is_valid_tile(move[0] + t[0] * k, move[1] + t[1] * k): break
                        if self.board[move[0] + t[0] * k][move[1] + t[1] * k] == 0: break
                        if self.board[move[0] + t[0] * k][move[1] + t[1] * k] == self.turn:
                            change = True
                            break
                    if change:
                        for m in range(k):
                            self.board[move[0] + t[0] * m][move[1] + t[1] * m] = self.turn
        self.turn = self.turn % 2 + 1
                    
    
    # Check for a certain board state and turn, return 1 if white wins, 2 if black wins, 3 if draw, 0 if neither wins
    def check_victory(self):
        if self.black_tiles + self.white_tiles == self.height * self.width or self.white_tiles == 0 or self.black_tiles == 0:
            return (1 if self.white_tiles > self.black_tiles else 2)
        return 0
    
    # Level 1 AI: return random move
    def level1(self):
        pass
    
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


def main():
    ot = Othello(8, 8)
    ot.terminal_print()
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    sys.exit()
    
    # main functionality here
    while(True):
        color = ("White" if ot.turn == 1 else "Black")
        print(f"It is player {ot.turn}'s turn ({color} pieces)")
        
        print(ot.possible_moves())
        while(True):
            move_y = int(input("Enter tile's height: "))
            move_x = int(input("Enter tile's width: "))
            if ot.valid_move((move_y, move_x)):
                break
            print("Invalid move, please try another move.")
            
        ot.make_move((move_y, move_x))
        ot.terminal_print()
        if ot.check_victory() != 0:
            break


if __name__ == "__main__":
    main()
