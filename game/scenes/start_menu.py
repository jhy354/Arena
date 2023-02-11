from engine.path import *
from engine.settings import *
from game import layout as glayout
from engine import layout
from engine import text_script
from engine.core.scene import Scene
from engine.utils import Debug
from engine.utils import custom_load
from engine.utils import import_folder
from engine.utils import set_fonts
from engine.utils import render_text
from engine.widget.ui import TextButton
from engine.widget.ui import DisplayCase
from engine.widget.sprite import Noise
from engine.widget.sprite import Generic


class StartMenu(Scene):
    """
    开始菜单界面
    """

    def __init__(self):
        super().__init__()

        self.background = None
        self.game_title = None
        self.version_text = None
        self.noise = None
        self.player_display_case = None

        # * Buttons * #
        self.start_button = None
        self.quit_button = None
        self.settings_button = None
        self.about_button = None

        Debug(True) << "Inited StartMenu" << "\n"
        Debug(True).div()

    def activate(self):
        super().activate()

        self.player_display_case.activate()

        self.start_button.activate()
        self.quit_button.activate()
        self.settings_button.activate()
        self.about_button.activate()

        Debug(True) << "Activated StartMenu" << "\n"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()

        self.player_display_case.deactivate()

        self.start_button.deactivate()
        self.quit_button.deactivate()
        self.settings_button.deactivate()
        self.about_button.deactivate()

        Debug(True) << "Deactivated StartMenu" << "\n"
        Debug(True).div()

    def setup(self):
        super().setup()

        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        self.game_title = Generic(
            pos=glayout.SM_TITLE_POS,
            surf=custom_load(PATH_UI_TEXT + "game_title.png", glayout.SM_TITLE_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        font_chs, font_eng = set_fonts(FONT_CHS_LIST, FONT_ENG_LIST)
        self.version_text = Generic(
            pos=glayout.SM_VERSION_POS,
            surf=render_text(text_script.SM_VERSION_TEXT, font_eng, glayout.SM_TEXT_SIZE, glayout.SM_TEXT_COLOR),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        # * Noise * #
        self.noise = Noise(
            pos=(0, 0),
            surf=custom_load(PATH_EFFECT_NOISE, SCR_SIZE),
            group=[self.all_sprites]
        )

        # * Player Display Case * #
        self.player_display_case = DisplayCase(
            start_pos=(900, 0),
            surf_list=import_folder(PATH_UI_P_DISPLAY_CASE, glayout.SM_P_DISPLAY_CASE_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        # * Buttons * #
        self.start_button = TextButton(
            text=text_script.SM_START_GAME,
            size=glayout.SM_BUTTON_TEXT_SIZE,
            color=glayout.SM_BUTTON_COLOR,
            pos=glayout.SM_START_POS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.quit_button = TextButton(
            text=text_script.SM_QUIT_GAME,
            size=glayout.SM_BUTTON_TEXT_SIZE,
            color=glayout.SM_BUTTON_COLOR,
            pos=glayout.SM_QUIT_POS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.settings_button = TextButton(
            text=text_script.SM_SETTINGS,
            size=glayout.SM_BUTTON_TEXT_SIZE,
            color=glayout.SM_BUTTON_COLOR,
            pos=glayout.SM_SETTINGS_POS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.about_button = TextButton(
            text=text_script.SM_ABOUT,
            size=glayout.SM_BUTTON_TEXT_SIZE,
            color=glayout.SM_BUTTON_COLOR,
            pos=glayout.SM_ABOUT_POS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        Debug(True) << "All Sprites in Current Scene: " << str(self.all_sprites) << "\n"
        Debug(True) << "Loaded StartMenu" << "\n"

    def release(self):
        super().release()

        self.player_display_case.deactivate()

        self.start_button.deactivate()
        self.quit_button.deactivate()
        self.settings_button.deactivate()
        self.about_button.deactivate()

        Debug(True) << "Released StartMenu" << "\n"
        Debug(True).div()

    def run(self, dt):
        super().run(dt)

        self.player_display_case.update()
