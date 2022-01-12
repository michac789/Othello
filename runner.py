from random import random
import pygame
import sys
import math
import time

from othello import Othello
from helper import *


class Game():
    
    def __init__(self):
        # Default normal board size and configuration (changeable from custom mode or set_config method)
        self.dim_height = 8
        self.dim_width = 8
        self.init_white = [(3, 3), (4, 4)]
        self.init_black = [(3, 4), (4, 3)]
        self.ot = None
        
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
        
        # Keep track of recent move, tracker used to end game when no 2 consecutive moves possible
        self.recent_move = (-1, -1)
        self.stored_move = (-2, -2)
        self.skip_index = -1
        
        # Confirmation window displayer
        self.confirmation_action = ""
        self.hover_yes = False
        self.hover_no = False
        
        # Choose modes in 'pre_classic' state
        self.classic_mode = "Human" # 'Human' by default for 2V2
    
    # Resize components relative to the overall screen width and height
    def resize(self):
        self.board_padding = self.screen_height / 15
        self.board_width = ((9 / 16) * self.screen_width) - (2 * self.board_padding)
        self.board_height = self.screen_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        
    def run(self):
        while True:
            # Terminate application when the game is quit, resizable window feature
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.ext()
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen_height, self.screen_width = event.h, event.w
            self.resize()

            # Based on 'state machine' concept, launch different states of the game depending on self.game_state
            if self.game_menu == "start":
                self.state_mainmenu()
            elif self.game_menu == "pre_classic":
                self.state_pre_classic()
            elif self.game_menu == "pre_custom":
                self.state_pre_custom()
            elif self.game_menu == "pre_puzzle":
                raise NotImplementedError
            elif self.game_menu == "play":
                self.state_play()

    def set_config(self):
        self.init_white = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.init_black = [(1, 0), (1, 1), (1, 2), (1, 3)]
        self.dim_height, self.dim_width = 4, 4
        # self.init_white = [(5, 5), (6, 6)]
        # self.init_black = [(5, 6), (6, 5)]
        self.recent_move = (-1, -1)
        self.stored_move = (-2, -2)
        self.skip_index = -1
    
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
        states = ["pre_classic", "pre_custom", "pre_puzzle"]
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                if button_dict[i].collidepoint(mouse): self.game_menu = states[i]
        
        pygame.display.flip()
        
    def state_pre_classic(self):
        # Display game mode as main title
        self.screen.fill(black)
        title = titleFont.render("Classic Mode", True, white)
        titleRect = title.get_rect()
        titleRect.center = (self.screen_width / 2, 50)
        self.screen.blit(title, titleRect)
        
        # Display various buttons
        button_texts = ["Choose your opponent:",
                        "Choose time constraint:", "Allow undo move:", "",
                        "Human VS Human", "Human VS AI", "No Limit", "5 Min", "10 Min", "15 Mins", "20 Mins", "30 Mins", "Yes", "No",
                        "Back to Menu", "Play Game"]
        button_dict = {}
        for i in range(len(button_texts)):
            if 0 <= i <= 3:
                buttonRect = pygame.Rect(self.board_start[0], self.board_height * (0.25 + 0.3 * i), self.screen_width / 3, self.screen_height / 10)
                buttonText = preptextFont.render(button_texts[i], True, white)
            if 4 <= i <= 5:
                buttonRect = pygame.Rect(self.screen_width * (0.4 + 0.3 * (i - 4)), self.screen_height * 0.25, self.screen_width * 0.27, self.screen_height / 5)
                buttonText = preptextFont.render(button_texts[i], True, black)
            if 6 <= i <= 13:
                buttonRect = pygame.Rect(self.screen_width * (0.4 + 0.2 * ((i - 6) % 3)), self.screen_height * (0.5 + 0.12 * math.floor((i - 6) / 3)), self.screen_width * 0.15, self.screen_height / 12)
                buttonText = preptextFont.render(button_texts[i], True, black)
            if 14 <= i <= 15:
                buttonRect = pygame.Rect(self.screen_width * (0.1 + 0.5 * (i - 14)), self.screen_height * 0.88, self.screen_width * 0.3, self.screen_height / 10)
                buttonText = preptextFont.render(button_texts[i], True, black)
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            if 0 <= i <= 3: pygame.draw.rect(self.screen, black, buttonRect)
            else: pygame.draw.rect(self.screen, white, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
            
        # Buttons functionality when clicked
        left, _, _ = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            pass
                
        pygame.display.flip()
    
    def state_pre_custom(self): #TODO
        raise NotImplementedError

    def state_play(self):
        # Initialize game with the required settings
        if self.game_state == "prep":
            self.set_config()
            self.ot = Othello(self.dim_height, self.dim_width)
            self.ot.set_initial_position(self.init_white, self.init_black)
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
        
        # Continue to next turn if there are no moves available; end game if no moves in 2 consecutive turns
        moves = self.ot.get_possible_moves()
        if len(moves) == 0:
            if self.skip_index != self.ot.turn and self.ot.skip_turn == 1:
                self.ot.skip_turn = 2
            if self.recent_move != self.stored_move:
                self.ot.skip_turn = 1
                self.skip_index = self.ot.turn
                self.ot.turn = self.ot.turn % 2 + 1
            self.stored_move = self.recent_move
        else:
            self.ot.skip_turn = 0
            self.skip_index = -1
        
        # Draw each pieces that are present in the board, including all tiles with possible moves, showing recent move made
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
        
        # Check if victory
        if self.ot.check_victory() != 0:
            self.game_state = "end"
        
        # Message to be displayed on screen
        Time1, Time2 = 0, 0
        b1, b2, b3, b4, b5 = f"{self.ot.get_color(self.ot.turn)}'s move (Turn: {self.ot.move_no + 1})", "No winner yet.", "Undo", "Reset", "Quit"
        if self.game_state == "end":
            b1 = f"No more moves! ({self.ot.move_no} turns)"
            b2 = f"{self.ot.get_color(self.ot.check_victory)} wins!"
        button_texts = [f"{Time1}", f"{Time2}", "Black", "White", f"{self.ot.black_tiles}", f"{self.ot.white_tiles}", b1, b2, b3, b4, b5]

        # Display various user interfaces (scoreboards, messages, buttons)
        scoreRect = pygame.Rect((self.screen_width * 0.55), (self.screen_height * 0.1), (self.screen_width * 0.4), (self.screen_height * 0.3))
        pygame.draw.rect(self.screen, white, scoreRect)
        button_dict = {}
        for i in range(len(button_texts)):
            if i == 2 or i == 3:
                buttonRect = pygame.Rect((self.screen_width * (0.58 + (i - 2) * 0.18)), (self.screen_height * 0.3), self.screen_width / 6, self.screen_height / 15)
            elif i == 4 or i == 5:
                buttonRect = pygame.Rect((self.screen_width * (0.58 + (i - 4) * 0.18)), (self.screen_height * 0.12), self.screen_width / 6, self.screen_height / 5)
            elif i == 6 or i == 7:
                buttonRect = pygame.Rect((self.screen_width * 0.55), (self.screen_height * (0.45 + (i - 6) / 6)), self.screen_width * 0.4, self.screen_height / 8)
            else:
                buttonRect = pygame.Rect((self.screen_width * (0.55 + (i - 8) * 0.13)), (self.screen_height * 0.79), self.screen_width * 0.12, self.screen_height / 8)
            button_dict[i] = buttonRect
            buttonText = smallFont.render(button_texts[i], True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, score_color, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
            
        # Display confirmation screen and yes/no buttons, proceed with action when 'yes' is clicked, back to game when 'no' is clicked
        if self.confirmation_action != "":
            confRectborder = pygame.Rect((self.screen_width / 4), (self.screen_height / 4), (self.screen_width / 2), (self.screen_height / 2))
            confRect = pygame.Rect((self.screen_width / 4 + 3), (self.screen_height / 4 + 3), (self.screen_width / 2 - 6), (self.screen_height / 2 - 6))
            confText1 = confFont1.render(f"Confirm {self.confirmation_action}?", True, black)
            confText2 = confFont2.render("Warning! This cannot be undone!", True, black)
            confTextRect1 = confText1.get_rect(center = (self.screen_width / 2, self.screen_height * 0.35))
            confTextRect2 = confText2.get_rect(center = (self.screen_width / 2, self.screen_height * 0.45))
            pygame.draw.rect(self.screen, conf_screen_border_color, confRectborder)
            pygame.draw.rect(self.screen, conf_screen_color, confRect)
            self.screen.blit(confText1, confTextRect1)
            self.screen.blit(confText2, confTextRect2)
            yes, no = confFont3.render("Yes", True, black), confFont3.render("No", True, black)
            if self.hover_yes: yes = confFont4.render("Yes", True, conf_hover_color)
            if self.hover_no: no = confFont4.render("No", True, conf_hover_color)
            yes_rect = yes.get_rect(center = (self.screen_width * 0.45, self.screen_height * 0.55))
            no_rect = no.get_rect(center = (self.screen_width * 0.55, self.screen_height * 0.55))
            self.screen.blit(yes, yes_rect)
            self.screen.blit(no, no_rect)
            left, _, _ = pygame.mouse.get_pressed()
            mouse = pygame.mouse.get_pos()
            if left == 1:
                if yes_rect.collidepoint(mouse):
                    if self.confirmation_action == "Quit":
                        self.game_menu = "start"
                        self.game_state = "prep"
                        self.set_config()
                    if self.confirmation_action == "Reset":
                        self.game_state = "prep"
                        self.set_config()
                    self.confirmation_action = ""
                    time.sleep(0.2)
                if no_rect.collidepoint(mouse):
                    self.confirmation_action = ""
            self.hover_yes, self.hover_no = False, False
            if yes_rect.collidepoint(mouse): self.hover_yes = True
            if no_rect.collidepoint(mouse): self.hover_no = True
        
        # Update changes when a valid tile is clicked, or when a button is clicked
        if self.confirmation_action == "":
            left, _, _ = pygame.mouse.get_pressed()
            mouse = pygame.mouse.get_pos()
            if left == 1:
                for i in range(self.dim_height):
                    for j in range(self.dim_width):
                        if tiles[i][j].collidepoint(mouse):
                            if (i, j) in moves:
                                self.ot.make_move((i, j))
                                self.recent_move = (i, j)
                if button_dict[8].collidepoint(mouse):
                    raise NotImplementedError
                if button_dict[9].collidepoint(mouse): # Reset board button (restart game with the same configuration)
                    self.confirmation_action = "Reset"
                if button_dict[10].collidepoint(mouse): # Quit button (back to main menu)
                    self.confirmation_action = "Quit"
        
        pygame.display.flip()         


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

# TODO
"""
- AI simple level 1 (random moves)
- Custom othello sizes and vs ai mode
- etc.. (coming soon)
"""
