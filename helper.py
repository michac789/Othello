# Helper file associated with runner.py
from pygame import font, init, image

# This library is used to ensure that the assets can be loaded independently of user's operating system
from os import path

# Define all RGB colors for various components here
main_title_color = (0, 255, 255)
main_button1_color = (217, 255, 179)
main_button1_hover_color = (217, 255, 209)
main_button1_text_color = (0, 51, 0)
main_button1_text_hover_color = (255, 0, 255)
main_button2_color = (255, 204, 153)
main_button2_hover_color = (255, 226, 163)
main_button2_text_color = (0, 0, 128)
main_button2_text_hover_color = (185, 0, 102)

mode_title = (255, 153, 255)
prep_text_color1 = (204, 255, 255)
prep_text_color2 = (255, 224, 224)
prep_option_color1 = (0, 51, 0)
prep_option_color2 = (0, 0, 153)
prep_option_color3 = (128, 0, 0)
prep_button_color1 = (240, 250, 255)
prep_button_color2 = (200, 225, 245)
prep_button_hover_color1 = (230, 77, 0)
prep_button_hover_color2 = (200, 25, 145)
prep_rect_hover_color = (179, 255, 255)
prep_chosen_color = (255, 210, 10)

custom_button_color1 = (255, 230, 204)
custom_button_color2 = (153, 255, 51)
custom_button_hover_color1 = (255, 255, 0)
custom_button_hover_color2 = (0, 204, 0)
custom_button_noclick_color = (70, 70, 70)

play_scoreboard_color = (115, 77, 38)
play_timer_color = (104, 43, 203)
play_score_color = (102, 255, 204)
play_sb_text_color = (0, 60, 102)
play_rect_displayer_color = (218, 179, 255)
play_rect_text_color = (51, 51, 0)
play_utility_text_color = (0, 64, 128)
play_utility_text_color_hover = (115, 0, 153)
play_utility_button_color = (223, 255, 128)

black = (0, 0, 0)
white = (255, 255, 255)
dark_grey = (60, 60, 60)
tile_color = (0, 160, 0)
tile_border_color = (110, 38, 14)
board_color = (50, 50, 50)
moves_color = (100, 100, 100)
recent_move_color = (255, 0, 0)
conf_screen_border_color = (30, 45, 240)
conf_screen_color = (75, 145, 200)
conf_text1_color = (96, 31, 64)
conf_text2_color = (179, 0, 0)
conf_hover_color = (159, 200, 45)

# Define all fonts used here
OPEN_SANS = path.join("assets", "fonts", "OpenSans-Regular.ttf")
PACIFICO = path.join("assets", "fonts", "Pacifico.ttf")
BLACKJACK = path.join("assets", "fonts", "blackjack.otf")
LOBSTER = path.join("assets", "fonts", "Lobster.otf")
ARIZONIA = path.join("assets", "fonts", "Arizonia-Regular.ttf")

# Define all background musics used here
BGM_MENU = path.join("assets", "bgm", "menumusic.mp3")
BGM_GAME = path.join("assets", "bgm", "gamemusic.mp3")

# Define all sfx used here
SFX_BLACK_MOVE = path.join("assets", "sfx", "black_move.wav")
SFX_WHITE_MOVE = path.join("assets", "sfx", "white_move.wav")
SFX_RESET_GAME = path.join("assets", "sfx", "reset_game.wav")
SFX_UNDO_GAME = path.join("assets", "sfx", "undo_game.wav")
SFX_QUIT_GAME = path.join("assets", "sfx", "quit_game.wav")
SFX_WIN_GAME = path.join("assets", "sfx", "win_game.wav")
SFX_BUTTON_CLICK = path.join("assets", "sfx", "button_click.wav")
SFX_BUTTON_INVALID = path.join("assets", "sfx", "button_invalid.wav")

# Define all icons (images) used here
BGM_TRUE = path.join("assets", "icons", "bgm_true.jpg")
BGM_FALSE = path.join("assets", "icons", "bgm_false.jpg")
BGM_TRUE_HOVER = path.join("assets", "icons", "bgm_true_hover.jpg")
BGM_FALSE_HOVER = path.join("assets", "icons", "bgm_false_hover.jpg")
SFX_TRUE = path.join("assets", "icons", "sfx_true.jpg")
SFX_FALSE = path.join("assets", "icons", "sfx_false.jpg")
SFX_TRUE_HOVER = path.join("assets", "icons", "sfx_true_hover.jpg")
SFX_FALSE_HOVER = path.join("assets", "icons", "sfx_false_hover.jpg")
BGM_TRUE = image.load(BGM_TRUE)
BGM_FALSE = image.load(BGM_FALSE)
BGM_TRUE_HOVER = image.load(BGM_TRUE_HOVER)
BGM_FALSE_HOVER = image.load(BGM_FALSE_HOVER)
SFX_TRUE = image.load(SFX_TRUE)
SFX_FALSE = image.load(SFX_FALSE)
SFX_TRUE_HOVER = image.load(SFX_TRUE_HOVER)
SFX_FALSE_HOVER = image.load(SFX_FALSE_HOVER)

# Define images in 'how to play' section
#TODO
