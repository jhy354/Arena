from random import randint

import pygame
from pytmx import load_pygame

from .scene import Scene
from engine import layout
from engine.settings import *
from engine.path import *
from engine.widget.sprite import Player
from engine.widget.sprite import P1Cfg
from engine.utils import Debug
from engine.utils import custom_load
from engine.widget.sprite import Generic
from engine.widget.sprite import GameObject


class Level(Scene):
    """
    长场景
    """

    def __init__(self, map_index, background_index):
        super().__init__()

        self.map_index = map_index
        self.background_index = background_index

        self.background = None

        # * TimerUI * #
        self.timer_ui = None

        # * Map Tiles * #
        self.map_edges = []
        self.map_floors = []

        # * Groups * #
        self.player_group = pygame.sprite.Group()
        self.bullet_groups = []

        # * Players * #
        self.player_1 = None

        self.weapon = None

        Debug(True) << "Inited PlayGround" << "\n"

    def setup(self):
        super().setup()

        '''
        # * Load Background * #
        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_BACKGROUND[self.background_index], layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )
        '''

        # * Load Map Data * #
        tmx_data = load_pygame(PATH_MAP_LEVEL[self.map_index])

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
        p1_cfg = P1Cfg()
        p1_cfg.skin = p1_skin

        self.player_1 = Player(
            [self.all_sprites, self.player_group],
            p1_cfg
        )

        for player in self.player_group.sprites():
            player.activate()

        # * Init Bullet Group * #
        for player in self.player_group.sprites():
            self.bullet_groups.append(player.weapon.bullet_group)

        Debug(True) << "All Sprites in Current Scene: " << str(self.all_sprites) << "\n"
        Debug(True) << "Loaded Level" << "\n"

    def release(self):
        super().release()
        Debug(True) << "Released Level" << "\n"

    def run(self, dt):
        super().run(dt)
        offset_x = self.player_1.rect.centerx - layout.SCR_CENTER[0]
        offset_y = self.player_1.rect.centery - layout.SCR_CENTER[1]
        self.all_sprites.custom_draw_level(offset_x, offset_y)
        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.check_bullet_coll()

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

                coll_flag = False

                for sprite in self.coll_rect_sprites.sprites():
                    if sprite.rect.colliderect(bullet.rect):
                        bullet.destroy()
                        coll_flag = True
                        break

                if coll_flag:
                    continue

                for player in self.player_group.sprites():
                    if player.rect.colliderect(bullet.rect):
                        if bullet not in player.weapon.bullet_group:

                            if player.get_shot(bullet.damage):
                                for p in self.player_group.sprites():
                                    if bullet in p.weapon.bullet_group:
                                        p.kills += 1
                                        self.update_crown()
                                        Debug(DEBUG_MODE) << f"(Player) Kills: {p.kills}" << "\n"

                            bullet.destroy()
                            break

    def activate(self):
        super().activate()
        Debug(True) << "Activated PlayGround" << "\n"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated PlayGround" << "\n"
        Debug(True).div()
