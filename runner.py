import pygame
import sys
import math

from othello import Othello

# Global variable for size of the board
HEIGHT = 8
WIDTH = 8

# Define RGB values of different colors here
black = (0, 0, 0)
white = (255, 255, 255)
tile_color = (0, 160, 0)
board_color = (50, 50, 50)

# Initialize game with 9:16 aspect ratio
pygame.init()
size = width, height = 800, 450
screen = pygame.display.set_mode(size)

# Define various fonts here
OPEN_SANS = "OpenSans-Regular.ttf"
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 20)
hugeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
board_padding = 30
board_width = ((9 / 16) * width) - (2 * board_padding)
board_height = height - (2 * board_padding)
tile_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_start = (board_padding, board_padding)
piece_radius = math.floor(tile_size / 2 - 5)

while True:
    game_state = "start"
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.ext()
            
    if game_state == "start":
        title = smallFont.render("Hello Othello", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width - 150), 50)
        screen.blit(title, titleRect)
        # do something here
    
    # rect = pygame.Rect(30, 30, 100, 100)
    # pygame.draw.rect(screen, board_color, rect)
        
    ot = Othello(8, 8)
    init_white = [(3, 3), (4, 4)]
    init_black = [(3, 4), (4, 3)]
    ot.set_initial_position(init_white, init_black)
    
    tiles = []
    for i in range(8):
        row_tiles = []
        for j in range(8):
            rect = pygame.Rect(
                board_start[0] + j * tile_size,
                board_start[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, tile_color, rect)
            pygame.draw.rect(screen, board_color, rect, 3)
    for i in range(8):
        for j in range(8):
            if ot.board [i][j] == 1:
                circ = pygame.draw.circle(screen, white, (board_start[0] + j * tile_size + tile_size / 2, board_start[1] + i * tile_size + tile_size / 2), piece_radius)

    
    pygame.display.flip()