import game.layout as layout
import game.text_script as text_script
from engine.layout import *
from engine.path import *
from engine.settings import *
from engine.core.scene import Scene
from engine.utils import custom_load
from engine.utils import Debug
from engine.widget.ui import TextButton
from engine.widget.sprite import Generic


class StartMenu(Scene):
    """
    开始菜单界面
    """

    def __init__(self):
        super().__init__()

        self.background = Generic(
            pos=BG_POS,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        self.game_title = Generic(
            pos=layout.SM_TITLE,
            surf=custom_load(PATH_UI_TEXT + "game_title.png", layout.SM_TITLE_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        # * Buttons * #

        self.start_button = TextButton(
            text=text_script.START_GAME,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_START,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.quit_button = TextButton(
            text=text_script.QUIT_GAME,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_QUIT,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.settings_button = TextButton(
            text=text_script.SETTINGS,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_SETTINGS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.about_button = TextButton(
            text=text_script.ABOUT,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_ABOUT,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        Debug(True) << "Inited StartMenu" << "\n"
        Debug(True).div()

    def activate(self):
        super().activate()
        Debug(True) << "Activated StartMenu" << "\n"

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated StartMenu" << "\n"
        Debug(True).div()

    def _setup(self):
        super()._setup()
        self.start_button.activate()
        self.quit_button.activate()
        self.settings_button.activate()
        self.about_button.activate()

    def _release(self):
        super()._release()
        self.start_button.deactivate()
        self.quit_button.deactivate()
        self.settings_button.deactivate()
        self.about_button.deactivate()
        Debug(True) << "Released StartMenu" << "\n"

    def run(self, dt):
        super().run(dt)
