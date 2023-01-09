import pygame

from engine.settings import *
from engine.core.camera import CameraGroup


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
        self.all_sprites.custom_draw()
        self.all_sprites.update(dt)
