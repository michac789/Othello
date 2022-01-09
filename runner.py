import pygame
import sys
import math

from othello import Othello
from helper import *


class Game():
    
    def __init__(self):
        self.dim_height = 8
        self.dim_width = 8
        
        self.ot = Othello(8, 8)
        
        self.screen_width = 800
        self.screen_height = 450
        self.board_padding = self.screen_height / 15
        
        self.size = width, height = 800, 450
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        
        # Compute board sizes
        self.board_width = ((9 / 16) * self.screen_width) - (2 * self.board_padding)
        self.board_height = self.screen_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        
        self.game_state = "start"
        self.game_prep = False
        
    def run(self):
        # Initialize game with 9:16 resizable aspect ratio
        pygame.init()
        pygame.display.set_caption("Othello")

        
        while True:
            # Terminate application when the game is quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.ext()
                elif event.type == pygame.VIDEORESIZE:
                    print("dfsf")
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    #screen.blit(surface, screen)
                    # TO-DO: resize feature

                if self.game_state == "start":
                    self.state_mainmenu()
                    continue
                
                if self.game_state == "play":
                    self.state_play()
                    continue
                
                pygame.display.flip()
                
    def state_mainmenu(self):
        # Display title
        self.screen.fill(black)
        title = titleFont.render("Hello Othello", True, white)
        titleRect = title.get_rect()
        titleRect.center = (self.screen_width / 2, 50)
        self.screen.blit(title, titleRect)
        
        # Display play button
        buttonRect = pygame.Rect((self.screen_width / 4), (9 / 16) * self.screen_height, self.screen_width / 2, 50)
        buttonText = buttonFont.render("Play Game", True, black)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(self.screen, white, buttonRect)
        self.screen.blit(buttonText, buttonTextRect)
        
        # Change the game_state to "play" if play button is left-clicked
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                self.game_state = "play"
        
        pygame.display.flip()

    def state_play(self):
        
        # Initialize game with default settings (first time only)
        if not self.game_prep:
            init_white = [(3, 3), (4, 4)]
            init_black = [(3, 4), (4, 3)]
            self.ot.set_initial_position(init_white, init_black)
            self.ot.turn = 2
            self.game_prep = True
        
        # Draw board and all the tiles
        self.screen.fill(black)
        tiles = []
        for i in range(self.dim_height):
            row_tiles = []
            for j in range(self.dim_width):
                rect = pygame.Rect(self.board_start[0] + j * self.tile_size, self.board_start[1] + i * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, tile_color, rect)
                pygame.draw.rect(self.screen, board_color, rect, 3)
                row_tiles.append(rect)
            tiles.append(row_tiles)
        
        # Draw each pieces that are present in the board, including all tiles with possible move
        moves = self.ot.get_possible_moves()
        for i in range(self.dim_height):
            for j in range(self.dim_width):
                coordinate = (self.board_start[0] + j * self.tile_size + self.tile_size / 2, self.board_start[1] + i * self.tile_size + self.tile_size / 2)
                if self.ot.board[i][j] != 0:
                    circ = pygame.draw.circle(self.screen, tile_border_color, coordinate, self.piece_radius + 2)
                    circ = pygame.draw.circle(self.screen, (white if self.ot.board[i][j] == 1 else black), coordinate, self.piece_radius)
                if (i, j) in moves:
                    circ = pygame.draw.circle(self.screen, moves_color, coordinate, self.piece_radius, int(self.piece_radius / 2))
        
        # Update changes when a valid tile is clicked
        left, _, right = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            for i in range(self.dim_height):
                for j in range(self.dim_width):
                    if tiles[i][j].collidepoint(mouse):
                        if (i, j) in moves:
                            self.ot.make_move((i, j))
                        # ot.terminal_print()
                        # if ot.check_victory() != 0:
                        #     break
        
        pygame.display.flip()         
            


def main():
    game = Game()
    game.run()

main()
