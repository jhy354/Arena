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


class UIGroup:
    """
    UI 控件组
    集中管理若干个有联系的 UI 控件 (surface)
    """

    def __init__(self, group):
        """
        在子类初始化 sprite 对象时记得加入 all_sprite 组
        """
        self.active = False
        self.group = group

    def activate(self):
        self.setup()
        self.active = True

    def deactivate(self):
        self.deactivate()
        self.active = False

    def setup(self):
        """
        调用 activate() 时运行
        """

    def release(self):
        """
        调用 deactivate() 时运行
        """
