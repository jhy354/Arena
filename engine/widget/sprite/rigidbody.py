import pygame

from .weapons import Pistol
from engine.layout import *
from engine.settings import *
from engine.path import *
from engine.utils import Debug
from engine.utils import import_folder
from engine.utils import Timer


class Player(pygame.sprite.Sprite):
    """
    控制玩家的行为
    """

    def __init__(self, group, cfg):
        """
        由于需要在内部实例化类 所以 group[0] 必须为 all_sprites
        """
        super().__init__(group)

        # * 图像参数 * #
        self.skin = cfg.skin
        self.display_surface = pygame.display.get_surface()
        self.animations = {}
        self.status = "idle"
        self.import_assets()
        self.frame_index = 0
        self.z = LAYERS["player"]
        self.source_image = self.animations[self.status][self.frame_index]
        self.image = self.source_image.copy()
        self.face_direction = "right"

        # * 角色判断参数 * #
        self.active = False
        self.rect = self.image.get_rect(center=cfg.spawn_point)

        # * 移动参数 * #
        self.enable_lan = cfg.enable_lan
        self.player_keys = cfg.player_keys
        self.speed = cfg.speed
        self.gravity = cfg.gravity
        self.jump_speed = cfg.jump_speed
        self.direction = pygame.math.Vector2(0, 0)
        self.can_jump = False
        self.jump_cnt = 0
        self.jump_time = 10

        # * 游戏 * #
        self.name = cfg.name
        self.kills = 0

        # * 其他 * #
        self.cfg = cfg
        self.hp = cfg.hp
        self.push_space = False
        self.weapon = Pistol([self.groups()[0]])
        self.timers = {
            "respawn": Timer(3000, self.call_respawn)
        }

        Debug(True) << "Inited Player" << "\n"

    def activate(self):
        self.setup()
        self.active = True
        Debug(True) << "Activated Player" << "\n"

    def deactivate(self):
        self.release()
        self.active = False
        Debug(True) << "Deactivated Player" << "\n"

    def setup(self):
        """
        调用 activate() 时运行
        """

    def release(self):
        """
        调用 deactivate() 时运行
        """

    def update(self, dt):
        super().update()

        self.update_timer()

        if self.active:
            self.respond_input(dt)
            # self.update_weapon() called in scene.horizontal_movement_coll()
            self.switch_status()
            self.switch_frame(dt)
            self.weapon.update(dt)

    def respond_input(self, dt):
        if not self.enable_lan:

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

    def apply_gravity(self, dt):  # dt can not be removed due to ArenaScene.gravity_group
        if self.active:
            self.direction.y += self.gravity

    def switch_frame(self, dt):

        if not self.enable_lan:
            # 常数 4 控制动画帧速度
            self.frame_index += 4 * dt

            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0

        # 必须在下一行使用 int()
        self.image = self.animations[self.status][int(self.frame_index)]
        if self.face_direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def switch_status(self):
        if self.enable_lan:
            return

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
            self.animations[animation] = import_folder(full_path, PLAYER_SIZE)

    def update_weapon(self):
        if not self.weapon.image.get_size() == (1, 1):
            self.weapon.image = self.weapon.source_image

        if self.face_direction == "left":
            self.weapon.direction = "left"
            self.weapon.image = pygame.transform.flip(self.weapon.image, True, False)
            self.weapon.rect.topright = self.rect.midleft

        elif self.face_direction == "right":
            self.weapon.direction = "right"
            self.weapon.rect.topleft = self.rect.midright
            self.weapon.rect.y -= 4

        if self.face_direction == "right":
            self.weapon.rect.x -= 4
        else:
            self.weapon.rect.x += 4

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def die(self):
        """
        移出游戏后等待并复活
        """
        self.deactivate()
        # 暂时移出游戏
        self.rect.x = -1000
        self.rect.y = -1000

        self.timers["respawn"].activate()

    def call_respawn(self):
        """
        Timer 目前无法接受参数
        故使用此函数实例化 Timer 来调用 respawn
        """
        self.respawn(self.cfg.spawn_point)

    def respawn(self, pos):
        self.timers["respawn"].deactivate()
        self.direction.y = 0
        self.hp = self.cfg.hp
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.activate()

    def hide(self):
        Debug(DEBUG_MODE) << "(Player) Hide Player" << "\n"
        self.image = pygame.surface.Surface((1, 1))

    def show(self):
        Debug(DEBUG_MODE) << "(Player) Show Player" << "\n"
        self.image = self.source_image.copy()

    def get_shot(self, damage):
        if self.hp - damage <= 0:
            self.die()
            return True
        else:
            self.hp -= damage
            return False


class DefaultCfg:
    """
    玩家配置类
    用于实例化 Player 对象
    """

    def __init__(self):
        # Default
        self.enable_lan = False
        self.spawn_point = SCR_CENTER
        self.hp = 100
        self.name = "Default"
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


class P1Cfg(DefaultCfg):
    def __init__(self):
        super().__init__()
        self.name = "P1"


class P2Cfg(DefaultCfg):
    def __init__(self):
        super().__init__()
        self.name = "P2"
        self.player_keys = {
            "jump": pygame.K_UP,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "shoot": pygame.K_DOWN
        }


class LANPlayerCfg(DefaultCfg):

    def __init__(self):
        super().__init__()
        self.name = "LAN"
        self.enable_lan = True
        self.skin = "p_soldier"
