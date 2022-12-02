import pygame

from engine.settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        """
        按图层顺序画出当前 Group 中所有 Sprite
        """
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)
