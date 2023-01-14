import webbrowser

import pygame

from engine.path import *
from engine.settings import *
from engine import text_script
from game import layout as glayout
from engine import layout
from engine.utils import custom_load
from engine.utils import Debug
from engine.utils import render_text
from engine.utils import set_fonts
from engine.core.scene import Scene
from engine.widget.sprite import Generic
from engine.widget.ui import TextButton
from engine.widget.ui import UrlButton


class AboutPage(Scene):
    """
    关于页面
    """

    def __init__(self):
        super().__init__()

        self.background = None
        self.shadow = None
        self.back_button = None

        self.url = None
        self.url_text = None

        self.logo = None
        self.title = None

        self.version_text = None
        self.author_text = None
        self.author_url = None

        self.setup()

    def setup(self):
        super().setup()

        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        shadow = pygame.surface.Surface(glayout.AP_SHADOW_SIZE, pygame.SRCALPHA)
        shadow.fill(glayout.AP_SHADOW_COLOR)
        self.shadow = Generic(
            pos=glayout.AP_SHADOW_POS,
            surf=shadow,
            group=[self.all_sprites],
            z=LAYERS["background_shadow"]
        )

        self.back_button = TextButton(
            text=text_script.AP_BACK,
            size=glayout.AP_BUTTON_TEXT_SIZE,
            color=(169, 169, 169),
            pos=glayout.AP_BACK_POS,
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        font_chs, font_eng = set_fonts(FONT_CHS_LIST, FONT_ENG_LIST)
        self.url_text = Generic(
            pos=glayout.AP_URL_TEXT_POS,
            surf=render_text(text_script.AP_URL_TEXT, font_eng, glayout.AP_TEXT_SIZE, glayout.AP_TEXT_COLOR),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.url = UrlButton(
            text=GITHUB_URL,
            size=glayout.AP_TEXT_SIZE,
            color=glayout.AP_URL_COLOR,
            pos=glayout.AP_URL_POS,
            group=[self.all_sprites],
            url=GITHUB_URL,
            z=LAYERS["ui"]
        )

        self.logo = Generic(
            pos=glayout.AP_LOGO_POS,
            surf=custom_load(PATH_UI_ICON + "logo.png", glayout.AP_LOGO_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.title = Generic(
            pos=glayout.AP_TITLE_POS,
            surf=custom_load(PATH_UI_TEXT + "game_title.png", glayout.AP_TITLE_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.version_text = Generic(
            pos=glayout.AP_VERSION_POS,
            surf=render_text(text_script.AP_VERSION_TEXT, font_eng, glayout.AP_TEXT_SIZE, glayout.AP_TEXT_COLOR),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.author_text = Generic(
            pos=glayout.AP_AUTHOR_TEXT_POS,
            surf=render_text(text_script.AP_AUTHOR_TEXT, font_eng, glayout.AP_TEXT_SIZE, glayout.AP_TEXT_COLOR),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.author_url = UrlButton(
            text=AUTHOR_NAME,
            size=glayout.AP_TEXT_SIZE,
            color=glayout.AP_URL_COLOR,
            pos=glayout.AP_AUTHOR_URL_POS,
            group=[self.all_sprites],
            url=AUTHOR_URL,
            z=LAYERS["ui"]
        )

        Debug(True) << "All Sprites in Current Scene: " << str(self.all_sprites) << "\n"
        Debug(True) << "Loaded AboutPage" << "\n"

    def release(self):
        super().release()

        Debug(True) << "Released AboutPage" << "\n"
        Debug(True).div()

    def activate(self):
        super().activate()

        self.back_button.activate()
        self.url.activate()
        self.author_url.activate()

        Debug(True) << "Activated AboutPage" << "\n"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()

        self.back_button.deactivate()
        self.url.deactivate()
        self.author_url.deactivate()

        Debug(True) << "Deactivated AboutPage" << "\n"
        Debug(True).div()
