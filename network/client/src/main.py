import socket
import threading
import json

from protocols import *

class Client:
    # 127.0.0.1 - Локальный порт.  55555 - Всегда открытый порт.
    def __init__(self, ip="127.0.0.1", port=55555):
        self.ip = ip
        self.name = "Jerry"
        self.port = port
        self.closed = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((self.ip, self.port))
            print("Connected to server")
        except socket.error as e:
            print(e)

    def handle_console(self):
        while True:
            str = input()
            if str == "/stop":
                print("Stopping...")
                self.send(Request.LEAVE, None)
                self.disconnect()
                exit(0)
            elif str == "/nickname":
                nick = input()
                print(f"Set nickname to {nick}")
                self.send_packet(Request.PROVIDE_NICKNAME, nick)


    def send_packet(self, type, data):
        message = {"type":type,"data":data}
        m = json.dumps(message).encode("ascii")
        print(f"Client {self.name}: sending packet {type}:{data} to server.")
        self.server.send(m)

    def listen_to_server(self):
        while not self.closed:
            message = self.get_response()
            if not message:
                break
            self.read_packet(message)

        self.disconnect()

    def start(self):
        # thread = threading.Thread(target=self.handle_console())
        # thread.start()
        thread = threading.Thread(target=self.listen_to_server())
        thread.start()

    def get_response(self):
        try:
            data = self.server.recv(1024).decode("ascii")
            message = json.loads(data)
            return message
        except:
            return None

    def disconnect(self):
        self.closed = True
        self.server.close()

    def read_packet(self, message):
        type = message.get("type")
        data = message.get("data")
        print(f"Client {self.name}: received packet {type}:{data}")
        if type == Response.REQUEST_NICKNAME:
            print("enter a fucking name.")
            name = input()
            self.send_packet(Request.PROVIDE_NICKNAME, name)

if __name__ == "__main__":
    client = Client()
    client.start()