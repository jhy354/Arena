from .sprites import Generic
from engine.settings import *


class Fog(Generic):
    """
    雾气特效
    """
    def __init__(self, pos, surf, group, z=LAYERS["fog"]):
        super().__init__(pos, surf, group, z)
        self.image.set_alpha(250)
        self.start_x = pos[0]
        self.move_speed = 1

    def move(self):
        self.rect.x += self.move_speed
        if self.rect.x >= SCR_SIZE[0]:
            self.rect.x = -SCR_SIZE[0]


class Noise(Generic):
    """
    噪音特效
    """
    def __init__(self, pos, surf, group, z=LAYERS["noise"]):
        super().__init__(pos, surf, group, z)
        self.image.set_alpha(127)
