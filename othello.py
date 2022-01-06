# python file where all functions and AI are defined

class Othello():
    
    # Initialize an empty board and variables needed; 0: empty, 1: white, 2: black
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.turn = 1
    
    # Accepts a list of initial black and white tiles to be filled with its respective colors
    def initial_position(self, initial_white, initial_black):
        for tile in initial_white:
            self.board[tile] == 1
        for tile in initial_black:
            self.board[tile] == 2
    
    # Prints the state of the board in the terminal
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j], end="   ")
            print("")
    
    # Returns the current state of the board
    def board_state(self):
        return self.board
    
    # Returns the current player's turn
    def player_turn(self):
        return self.turn
    
    def valid_move(self, move):
        pass
    
    # Returns a list containing all possible valid moves
    def possible_move(self):
        pass
    
    # Updates the board with the current move and change player's turn
    def make_move(self, move):
        pass
    
    # Check for a certain board state and turn, return 1 if white wins, 2 if black wins, 0 if neither wins
    def check_victory(self):
        pass


def main():
    ot = Othello(8, 8)
    ot.print()
    
    # main functionality here
    while(True):
        color = ("White" if ot.player_turn == 1 else "Black")
        print(f"It is player {ot.player_turn}'s turn ({color} pieces)")
        while(True):
            move_y = int(input("Enter tile's height: "))
            move_x = int(input("Enter tile's width: "))
            if ot.valid_move((move_y, move_x)):
                break
        ot.make_move((move_y, move_x))
        if ot.check_victory() != 0:
            break
        

if __name__ == "__main__":
    main()
