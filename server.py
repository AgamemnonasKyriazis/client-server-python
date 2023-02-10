import socket
import threading
import sys
import pickle
import selectors
import signal


HOST = ""
PORT = 7777
sprites_dict = dict()


def handler(signum, frame):
    global running
    running = False
    print("Stopping main thread")
    sys.exit(0)


def accept_connection(server:socket.socket):
    global next_client_id, selector, active_clients
    conn, addr = server.accept()
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    client_id = next_client_id
    conn.send(pickle.dumps(client_id))
    next_client_id += 1
    selector.register(conn, selectors.EVENT_READ, receive)
    active_clients[conn] = client_id


def receive(conn: socket.socket):
    global selector
    reply = ""
    try:
        data = conn.recv(2048)
        if not data:
            print("Client disconnected")
            selector.unregister(conn)
            sprites_dict.pop(active_clients[conn])
            active_clients.pop(conn)
            conn.close()
            return
        else:
            reply = pickle.loads(data)
            sprites_dict.update(reply)
            print(sprites_dict)
            conn.send(pickle.dumps(sprites_dict))
            print(f"Reply = {reply}")
    except:
        print("Error on receive")


def main():
    global running
    while running:
        events = selector.select()
        for key, mask in events:
            sock = key.fileobj
            callback = key.data
            callback(sock)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    running = True
    next_client_id = 0
    active_clients = dict()
    selector = selectors.DefaultSelector()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    selector.register(server, selectors.EVENT_READ, accept_connection)
    threading.Thread(target=main, daemon=True).start()
    while running:
        pass
