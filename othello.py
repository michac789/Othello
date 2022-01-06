# python file where all functions and AI are defined

class Othello():
    
    # Initialize the starting board and turn
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.turn = 1
    
    # Prints the state of the board in the terminal
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.board[i][j], end="   ")
            print("")
    
    # Returns the current state of the board
    def board_state(self):
        pass
    
    # Returns the current player's turn
    def player_turn(self):
        pass
    
    # Returns a list containing all possible valid moves
    def possible_move(self, state, turn):
        pass
    
    # Updates the board with the current move
    def make_move(self, move, player):
        pass
    


ot = Othello(8, 8)
ot.print()
