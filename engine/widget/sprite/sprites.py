import pygame

from engine.settings import *


class Generic(pygame.sprite.Sprite):
    """
    用于 CameraGroup 的通用的 Sprite 类
    无碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(group)
        self.source_image = surf
        self.image = self.source_image.copy()
        self.z = z
        self.rect = self.image.get_rect(topleft=pos)

    def hide(self):
        self.image = pygame.surface.Surface((1, 1))

    def show(self):
        self.image = self.source_image.copy()


class GameObject(Generic):
    """
    矩形碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(pos, surf, group, z)
        self.hitbox = self.rect.copy()
