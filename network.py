import socket
import pickle

class NetworkInterface:

    def __init__(self, host="", port=7777) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.id = -1
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            response = pickle.loads(self.client.recv(1024))
            return response
        except:
            print("Connecting to server failed")
            return None
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            response = self.client.recv(1024)
            return pickle.loads(response)
        except:
            print("Transmission to server failed")
            return None
    
    def close(self):
        self.client.close()


if __name__ == "__main__":
    my_network = NetworkInterface(host="loukoumades.ddns.net", port=7777)
    response = my_network.connect()
    print(response)
    response = my_network.send("Hello World")
    print(response)
    my_network.close()
    exit(0)