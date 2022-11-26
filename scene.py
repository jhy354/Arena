from random import randint

import pygame
from pytmx.util_pygame import load_pygame

import layout
import text_script
from settings import *
from path import *
from utils import Debug
from player import Player
from player import DefaultCfg
from player import P2Cfg
from sprites import Generic
from sprites import GameObject
from sprites import TextButton
from sprites import Fog
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
        self.display_surface.fill("white")
        self.all_sprites.custom_draw()
        self.all_sprites.update(dt)


class StartMenu(Scene):
    """
    开始菜单界面
    """

    def __init__(self):
        super().__init__()

        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", layout.BG_SIZE),
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


class PlayGround(Scene):
    """
    玩家进行游戏的场景
    """

    def __init__(self):
        super().__init__()

        self.background = None

        # * Map Tiles * #
        self.map_edges = []
        self.map_floors = []

        # * Groups * #
        self.player_group = pygame.sprite.Group()
        self.bullet_groups = []

        # * Players * #
        self.player_1 = None
        self.player_2 = None

        # * Weapon * #
        # Weapon 只是一个跟随 player 移动的 surface
        # 不实现其他功能
        # 其他功能在 weapon.py 中实现
        self.weapon = None

        # * Special Effects * #
        self.fog_1 = None
        self.fog_2 = None

        Debug(True) << "Inited PlayGround" << "\n"

    def horizontal_movement_coll(self, dt):
        """
        注意 update_hitbox() 在代码中的执行位置
        否则碰撞会出错
        """
        for player in self.player_group.sprites():

            player.rect.x += player.direction.x * dt * MOVEMENT_RATING
            player.update_hitbox()

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.hitbox):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        player.update_hitbox()
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                        player.update_hitbox()

    def vertical_movement_coll(self, dt):
        for player in self.player_group.sprites():
            player.apply_gravity()

            player.rect.y += player.direction.y * dt * MOVEMENT_RATING
            player.update_hitbox()

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.hitbox):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.update_hitbox()
                        player.direction.y = 0
                        player.jump_cnt = 0
                        if not player.can_jump and not player.push_space:
                            player.can_jump = True
                            Debug(DEBUG_MODE) << "(Player) Enabled Jump" << "\n"
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.update_hitbox()
                        player.direction.y = 0
                        player.can_jump = False

    def check_bullet_coll(self):
        for group in self.bullet_groups:
            for bullet in group.sprites():

                for sprite in self.coll_rect_sprites:
                    if sprite.rect.colliderect(bullet.rect):
                        bullet.destroy()

    def activate(self):
        super().activate()
        Debug(True) << "Activated PlayGround" << "\n"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated PlayGround" << "\n"
        Debug(True).div()

    def _setup(self):
        super()._setup()

        # * Load Background * #
        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_UI_BG + "1_bg_dust.png", layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        # * Load Map Data * #
        rand_map = randint(0, len(PATH_MAP) - 1)
        tmx_data = load_pygame(PATH_MAP[rand_map])

        for x, y, surf in tmx_data.get_layer_by_name("edge").tiles():
            self.map_edges.append(
                Generic(
                    pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                    surf=surf,
                    group=[self.all_sprites],
                    z=LAYERS["map_floor"]
                )
            )

        for x, y, surf in tmx_data.get_layer_by_name("floor").tiles():
            self.map_floors.append(
                GameObject(
                    pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                    surf=surf,
                    group=[self.all_sprites, self.coll_rect_sprites],
                    z=LAYERS["map_floor"]
                )
            )

        for x, y, surf in tmx_data.get_layer_by_name("decoration").tiles():
            self.map_floors.append(
                GameObject(
                    pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                    surf=surf,
                    group=[self.all_sprites],
                    z=LAYERS["map_decoration"]
                )
            )

        # * Load Player * #
        p1_skin = SKIN_DICT[randint(0, len(SKIN_DICT) - 1)]
        p2_skin = SKIN_DICT[randint(0, len(SKIN_DICT) - 1)]
        p1_cfg = DefaultCfg()
        p1_cfg.skin = p1_skin
        p2_cfg = P2Cfg()
        p2_cfg.skin = p2_skin

        self.player_1 = Player(
            [self.all_sprites, self.player_group],
            p1_cfg
        )

        self.player_2 = Player(
            [self.all_sprites, self.player_group],
            p2_cfg
        )

        for player in self.player_group.sprites():
            player.activate()

        # * Load Fog * #
        self.fog_1 = Fog(
            pos=(0, 0),
            surf=custom_load(PATH_EFFECT_FOG + "fog_thin.png", layout.FOG_SIZE),
            group=[self.all_sprites],
        )

        self.fog_2 = Fog(
            pos=(-SCR_SIZE[0], 0),
            surf=custom_load(PATH_EFFECT_FOG + "fog_thin.png", layout.FOG_SIZE),
            group=[self.all_sprites],
        )

        # * Bullet Group * #
        for player in self.player_group.sprites():
            self.bullet_groups.append(player.weapon.bullet_group)

    def _release(self):
        super()._release()
        Debug(True) << "Released PlayGround" << "\n"

    def run(self, dt):
        super().run(dt)
        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.check_bullet_coll()
        self.fog_1.move()
        self.fog_2.move()


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
