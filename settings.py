# * Basic Settings * #
SCR_SIZE = (1280, 960)
FPS = 144
FONT = "方正粗黑宋简体"
MOVEMENT_RATING = 100

VERSION = "e0.0.2.1111"
CAPTION = "Arena - e" + VERSION

# * Game Settings * #
DEBUG_MODE = True

# * Path Settings * #
PATH_ASSETS = r"./assets/"

# UI
PATH_UI_BG = r"./assets/ui/background/"
PATH_BUTTON = r"./assets/ui/button/"
PATH_UI_ETC = r"./assets/ui/etc/"
PATH_EFFECT = r"./assets/ui/special_effect/"
PATH_TEXT = r"./assets/ui/text/"

# Player
PATH_PLAYER = r"./assets/game/player/"
PATH_PLAYER_FOOT = "./assets/game/player/etc/foot.png"

# Map
PATH_MAP_DU_ARENA = "./assets/game/map/du_arena/du_arena.tmx"
PATH_MAP_DU_DUST = "./assets/game/map/du_dust/du_dust.tmx"

# * Layer Settings * #
LAYERS = {
    "background": 0,
    "map_floor": 1,
    "default": 3,
    "weapon": 4,
    "player": 5,
    "map_decoration": 6,
    "prop": 7,
    "fog": 8,
    "ui": 9,
}
