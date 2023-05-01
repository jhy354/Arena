import socket
import pickle
import select

from .playground import PlayGround
from .scene import Scene
from engine.settings import *
from engine.path import *
from engine import layout
from engine.utils import Debug
from engine.utils import custom_load
from engine.widget.sprite import P1Cfg
from engine.widget.sprite import LANPlayerCfg
from engine.widget.sprite import Player
from engine.widget.sprite import Generic
from engine.widget.sprite import Fog


class LAN_PlayGround(PlayGround):

    def __init__(self, map_index, background_index):

        super().__init__(map_index, background_index)

        self.player_id = None
        self.player_obj = {}
        self.sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        if self.active:
            try:
                self.sk_server.connect((SERVER_IP, SERVER_PORT))
            except Exception as error:
                print(f"[WARNING] {error}")
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

    def setup_player(self, data):

        if data is None:
            return

        for p_data in data["players"]:

            if not p_data["id"] in self.player_obj.keys():

                if self.player_id == int(p_data["id"]):
                    self.player_obj[p_data["id"]] = Player(
                        [self.all_sprites, self.creature_group, self.player_group, self.gravity_group, self.shoot_group],
                        P1Cfg()
                    )

                else:
                    self.player_obj[p_data["id"]] = Player(
                        [self.all_sprites, self.creature_group, self.player_group, self.gravity_group, self.shoot_group],
                        LANPlayerCfg()
                    )

                self.player_obj[p_data["id"]].activate()

    '''
    def vertical_movement_coll(self, dt):
        pass

    def horizontal_movement_coll(self, dt):
        pass

    def apply_sprite_gravity(self, dt):
        pass
    '''

    def connect_server(self):
        """
        当前客户端首次连接到服务端时调用
        """
        try:
            self.sk_server.connect((SERVER_IP, SERVER_PORT))
            self.connected = True
            data = self.receive_server()

            # 服务端在首次发送数据为 玩家id: str
            # 后发送正常数据
            if isinstance(data, str):
                if data.isdigit():
                    self.player_id = int(data)
                else:
                    print(f"[WARNING] incorrect data form")
                    Debug(True).div()

            else:
                print(f"[WARNING] incorrect data form")
                Debug(True).div()

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
                    #print(f"[RECEIVING]")
                    #print(data)
                    return data
                except Exception as error:
                    print(f"[GLOBAL WARNING] {error}")

        except Exception as error:
            print(f"[GLOBAL ERROR] {error}")
            Debug(True).div()

            data = {'action': 'error', 'value': {'error': error}}
            self.sk_server.send(pickle.dumps(data))
            print(f"[SENDING]")
            print(data)
            # traceback.print_exc()
            exit(0)

    def respond_server(self, data):
        response = {
            "commands": [
                {
                    "animation": {
                        "aaa": 1,
                        "bbb": 2,
                        "ccc": 3
                    }
                },
                {
                    "attack": {
                        "fk": 666,
                        "st": 888,
                        "ah": 999
                    }
                }
            ],
            'id': -1
        }
        response = {"action": "commands", "value": response}
        #print(f"[SENDING]")
        #print(response)
        try:
            self.sk_server.send(pickle.dumps(response))
        except OSError:
            exit(OSError)

    def run(self, dt):

        self.display_surface.fill("white")

        data = self.receive_server()

        self.horizontal_movement_coll(dt)
        self.vertical_movement_coll(dt)
        self.apply_sprite_gravity(dt)
        self.check_bullet_coll()

        self.update_player_weapon()
        self.fog_1.move()
        self.fog_2.move()

        self.setup_player(data)

        self.respond_server(data)
        # 没有继承, 故需要手动更新 all_sprites
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw()
