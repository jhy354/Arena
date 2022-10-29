import pygame

import layout
import text_script
from settings import *
from utils import Debug
from player import Player
from sprites import Generic
from sprites import TextButton
from sprites import Map
from support import import_folder
from support import custom_load


class Scene:
    """
    场景基类定义
    """

    def __init__(self):
        # * General * #
        self.active = False
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.surface.Surface(SCR_SIZE)

        # * Groups * #
        self.all_sprites = CameraGroup()
        self.coll_rect_sprites = pygame.sprite.Group()
        self.coll_mask_sprites = pygame.sprite.Group()

    def activate(self):
        """
        激活场景
        """
        self.active = True
        self._setup()

    def deactivate(self):
        """
        停用场景
        """
        self.active = False
        self._release()

    def _setup(self):
        """
        调用 activate() 时运行
        protected function
        """

    def _release(self):
        """
        调用 deactivate() 时运行
        protected function
        """
        self.all_sprites.empty()

    def run(self, dt):
        """
        在 self.active == True 时循环运行
        """
        self.display_surface.fill("black")
        self.all_sprites.custom_draw()
        self.all_sprites.update(dt)


class StartMenu(Scene):
    """
    开始菜单界面
    """

    def __init__(self):
        super().__init__()

        self.background = Generic(
            pos=layout.SM_BG,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", layout.SM_BG_SIZE),
            group=self.all_sprites,
            z=LAYERS["background"]
        )

        self.game_title = Generic(
            pos=layout.SM_TITLE,
            surf=custom_load(PATH_TEXT + "game_title.png", layout.SM_TITLE_SIZE),
            group=self.all_sprites
        )

        self.start_button = TextButton(
            text=text_script.START_GAME,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_START,
            group=self.all_sprites,
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

    def _release(self):
        super()._release()
        self.start_button.deactivate()
        Debug(True) << "Released StartMenu" << "\n"

    def run(self, dt):
        super().run(dt)


class PlayGround(Scene):
    """
    玩家进行游戏的场景
    """
    def __init__(self):
        super().__init__()

        self.map = Generic(
            pos=(0, 0),
            surf=import_folder(PATH_MAP_IMG, SCR_SIZE)[0],
            group=self.all_sprites,
            z=LAYERS["map"]
        )

        self.map_cb = Map(
            pos=(0, 0),
            surf=import_folder(PATH_MAP_COLL, SCR_SIZE)[0],
            group=[self.all_sprites, self.coll_mask_sprites],
            z=LAYERS["map_coll"]
        )

        self.player = Player(layout.SCR_CENTER, self.all_sprites, self.coll_rect_sprites, self.coll_mask_sprites)

        Debug(True) << "Inited PlayGround" << "\n"

    def activate(self):
        super().activate()
        Debug(True) << "Activated PlayGround" << "\n"

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated PlayGround" << "\n"
        Debug(True).div()

    def _setup(self):
        super()._setup()
        self.player.activate()

    def _release(self):
        super()._release()
        Debug(True) << "Released PlayGround" << "\n"

    def run(self, dt):
        super().run(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        """
        按图层顺序画出当前 Group 中所有 Sprite
        """
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)
