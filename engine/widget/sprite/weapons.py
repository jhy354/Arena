import pygame

from engine.layout import *
from engine.settings import *
from engine.path import *
from engine.utils import Debug
from engine.utils import Timer
from engine.utils import custom_load


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


# noinspection PyTypeChecker
class Pistol(Weapon):
    def __init__(self, group):
        super().__init__(group)
        self.source_image = custom_load(PATH_WEAPON_GUN_COMMON + "pistol.png", WEAPON_SIZE)
        self.image = self.source_image
        self.direction = "right"
        self.rect = self.image.get_rect()
        self.cd = 500  # ms
        self.can_shoot = True
        self.bullet_group = pygame.sprite.Group()
        self.timers = {
            "cd": Timer(self.cd, self.activate_shoot)
        }

    def activate_shoot(self):
        self.can_shoot = True

    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.timers["cd"].activate()
            if self.direction == "right":
                Bullet(self.rect.midright, [self.groups()[0], self.bullet_group], 1)
            else:
                Bullet(self.rect.midright, [self.groups()[0], self.bullet_group], -1)

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def check_bullet_remove(self, dt):
        for bullet in self.bullet_group.sprites():
            if bullet.destroyed:
                self.bullets.remove(bullet)
            bullet.fly(dt)

    def hide(self):
        Debug(DEBUG_MODE) << "(Pistol) Hide Pistol" << "\n"
        self.image = pygame.surface.Surface((1, 1))

    def show(self):
        Debug(DEBUG_MODE) << "(Pistol) Show Pistol" << "\n"
        self.image = self.source_image.copy()
    
    def update(self, dt):
        self.check_bullet_remove(dt)
        self.update_timer()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, direction, z=LAYERS["bullet"]):
        super().__init__(group)
        self.image = custom_load(PATH_WEAPON_GUN_BULLET, BULLET_SIZE, silent=True)
        self.direction = direction
        self.z = z
        self.rect = self.image.get_rect(center=pos)
        self.speed = 600
        self.damage = 50
        self.destroyed = False

    def fly(self, dt):
        self.rect.x += self.direction * 0.01 * self.speed

    def update(self, dt):
        """
        if any([self.rect.x <= 0, self.rect.y <= 0, self.rect.x >= SCR_SIZE[0], self.rect.y >= SCR_SIZE[1]]):
            self.destroy()
        """
        pass

    def destroy(self):
        self.kill()
        self.destroyed = True
        Debug(DEBUG_MODE) << "(Bullet) Destroyed" << "\n"
