import pygame as pg

DEBUG_LOGGING = True

EMPTY_SYMBOL = '-'
TUBE_HEIGHT = 4

FPS = 15

# define all the colors used as RGB values
COLORS = {
    "BLACK": (0, 0, 0),
    "GRAY": (127, 127, 127),
    "WHITE": (255, 255, 255),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 215, 0),
    "MINT_GREEN": (152, 255, 152),
    "BROWN": (165, 42, 42),
    "RED": (255, 0, 0),
    "BEIGE": (244, 226, 198),
    "YELLOW": (255, 255, 0),
    "DARK_GREEN": (0, 100, 0),
    "GREEN": (0, 255, 0),
    "PINK": (255, 192, 203),
    "CYAN": (0, 255, 255),
    "PURPLE": (128, 0, 128),
    "INDIGO": (75, 0, 130),
    EMPTY_SYMBOL: (127, 127, 127)  # GRAY - default background color
}

# set default background color
BACKGROUND_COLOR = COLORS[EMPTY_SYMBOL]

# graphics constants
WIDTH, HEIGHT = WINDOW_SIZE = (900, 600)

TUBE_GRAPHIC_WIDTH, TUBE_GRAPHIC_HEIGHT = WIDTH // 10, HEIGHT // 2
TUBE_BORDER_WIDTH = 5
TUBE_BORDER_RADIUS = TUBE_GRAPHIC_WIDTH // 2
TUBE_VISUAL_INDICATOR_OFFSET = 20

# pygame events

UPDATE_TUBE_EVENT = pg.USEREVENT + 1
HINT_BUTTON_EVENT = pg.USEREVENT + 2
