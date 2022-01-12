# Helper file associated with runner.py
from pygame import font, init

# Define all RGB colors for various components here
black = (0, 0, 0)
white = (255, 255, 255)
tile_color = (0, 160, 0)
tile_border_color = (110, 38, 14)
board_color = (50, 50, 50)
moves_color = (100, 100, 100)
score_color = (104, 43, 203)
recent_move_color = (255, 0, 0)
conf_screen_border_color = (30, 45, 240)
conf_screen_color = (75, 145, 200)
conf_hover_color = (159, 200, 45)

# Define all fonts used here
init()
OPEN_SANS = "OpenSans-Regular.ttf"
smallFont = font.Font(OPEN_SANS, 20)
hugeFont = font.Font(OPEN_SANS, 40)
titleFont = font.Font(OPEN_SANS, 50)
buttonFont = font.Font(OPEN_SANS, 30)
confFont1 =  font.Font(OPEN_SANS, 25)
confFont2 =  font.Font(OPEN_SANS, 15)
confFont3 = font.Font(OPEN_SANS, 30)
confFont4 = font.Font(OPEN_SANS, 35)
preptextFont = font.Font(OPEN_SANS, 25)
