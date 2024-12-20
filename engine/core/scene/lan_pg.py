import socket
import pickle
import select

import pygame

from .playground import PlayGround
from engine.settings import *
from engine.path import *
from engine import layout
from engine import text_script
from engine.utils import Debug
from engine.utils import set_fonts
from engine.utils import render_text
from engine.utils import custom_load
from engine.widget.sprite import P1Cfg
from engine.widget.sprite import Bullet
from engine.widget.sprite import LANPlayerCfg
from engine.widget.sprite import Player
from engine.widget.sprite import Generic
from engine.widget.sprite import Fog
from engine.widget.sprite import TimerUI


class LAN_PlayGround(PlayGround):

    def __init__(self, server_ip, map_index, background_index):

        super().__init__(map_index, background_index)

        if server_ip is not None:
            self.server_ip = server_ip
        else:
            self.server_ip = DEFAULT_SERVER_IP

        self.player_id = None  # str
        self.player_obj = {}
        self.sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk_server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.sk_server.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        self.connected = False

        self.crown = None
        self.crown_text = None
        self.crown_text_sprite = None

        self.timer_ui = None

        self.score_dist = {}

        self.other_bullet_group = pygame.sprite.Group()
        self.other_bullet_sprite_dict = {}

        if self.active:
            try:
                self.sk_server.connect((self.server_ip, DEFAULT_SERVER_PORT))
            except Exception as error:
                print(f"\033[1;32m[WARNING]\033[0m {error}")
                Debug(True).div()
                if self.active:
                    exit(1)

    def setup(self):

        # * Load Fog * #
        self.fog_1 = Fog(
            pos=(0, 0),
            surf=custom_load(PATH_EFFECT_FOG + "fog_thin.png", layout.FOG_SIZE),
            group=[self.all_sprites],
        )

        self.fog_2 = Fog(
            pos=(-SCR_SIZE[0], 0),
            surf=custom_load(PATH_EFFECT_FOG + "fog_thin.png", layout.FOG_SIZE),
            group=[self.all_sprites],
        )

        data = self.receive_server()
        while not isinstance(data, dict):
            data = self.receive_server()

        self.map_index = data["map"]
        self.background_index = data["bg"]

        # * Load Background * #
        self.background = Generic(
            pos=layout.BG_POS,
            surf=custom_load(PATH_BACKGROUND[self.background_index], layout.BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )

        self.load_map(map_type="playground")

        # * TimerUI * #
        self.timer_ui = TimerUI(self.all_sprites, ARENA_MODE_TIME)
        self.timer_ui.activate()

        # * Crown * #
        self.crown = Generic(
            pos=layout.CROWN_POS,
            surf=custom_load(PATH_UI_ICON + "crown/crown_gray.png", layout.CROWN_SIZE),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

        self.crown_text_sprite = Generic(
            pos=layout.CROWN_TEXT_POS,
            surf=pygame.surface.Surface((1, 1)),
            group=[self.all_sprites],
            z=LAYERS["ui"]
        )

    def setup_player(self, data):

        if not isinstance(data, dict):
            return

        for p_data in data["players"]:

            if not p_data["id"] in self.player_obj.keys():

                if self.player_id == p_data["id"]:
                    self.player_obj[p_data["id"]] = Player(
                        [self.all_sprites, self.creature_group, self.player_group, self.gravity_group,
                         self.shoot_group],
                        P1Cfg(),
                        all_sprite_group=self.all_sprites
                    )

                else:
                    self.player_obj[p_data["id"]] = Player(
                        [self.all_sprites, self.creature_group, self.player_group, self.gravity_group,
                         self.shoot_group],
                        LANPlayerCfg(),
                        all_sprite_group=self.all_sprites
                    )

                # * Init Bullet Group * #
                self.bullet_groups.append(self.player_obj[p_data["id"]].weapon.bullet_group)
                self.player_obj[p_data["id"]].activate()

    def connect_server(self):
        """
        当前客户端首次连接到服务端时调用
        """
        try:

            if not self.connected:
                print(f"Connecting {self.server_ip}:{DEFAULT_SERVER_PORT}")
                self.sk_server.connect((self.server_ip, DEFAULT_SERVER_PORT))
                self.connected = True

            data = self.receive_server()

            # 服务端在首次发送数据为 玩家id: str
            # 后发送正常数据
            if isinstance(data, str):
                if data.isdigit():
                    self.player_id = data
                else:
                    print(f"[WARNING] incorrect data form")
                    Debug(True).div()

            else:
                print(f"[WARNING] incorrect data form")
                Debug(True).div()
                self.connect_server()

        except Exception as error:
            print(f"[WARNING] {error}")
            Debug(True).div()
            exit(1)

    def receive_server(self):
        """
        调用 Scene.activate() 前只可接受 玩家id: str
        调用后方可正常接受数据
        """

        ready_sockets, _, _ = select.select([self.sk_server], [], [], CLIENT_TIMEOUT)

        try:
            if ready_sockets:
                try:
                    data = pickle.loads(self.sk_server.recv(HEADER))
                    if data is None:
                        print(f"[WARNING] receiving None data")
                    # print(f"[RECEIVING]")
                    # print(data)
                    return data
                except Exception as error:
                    print(f"\033[1;32m[GLOBAL WARNING]\033[0m {error}")

        except Exception as error:
            print(f"[GLOBAL ERROR] {error}")
            Debug(True).div()

            data = {'action': 'error', 'value': {'error': error}}
            self.sk_server.send(pickle.dumps(data))
            print(f"\033[1;32m[SENDING]\033[0m")
            print(data)
            # traceback.print_exc()
            exit(0)

    def respond_server(self):
        self.update_crown()

        me = self.player_obj[self.player_id]
        bullet_list = []
        for b in me.weapon.bullet_group.sprites():
            cur_status = {
                "bullet_id": id(b),
                "pos": (b.rect.x, b.rect.y),
                "image_path": b.image_path,
                "damage": b.damage,
            }
            bullet_list.append(cur_status)

        response = {
            "commands": [
                {
                    "movement": {
                        "id": self.player_id,
                        "pos": (me.rect.x, me.rect.y),
                    }
                },

                {
                    "animation": {
                        "id": self.player_id,
                        "skin": me.skin,
                        "status": me.status,
                        "frame_index": round(me.frame_index, 2),
                        "face_direction": me.face_direction,
                    }
                },

                {
                    "bullet": {
                        "id": self.player_id,
                        "bullet_list": bullet_list,
                    }
                },

                {
                    "score": {
                        "id": self.player_id,
                        "score": me.kills,
                    }
                },
            ],
            "id": self.player_id,
        }
        response = {"action": "commands", "value": response}
        # print(self.player_id, me.kills)
        # print(f"[SENDING]")
        # print(response)
        try:
            self.sk_server.send(pickle.dumps(response))
        except OSError:
            exit(OSError)

    def update_from_server(self, data):
        """
        根据服务端数据修改客户端 player 数据
        """

        if not isinstance(data, dict):
            return

        # Timer
        if data["timer"]["time"] is not None and not data["timer"]["finished"]:
            self.timer_ui.set_time_str(ARENA_MODE_TIME - data["timer"]["time"])
            self.timer_ui.render_str_surf(self.timer_ui.time_str)
        if data["timer"]["finished"]:
            self.timer_ui.render_str_surf("77:77")  # finished

        for player in data["players"]:

            # 只有一个元素时跳过
            if len(player.keys()) <= 1:
                continue

            # 不跳过自己 #
            self.score_dist[player["id"]] = player["score"]

            # 跳过自己 #
            if player["id"] == self.player_id:
                continue

            try:
                # movement
                self.player_obj[player["id"]].rect.x = player["pos"][0]
                self.player_obj[player["id"]].rect.y = player["pos"][1]

                # animation
                self.player_obj[player["id"]].skin = player["skin"]
                self.player_obj[player["id"]].status = player["status"]
                self.player_obj[player["id"]].frame_index = player["frame_index"]
                self.player_obj[player["id"]].face_direction = player["face_direction"]

                # bullet
                self.update_bullet_from_server(player["bullet_list"])

            except Exception as error:
                print(f"\033[1;32m[ERROR]\033[0m {error}")
                Debug(True).div()

    def update_bullet_from_server(self, bullet_list):
        # 在 other_bullet_sprite_dict 中而不在 bullet_list 中则删除
        del_list = []
        for bullet_id in self.other_bullet_sprite_dict.keys():
            exist_flag = False
            for bullet in bullet_list:
                if bullet_id == bullet["bullet_id"]:
                    exist_flag = True
            if not exist_flag:
                self.other_bullet_sprite_dict[bullet_id].destroy()
                del_list.append(bullet_id)
        for del_id in del_list:
            del self.other_bullet_sprite_dict[del_id]

        if bullet_list is None or bullet_list == []:
            return

        for bullet in bullet_list:
            if bullet["bullet_id"] not in self.other_bullet_sprite_dict.keys():
                self.other_bullet_sprite_dict[bullet["bullet_id"]] = Bullet(
                    bullet["pos"],
                    [self.all_sprites, self.other_bullet_group],
                    "right",
                )
            else:
                self.other_bullet_sprite_dict[bullet["bullet_id"]].set_pos(bullet["pos"])

    def update_crown(self):
        if not self.score_dist:  # 检查 score_dist 是否为空
            self.crown_text = "No players"
            return  # 提前返回，不进行后续处理

        score_counts = {}
        max_score = float('-inf')
        leaders = []

        # 统计每个分数出现的次数并寻找最高分数
        for player_id, score in self.score_dist.items():
            # 更新分数计数
            if score in score_counts:
                score_counts[score] += 1
            else:
                score_counts[score] = 1

            # 查找最高分
            if score > max_score:
                max_score = score
                leaders = [player_id]  # 新的最高分, 重置leaders列表
            elif score == max_score:
                leaders.append(player_id)  # 同样的最高分, 添加到leaders列表

        # 检查是否存在平局
        has_tie = any(count > 1 for count in score_counts.values())

        if has_tie:  # 存在平局现象
            self.crown_text = text_script.CONTESTED
            max_name = "contested"
        else:
            max_name = leaders[0]
            self.crown_text = f"{text_script.PLAYER_IN_LEAD[0]} {max_name} {text_script.PLAYER_IN_LEAD[1]}"

        font_chs, font_eng = set_fonts(FONT_CHS_LIST, FONT_ENG_LIST)
        self.crown_text_sprite.image = render_text(
            self.crown_text,
            font_eng,
            layout.CROWN_TEXT_FONT_SIZE,
            layout.CROWN_TEXT_COLOR
        )

        if max_name in CROWN_COLOR_LAN:
            path = PATH_UI_ICON + "crown/crown_" + CROWN_COLOR_LAN[max_name] + ".png"
            self.crown.image = custom_load(path, layout.CROWN_SIZE, silent=True)

    def run(self, dt):

        self.display_surface.fill("white")

        data = self.receive_server()
        self.setup_player(data)

        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.apply_sprite_gravity(dt)
        self.check_bullet_coll()

        # self.update_player_weapon()
        self.fog_1.move()
        self.fog_2.move()

        # 没有继承, 故需要手动更新 all_sprites
        self.all_sprites.update(dt)
        for p in self.player_obj.values():
            p.update(dt)
            p.update_weapon()

        self.respond_server()
        self.update_from_server(data)
        self.all_sprites.custom_draw()
