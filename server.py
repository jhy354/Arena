# response format:
# for commands: {'action': 'commands', 'value': {'commands': ...}}
# for errors: {'action': 'error', 'value': {'error': ...}}

import sys
import time
import socket
import select
import pickle
import threading

from engine.settings import *


class ResponseHandler:

    def handle_commands(self, status, response):

        for command in response["command"]:
            cmd = list(command.keys())[0]

            # * Call Handler * #
            handler = getattr(self, f"handle_{cmd}", None)

            if callable(handler):
                status = handler(status, command[cmd])
            else:
                print(f'No handler for {cmd}')

        return status

    @staticmethod
    def handle_movement(status, command):
        return status

    @staticmethod
    def handle_animation(status, command):
        return status

    @staticmethod
    def handle_attack(status, command):
        return status


class GameServer:

    def __init__(self, host, port, response_handler: ResponseHandler):
        self.HOST = host
        self.PORT = port
        self.status = {
            "players": []
        }

        self.sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.response_handler = response_handler
        self.tot_player_cnt = 0

        try:
            self.sk_server.bind((self.HOST, self.PORT))
            self.sk_server.listen(MAX_LISTEN)
            self.sk_server.settimeout(1.0)  # Allow timeout to process KeyboardInterrupt
        except Exception as error:
            sys.exit(f"[ERROR IN CREATING A SERVER] {error}")
        else:
            print(f"[SERVER IS LISTENING] @ {host}:{port}")

    def establish_conn(self, address, connect_time):
        print(f"Connection has been established with: {address} at {connect_time}. Welcome :)")

        self.status["players"].append({
            "id": str(self.tot_player_cnt),
        })

    def handler(self, conn: socket.socket, status):

        while True:
            ready_sockets, _, _ = select.select([conn], [], [], SERVER_TIMEOUT)

            if not ready_sockets:
                conn.send(pickle.dumps(status))
                continue

            try:
                response = pickle.loads(conn.recv(HEADER))
                handler = getattr(self.response_handler, f"handle_{response['action']}", None)

                if callable(handler):
                    status = handler(status, response["value"])
                    conn.send(pickle.dumps(status))
                else:
                    print(f'[WARNING] No handler for {response["action"]}')

            except Exception as error:
                print(f"[WARNING IN SENDING DATA] {error}")
                break

    @property
    def active_player_count(self) -> int:
        return threading.active_count() - 1  # Subtract 1 to exclude the main thread

    def run(self):
        with open("ascii_logo.txt") as f:
            for line in f.readlines():
                print(line, end="")
        print("")
        print(VERSION)

        # MAIN LOOP #
        while True:

            try:
                client, address = self.sk_server.accept()
                self.tot_player_cnt += 1
                self.establish_conn(address, time.time())

                client.send(pickle.dumps(str(self.tot_player_cnt)))
                conn_thread = threading.Thread(target=self.handler, args=(client, self.status))
                conn_thread.start()

            except KeyboardInterrupt:
                self.sk_server.close()
                sys.exit(f"[WARNING] {KeyboardInterrupt}")

            except socket.timeout:
                # print(f"[WARNING] {socket.timeout}")
                continue

            except BaseException as error:
                print(f'[ERROR] {error}')
                self.sk_server.close()
                sys.exit()


if __name__ == "__main__":

    server = GameServer(SERVER_IP, SERVER_PORT, ResponseHandler())
    server.run()

    sys.exit(0)
