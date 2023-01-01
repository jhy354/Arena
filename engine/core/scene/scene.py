from random import randint

import pygame
from pytmx import load_pygame

from engine import layout
from engine.settings import *
from engine.path import *
from engine.widget.sprite import Player
from engine.widget.sprite import DefaultCfg
from engine.widget.sprite import P2Cfg
from engine.utils import Debug
from engine.utils import custom_load
from engine.widget.sprite import Generic
from engine.widget.sprite import GameObject
from engine.widget.sprite import Fog
from engine.core.camera import CameraGroup


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


class PlayGround(Scene):
    """
    玩家进行游戏的场景
    """

    def __init__(self, map_index, background_index):
        super().__init__()

        self.map_index = map_index
        self.background_index = background_index

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
        # 其他功能在 engine 中 weapons.py 中实现
        self.weapon = None

        # * Special Effects * #
        self.fog_1 = None
        self.fog_2 = None

        Debug(True) << "Inited PlayGround" << "\n"

    def run(self, dt):
        super().run(dt)
        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.check_bullet_coll()
        self.fog_1.move()
        self.fog_2.move()

    def horizontal_movement_coll(self, dt):
        for player in self.player_group.sprites():

            player.rect.x += player.direction.x * dt * MOVEMENT_RATING

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

            player.update_weapon()

    def vertical_movement_coll(self, dt):
        for player in self.player_group.sprites():
            player.apply_gravity()

            player.rect.y += player.direction.y * dt * MOVEMENT_RATING

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.jump_cnt = 0
                        if not player.can_jump and not player.push_space:
                            player.can_jump = True
                            Debug(DEBUG_MODE) << "(Player) Enabled Jump" << "\n"
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.can_jump = False

    def check_bullet_coll(self):
        for group in self.bullet_groups:
            for bullet in group.sprites():
                coll_wall_first = False

                for sprite in self.coll_rect_sprites.sprites():
                    if sprite.rect.colliderect(bullet.rect):
                        bullet.destroy()
                        coll_wall_first = True

                for player in self.player_group.sprites():
                    if player.rect.colliderect(bullet.rect):
                        if bullet not in player.weapon.bullet_group:
                            bullet.destroy()
                            if not coll_wall_first:
                                player.get_shot(bullet.damage)

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
            surf=custom_load(PATH_BACKGROUND[self.background_index], layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        # * Load Map Data * #
        tmx_data = load_pygame(PATH_MAP[self.map_index])

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
