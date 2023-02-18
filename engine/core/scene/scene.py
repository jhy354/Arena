import pygame
from pytmx import load_pygame

from engine.settings import *
from engine.path import *
from engine import layout
from engine.core.camera import CameraGroup
from engine.widget.sprite import Generic
from engine.widget.sprite import GameObject
from engine.utils import Debug


class Scene:
    """
    场景基类定义
    """

    def __init__(self):
        # * General * #
        self.active = False
        self.display_surface = pygame.display.get_surface()

        # * Groups * #
        self.all_sprites = CameraGroup()
        self.coll_rect_sprites = pygame.sprite.Group()

    def activate(self):
        """
        激活场景
        """
        self.active = True
        self.setup()

    def deactivate(self):
        """
        停用场景
        """
        self.active = False
        self.release()

    def setup(self):
        """
        调用 activate() 时运行
        """

    def release(self):
        """
        调用 deactivate() 时运行
        """
        self.all_sprites.empty()

    def run(self, dt):
        """
        在 self.active == True 时循环运行
        """
        self.display_surface.fill("white")
        self.all_sprites.update(dt)


class ArenaScene(Scene):
    """
    无实际功能, 用于创建子类
    """

    def __init__(self, map_index, background_index):
        super().__init__()

        self.background = None

        self.map_index = map_index
        self.background_index = background_index

        # * Groups * #
        self.player_group = pygame.sprite.Group()
        self.bullet_groups = []

        # * Map Tiles * #
        self.map_edges = []
        self.map_floors = []

    def run(self, dt):
        super().run(dt)
        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.check_bullet_coll()
        self.update_player_weapon()

    def load_map(self, map_type="playground"):

        # * Load Map Data * #
        tmx_data = None

        if map_type == "playground":
            tmx_data = load_pygame(PATH_MAP[self.map_index])
        elif map_type == "level":
            tmx_data = load_pygame(PATH_MAP_LEVEL[self.map_index])
        else:
            Debug(True) << "ERROR: Unexpected Map Type" << "\n"
            exit()

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
        try:
            for x, y, surf in tmx_data.get_layer_by_name("decoration2").tiles():
                self.map_floors.append(
                    GameObject(
                        pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                        surf=surf,
                        group=[self.all_sprites],
                        z=LAYERS["map_decoration2"]
                    )
                )
        except ValueError:
            pass

        try:
            for x, y, surf in tmx_data.get_layer_by_name("decoration3").tiles():
                self.map_floors.append(
                    GameObject(
                        pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                        surf=surf,
                        group=[self.all_sprites],
                        z=LAYERS["map_decoration3"]
                    )
                )
        except ValueError:
            pass

        try:
            for x, y, surf in tmx_data.get_layer_by_name("background").tiles():
                self.map_floors.append(
                    GameObject(
                        pos=(x * layout.TILE_SIZE, y * layout.TILE_SIZE),
                        surf=surf,
                        group=[self.all_sprites],
                        z=LAYERS["map_background"]
                    )
                )
        except ValueError:
            pass

    def update_player_weapon(self):
        for player in self.player_group.sprites():
            player.update_weapon()

    def horizontal_movement_coll(self, dt):
        for player in self.player_group.sprites():

            player.rect.x += player.direction.x * dt * MOVEMENT_RATING

            for sprite in self.coll_rect_sprites:
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

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
