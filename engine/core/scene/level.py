from random import randint

from .scene import ArenaScene
from engine import layout
from engine.path import *
from engine.widget.sprite import Player
from engine.widget.sprite import P1Cfg
from engine.utils import Debug


class Level(ArenaScene):
    """
    长场景(可移动)
    """

    def __init__(self, map_index, background_index):
        super().__init__(map_index, background_index)

        # * Players * #
        self.player_1 = None

        Debug(True) << "Inited PlayGround"

    def setup(self):
        super().setup()

        self.load_map(map_type="level")

        # * Load Player * #
        p1_skin = SKIN_DICT[randint(0, len(SKIN_DICT) - 1)]
        p1_cfg = P1Cfg()
        p1_cfg.skin = p1_skin

        self.player_1 = Player(
            [self.all_sprites, self.creature_group, self.player_group, self.gravity_group, self.shoot_group],
            p1_cfg,
            all_sprite_group=self.all_sprites
        )

        for player in self.player_group.sprites():
            player.activate()

        # * Init Bullet Group * #
        for player in self.player_group.sprites():
            self.bullet_groups.append(player.weapon.bullet_group)

        Debug(True) << "All Sprites in Current Scene: " << str(self.all_sprites)
        Debug(True) << "Loaded Level"

    def release(self):
        super().release()
        Debug(True) << "Released Level"

    def run(self, dt):
        super().run(dt)
        offset_x = self.player_1.rect.centerx - layout.SCR_CENTER[0]
        offset_y = self.player_1.rect.centery - layout.SCR_CENTER[1]
        self.all_sprites.custom_draw_level(offset_x, offset_y)

    def activate(self):
        super().activate()
        Debug(True) << "Activated PlayGround"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated PlayGround"
        Debug(True).div()
