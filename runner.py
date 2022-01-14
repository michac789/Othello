from turtle import color
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
        pygame.mixer.init()
        pygame.display.set_caption("Othello")
        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
        
        # Compute various component sizes relative to screen_width and screen_height
        self.virtual_height = min((9 / 16) * self.screen_width, self.screen_height)
        self.virtual_width = (16 / 9) * self.virtual_height
        self.board_padding = self.virtual_height / 15
        self.board_width = ((9 / 16) * self.virtual_width) - (2 * self.board_padding)
        self.board_height = self.virtual_height - (2 * self.board_padding)
        self.tile_size = int(min(self.board_width / self.dim_width, self.board_height / self.dim_height))
        self.board_start = (self.board_padding, self.board_padding)
        self.piece_radius = math.floor(self.tile_size / 2 - 5)
        self.icon_sides = math.floor(self.virtual_height / 9)
        
        # Keep track of game menus and states (state machine updator)
        # Menu: start, play, pre_classic, pre_custom, pre_puzzle, tutorial, leaderboard
        # State (when menu is play): prep, play, end
        self.game_menu = "start"
        self.game_state = "prep"
        
        # Confirmation window displayer
        self.confirmation_action = ""
        self.hover_yes = False
        self.hover_no = False
        
        # Choose modes in 'pre_classic' state
        self.classic_mode = "Human" # 'Human' by default for 2 players, or 'AI' against computer
        self.classic_time = -1 # '-1' for no time limit by default, or 5/10/15/20/30 mins for each player
        self.classic_undo = True # Allow undo move by default, can be set to False
        self.classic_ai_level = 1 # Level 1 AI (easiest) by default, available up to level 6 (hopefully) #TODO
        self.classic_ai_black = False # AI goes later (second turn) as white by default, can be set to true so AI makes first turn
        self.classic_chosen = [False for i in range(16)]
        
        # Keep track of time (time left & time since pygame was init for starting relative time)
        self.timer_player1 = 0
        self.timer_player2 = 0
        self.time_start1 = None
        self.time_start2 = None
        
        # Keep track whether bgm and soundfx is on or not, by default is on, can be turned off
        self.bgm_on = True
        self.sfx_on = True
        self.bgm_hover = False
        self.sfx_hover = False
        
        # Various hover effects
        self.hover_main = [False for i in range(9)]
        self.hover_pre_classic = [False for i in range(16)]
    
    # Resize components relative to the overall screen width and height; maintaining 16:9 aspect ratio
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

    # Reset configuration made to self, called upon when restarting or quitting a game
    def set_config(self):
        pygame.mixer.music.unload()
    
    # Handles all the choosing mode buttons and its action towards self.classic_(xxx) in the 'pre_classic' state
    def classic_choose(self, index):
        self.classic_chosen = [False for i in range(16)]
        if 4 <= index <= 5: self.classic_mode = ("Human" if index == 4 else "AI")
        if 6 <= index <= 11: self.classic_time = (-1 if index == 6 else int(-30 + 5 * index) if 7 <= index <= 10 else 30)
        if 12 <= index <= 13: self.classic_undo = (True if index == 12 else False)
        if self.classic_mode == "Human": self.classic_chosen[4] = True
        else: self.classic_chosen[5] = True
        if self.classic_time == -1: self.classic_chosen[6] = True
        elif self.classic_time == 30: self.classic_chosen[11] = True
        else: self.classic_chosen[int(self.classic_time / 5 + 6)] = True
        if self.classic_undo == True: self.classic_chosen[12] = True
        else: self.classic_chosen[13] = True
        if self.classic_time > 0: self.timer_player1, self.timer_player2 = 60000 * self.classic_time, 60000 * self.classic_time
        else: self.timer_player1, self.timer_player2 = 0, 0
    
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
    
    def state_mainmenu(self):
        # Play BGM, display title
        self.play_main_bgm()
        self.screen.fill(black)
        title = maintitleFont.render("OTHELLO", True, main_title_color)
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
                buttonText = mainbuttonFont1.render(button_texts[i], True, main_button1_text_color)
                if self.hover_main[i] == True: buttonText = mainbuttonHoverFont1.render(button_texts[i], True, main_button1_text_hover_color)
                if i != 3:
                    if self.hover_main[i] == True: pygame.draw.rect(self.screen, main_button1_hover_color, buttonRect)
                    else: pygame.draw.rect(self.screen, main_button1_color, buttonRect)
            elif 4 <= i <= 6:
                buttonRect = pygame.Rect(self.virtual_width * (0.1 + 0.25 * (i - 4)), self.virtual_height * 0.8, self.virtual_width * 0.2, self.virtual_height / 10)
                if self.hover_main[i] == True: buttonRect = pygame.Rect((self.virtual_width * (0.1 + 0.25 * (i - 4))) - (self.virtual_width * 0.2) * 0.02, self.virtual_height * 0.8, (self.virtual_width * 0.2) * 1.04, (self.virtual_height / 10) * 1.03)
                buttonText = mainbuttonFont2.render(button_texts[i], True, main_button2_text_color)
                if self.hover_main[i] == True: buttonText = mainbuttonHoverFont2.render(button_texts[i], True, main_button2_text_hover_color)
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
        # Display game mode as main title
        self.screen.fill(black)
        title = titleFont.render("Classic Mode", True, mode_title)
        titleRect = title.get_rect()
        titleRect.center = (self.virtual_width / 2, 50)
        self.screen.blit(title, titleRect)
        self.classic_choose(-1)
        self.play_main_bgm()
        
        # Display various buttons
        button_texts = ["Choose your opponent:",
                        "Choose time constraint:", "Allow undo move:", "",
                        "Human VS Human", "Human VS AI", "No Limit", "5 Mins", "10 Mins", "15 Mins", "20 Mins", "30 Mins", "Yes", "No",
                        "Back to Menu", "Play Game"]
        button_dict = {}
        for i in range(len(button_texts)):
            if 0 <= i <= 3:
                buttonRect = pygame.Rect(self.board_start[0], self.board_height * (0.25 + 0.3 * i), self.virtual_width / 3, self.virtual_height / 10)
                buttonText = preptextFont.render(button_texts[i], True, (prep_text_color1 if i == 0 else prep_text_color2))
            if 4 <= i <= 5:
                buttonRect = pygame.Rect(self.virtual_width * (0.4 + 0.3 * (i - 4)), self.virtual_height * 0.25, self.virtual_width * 0.27, self.virtual_height / 5)
                buttonText = prepoptionFont.render(button_texts[i], True, (prep_option_color1 if self.hover_pre_classic[i] == False else prep_button_hover_color1))
            if 6 <= i <= 13:
                buttonRect = pygame.Rect(self.virtual_width * (0.4 + 0.2 * ((i - 6) % 3)), self.virtual_height * (0.5 + 0.12 * math.floor((i - 6) / 3)), self.virtual_width * 0.15, self.virtual_height / 12)
                buttonText = prepoptionFont.render(button_texts[i], True, (prep_option_color2 if self.hover_pre_classic[i] == False else prep_button_hover_color1))
            if 14 <= i <= 15:
                buttonRect = pygame.Rect(self.virtual_width * (0.1 + 0.4 * (i - 14)), self.virtual_height * 0.88, self.virtual_width * 0.3, self.virtual_height / 10)
                buttonText = prepgoFont.render(button_texts[i], True, (prep_option_color3 if self.hover_pre_classic[i] == False else prep_button_hover_color2))
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            if 0 <= i <= 3: pygame.draw.rect(self.screen, black, buttonRect)
            elif i == 14 or i == 15: pygame.draw.rect(self.screen, (prep_button_color2 if self.hover_pre_classic[i] == False else prep_rect_hover_color), buttonRect)
            else: pygame.draw.rect(self.screen, (prep_button_color1 if self.classic_chosen[i] == False else prep_chosen_color), buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        self.display_icon()

        # Buttons functionality when clicked
        left, _, _ = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if left == 1:
            for i in range(4, 14, 1):
                if button_dict[i].collidepoint(mouse):
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                    self.classic_choose(i)
            if button_dict[14].collidepoint(mouse):
                if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                self.game_menu = "start"
            if button_dict[15].collidepoint(mouse):
                if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                self.init_white, self.init_black = [(3, 3), (4, 4)], [(3, 4), (4, 3)]
                self.dim_height, self.dim_width = 8, 8
                self.game_menu = "play"
                time.sleep(0.2)
        for i in range(4, 16, 1):
            self.hover_pre_classic[i] = False
            if button_dict[i].collidepoint(mouse): self.hover_pre_classic[i] = True
    
    def state_pre_custom(self): #TODO        
        self.init_white = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.init_black = [(1, 0), (1, 1), (1, 2), (1, 3)]
        self.dim_height, self.dim_width = 4, 4
        self.game_menu = "play"
        time.sleep(0.2)
        # TEMPORARY PLACEHOLDER TODO

    def state_play(self):
        # Initialize game with the required settings; added bgm for gameplay
        if self.game_state == "prep":
            self.set_config()
            self.ot = Othello(self.dim_height, self.dim_width)
            self.ot.set_initial_position(self.init_white, self.init_black)
            self.ot.turn = 1
            self.game_state = "play"
            self.time_start1 = pygame.time.get_ticks()
            pygame.mixer.music.load(BGM_GAME)
            pygame.mixer.music.play(loops = -1)
        pygame.mixer.music.set_volume((0.2 if self.bgm_on == True else 0))
        
        #print(self.ot.moves_made)
        
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
        
        # Continue to next turn if there are no moves available; end game if no moves in 2 consecutive turns
        moves = self.ot.get_possible_moves()
        self.ot.check_no_move(moves)
        
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
                if self.ot.recent_move == (i, j):
                    circ = pygame.draw.circle(self.screen, recent_move_color, coordinate, self.piece_radius / 3)
        
        # Check if victory
        if self.ot.check_victory() != 0 and self.game_state != "end":
            if self.sfx_on: pygame.mixer.Channel(2).play(pygame.mixer.Sound(SFX_WIN_GAME))
            self.game_state = "end"
        
        # Message to be displayed on screen
        time1, time2 = (self.timer_player1 if self.timer_player1 > 0 else 0), (self.timer_player2 if self.timer_player2 > 0 else 0)
        time1, time2 = f"{(time1 // 60000):02d}:{((time1 // 1000) % 60):02d}:{((time1 // 10) % 100):02d}", f"{(time2 // 60000):02d}:{((time2 // 1000) % 60):02d}:{((time2 // 10) % 100):02d}"
        b1, b2, b3, b4, b5 = f"{self.ot.get_color(self.ot.turn)}'s move (Turn: {self.ot.move_no + 1})", "No winner yet.", "Undo", "Reset", "Quit"
        if self.game_state == "end":
            ms = ("No more moves!" if self.ot.force_win == -1 else "Time is up!")
            b1 = f"{ms} ({self.ot.move_no} turns)"
            b2 = f"{self.ot.get_color(self.ot.check_victory())} wins!"
        button_texts = [f"{time1}", f"{time2}", f"{self.ot.black_tiles}", f"{self.ot.white_tiles}", "Black", "White", b1, b2, b3, b4, b5]

        # Display various user interfaces (scoreboards, messages, buttons)
        scoreRect = pygame.Rect((self.virtual_width * 0.55), (self.virtual_height * 0.05), (self.virtual_width * 0.4), (self.virtual_height * 0.37))
        pygame.draw.rect(self.screen, play_scoreboard_color, scoreRect)
        button_dict = {}
        for i in range(len(button_texts)):
            if (i == 0 or i == 1) and self.classic_time != -1:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + i * 0.18)), (self.virtual_height * 0.07), self.virtual_width / 6, self.virtual_height / 15)
                buttonText = playtimerFont.render(button_texts[i], True, play_timer_color)
                color_x = play_score_color
            elif i == 2 or i == 3:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + (i - 2) * 0.18)), (self.virtual_height * 0.16), self.virtual_width / 6, self.virtual_height / 5)
                buttonText = playscoreFont.render(button_texts[i], True, play_sb_text_color)
                color_x = play_score_color
            elif i == 4 or i == 5:
                buttonRect = pygame.Rect((self.virtual_width * (0.58 + (i - 4) * 0.18)), (self.virtual_height * 0.32), self.virtual_width / 6, self.virtual_height / 15)
                buttonText = playcolorFont.render(button_texts[i], True, play_sb_text_color)
                color_x = play_score_color
            elif i == 6 or i == 7:
                buttonRect = pygame.Rect((self.virtual_width * 0.55), (self.virtual_height * (0.45 + (i - 6) / 6)), self.virtual_width * 0.35, self.virtual_height / 8)
                buttonText = playtextFont.render(button_texts[i], True, play_rect_text_color)
                color_x = play_rect_displayer_color
            else:
                buttonRect = pygame.Rect((self.virtual_width * (0.55 + (i - 8) * 0.12)), (self.virtual_height * 0.79), self.virtual_width * 0.1, self.virtual_height / 8)
                buttonText = playutilFont.render(button_texts[i], True, play_utility_text_color)
                color_x = play_utility_button_color
            button_dict[i] = buttonRect
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(self.screen, color_x, buttonRect)
            self.screen.blit(buttonText, buttonTextRect)
        
        # Update changes when a valid tile is clicked, or when a button is clicked
        if self.confirmation_action == "":
            left, _, _ = pygame.mouse.get_pressed()
            mouse = pygame.mouse.get_pos()
            if left == 1:
                if self.game_state == "play":
                    for i in range(self.dim_height):
                        for j in range(self.dim_width):
                            if tiles[i][j].collidepoint(mouse):
                                if (i, j) in moves:
                                    self.ot.make_move((i, j))
                                    if self.ot.turn == 1:
                                        self.time_start1 = pygame.time.get_ticks()
                                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_WHITE_MOVE))
                                    elif self.ot.turn == 2:
                                        self.time_start2 = pygame.time.get_ticks()
                                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_BLACK_MOVE))
                                elif self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_BUTTON_INVALID))
                if button_dict[8].collidepoint(mouse) or button_dict[9].collidepoint(mouse) or button_dict[10].collidepoint(mouse):
                    if self.sfx_on: pygame.mixer.Channel(3).play(pygame.mixer.Sound(SFX_BUTTON_CLICK))
                if button_dict[8].collidepoint(mouse): self.confirmation_action = "Undo" # Undo last move button
                if button_dict[9].collidepoint(mouse): self.confirmation_action = "Reset" # Reset board button (restart game with the same configuration)
                if button_dict[10].collidepoint(mouse): self.confirmation_action = "Quit" # Quit button (back to main menu)
                
        # Display confirmation screen and yes/no buttons, proceed with action when 'yes' is clicked, back to game when 'no' is clicked
        if self.confirmation_action != "":
            confRectborder = pygame.Rect((self.virtual_width / 4), (self.virtual_height / 4), (self.virtual_width / 2), (self.virtual_height / 2))
            confRect = pygame.Rect((self.virtual_width / 4 + 3), (self.virtual_height / 4 + 3), (self.virtual_width / 2 - 6), (self.virtual_height / 2 - 6))
            confText1 = confFont1.render(f"Confirm {self.confirmation_action}?", True, black)
            confText2 = confFont2.render("Warning! This cannot be undone!", True, black)
            confTextRect1 = confText1.get_rect(center = (self.virtual_width / 2, self.virtual_height * 0.35))
            confTextRect2 = confText2.get_rect(center = (self.virtual_width / 2, self.virtual_height * 0.45))
            pygame.draw.rect(self.screen, conf_screen_border_color, confRectborder)
            pygame.draw.rect(self.screen, conf_screen_color, confRect)
            self.screen.blit(confText1, confTextRect1)
            self.screen.blit(confText2, confTextRect2)
            yes, no = confFont3.render("Yes", True, black), confFont3.render("No", True, black)
            if self.hover_yes: yes = confFont4.render("Yes", True, conf_hover_color)
            if self.hover_no: no = confFont4.render("No", True, conf_hover_color)
            yes_rect = yes.get_rect(center = (self.virtual_width * 0.45, self.virtual_height * 0.55))
            no_rect = no.get_rect(center = (self.virtual_width * 0.55, self.virtual_height * 0.55))
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
                        time.sleep(0.2)
                    if self.confirmation_action == "Quit":
                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_QUIT_GAME))
                        self.game_menu = "start"
                        self.game_state = "prep"
                        self.set_config()
                    if self.confirmation_action == "Reset":
                        if self.sfx_on: pygame.mixer.Channel(1).play(pygame.mixer.Sound(SFX_RESET_GAME))
                        self.game_state = "prep"
                        self.set_config()
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
1. Improve UI in pre_classic state (hover effects) and play state
2. Add undo feature
3. Create pre_custom feature user interface
4. Add AI level 1 and basic against AI gameplay
5. 'How to play' pages and pics, UI
6. AI minimax algorithm??
7. Puzzle mode??

- Pre_custom UI
- Fix UI, texts and colors
- Add Undo Feature
- AI simple level 1 (random moves)
- Custom othello sizes and vs ai mode
- etc.. (coming soon)
BUGS:
Handles self.timer when choosing timer!!!
"""
