import pygame.surface

import layout
from settings import *
from path import *
from utils import Debug
from support import custom_load


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group, z=LAYERS["weapon"]):
        super().__init__(group)
        self.z = z
        self.active = False

    def activate(self):
        self._setup()
        self.active = True

    def deactivate(self):
        self._release()
        self.active = False

    def _setup(self):
        """
        调用 activate() 时运行
        protected function
        """

    def _release(self):
        """
        调用 deactivate() 时运行
        protected function
        """

    def update(self, dt):
        super().update()

        if self.active:
            pass


class Pistol(Weapon):
    def __init__(self, group):
        super().__init__(group)
        self.init_image = custom_load(PATH_WEAPON_GUN_COMMON + "pistol.png", layout.WEAPON_SIZE)
        self.image = self.init_image
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, z=LAYERS["bullet"]):
        super().__init__(group)
        self.image = custom_load(PATH_WEAPON_GUN_BULLET, layout.BULLET_SIZE)
        self.z = z
        self.rect = self.image.get_rect(center=pos)
        self.speed = 100
        # self.shadow = custom_load(PATH_WEAPON_GUN_BULLET, layout.BULLET_SHADOW_SIZE)

    def fly(self, direct, dt):
        self.rect.x += direct * dt * self.speed

    def destroy(self):
        self.kill()
        Debug(DEBUG_MODE) << "Destroyed bullet" << "\n"
