import sys

import pygame

from utils import Debug
from utils import Timer
from support import import_folder
from settings import *


class Player(pygame.sprite.Sprite):
    """
    不同于 Generic 的特殊类
    控制玩家的行为
    """

    def __init__(self, pos, group):
        super().__init__(group)

        # * Image Attributes * #
        self.active = False
        self.skin = "p_pale"
        self.animations = {}
        self.import_assets()
        self.animation_status = "idle"
        self.frame_index = 0
        self.image = self.animations[self.animation_status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["player"]

        # * Movement Attributes * #
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)

        # Speed Attributes
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 10
        self.max_speed = 200

        # * Timers * #
        self.timers = {
            # 函数后不应有 "()"
            "jump": Timer(1000, self.done_jump)
        }

        Debug(True) << "Inited Player" << "\n"

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self, dt):
        super().update()

        if self.active:
            self.respond_input()
            self.horizontal_move(dt)
            self.vertical_move(dt)
            self.update_timers()

            # Animation
            self.switch_frame(dt)
            self.switch_status()

    def import_assets(self):
        self.animations = {
            "idle": [],
            "walk": [],
            "jump": []
        }

        for animation in self.animations.keys():
            full_path = PATH_PLAYER + self.skin + "/" + animation
            self.animations[animation] = import_folder(full_path)

    def respond_input(self):
        if not self.timers["jump"].active:
            # Better than "event.type == KEYDOWN"
            keys = pygame.key.get_pressed()

            # * Horizontal Movement * #
            if keys[pygame.K_LEFT]:
                self.animation_status = "walk"
                self.direction.x = -1
                if self.speed_x <= self.max_speed:
                    self.speed_x += self.acceleration

            elif keys[pygame.K_RIGHT]:
                self.animation_status = "walk"
                self.direction.x = 1
                if self.speed_x <= self.max_speed:
                    self.speed_x += self.acceleration

            else:
                if self.speed_x >= 0:
                    self.speed_x -= self.acceleration
                else:
                    self.direction.x = 0

            # * Vertical Movement * #
            if keys[pygame.K_UP]:
                self.direction.y = -1
                if self.speed_y <= self.max_speed:
                    self.speed_y += self.acceleration

            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                if self.speed_y <= self.max_speed:
                    self.speed_y += self.acceleration

            else:
                if self.speed_y >= 0:
                    self.speed_y -= self.acceleration
                else:
                    self.direction.y = 0

            # * Other Movement * #
            if keys[pygame.K_SPACE]:
                self.timers["jump"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0  # Start a new animation
            else:
                pass

    def horizontal_move(self, dt):
        # Vector Normalize
        # 获取单位向量, 防止斜走速度为根号2倍
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            # Debug(DEBUG_MODE) << self.direction << "\n"

        self.pos.x += self.direction.x * self.speed_x * dt
        self.rect.centerx = self.pos.x

    def vertical_move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction.normalize()

        self.pos.y += self.direction.y * self.speed_y * dt
        self.rect.centery = self.pos.y

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def switch_frame(self, dt):
        # 常数 4 控制动画帧速度
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.animation_status]):
            self.frame_index = 0

        # 必须在下一行使用 int()
        self.image = self.animations[self.animation_status][int(self.frame_index)]

    def switch_status(self):
        # 注意优先级
        # * Jump * #
        if self.timers["jump"].active:
            self.animation_status = "jump"

        # * Idle * #
        elif self.direction.magnitude() == 0:
            self.animation_status = "idle"

    def done_jump(self):
        Debug(DEBUG_MODE) << "Done Jump" << "\n"
