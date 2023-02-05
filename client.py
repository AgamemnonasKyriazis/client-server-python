# echo-client.py

import socket
import time
import pickle


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5555  # The port used by the server


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        try:
            while(True):
                s.sendall(pickle.dumps("Hello, world"))
                time.sleep(1)
        except KeyboardInterrupt:
            exit(0)