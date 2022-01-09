import pygame
import sys
import math

from othello import Othello

# Global variable for size of the board
HEIGHT = 8
WIDTH = 8

# Define RGB values of different colors for various components here
black = (0, 0, 0)
white = (255, 255, 255)
tile_color = (0, 160, 0)
tile_border = (110, 38, 14)
board_color = (50, 50, 50)

# Initialize game with 9:16 aspect ratio
pygame.init()
size = width, height = 800, 450
screen = pygame.display.set_mode(size)

# Define various fonts here
OPEN_SANS = "OpenSans-Regular.ttf"
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 20)
hugeFont = pygame.font.Font(OPEN_SANS, 40)

titleFont = pygame.font.Font(OPEN_SANS, 50)
buttonFont = pygame.font.Font(OPEN_SANS, 30)

# Compute board size
board_padding = 30
board_width = ((9 / 16) * width) - (2 * board_padding)
board_height = height - (2 * board_padding)
tile_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_start = (board_padding, board_padding)
piece_radius = math.floor(tile_size / 2 - 5)

# Initialize game (CHANGED TO LATER PARTS)
# ot = Othello(8, 8)
# init_white = [(3, 3), (4, 4)]
# init_black = [(3, 4), (4, 3)]
# ot.set_initial_position(init_white, init_black)

# States: start (for main menu)
game_state = "start"
game_prep = False

ot = Othello(8, 8) #??

def main():
    while True:

        # Terminate application when the game is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.ext()
            
        screen.fill(black)
                
        if game_state == "start":
            state_mainmenu()
            continue
        
        if game_state == "play":
            state_play()
            continue


def state_mainmenu():
    
    # Display title
    screen.fill(black)
    title = titleFont.render("Hello Othello", True, white)
    titleRect = title.get_rect()
    titleRect.center = (width / 2, 50)
    screen.blit(title, titleRect)
    
    # Display play button
    buttonRect = pygame.Rect((width / 4), (9 / 16) * height, width / 2, 50)
    buttonText = buttonFont.render("Play Game", True, black)
    buttonTextRect = buttonText.get_rect()
    buttonTextRect.center = buttonRect.center
    pygame.draw.rect(screen, white, buttonRect)
    screen.blit(buttonText, buttonTextRect)
    
    # Change the game_state to "play" if play button is clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse):
            global game_state
            game_state = "play"
    
    pygame.display.flip()


def state_play():
    
    # Initialize game with default settings (first time only)
    global game_prep
    if not game_prep:
        init_white = [(3, 3), (4, 4)]
        init_black = [(3, 4), (4, 3)]
        ot.set_initial_position(init_white, init_black)
        game_prep = True
    
    # Draw board and all the tiles
    screen.fill(black)
    tiles = []
    for i in range(HEIGHT):
        row_tiles = []
        for j in range(WIDTH):
            rect = pygame.Rect(board_start[0] + j * tile_size,board_start[1] + i * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, tile_color, rect)
            pygame.draw.rect(screen, board_color, rect, 3)
            row_tiles.append(rect)
        tiles.append(row_tiles)

    # Draw each pieces that are present in the board
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if ot.board[i][j] != 0:
                coordinate = (board_start[0] + j * tile_size + tile_size / 2, board_start[1] + i * tile_size + tile_size / 2)
                circ = pygame.draw.circle(screen, tile_border, coordinate, piece_radius + 2)
                circ = pygame.draw.circle(screen, (white if ot.board[i][j] == 1 else black), coordinate, piece_radius)
    
    # ..         
    left, _, right = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    
    if left == 1:
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if tiles[i][j].collidepoint(mouse):
                    ot.make_move((i, j))
                    # ot.terminal_print()
                    # if ot.check_victory() != 0:
                    #     break
    
    pygame.display.flip()
        
main()
