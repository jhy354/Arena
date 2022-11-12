import pygame

import layout
from settings import *
from path import *
from utils import Debug
from support import import_folder


class Player(pygame.sprite.Sprite):
    """
    控制玩家的行为
    """

    def __init__(self, start_pos, group):
        super().__init__(group)

        # * 图像参数 * #
        self.display_surface = pygame.display.get_surface()
        self.skin = "p_pale"
        self.animations = {}
        self.status = "idle"
        self.import_assets()
        self.frame_index = 0
        self.z = LAYERS["player"]
        self.image = self.animations[self.status][self.frame_index]
        self.face_direction = "right"

        # * 角色判断参数 * #
        self.active = False
        self.start_pos = start_pos
        self.rect = self.image.get_rect(center=start_pos)

        # * 移动参数 * #
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.can_jump = False
        self.jump_cnt = 0
        self.jump_time = 10

        # * 其他 * #
        self.push_space = False

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

    def _release(self):
        """
        调用 deactivate() 时运行
        protected function
        """

    def update(self, dt):
        super().update()

        if self.active:
            # print(self.status)
            self.respond_input(dt)
            self.switch_status()
            self.switch_frame(dt)

    def respond_input(self, dt):
        keys = pygame.key.get_pressed()

        # * Horizontal Movement * #
        if keys[pygame.K_a]:
            self.status = "walk"
            self.face_direction = "left"
            self.direction.x = -1 * self.speed

        elif keys[pygame.K_d]:
            self.status = "walk"
            self.face_direction = "right"
            self.direction.x = 1 * self.speed

        else:
            self.direction.x = 0

        # * Other Movement * #
        if keys[pygame.K_SPACE]:
            self.push_space = True
            if self.can_jump:
                self.jump(dt)

        else:
            self.push_space = False

    def jump(self, dt):
        if self.jump_cnt == 0:
            Debug(DEBUG_MODE) << "Player Jump" << "\n"
        self.direction.y = self.jump_speed
        self.jump_cnt += dt * MOVEMENT_RATING
        if self.jump_cnt >= self.jump_time:
            self.jump_cnt = 0
            self.can_jump = False

    def apply_gravity(self):
        self.direction.y += self.gravity

    def switch_frame(self, dt):
        # 常数 4 控制动画帧速度
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        # 必须在下一行使用 int()
        self.image = self.animations[self.status][int(self.frame_index)]
        if self.face_direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def switch_status(self):
        # 注意优先级

        # * Jump * #
        if self.jump_cnt != 0:
            self.status = "jump"
            # start a new animation
            self.frame_index = 0

        # * Idle * #
        elif self.direction.x == 0:
            self.status = "idle"

    def import_assets(self):
        self.animations = {
            "idle": [],
            "walk": [],
            "jump": []
        }

        for animation in self.animations.keys():
            full_path = PATH_PLAYER + self.skin + "/" + animation
            self.animations[animation] = import_folder(full_path, layout.PLAYER_SIZE)
