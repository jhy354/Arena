import socket
import pickle
import select

from engine.settings import *

if __name__ == "__main__":

    sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sk_server.connect((SERVER_IP, SERVER_PORT))
    except Exception as error:
        print(f"[WARNING] {error}")
        exit(1)

    # * MAIN LOOP * #
    while True:

        ready_sockets, _, _ = select.select([sk_server], [], [], CLIENT_TIMEOUT)

        try:
            if ready_sockets:
                try:
                    data = pickle.loads(sk_server.recv(HEADER))
                except Exception as error:
                    print(f"[GLOBAL WARNING] {error}")
                    continue

                if isinstance(data, str) and data == "":
                    pass
                elif isinstance(data, str) and data == "":
                    pass

                # 回应服务端
                response = {
                    'commands': [
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
                response = {'action': 'commands', 'value': response}
                print(response)
                sk_server.send(pickle.dumps(response))
                exit(-1)

        except Exception as error:
            print(f"[GLOBAL ERROR] {error}")
            sk_server.send(pickle.dumps({'action': 'error', 'value': {'error': error}}))
            # traceback.print_exc()
            exit(0)
