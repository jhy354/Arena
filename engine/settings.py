# * Basic Settings * #
AUTHOR_NAME = "jhy354(Romulus)"
GITHUB_URL = r"https://github.com/jhy354/Arena"
AUTHOR_URL = r"https://github.com/jhy354/"
SCR_SIZE = (1280, 960)
FPS = 144
MOVEMENT_RATING = 100

VERSION = "e0.1.0.0429"
CAPTION = "Arena - " + VERSION

FONT_CHS_LIST = [
    "simhei",
    "dengxian",
]
FONT_ENG_LIST = [
    "calibri",
    "arial",
]

# Server Settings #
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1453
HEADER = 1024  # Default header length
SERVER_TIMEOUT = 0.001
CLIENT_TIMEOUT = 0.001
MAX_LISTEN = 5

# * Game Settings * #
DEBUG_MODE = True

# * Layer Settings * #
LAYERS = {
    "background": 0,
    "background_shadow": 1,

    "map_background": 18,
    "map_edge": 19,
    "map_floor": 20,
    "map_break": 21,
    "map_gravity": 22,

    "default": 30,

    "bullet": 39,
    "player": 40,
    "weapon": 41,

    "map_decoration": 50,
    "map_decoration2": 51,
    "map_decoration3": 52,

    "prop": 60,

    "fog": 70,

    "ui": 100,
    "noise": 101,
}

# * Crown Color Settings * #
CROWN_COLOR = {
    "contested": "gray",
    "1": "red",
    "2": "blue"
}
