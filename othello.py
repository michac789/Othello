import copy


class Othello():
    
    # Initialize an empty board and variables needed; 0: empty, 1: black, 2: white; black goes first by default
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.turn = 1
        self.white_tiles = 0
        self.black_tiles = 0
        self.move_no = 0
        self.surrounding_tiles = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i != 0 or j != 0]
        self.no_more_move = False # Changes to True when there are no more moves available for both players
        self.force_win = -1 # Used when time runs out (in time mode) to force a certain player to win
        self.moves_made = {} # Dictionary mapping move_no with the tuple (board state, player turn to move, move made)
    
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
        return ("Black" if turn == 1 else "White" if turn == 2 else "INVALID")
    
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
                                if self.board[tile[0] + t[0] * k][tile[1] + t[1] * k] == self.turn: possible_moves.add(tile)
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
        self.moves_made[self.move_no] = (copy.deepcopy(self.board), self.turn, move)
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
        if self.black_tiles + self.white_tiles == self.height * self.width or self.no_more_move == True:
            self.moves_made[self.move_no] = (copy.deepcopy(self.board), self.turn, None)
            return (2 if self.white_tiles > self.black_tiles else 1 if self.white_tiles < self.black_tiles else 3)
        return 0
    
    # Always call this function once after making a move, updates turn when necessary and update no_more_move if there are no more moves
    def check_no_move(self, moves):
        if len(moves) == 0:
            self.turn = self.turn % 2 + 1
            if len(self.get_possible_moves()) == 0: self.no_more_move = True
            return True
        return False
    
    # Undo last move made, revert self objects to previous state
    def undo_move(self):
        if self.move_no > 0:
            self.board = self.moves_made[self.move_no - 1][0]
            self.turn = self.moves_made[self.move_no - 1][1]
            self.move_no -= 1
            self.update_piece_count()


# This is used only for initial testing purposes using the terminal
def main():
    
    # Initialize the game (apply standard game settings; can be customized here)
    ot = Othello(8, 8)
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    ot.terminal_print()
    
    # Testing purpose
    # ot = Othello(4, 4)
    # init_white = [(1, 1), (2, 2)]
    # init_black = [(1, 2), (2, 1)]
    # ot.set_initial_position(init_white, init_black)
    # ot.terminal_print()
    
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

def human_vs_ai(ot, level): #THIS IS NOT FUNCTIONING ANYMORE
    raise NotImplemented
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
