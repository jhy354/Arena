# * Basic Settings * #
SCR_SIZE = (1280, 720)
FPS = 60
FONT = "方正粗黑宋简体"

VERSION = "0.0.1.1022"
CAPTION = "Arena - v" + VERSION

# * Game Settings * #
DEBUG_MODE = True

# * Path Settings * #
PATH_ASSETS = r"./assets/"
PATH_UI_BG = r"./assets/ui/background/"
PATH_BUTTON = r"./assets/ui/button/"
PATH_UI_ETC = r"./assets/ui/etc/"
PATH_EFFECT = r"./assets/ui/special_effect/"
PATH_TEXT = r"./assets/ui/text/"
PATH_PLAYER = r"./assets/game/player/"
PATH_MAP_IMG = r"./assets/game/map/image/"
PATH_MAP_COLL = r"./assets/game/map/collision_box/"

# * Layer Settings * #
LAYERS = {
    "background": 0,
    "map_coll": 1,  # Collision Box
    "map": 2,
    "default": 3,
    "weapon": 4,
    "player": 5,
    "prop": 6,
    "fog": 7,
    "ui": 8
}
