# echo-server.py

import socket
import time
import threading
import sys
import pickle

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on (non-privileged ports are > 1023)

activeThreadList = []

def readStream(conn):
    reply = ""
    while(True):
        try:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected")
                conn.close()
                return
            else:
                reply = pickle.loads(data)
                print(f"Reply = {reply}")
        except:
            break


def initServerSocket():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    while True:
        conn, addr = lsock.accept()
        th = threading.Thread(target=readStream, args=(conn,), daemon=True)
        activeThreadList.append(th)
        th.start()


if __name__ == "__main__":
    th = threading.Thread(target=initServerSocket, daemon=True)
    activeThreadList.append(th)
    th.start()
    try:
        while True:
            continue
    except KeyboardInterrupt:
        for th in activeThreadList:
            th.close()
    finally:
        sys.exit(0)