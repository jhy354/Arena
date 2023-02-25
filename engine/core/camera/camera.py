import pygame

from engine.settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        """
        地图固定
        按图层顺序画出当前 Group 中所有 Sprite
        """
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)

    def custom_draw_level(self, offset_x, offset_y):
        """
        长地图
        """
        self.offset.x = offset_x
        self.offset.y = offset_y

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
