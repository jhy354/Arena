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


class GravityObj(GameObject):
    """
    有重力
    """

    def __init__(self, pos, surf, group, gravity, max_gravity, z=LAYERS["map_gravity"]):
        super().__init__(pos, surf, group, z)
        self.active = True
        self.gravity = gravity
        self.max_gravity = max_gravity
        self.direction = pygame.math.Vector2(0, 0)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def apply_gravity(self, dt):
        if self.active:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y * dt * MOVEMENT_RATING


class BreakObj(GameObject):
    """
    可破坏
    """

    def __init__(self, pos, surf, group, bullet_cnt=1, z=LAYERS["map_break"]):
        super().__init__(pos, surf, group, z)
        self.bullet_cnt = bullet_cnt

    def update_bullet_cnt(self):
        self.bullet_cnt -= 1
        if self.bullet_cnt <= 0:
            self.kill()
