import pygame
import sys
import math

from othello import Othello
from helper import *


class Game():
    
    def __init__(self):
        # Initialize default board size and othello object
        self.dim_height = 8
        self.dim_width = 8
        self.ot = Othello(8, 8)
        
        # Initialize pygame, set title, set default screen size with 9:16 resizable aspect ratio
        self.screen_width = 800
        self.screen_height = 450
        pygame.init()
        pygame.display.set_caption("Othello")
        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
        
        # Compute various component sizes relative to screen_width and screen_height
        self.board_padding = self.screen_height / 15
        self.board_width = ((9 / 16) * self.screen_width) - (2 * self.board_padding)
        self.board_height = self.screen_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        
        # Keep track of game menus and states (state machine updator)
        # Menu: start, play, pre_classic, pre_custom, pre_puzzle, tutorial, leaderboard
        # State (when menu is play): prep, play, end
        self.game_menu = "start"
        self.game_state = "prep"
        
        self.recent_move = None
    
    # Resize components relative to the overall screen width and height while maintaining 9:16 ratio
    def resize(self):
        self.board_padding = self.screen_height / 15
        self.board_width = ((9 / 16) * self.screen_width) - (2 * self.board_padding)
        self.board_height = self.screen_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        
    def run(self):
        while True:
            # Terminate application when the game is quit, smart resizable window feature
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.ext()
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen_height, self.screen_width = event.h, event.w
                    self.resize()

            # Based on 'state machine' concept, launch different states of the game depending on self.game_state
            if self.game_menu == "start":
                self.state_mainmenu()
            elif self.game_menu == "play":
                self.state_play()
            # TODO
            elif self.game_menu == "pre_classic":
                pass
                
    def state_mainmenu(self):
        # Display title
        self.screen.fill(black)
        title = titleFont.render("Hello Othello", True, white)
        titleRect = title.get_rect()
        titleRect.center = (self.screen_width / 2, 50)
        self.screen.blit(title, titleRect)
        
        # Display buttons (classic mode, custom mode, puzzle mode)
        button_texts = ["Classic Mode", "Custom Mode", "Puzzle Mode"]
        button_dict = {}
        for i in range(3):
            buttonRect = pygame.Rect((self.screen_width / 4), ((6 + 2 * i) / 16) * self.screen_height, self.screen_width / 2, self.screen_height / 10)
            button_dict[i] = buttonRect
            buttonText = buttonFont.render(button_texts[i], True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, white, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        # Change the game_menu to "play" if play button is left-clicked
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            mouse = pygame.mouse.get_pos()
            if button_dict[0].collidepoint(mouse): self.game_menu = "play"
            #if button_dict[1].collidepoint(mouse): self.game_menu = "???" #TODO
            #if button_dict[1].collidepoint(mouse): self.game_menu = "???" #TODO
        
        pygame.display.flip()

    def state_play(self):
        
        # Initialize game with default settings (first time only)
        if self.game_state == "prep":
            init_white = [(3, 3), (4, 4)]
            init_black = [(3, 4), (4, 3)]
            self.ot.set_initial_position(init_white, init_black)
            self.ot.turn = 1
            self.game_state = "play"
        
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
                    circ = pygame.draw.circle(self.screen, (white if self.ot.board[i][j] == 2 else black), coordinate, self.piece_radius)
                if (i, j) in moves:
                    circ = pygame.draw.circle(self.screen, moves_color, coordinate, self.piece_radius, int(self.piece_radius / 2))
                if self.recent_move == (i, j):
                    circ = pygame.draw.circle(self.screen, recent_move_color, coordinate, self.piece_radius / 3)
                    
        # Display scoreboard
        button_texts = ["Black", "White", f"{self.ot.black_tiles}", f"{self.ot.white_tiles}"]
        button_dict = {}
        scoreRect = pygame.Rect((self.screen_width * 0.55), (self.screen_height * 0.1), (self.screen_width * 0.4), (self.screen_height * 0.3))
        pygame.draw.rect(self.screen, white, scoreRect)
        for i in range(4):
            if i == 0 or i == 1:
                buttonRect = pygame.Rect((self.screen_width * (0.58 + i * 0.18)), (self.screen_height * 0.3), self.screen_width / 6, self.screen_height / 15)
            else:
                buttonRect = pygame.Rect((self.screen_width * (0.22 + i * 0.18)), (self.screen_height * 0.12), self.screen_width / 6, self.screen_height / 5)
            button_dict[i] = buttonRect
            buttonText = smallFont.render(button_texts[i], True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, score_color, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
            
        # Display other buttons and utilities
        button_texts = ["Turn", "Winner", "Undo", "Quit"]
        for i in range(4, 8, 1):
            if i == 4 or i == 5:
                buttonRect = pygame.Rect((self.screen_width * 0.55), (self.screen_height * (0.45 + (i - 4) / 6)), self.screen_width * 0.4, self.screen_height / 8)
            else:
                buttonRect = pygame.Rect((self.screen_width * (0.55 + (i - 6) * 0.2)), (self.screen_height * 0.79), self.screen_width * 0.18, self.screen_height / 8)
            button_dict[i] = buttonRect
            buttonText = smallFont.render(button_texts[i - 4], True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, score_color, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        # Update changes when a valid tile is clicked
        left, _, _ = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            for i in range(self.dim_height):
                for j in range(self.dim_width):
                    if tiles[i][j].collidepoint(mouse):
                        if (i, j) in moves:
                            self.ot.make_move((i, j))
                            self.recent_move = (i, j)
        

        
        if self.ot.check_victory() != 0:
            print("Game over")
            print(f"{self.ot.get_color(self.ot.check_victory)} wins!")
            self.game_state = "end"
        if self.game_state == "end":
            pass
        
        pygame.display.flip()         


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

# TODO
"""
- Detect victory or draws when there are no moves left
- Quit / Back to main menu button when playing
- AI simple level 1 (random moves)
- Custom othello sizes and vs ai mode
- etc.. (coming soon)
"""
