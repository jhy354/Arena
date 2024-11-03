from random import randint

import pygame

from .scene import ArenaScene
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
from engine.widget.sprite import Fog
from engine.widget.sprite import TimerUI


class PlayGround(ArenaScene):
    """
    玩家进行游戏的场景(对战模式)
    """

    def __init__(self, map_index, background_index):
        super().__init__(map_index, background_index)

        # * TimerUI * #
        self.timer_ui = None

        # * Players * #
        self.player_1 = None
        self.player_2 = None

        # * Special Effects * #
        self.fog_1 = None
        self.fog_2 = None

        # * Crown * #
        self.crown = None
        self.crown_text_sprite = None
        self.crown_text = text_script.CONTESTED

        Debug(True) << "Inited PlayGround"

    def run(self, dt):
        super().run(dt)
        self.all_sprites.custom_draw()
        self.timer_ui.update()
        self.fog_1.move()
        self.fog_2.move()

    def activate(self):
        super().activate()
        Debug(True) << "Activated PlayGround"
        Debug(True).div()

    def deactivate(self):
        super().deactivate()
        Debug(True) << "Deactivated PlayGround"
        Debug(True).div()

    def setup(self):
        super().setup()

        # * Load Background * #
        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_BACKGROUND[self.background_index], layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        self.load_map()

        # * Load Player * #
        p1_skin = SKIN_DICT[randint(0, len(SKIN_DICT) - 1)]
        p2_skin = SKIN_DICT[randint(0, len(SKIN_DICT) - 1)]
        p1_cfg = P1Cfg()
        p1_cfg.skin = p1_skin
        p2_cfg = P2Cfg()
        p2_cfg.skin = p2_skin

        self.player_1 = Player(
            [self.all_sprites, self.creature_group, self.player_group, self.gravity_group, self.shoot_group],
            p1_cfg,
            all_sprite_group=self.all_sprites
        )

        self.player_2 = Player(
            [self.all_sprites, self.creature_group, self.player_group, self.gravity_group, self.shoot_group],
            p2_cfg,
            all_sprite_group=self.all_sprites
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

        # * TimerUI * #
        self.timer_ui = TimerUI(self.all_sprites, 180)
        self.timer_ui.activate()

        Debug(True) << "All Sprites in Current Scene: " << str(self.all_sprites)
        Debug(True) << "Loaded PlayGround"

    def release(self):
        super().release()
        Debug(True) << "Released PlayGround"

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
            layout.CROWN_TEXT_COLOR
        )

        '''
        # anti-alias for bold
        size = (self.crown_text_sprite.image.get_rect().size[0] + 1, self.crown_text_sprite.image.get_rect().size[1] + 1)
        self.crown_text_sprite.image = pygame.transform.smoothscale(
            self.crown_text_sprite.image,
            size
        )
        '''

        if max_name in CROWN_COLOR:
            path = PATH_UI_ICON + "crown/crown_" + CROWN_COLOR[max_name] + ".png"
            self.crown.image = custom_load(path, layout.CROWN_SIZE)
