from random import randint

import pygame
from pytmx.util_pygame import load_pygame

import layout
import text_script
from settings import *
from path import *
from utils import Debug
from player import Player
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
            group=[self.all_sprites]
        )

        self.start_button = TextButton(
            text=text_script.START_GAME,
            size=35,
            color=(169, 169, 169),
            pos=layout.SM_START,
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

        self.background = None

        self.map_edges = []
        self.map_floors = []

        self.player_group = pygame.sprite.Group()

        self.player_1 = None
        self.player_2 = None

        # * 武器 * #
        # 武器只是一个跟随 player 移动的 surface
        # 不实现其他功能
        self.weapon = None

        self.fog_1 = None
        self.fog_2 = None

        Debug(True) << "Inited PlayGround" << "\n"

    def horizontal_movement_coll(self, dt):
        for player in self.player_group:

            player.rect.x += player.direction.x * dt * MOVEMENT_RATING

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def vertical_movement_coll(self, dt):
        for player in self.player_group:
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
                            Debug(DEBUG_MODE) << "Player Enabled Jump" << "\n"
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.can_jump = False

    def move_weapon(self):
        for player in self.player_group:
            player.weapon.image = player.weapon.init_image
            if player.face_direction == "left":
                player.weapon.image = pygame.transform.flip(player.weapon.image, True, False)
                player.weapon.rect.topright = player.rect.midleft
            else:
                player.weapon.rect.topleft = player.rect.midright
            player.weapon.rect.y -= 5
            if player.face_direction == "right":
                player.weapon.rect.x -= 5
            else:
                player.weapon.rect.x += 5

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
        rand_map = randint(0, len(PATH_MAP)-1)
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
        p1_skin = SKIN_DICT[randint(0, len(SKIN_DICT)-1)]
        p2_skin = SKIN_DICT[randint(0, len(SKIN_DICT)-1)]

        self.player_1 = Player(
            start_pos=layout.SCR_CENTER,
            group=[self.all_sprites, self.player_group],
            player_keys={"jump": pygame.K_w, "left": pygame.K_a, "right": pygame.K_d},
            skin=p1_skin
        )

        self.player_2 = Player(
            start_pos=layout.SCR_CENTER,
            group=[self.all_sprites, self.player_group],
            player_keys={"jump": pygame.K_UP, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
            skin=p2_skin
        )

        for player in self.player_group:
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

    def _release(self):
        super()._release()
        Debug(True) << "Released PlayGround" << "\n"

    def run(self, dt):
        super().run(dt)
        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.move_weapon()
        self.fog_1.move(dt)
        self.fog_2.move(dt)


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
