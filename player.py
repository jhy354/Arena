import pygame

import layout
from settings import *
from utils import Debug
from utils import Timer
from support import import_folder


class Player(pygame.sprite.Sprite):
    """
    不同于 Generic 的特殊类
    控制玩家的行为
    """

    def __init__(self, pos, group, coll_rect_sprites, coll_mask_sprites):
        super().__init__(group)
        self.coll_rect_sprites = coll_rect_sprites
        self.coll_mask_sprites = coll_mask_sprites

        # * Image Attributes * #
        self.skin = "p_pale"
        self.animations = {}
        self.import_assets()
        self.status = "idle"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.z = LAYERS["player"]

        # * Movement Attributes * #
        self.active = False
        self.on_ground = False
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

        # Physical Attributes
        self.mass = 2
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 10
        self.max_speed = 200
        self.max_jump_h = 50

        # * Timers * #
        self.timers = {
            # 函数后不应有 "()"
            "jump_up": Timer(1000, self.jump_down)  # 跳跃上升
        }

        Debug(True) << "Inited Player" << "\n"

    def activate(self):
        self._setup()
        self.active = True
        Debug(True) << "Activated Player" << "\n"

    def deactivate(self):
        self._release()
        self.active = False
        Debug(True) << "Deactivated Player" << "\n"

    def _setup(self):
        """
        调用 activate() 时运行
        protected function
        """
        # self.image = pygame.transform.scale(self.image, layout.PLAYER_SIZE)
        # self.rect = self.image.get_rect()

    def _release(self):
        """
        调用 deactivate() 时运行
        protected function
        """
        pass

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
            self.animations[animation] = import_folder(full_path, layout.PLAYER_SIZE)

    def respond_collide(self, direction):
        # Rect Collision
        for sprite in self.coll_rect_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    Debug(DEBUG_MODE) << "Collide with Hitbox" << "\n"
                    if direction == "horizontal":
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

        # Mask Collision
        for sprite in self.coll_mask_sprites.sprites():
            if hasattr(sprite, "mask") and hasattr(sprite, "rect"):
                offset = (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)
                tmp_rect = self.rect.copy()
                if self.mask.overlap(sprite.mask, offset) is not None:
                    Debug(DEBUG_MODE) << "Collide with Mask" << "\n"
                    if direction == "horizontal":
                        if self.direction.x > 0:  # moving right
                            self.rect.right = tmp_rect.right - 4
                        if self.direction.x < 0:  # moving left
                            self.rect.left = tmp_rect.left - 4
                        self.pos.x = self.rect.centerx

    def respond_input(self):
        if not self.status == "jump":
            # Better than "event.type == KEYDOWN"
            keys = pygame.key.get_pressed()

            # * Horizontal Movement * #
            if keys[pygame.K_LEFT]:
                self.status = "walk"
                self.direction.x = -1
                if self.speed_x <= self.max_speed:
                    self.speed_x += self.acceleration

            elif keys[pygame.K_RIGHT]:
                self.status = "walk"
                self.direction.x = 1
                if self.speed_x <= self.max_speed:
                    self.speed_x += self.acceleration

            else:
                if self.speed_x >= 0:
                    self.speed_x -= self.acceleration
                else:
                    self.direction.x = 0

            # * Vertical Movement * #
            """
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
            """

            # * Other Movement * #
            if keys[pygame.K_SPACE]:
                self.frame_index = 0  # Start a new animation
                self.status = "jump"
                # self.direction = pygame.math.Vector2()
            else:
                pass

    def horizontal_move(self, dt):
        # Vector Normalize
        # 获取单位向量, 防止斜走速度为根号2倍
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed_x * dt
        self.rect.centerx = self.pos.x

        self.respond_collide("horizontal")

    def vertical_move(self, dt):
        if self.status == "jump":
            self.jump_up(dt)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def switch_frame(self, dt):
        # 常数 4 控制动画帧速度
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        # 必须在下一行使用 int()
        self.image = self.animations[self.status][int(self.frame_index)]

    def switch_status(self):
        # 注意优先级
        # * Jump * #
        # if self.timers["jump"].active:
        #     self.status = "jump"

        # * Idle * #
        if self.direction.magnitude() == 0:
            self.status = "idle"

    def jump_up(self, dt):
        vmax = 20 * self.max_jump_h
        if self.speed_y >= vmax:
            self.speed_y -= 10 / dt  # g = 10 m/s^2
        self.pos.y += self.speed_y

    def jump_down(self):
        self.status = "jump_down"
