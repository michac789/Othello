import sys


class Othello():
    
    # Initialize an empty board and variables needed; 0: empty, 1: white, 2: black
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.turn = 1
    
    # Accepts a list of initial black and white tiles to be filled with its respective colors
    def set_initial_position(self, initial_white, initial_black):
        for tile in initial_white:
            self.board[tile[0]][tile[1]] = 1
        for tile in initial_black:
            self.board[tile[0]][tile[1]] = 2
    
    # Prints the state of the board in the terminal
    def terminal_print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j], end="   ")
            print("")
        print("")
    
    # Returns the current state of the board
    def board_state(self):
        return self.board
    
    # Returns the current player's turn
    def player_turn(self):
        return self.turn
    
    # Returns True if (tile_y, tile_x) is a valid tile on the board, otherwise False
    def valid_tile(self, tile_y, tile_x):
        return (True if 0 <= tile_y < self.height and 0 <= tile_x < self.width else False)
    
    # Returns True if a move is valid, otherwise False
    def valid_move(self, move):
        direction_list = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i != 0 or j != 0]
        for direction in direction_list:
            if self.valid_tile(move[0] + direction[0], move[0] + direction[1]):
                if self.board[move[0] + direction[0]][move[1] + direction[1]] == self.turn % 2 + 1:
                    k = 1
                    while(True):
                        k += 1
                        if not self.valid_tile(move[0] + direction[0] * k, move[1] + direction[1] * k):
                            break
                        if self.board[move[0] + direction[0] * k][move[1] + direction[1] * k] == 0:
                            break
                        if self.board[move[0] + direction[0] * k][move[1] + direction[1] * k] == self.turn:
                            return True
        return False
    
    # Updates the board with the current move and change player's turn
    def make_move(self, move):
        pass
    
    # Check for a certain board state and turn, return 1 if white wins, 2 if black wins, 0 if neither wins
    def check_victory(self):
        pass
    
    # Returns a list containing all possible valid moves
    def possible_move(self):
        pass


def main():
    ot = Othello(8, 8)
    ot.terminal_print()
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    # main functionality here
    while(True):
        color = ("White" if ot.player_turn() == 1 else "Black")
        print(f"It is player {ot.player_turn()}'s turn ({color} pieces)")
        
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
