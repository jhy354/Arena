import pygame

import layout
from settings import *
from path import *
from utils import Debug
from support import import_folder
from weapons import Pistol


class Player(pygame.sprite.Sprite):
    """
    控制玩家的行为
    """

    def __init__(self, group, cfg):
        super().__init__(group)

        # * 图像参数 * #
        self.skin = cfg.skin
        self.display_surface = pygame.display.get_surface()
        self.animations = {}
        self.status = "idle"
        self.import_assets()
        self.frame_index = 0
        self.z = LAYERS["player"]
        self.image = self.animations[self.status][self.frame_index]
        self.face_direction = "right"

        # * 角色判断参数 * #
        self.spawn_point = cfg.spawn_point
        self.active = False
        self.rect = self.image.get_rect(center=cfg.spawn_point)

        # * 移动参数 * #
        self.player_keys = cfg.player_keys
        self.speed = cfg.speed
        self.gravity = cfg.gravity
        self.jump_speed = cfg.jump_speed
        self.direction = pygame.math.Vector2(0, 0)
        self.can_jump = False
        self.jump_cnt = 0
        self.jump_time = 10

        # * 其他 * #
        self.hp = cfg.hp
        self.push_space = False
        self.weapon = Pistol([self.groups()[0]])

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
            self.update_weapon()
            self.weapon.update(dt)

    def respond_input(self, dt):
        keys = pygame.key.get_pressed()

        # * Horizontal Movement * #
        if keys[self.player_keys["left"]]:
            self.status = "walk"
            self.face_direction = "left"
            self.direction.x = -1 * self.speed

        elif keys[self.player_keys["right"]]:
            self.status = "walk"
            self.face_direction = "right"
            self.direction.x = 1 * self.speed

        else:
            self.direction.x = 0

        # * Other Movement * #
        if keys[self.player_keys["jump"]]:
            self.push_space = True
            if self.can_jump:
                self.jump(dt)

        else:
            self.push_space = False

        # * Game * #
        if keys[self.player_keys["shoot"]]:
            self.weapon.shoot()

    def jump(self, dt):
        if self.jump_cnt == 0:
            Debug(DEBUG_MODE) << "(Player) Player Jump" << "\n"
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

    def update_weapon(self):
        self.weapon.image = self.weapon.init_image

        if self.face_direction == "left":
            self.weapon.direction = "left"
            self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
            self.weapon.rect.topright = self.rect.midleft

        elif self.face_direction == "right":
            self.weapon.direction = "right"
            self.weapon.rect.topleft = self.rect.midright
            self.weapon.rect.y -= 5

        if self.face_direction == "right":
            self.weapon.rect.x -= 5
        else:
            self.weapon.rect.x += 5


class DefaultCfg:
    """
    玩家配置类
    用于实例化 Player 对象
    """
    def __init__(self):
        # Default
        self.spawn_point = layout.SCR_CENTER
        self.hp = 100
        self.skin = "p_pale"
        self.player_keys = {
            "jump": pygame.K_w,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "shoot": pygame.K_s
        }
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16


class P2Cfg(DefaultCfg):
    def __init__(self):
        super().__init__()
        self.player_keys = {
            "jump": pygame.K_UP,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "shoot": pygame.K_DOWN
        }
