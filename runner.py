""" 
This is the main game launcher file with full user interface using pygame.
Be sure to have this file in the same directory with all of the other files, and ensure to have pygame installed.
Most configurations such as music/sfx, images, hover effects, main functionality of the app are all performed here.
"""

import pygame
import sys
import math
import time

from othello import Othello
from othello_ai import AI_move
from helper import *


class Game():
    
    def __init__(self):
        # Initialize pygame, board default configuration, set title, set default 16:9 resizable screen
        self.dim_height, self.dim_width = 8, 8
        self.init_white, self.init_black = [(3, 3), (4, 4)], [(3, 4), (4, 3)]
        self.ot = None
        self.screen_width, self.screen_height = 800, 450
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Othello")
        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
        
        # State machine updator; Menu: start, play, pre_classic, pre_custom, pre_puzzle, tutorial, leaderboard; 
        self.game_menu = "start"
        self.game_state = "prep" # State: prep, play, end
        self.confirmation_action = "" # Confirmation window displayer
        self.tracker = False # Track to only launch method check_no_move once every time a move is done
        
        # Choose modes in 'pre_classic' state
        self.classic_mode = "Human" # 'Human' by default for 2 players, or 'AI' against computer, or "AI2" for both computer players
        self.classic_time = -1 # '-1' for no time limit by default, or 5/10/15/20/30 mins for each player
        self.classic_undo = True # Allow undo move by default, can be set to False
        self.classic_ai_level = 1 # Level 1 AI (easiest) by default, available up to level 6 (hopefully) #TODO
        self.classic_ai_black = False # AI goes later (second turn) as white by default, can be set to true so AI makes first turn
        self.classic_chosen = [False for i in range(16)] # For UI purposes
        self.classic_ai2_level_b, self.classic_ai2_level_w, self.classic_ai2_color = 1, 1, 'b' # Level for AI VS AI Mode (black and white)
        
        # Choose modes in 'pre_custom' state
        # TODO
        
        # Keep track of time (time left & time since pygame was init for starting relative time)
        self.timer_player1, self.timer_player2 = 0, 0
        self.time_start1, self.time_start2 = None, None
        
        # Keep track whether bgm and soundfx is on or not, by default is on, can be turned off
        self.bgm_on, self.sfx_on = True, True
        self.bgm_hover, self.sfx_hover = False, False
        
        # Various hover effects tracker
        self.hover_main = [False for i in range(9)]
        self.hover_pre_buttons = [False for i in range(2)]
        self.hover_pre_classic = [False for i in range(15)]
        self.hover_play_util = [False for i in range(11)]
        self.hover_yes, self.hover_no = False, False
    
    # Resize various components relative to the virtual screen width and height; maintaining 16:9 aspect ratio
    def resize(self):
        self.virtual_height = min((9 / 16) * self.screen_width, self.screen_height)
        self.virtual_width = (16 / 9) * self.virtual_height
        self.board_padding = self.virtual_height / 15
        self.board_width = ((9 / 16) * self.virtual_width) - (2 * self.board_padding)
        self.board_height = self.virtual_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        self.icon_sides = math.floor(self.virtual_height / 9)
        self.maintitleFont = font.Font(LOBSTER, int(self.virtual_height * (2 / 9)))
        self.mainbuttonFont1 = font.Font(OPEN_SANS, int(self.virtual_height * (1 / 15)))
        self.mainbuttonHoverFont1 = font.Font(OPEN_SANS, int(self.virtual_height * (16 / 225)))
        self.mainbuttonFont2 = font.Font(BLACKJACK, int(self.virtual_height * (1 / 18)))
        self.mainbuttonHoverFont2 = font.Font(BLACKJACK, int(self.virtual_height * (3 / 50)))
        self.titleFont = font.Font(ARIZONIA, int(self.virtual_height * (8 / 45)))
        self.preptextFont = font.Font(OPEN_SANS, int(self.virtual_height * (1 / 18)))
        self.prepoptionFont = font.Font(PACIFICO, int(self.virtual_height * (1 / 18)))
        self.prepgoFont = font.Font(LOBSTER, int(self.virtual_height * (1 / 15)))
        self.playtimerFont = font.Font(OPEN_SANS, int(self.virtual_height * (2 / 45)))
        self.playscoreFont = font.Font(BLACKJACK, int(self.virtual_height * (2 / 15)))
        self.playtextFont = font.Font(BLACKJACK, int(self.virtual_height * (1 / 18)))
        self.playutilFont = font.Font(OPEN_SANS, int(self.virtual_height * (1 / 18)))
        self.confFont1 =  font.Font(PACIFICO, int(self.virtual_height * (7 / 90)))
        self.confFont2 =  font.Font(OPEN_SANS, int(self.virtual_height * (2 / 45)))
        self.confFont3 = font.Font(OPEN_SANS, int(self.virtual_height * (4 / 45)))
        self.confFont4 = font.Font(OPEN_SANS, int(self.virtual_height * (1 / 10)))
    
    # This function is called to loop through the game and render each frame while game is still running
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
            pygame.display.flip()
    
    # Handles all the choosing mode buttons and its action towards self.classic_(xxx) in the 'pre_classic' state
    def classic_choose(self, index):
        self.classic_chosen = [False for i in range(16)]
        if 4 <= index <= 6: self.classic_mode = ("Human" if index == 4 else "AI" if index == 5 else "AI2")
        if self.classic_mode == "Human": self.classic_chosen[4] = True
        elif self.classic_mode == "AI": self.classic_chosen[5] = True
        else: self.classic_chosen[6] = True
        if self.classic_mode == "Human":
            if 7 <= index <= 12: self.classic_time = (-1 if index == 7 else int(-35 + 5 * index) if 8 <= index <= 11 else 30)
            if 13 <= index <= 14: self.classic_undo = (True if index == 13 else False)
            if self.classic_time == -1: self.classic_chosen[7] = True
            elif self.classic_time == 30: self.classic_chosen[12] = True
            else: self.classic_chosen[int(self.classic_time / 5 + 7)] = True
            if self.classic_undo == True: self.classic_chosen[13] = True
            else: self.classic_chosen[14] = True
            if self.classic_time > 0: self.timer_player1, self.timer_player2 = 60000 * self.classic_time, 60000 * self.classic_time
            else: self.timer_player1, self.timer_player2 = 0, 0
        if self.classic_mode == "AI":
            if 7 <= index <= 12: self.classic_ai_level = index - 6
            if 13 <= index <= 14: self.classic_ai_black = (True if index == 14 else False)
            self.classic_chosen[self.classic_ai_level + 6] = True
            if self.classic_ai_black: self.classic_chosen[14] = True
            else: self.classic_chosen[13] = True
        if self.classic_mode == "AI2":
            if 7 <= index <= 12 and self.classic_ai2_color == "b": self.classic_ai2_level_b = index - 6
            if 7 <= index <= 12 and self.classic_ai2_color == "w": self.classic_ai2_level_w = index - 6
            if 13 <= index <= 14: self.classic_ai2_color = ("b" if index == 13 else "w")
            if self.classic_ai2_color == "b": self.classic_chosen[13] = True
            else: self.classic_chosen[14] = True
            if self.classic_ai2_color == "b": self.classic_chosen[self.classic_ai2_level_b + 6] = True
            if self.classic_ai2_color == "w": self.classic_chosen[self.classic_ai2_level_w + 6] = True

    # Called upon to play main menu bgm and set its volume when not played yet, also called from several other game states
    def play_main_bgm(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(BGM_MENU)
            pygame.mixer.music.play(loops = 0, start = 1.5)
        pygame.mixer.music.set_volume((0.2 if self.bgm_on == True else 0))
    
    # Draw icons on bottom right of the screen
    def display_icon(self):
        img_name = [(BGM_TRUE_HOVER if self.bgm_on == True and self.bgm_hover == True else BGM_TRUE if self.bgm_on == True else BGM_FALSE_HOVER if self.bgm_hover == True else BGM_FALSE),
                 (SFX_TRUE_HOVER if self.sfx_on == True and self.sfx_hover == True else SFX_TRUE if self.sfx_on == True else SFX_FALSE_HOVER if self.sfx_hover == True else SFX_FALSE)]
        button_dict = {}
        for i in range(2):
            image = pygame.transform.scale(img_name[i], (self.icon_sides, self.icon_sides))
            buttonRect = pygame.Rect(self.virtual_width * 0.92, self.virtual_height * (0.85 - 0.1 * i), self.icon_sides, self.icon_sides)
            buttonTextRect = image.get_rect()
            buttonTextRect.center = buttonRect.center
            self.screen.blit(image, buttonTextRect)
            button_dict[i] = buttonRect
        
        # Implement clicking functionality and hover effect
        mouse = pygame.mouse.get_pos()
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            if button_dict[0].collidepoint(mouse): self.bgm_on = (False if self.bgm_on == True else True)
            if button_dict[1].collidepoint(mouse): self.sfx_on = (False if self.sfx_on == True else True)
            time.sleep(0.2)
        self.bgm_hover = (True if button_dict[0].collidepoint(mouse) else False)
        self.sfx_hover = (True if button_dict[1].collidepoint(mouse) else False)
    
    # Used in pre__ states, display the title of the current screen and make some common settings
    def display_title(self, title):
        self.screen.fill(black)
        title = self.titleFont.render(title, True, mode_title)
        titleRect = title.get_rect()
        titleRect.center = (self.virtual_width / 2, 50)
        self.screen.blit(title, titleRect)
        self.classic_choose(-1)
        self.play_main_bgm()
    
    # Used in pre__ states, display 'play' and 'back' buttons, along with its functionality
    def display_buttons(self):
        # Draw 'back to menu' and 'play game' buttons
        buttons = ["Back to Menu", "Play Game"]
        button_dict = {}
        for i in range(2):
            buttonRect = pygame.Rect(self.virtual_width * (0.1 + 0.4 * (i)), self.virtual_height * 0.88, self.virtual_width * 0.3, self.virtual_height / 10)
            buttonText = self.prepgoFont.render(buttons[i], True, (prep_option_color3 if self.hover_pre_buttons[i] == False else prep_button_hover_color2))
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, (prep_button_color2 if self.hover_pre_buttons[i] == False else prep_rect_hover_color), buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        # Implement buttons functionality (when clicked & hover effect)
        left, _, _ = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            if button_dict[0].collidepoint(mouse):
                if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                self.game_menu = "start"
            if button_dict[1].collidepoint(mouse):
                if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                self.init_white, self.init_black = [(3, 3), (4, 4)], [(3, 4), (4, 3)]
                self.dim_height, self.dim_width = 8, 8
                self.game_menu = "play"
                time.sleep(0.2)
        for i in range(2):
            self.hover_pre_buttons[i] = False
            if button_dict[i].collidepoint(mouse):
                self.hover_pre_buttons[i] = True
    
    # Prepare othello object from play state when first launched (prep stage)
    def play_set_config(self):
        self.prevent_undo = False
        pygame.mixer.music.unload()
        self.ot = Othello(self.dim_height, self.dim_width)
        self.ot.set_initial_position(self.init_white, self.init_black)
        self.ot.turn = 1
        self.game_state = "play"
        self.tracker = False
        self.time_start1 = pygame.time.get_ticks()
        pygame.mixer.music.load(BGM_GAME)
        pygame.mixer.music.play(loops = -1)
        self.ai_turn, self.human_turn = -1, -1
        if self.classic_mode == "AI":
            self.classic_time, self.classic_undo = -1, True
            self.ai_turn = (1 if self.classic_ai_black else 2)
            self.human_turn = (2 if self.classic_ai_black else 1)
        if self.classic_mode == "AI2":
            self.classic_time, self.prevent_undo = -1, True
            self.human_turn = -1
    
    def state_mainmenu(self):
        # Play BGM, display title
        self.play_main_bgm()
        self.screen.fill(black)
        title = self.maintitleFont.render("OTHELLO", True, main_title_color)
        titleRect = title.get_rect()
        titleRect.center = (self.virtual_width / 2, self.virtual_height * 0.2)
        self.screen.blit(title, titleRect)
        
        # Display buttons (classic mode, custom mode, puzzle mode), supporting buttons and toogle bgm / sfx / full screen buttons
        button_texts = ["Classic Mode", "Custom Mode", "Puzzle Mode", "", "How To Play", "Leaderboards", "About", "BGM", "SFX"]
        button_dict = {}
        for i in range(len(button_texts)):
            if 0 <= i <= 3:
                buttonRect = pygame.Rect((self.virtual_width / 4), ((6 + 2 * i) / 16) * self.virtual_height, self.virtual_width / 2, self.virtual_height / 10)
                if self.hover_main[i] == True: buttonRect = pygame.Rect((self.virtual_width / 4) - (self.virtual_width / 2) * 0.02, ((6 + 2 * i) / 16) * self.virtual_height, (self.virtual_width / 2) * 1.04, (self.virtual_height / 10) * 1.05)
                buttonText = self.mainbuttonFont1.render(button_texts[i], True, main_button1_text_color)
                if self.hover_main[i] == True: buttonText = self.mainbuttonHoverFont1.render(button_texts[i], True, main_button1_text_hover_color)
                if i != 3:
                    if self.hover_main[i] == True: pygame.draw.rect(self.screen, main_button1_hover_color, buttonRect)
                    else: pygame.draw.rect(self.screen, main_button1_color, buttonRect)
            elif 4 <= i <= 6:
                buttonRect = pygame.Rect(self.virtual_width * (0.1 + 0.25 * (i - 4)), self.virtual_height * 0.8, self.virtual_width * 0.2, self.virtual_height / 10)
                if self.hover_main[i] == True: buttonRect = pygame.Rect((self.virtual_width * (0.1 + 0.25 * (i - 4))) - (self.virtual_width * 0.2) * 0.02, self.virtual_height * 0.8, (self.virtual_width * 0.2) * 1.04, (self.virtual_height / 10) * 1.03)
                buttonText = self.mainbuttonFont2.render(button_texts[i], True, main_button2_text_color)
                if self.hover_main[i] == True: buttonText = self.mainbuttonHoverFont2.render(button_texts[i], True, main_button2_text_hover_color)
                if self.hover_main[i] == True: pygame.draw.rect(self.screen, main_button2_hover_color, buttonRect)
                else: pygame.draw.rect(self.screen, main_button2_color, buttonRect)
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            self.screen.blit(buttonText, buttonTextRect)
        self.display_icon()
        
        # Change state when respective buttons are clicked, add hover effects
        states = ["pre_classic", "pre_custom", "pre_puzzle"]
        mouse = pygame.mouse.get_pos()
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            for i in range(3):
                if button_dict[i].collidepoint(mouse):
                    self.game_menu = states[i]
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                time.sleep(0.1)
        self.hover_main = [False for i in range(9)]
        for i in range(9):
            if button_dict[i].collidepoint(mouse): self.hover_main[i] = True
        
    def state_pre_classic(self):
        # Display title and various buttons
        self.display_title("Classic Mode")
        self.display_buttons()
        self.display_icon()
        if self.classic_mode == "Human":
            button_texts = ["Choose classic mode:", "Choose time constraint:", "Allow undo move:", "", "Human VS Human", "Human VS AI", "AI VS AI",
                            "No Limit", "5 Mins", "10 Mins", "15 Mins", "20 Mins", "30 Mins", "Yes", "No"]
        elif self.classic_mode == "AI" or self.classic_mode == "AI2":
            button_texts = ["Choose classic mode:", "Choose AI difficulty:", "Your color piece:", "", "Human VS Human", "Human VS AI", "AI VS AI",
                            "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Black", "White"]
        if self.classic_mode == "AI2": button_texts[3] = "Level for this piece:"
        button_dict = {}
        for i in range(len(button_texts)):
            if 0 <= i <= 3:
                buttonRect = pygame.Rect(self.board_start[0], self.board_height * (0.25 + 0.3 * i), self.virtual_width / 3, self.virtual_height / 10)
                buttonText = self.preptextFont.render(button_texts[i], True, (prep_text_color1 if i == 0 else prep_text_color2))
            if 4 <= i <= 6:
                if i != 6: buttonRect = pygame.Rect(self.virtual_width * (0.4 + 0.3 * (i - 4)), self.virtual_height * 0.25, self.virtual_width * 0.27, self.virtual_height / 11)
                else: buttonRect = pygame.Rect(self.virtual_width * (0.55), self.virtual_height * 0.37, self.virtual_width * 0.27, self.virtual_height / 11)
                buttonText = self.prepoptionFont.render(button_texts[i], True, (prep_option_color1 if self.hover_pre_classic[i] == False else prep_button_hover_color1))
            if 7 <= i <= 14:
                buttonRect = pygame.Rect(self.virtual_width * (0.4 + 0.18 * ((i - 7) % 3)), self.virtual_height * (0.5 + 0.12 * math.floor((i - 7) / 3)), self.virtual_width * 0.15, self.virtual_height / 12)
                buttonText = self.prepoptionFont.render(button_texts[i], True, (prep_option_color2 if self.hover_pre_classic[i] == False else prep_button_hover_color1))
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            if 0 <= i <= 3: pygame.draw.rect(self.screen, black, buttonRect) 
            else: pygame.draw.rect(self.screen, (prep_button_color1 if self.classic_chosen[i] == False else prep_chosen_color), buttonRect)
            self.screen.blit(buttonText, buttonTextRect)

        # Buttons functionality when clicked & hover effects
        left, _, _ = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            for i in range(4, 15, 1):
                if button_dict[i].collidepoint(mouse):
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                    self.classic_choose(i)
        for i in range(4, 15, 1):
            self.hover_pre_classic[i] = False
            if button_dict[i].collidepoint(mouse):
                self.hover_pre_classic[i] = True
    
    def state_pre_custom(self): #TODO        
        self.display_title("Custom Mode")
        self.display_buttons()
        self.display_icon()
        
        timer = 0
        button_texts = ["Choose board height:", "Choose board width:", "Time limit (minutes):", "Initial board position:", "",
                        f"{self.dim_height}", f"{self.dim_width}", f"{timer}", "+", "-", "+", "-", "+", "-", "Set Board"]
        button_dict = {}
        for i in range(len(button_texts)):
            if 0 <= i <= 4:
                buttonRect = pygame.Rect(self.board_start[0] * 1.5, self.board_height * (0.3 + 0.15 * i), self.virtual_width / 3, self.virtual_height / 10)
                buttonText = self.preptextFont.render(button_texts[i], True, prep_text_color1)
            if 5 <= i <= 7:
                buttonRect = pygame.Rect(self.virtual_width * 0.55, self.virtual_height * (0.27 + 0.13 * (i - 5)), self.virtual_width * 0.15, self.virtual_height / 11)
                buttonText = self.prepoptionFont.render(button_texts[i], True, prep_option_color1)
            if 8 <= i <= 13:
                buttonRect = pygame.Rect(self.virtual_width * (0.47 + 0.26 * ((i - 7) % 2)), self.virtual_height * (0.27 + 0.13 * math.floor((i - 8) / 2)), self.virtual_width * 0.05, self.virtual_height / 12)
                buttonText = self.prepoptionFont.render(button_texts[i], True, (prep_option_color2 if self.hover_pre_classic[i] == False else prep_button_hover_color1))
            if i == 14:
                buttonRect = pygame.Rect(self.virtual_width * 0.55, self.virtual_height * 0.67, self.virtual_width * 0.15, self.virtual_height / 11)
                buttonText = self.prepoptionFont.render(button_texts[i], True, prep_option_color1)
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            if 0 <= i <= 4: pygame.draw.rect(self.screen, black, buttonRect) 
            else: pygame.draw.rect(self.screen, (prep_button_color1 if self.classic_chosen[i] == False else prep_chosen_color), buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        self.init_white = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.init_black = [(1, 0), (1, 1), (1, 2), (1, 3)]
        self.dim_height, self.dim_width = 4, 4
        # self.game_menu = "play"
        # time.sleep(0.2)
        
        # TEMPORARY PLACEHOLDER TODO

    def state_play(self):
        # Initialize game with the required settings; added bgm for gameplay
        if self.game_state == "prep":
            self.play_set_config()
            self.loop = 0
        pygame.mixer.music.set_volume((0.2 if self.bgm_on == True else 0))
        
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
        self.display_icon()
        
        # Generate all valid moves, continue to next turn if there are no moves available; end game if no moves in 2 consecutive turns
        moves = self.ot.get_possible_moves()
        if not self.tracker:
            self.ot.check_no_move(moves)
            self.tracker = True
        
        # Keep track of time if time limit is given; opponent wins if your time runs out and there are still moves possible to made
        if self.classic_time != -1 and self.game_state != "end":
            if self.ot.turn == 1:
                self.timer_player1 = self.timer_player1 + (self.time_start1 - pygame.time.get_ticks())
                self.time_start1 = pygame.time.get_ticks()
            elif self.ot.turn == 2:
                self.timer_player2 = self.timer_player2 + (self.time_start2 - pygame.time.get_ticks())
                self.time_start2 = pygame.time.get_ticks()
            if self.timer_player1 < 0: self.ot.force_win = 2
            if self.timer_player2 < 0: self.ot.force_win = 1
        
        # Draw each pieces that are present in the board, including all tiles with possible moves, showing recent move made
        for i in range(self.dim_height):
            for j in range(self.dim_width):
                coordinate = (self.board_start[0] + j * self.tile_size + self.tile_size / 2, self.board_start[1] + i * self.tile_size + self.tile_size / 2)
                if self.ot.board[i][j] != 0:
                    circ = pygame.draw.circle(self.screen, tile_border_color, coordinate, self.piece_radius + 2)
                    circ = pygame.draw.circle(self.screen, (white if self.ot.board[i][j] == 2 else black), coordinate, self.piece_radius)
                if (i, j) in moves:
                    circ = pygame.draw.circle(self.screen, moves_color, coordinate, self.piece_radius, int(self.piece_radius / 2))
                if self.ot.move_no > 0 and self.ot.moves_made[self.ot.move_no - 1][2] == (i, j):
                    circ = pygame.draw.circle(self.screen, recent_move_color, coordinate, self.piece_radius / 3)
        
        # Check if victory
        if self.ot.check_victory() != 0 and self.game_state != "end":
            if self.sfx_on: pygame.mixer.Channel(2).play(pygame.mixer.Sound(SFX_WIN_GAME))
            self.game_state = "end"
            self.prevent_undo = True
        
        # Message to be displayed on screen
        time1, time2 = (self.timer_player1 if self.timer_player1 > 0 else 0), (self.timer_player2 if self.timer_player2 > 0 else 0)
        time1, time2 = f"{(time1 // 60000):02d}:{((time1 // 1000) % 60):02d}:{((time1 // 10) % 100):02d}", f"{(time2 // 60000):02d}:{((time2 // 1000) % 60):02d}:{((time2 // 10) % 100):02d}"
        b1, b2, b3, b4, b5 = f"{self.ot.get_color(self.ot.turn)}'s move (Turn: {self.ot.move_no + 1})", "No winner yet.", "Undo", "Reset", "Quit"
        if self.game_state == "end":
            ms = ("No more moves!" if self.ot.force_win == -1 else "Time is up!")
            b1 = f"{ms} ({self.ot.move_no} turns)"
            b2 = f"{self.ot.get_color(self.ot.check_victory())} wins!"
            if self.ot.check_victory() == 3: b2 = "Game draw!"
        button_texts = [f"{time1}", f"{time2}", f"{self.ot.black_tiles}", f"{self.ot.white_tiles}", "Black", "White", b1, b2, b3, b4, b5]
        
        # Display various user interfaces (scoreboards, messages, buttons)
        scoreRect = pygame.Rect((self.virtual_width * 0.55), (self.virtual_height * 0.05), (self.virtual_width * 0.4), (self.virtual_height * 0.37))
        pygame.draw.rect(self.screen, play_scoreboard_color, scoreRect)
        button_dict = {}
        for i in range(len(button_texts)):
            if (i == 0 or i == 1) and self.classic_time != -1:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + i * 0.18)), (self.virtual_height * 0.07), self.virtual_width / 6, self.virtual_height / 15)
                buttonText = self.playtimerFont.render(button_texts[i], True, play_timer_color)
                color_x = play_score_color
            elif i == 2 or i == 3:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + (i - 2) * 0.18)), (self.virtual_height * 0.16), self.virtual_width / 6, self.virtual_height / 5)
                buttonText = self.playscoreFont.render(button_texts[i], True, play_sb_text_color)
                color_x = play_score_color
            elif i == 4 or i == 5:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + (i - 4) * 0.18)), (self.virtual_height * 0.32), self.virtual_width / 6, self.virtual_height / 15)
                buttonText = self.playtextFont.render(button_texts[i], True, play_sb_text_color)
                color_x = play_score_color
            elif i == 6 or i == 7:
                buttonRect = pygame.Rect((self.virtual_width * 0.55), (self.virtual_height * (0.45 + (i - 6) / 6)), self.virtual_width * 0.35, self.virtual_height / 8)
                buttonText = self.playtextFont.render(button_texts[i], True, play_rect_text_color)
                color_x = play_rect_displayer_color
            else:
                buttonRect = pygame.Rect((self.virtual_width * (0.55 + (i - 8) * 0.12)), (self.virtual_height * 0.79), self.virtual_width * 0.1, self.virtual_height / 8)
                buttonText = self.playutilFont.render(button_texts[i], True, (play_utility_text_color_hover if self.hover_play_util[i] and ((not self.prevent_undo and self.classic_undo) or i != 8) else play_utility_text_color))
                color_x = (dark_grey if (not self.classic_undo or self.prevent_undo) and i == 8 else play_utility_button_color)
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, color_x, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        # AI Move (only for Human VS AI mode)
        if self.game_state == "play" and (self.classic_mode == "AI" and self.ai_turn == self.ot.turn):
            self.loop += 1
            if self.loop == 2:
                self.ot.make_move(AI_move(self.ot, self.classic_ai_level, True))
                self.tracker = False
                if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound((SFX_WHITE_MOVE if self.ai_turn == 2 else SFX_BLACK_MOVE)))
                self.loop = 0
        
        # AI VS AI Move (only for AI VS AI mode)
        if self.game_state == "play" and self.classic_mode == "AI2":
            self.loop += 1
            if self.loop == 2:
                if self.ot.turn == 1: self.ot.make_move(AI_move(self.ot, self.classic_ai2_level_b, False))
                elif self.ot.turn == 2: self.ot.make_move(AI_move(self.ot, self.classic_ai2_level_w, False))
                self.tracker = False
                if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound((SFX_WHITE_MOVE if self.ot.turn == 1 else SFX_BLACK_MOVE)))
                self.loop = 0
        
        # Update changes when a valid tile is clicked, or when a button is clicked
        mouse = pygame.mouse.get_pos()
        if self.confirmation_action == "":
            left, _, _ = pygame.mouse.get_pressed()
            if left == 1:
                #if self.game_state == "play" and (self.classic_mode == "human" or self.human_turn == self.ot.turn):
                if self.game_state == "play":
                    for i in range(self.dim_height):
                        for j in range(self.dim_width):
                            if tiles[i][j].collidepoint(mouse):
                                if (i, j) in moves:
                                    self.ot.make_move((i, j))
                                    self.tracker = False
                                    if self.ot.turn == 1:
                                        self.time_start1 = pygame.time.get_ticks()
                                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_WHITE_MOVE))
                                    elif self.ot.turn == 2:
                                        self.time_start2 = pygame.time.get_ticks()
                                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_BLACK_MOVE))
                                elif self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_BUTTON_INVALID))
                if button_dict[8].collidepoint(mouse) or button_dict[9].collidepoint(mouse) or button_dict[10].collidepoint(mouse):
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                if button_dict[8].collidepoint(mouse):
                    if self.classic_undo and not self.prevent_undo: self.confirmation_action = "Undo" # Undo last move button
                    elif self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_INVALID))
                if button_dict[9].collidepoint(mouse): self.confirmation_action = "Reset" # Reset board button (restart game with the same configuration)
                if button_dict[10].collidepoint(mouse): self.confirmation_action = "Quit" # Quit button (back to main menu)
        self.hover_play_util = [False for i in range(11)]
        for i in range(8, 11, 1):
            if button_dict[i].collidepoint(mouse): self.hover_play_util[i] = True
                
        # Display confirmation screen and yes/no buttons, proceed with action when 'yes' is clicked, back to game when 'no' is clicked
        if self.confirmation_action != "":
            confRectborder = pygame.Rect((self.virtual_width / 4), (self.virtual_height / 4), (self.virtual_width / 2), (self.virtual_height / 2))
            confRect = pygame.Rect((self.virtual_width / 4 + 3), (self.virtual_height / 4 + 3), (self.virtual_width / 2 - 6), (self.virtual_height / 2 - 6))
            confText1 = self.confFont1.render(f"Confirm {self.confirmation_action}?", True, conf_text1_color)
            confText2 = self.confFont2.render("Warning! This cannot be undone!", True, conf_text2_color)
            confTextRect1 = confText1.get_rect(center = (self.virtual_width / 2, self.virtual_height * 0.35))
            confTextRect2 = confText2.get_rect(center = (self.virtual_width / 2, self.virtual_height * 0.45))
            pygame.draw.rect(self.screen, conf_screen_border_color, confRectborder)
            pygame.draw.rect(self.screen, conf_screen_color, confRect)
            self.screen.blit(confText1, confTextRect1)
            self.screen.blit(confText2, confTextRect2)
            yes, no = self.confFont3.render("Yes", True, black), self.confFont3.render("No", True, black)
            if self.hover_yes: yes = self.confFont4.render("Yes", True, conf_hover_color)
            if self.hover_no: no = self.confFont4.render("No", True, conf_hover_color)
            yes_rect = yes.get_rect(center = (self.virtual_width * 0.4, self.virtual_height * 0.6))
            no_rect = no.get_rect(center = (self.virtual_width * 0.6, self.virtual_height * 0.6))
            self.screen.blit(yes, yes_rect)
            self.screen.blit(no, no_rect)
            left, _, _ = pygame.mouse.get_pressed()
            mouse = pygame.mouse.get_pos()
            if left == 1:
                if yes_rect.collidepoint(mouse):
                    if self.confirmation_action == "Undo":
                        if self.ot.move_no == 1: self.confirmation_action = "Reset"
                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_UNDO_GAME))
                        self.ot.undo_move()
                        if self.classic_mode == "AI" and len(self.ot.moves_made) > 1:
                            if self.ot.moves_made[self.ot.move_no][1] == self.ai_turn: self.ot.undo_move()
                    time.sleep(0.2)
                    if self.confirmation_action == "Quit":
                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_QUIT_GAME))
                        self.game_menu = "start"
                        self.game_state = "prep"
                        pygame.mixer.music.unload()
                    if self.confirmation_action == "Reset":
                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_RESET_GAME))
                        self.game_state = "prep"
                        pygame.mixer.music.unload()
                        self.classic_choose(-1)
                    self.confirmation_action = ""
                    time.sleep(0.2)
                if no_rect.collidepoint(mouse):
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                    self.confirmation_action = ""
            self.hover_yes, self.hover_no = False, False
            if yes_rect.collidepoint(mouse): self.hover_yes = True
            if no_rect.collidepoint(mouse): self.hover_no = True

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

# TODO
"""



- Custom mode (othello sizes & starting positions)
- Create pre_custom feature user interface

- 'How to play' pages and pics, UI

7. Puzzle mode??

- Custom othello sizes and vs ai mode
- etc.. (coming soon)

"""
