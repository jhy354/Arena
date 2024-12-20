import sys
import getopt
import time
import socket
import select
import pickle
import threading
import random

from engine.settings import *
from engine.utils import Debug

usage = "usage: python server.py [-a | --address] [-m | --map_index] [-b | background_index]"


class ResponseHandler:
    """
    处理客户端回复
    该类所有函数均在 GameServer.handler() 中调用
    """

    def handle_commands(self, status, response):

        for command in response["commands"]:
            cmd = list(command.keys())[0]

            # * Call Handler * #
            handler = getattr(self, f"handle_{cmd}", None)

            if callable(handler):
                status = handler(status, command[cmd])
            else:
                print(f'[WARNING] no handler for {cmd}')

        return status

    @staticmethod
    def handle_movement(status, command):

        for player in status["players"]:
            if player["id"] == command["id"]:
                player["pos"] = command["pos"]

        return status

    @staticmethod
    def handle_animation(status, command):

        for player in status["players"]:
            if player["id"] == command["id"]:
                player["skin"] = command["skin"]
                player["status"] = command["status"]
                player["frame_index"] = command["frame_index"]
                player["face_direction"] = command["face_direction"]

        return status

    @staticmethod
    def handle_bullet(status, command):

        for player in status["players"]:
            if player["id"] == command["id"]:
                player["bullet_list"] = command["bullet_list"]

        return status

    @staticmethod
    def handle_score(status, command):

        for player in status["players"]:
            if player["id"] == command["id"]:
                player["score"] = command["score"]

        return status


class GameServer:

    def __init__(self, host, port, _map_index, _bg_index, response_handler: ResponseHandler):
        self.HOST = host
        self.PORT = port
        # 发送给客户端
        self.status = {
            "map": _map_index,
            "bg": _bg_index,
            "players": [],
            "timer": {
                "time": None,
                "finished": False
            }
        }

        self.sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.response_handler = response_handler
        self.tot_player_cnt = 0

        # Timer
        self.is_timer_started = False
        self.start_time = None
        self.current_time = None

        Debug(True).div()
        try:
            self.sk_server.bind((self.HOST, self.PORT))
            self.sk_server.listen(MAX_LISTEN)
            self.sk_server.settimeout(1.0)  # Allow timeout to process KeyboardInterrupt
        except Exception as error:
            sys.exit(f"\033[1;32m[ERROR IN CREATING A SERVER]\033[0m {error}")
        else:
            print(f"\033[1;36m[SERVER IS LISTENING]\033[0m "
                  f"@ "
                  f"\033[1;32m{host}:{port}\033[0m")

    def establish_conn(self, address, connect_time):
        print(f"\033[1;36m[CONN ESTABLISHED]\033[0m "
              f"@ "
              f"\033[1;32m{address[0]}:{str(address[1])}\033[0m "
              f"at "
              f"\033[1;34m{connect_time}\033[0m "
              f"\033[3;33mEnjoy Yourself in Arena :)\033[0m")

        self.status["players"].append({
            "id": str(self.tot_player_cnt),
        })

        if self.tot_player_cnt >= 2 and not self.is_timer_started:
            self.start_timer()
            self.is_timer_started = True

    def handler(self, conn: socket.socket, status):
        """
        接受客户端回复并回复客户端
        """
        while True:
            ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)
            response = None

            if not ready_sockets:
                conn.send(pickle.dumps(status))
                # print(f"[SENDING] not ready")
                # print(status)
                # Debug(True).div()
                continue

            try:
                response = pickle.loads(conn.recv(HEADER))
                handler = getattr(self.response_handler, f"handle_{response['action']}", None)

                if callable(handler):
                    status = handler(status, response["value"])

                    if self.is_timer_started:
                        status["timer"]["time"] = self.get_updated_time()
                        if self.get_updated_time() < ARENA_MODE_TIME:
                            status["timer"]["finished"] = False
                        else:
                            status["timer"]["finished"] = True

                    conn.send(pickle.dumps(status))
                    # print(f"[SENDING]")
                    # print(status)
                    # Debug(True).div()
                else:
                    print(f'\033[1;32m[WARNING]\033[0m no handler for {response["action"]}')

            # 客户端强制断开
            except ConnectionResetError as error:
                # print(error)
                print(f"\033[1;32m[CLIENT]\033[0m Client Connection Reset")
                break

            except Exception as error:
                print(f"\033[1;32m[WARNING IN RECEIVING DATA]\033[0m {error}")
                print("\033[1;32mResponse:\033[0m")
                Debug(True).div()
                print(response)
                Debug(True).div()
                break

    @property
    def active_player_count(self) -> int:
        return threading.active_count() - 1  # Subtract 1 to exclude the main thread

    def run(self):
        with open("ascii_logo.txt") as f:
            for line in f.readlines():
                print(f"\033[1;34m{line}\033[0m", end="")
        print("")
        print(f"\033[1;33m{VERSION}\033[0m")
        Debug(True).div()

        # MAIN LOOP #
        while True:

            try:
                client, address = self.sk_server.accept()
                self.tot_player_cnt += 1
                self.establish_conn(address, time.strftime("%H:%M:%S", time.localtime()))

                # 建立连接后首次发送数据
                d = str(self.tot_player_cnt)
                client.send(pickle.dumps(d))
                # print(f"[SENDING]")
                # print(d)
                # Debug(True).div()

                conn_thread = threading.Thread(target=self.handler, args=(client, self.status))
                conn_thread.start()

            except KeyboardInterrupt:
                self.sk_server.close()
                sys.exit(f"\033[1;32m[WARNING]\033[0m {KeyboardInterrupt}")

            except socket.timeout:
                # print(f"[WARNING] {socket.timeout}")
                try:
                    continue
                except KeyboardInterrupt:
                    self.sk_server.close()
                    sys.exit(f"\033[1;32m[WARNING]\033[0m {KeyboardInterrupt}")

            except BaseException as error:
                print(f'\033[1;32m[ERROR]\033[0m {error}')
                self.sk_server.close()
                sys.exit()

    def start_timer(self):
        self.start_time = time.time()  # 浮点秒数

    def get_updated_time(self):
        self.current_time = time.time() - self.start_time
        if self.current_time >= ARENA_MODE_TIME:
            return -1
        else:
            return int(self.current_time)


if __name__ == "__main__":
    server_ip = DEFAULT_SERVER_IP
    server_port = DEFAULT_SERVER_PORT
    map_index = random.randint(0, 2)
    bg_index = random.randint(0, 3)

    argv = sys.argv
    opts = None
    args = None

    try:
        opts, args = getopt.getopt(argv[1:], "-a:-m:-b:", ["address=", "map_index=", "background_index="])
    except getopt.GetoptError:
        print(usage)
        exit(1)

    for opt, arg in opts:
        if opt in ("-a", "--address"):
            server_ip = str(arg)
        elif opt in ("-m", "--map_index"):
            map_index = int(arg)
        elif opt in ("-b", "--background_index"):
            bg_index = int(arg)
        else:
            print(f"unknown option: {opt}")
            print(usage)
            exit(1)

    server = GameServer(server_ip, server_port, map_index, bg_index, ResponseHandler())
    server.run()

    sys.exit(0)
