import pygame

from .sprites import UIGroup
from .sprites import Generic
from engine.settings import *
from engine.path import *
from engine import layout
from engine.utils import custom_load
from engine.utils import render_text
from engine.utils import set_fonts
from engine.utils import Debug


class TimerUI(UIGroup):
    """
    计时器(UI)类
    """

    def __init__(self, group, cntdown_seconds):
        super().__init__(group)

        self.finish = False
        self.cntdown_seconds = cntdown_seconds
        self.current_seconds = cntdown_seconds
        self.start_time = None
        self.time_str = ""

        self.timer_icon = None
        self.time_surf = None

    def activate(self):
        super().activate()
        self.start_time = pygame.time.get_ticks()  # ms
        Debug(True) << f"(TimerUI) Count Down Started on {pygame.time.get_ticks()}" << "\n"
        self.set_time_str()
        self.render_str_surf()

    def setup(self):
        super().setup()

        self.timer_icon = Generic(
            pos=layout.TIMER_ICON_POS,
            surf=custom_load(PATH_UI_ICON + "timer.png", layout.TIMER_ICON_SIZE),
            group=[self.group],
            z=LAYERS["ui"]
        )

        self.time_surf = Generic(
            pos=layout.TIMER_TEXT_POS,
            surf=pygame.surface.Surface((1, 1)),
            group=[self.group],
            z=LAYERS["ui"]
        )

    def pause_timer(self):
        pass

    def reset_timer(self):
        pass

    def cntdown_finish(self):
        self.finish = True
        Debug(True) << f"(TimerUI) Count Down Finished on {pygame.time.get_ticks()}" << "\n"

    def set_time_str(self):
        m = self.current_seconds // 60
        self.time_str = f"0{m}:" if m < 10 else f"{m}:"
        s = int(self.current_seconds % 60)
        self.time_str += f"0{s}" if s < 10 else f"{s}"

    def render_str_surf(self):
        font_chs, font_eng = set_fonts(FONT_CHS_LIST, FONT_ENG_LIST)
        self.time_surf.image = render_text(
            self.time_str,
            font_eng,
            layout.TIMER_TEXT_SIZE,
            layout.TIMER_TEXT_COLOR
        )

    def update(self):
        if self.finish:
            self.deactivate()

        if self.active:
            t = pygame.time.get_ticks()
            if t - self.start_time >= 1000:
                self.current_seconds -= 1
                if self.current_seconds <= 0:
                    self.cntdown_finish()
                self.set_time_str()
                self.start_time = pygame.time.get_ticks()  # ms
                self.render_str_surf()
