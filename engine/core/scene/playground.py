from random import randint

import pygame
from pytmx import load_pygame

from .scene import Scene
from engine import text_script
from engine import layout
from engine.settings import *
from engine.path import *
from engine.widget.sprite import Player
from engine.widget.sprite import P1Cfg
from engine.widget.sprite import P2Cfg
from engine.utils import Debug
from engine.utils import custom_load
from engine.utils import render_text
from engine.utils import set_fonts
from engine.widget.sprite import Generic
from engine.widget.sprite import GameObject
from engine.widget.sprite import Fog


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

        # * Crown * #
        self.crown = None
        self.crown_text_sprite = None
        self.crown_text = text_script.CONTESTED

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
        p1_cfg = P1Cfg()
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

        # * Init Bullet Group * #
        for player in self.player_group.sprites():
            self.bullet_groups.append(player.weapon.bullet_group)

        # * Crown * #
        self.crown = Generic(
            pos=layout.CROWN_POS,
            surf=custom_load(PATH_UI_ICON + "crown/crown_gray.png", layout.CROWN_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.crown_text_sprite = Generic(
            pos=layout.CROWN_TEXT_POS,
            surf=pygame.surface.Surface((1, 1)),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.update_crown()

        # * Timer * #
        self.timer = Generic(
            pos=layout.TIMER_POS,
            surf=custom_load(PATH_UI_ICON + "timer.png", layout.TIMER_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        Debug(True) << "Set PlayGround" << "\n"

    def _release(self):
        super()._release()
        Debug(True) << "Released PlayGround" << "\n"

    def update_crown(self):

        kills = {}
        for player in self.player_group.sprites():
            kills[player.name] = player.kills

        contest_flag = True
        max_k = kills[list(kills.keys())[0]]
        max_name = "contested"
        for k in kills.keys():
            if kills[k] != max_k:
                contest_flag = False
            if kills[k] >= max_k:
                max_k = kills[k]
                max_name = k

        if contest_flag:
            max_name = "contested"
            self.crown_text = text_script.CONTESTED
        else:
            self.crown_text = f"{text_script.PLAYER_IN_LEAD[0]} {max_name} {text_script.PLAYER_IN_LEAD[1]}"

        font_chs, font_eng = set_fonts(FONT_CHS_LIST, FONT_ENG_LIST)
        self.crown_text_sprite.image = render_text(
            self.crown_text,
            font_eng,
            layout.CROWN_TEXT_FONT_SIZE,
            layout.CROWN_TEXT_COLOR,
            bold=True
        )

        size = (self.crown_text_sprite.image.get_rect().size[0] + 1, self.crown_text_sprite.image.get_rect().size[1] + 1)
        self.crown_text_sprite.image = pygame.transform.smoothscale(
            self.crown_text_sprite.image,
            size
        )

        if max_name in CROWN_COLOR:
            print(max_name)
            path = PATH_UI_ICON + "crown/crown_" + CROWN_COLOR[max_name] + ".png"
            self.crown.image = custom_load(path, layout.CROWN_SIZE)
