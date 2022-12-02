import pygame

from engine.settings import *


class Generic(pygame.sprite.Sprite):
    """
    用于 CameraGroup 的通用的 Sprite 类
    无碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(group)
        self.image = surf
        self.z = z
        self.rect = self.image.get_rect(topleft=pos)


class GameObject(Generic):
    """
    矩形碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(pos, surf, group, z)
        self.hitbox = self.rect.copy()


class Fog(Generic):
    def __init__(self, pos, surf, group, z=LAYERS["fog"]):
        super().__init__(pos, surf, group, z)
        self.image.set_alpha(250)
        self.start_x = pos[0]
        self.move_speed = 1

    def move(self):
        self.rect.x += self.move_speed
        if self.rect.x >= SCR_SIZE[0]:
            self.rect.x = -SCR_SIZE[0]
