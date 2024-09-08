import socket
import threading
import json
from protocols import *

class Client:
    def __init__(self, connection, name="Jerry"):
        self.connection = connection
        self.name = name
        self.opponent = None


class Server:
    # 127.0.0.1 - Локальный порт.  55555 - Всегда открытый порт.
    def __init__(self, ip="127.0.0.1", port=55555):
        self.ip = ip
        self.is_running = True
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            print(e)
        self.server.listen()

        self.clients = []
        self.waiting_for_connection = True
        print("Server started. Waiting for players")
        self.open_server()

    def disconnect(self, client):
        client.connection.close()

    def sent_packet(self, request_type, data, client):
        message = {"type":request_type, "data":data}
        client.connection.send(   json.dumps(message).encode("ascii")    )
        print(f"Server: sending packet {request_type}:{data} to client {client.name}.")

    def get_client_respose(self, client):
        """
            Функция будет ждать, когда клиент отправит какой-нибудь пакет серверу

            Returns:
                response_type - Protocols.Request тип пакета, отправленного клиентом.
                data - подробности пакета.
            """
        # client.recv() будет ждать до тех пор,
        # пока не получит ответ от клиента
        try:
            data = client.connection.recv(1024).decode("ascii")
        except ConnectionResetError:
            print(f"Client {client.name}: ConnectionReset: Disconnected.")
            return None, None
        if not data:
            return None, None
        message = json.loads(data)

        request_type = message.get("type")
        data = message.get("data")
        return request_type, data

    def handle_console(self):
        while self.is_running:
            str = input()
            if str == "/stop":
                print("Stopping...")
                for client in self.clients:
                    self.sent_packet(Response.SERVER_CLOSED, None, client)
                    self.disconnect(client)
                exit(0)

    def open_server(self):
        while True:
            # server.accept() будет ждать до тех пор,
            # пока не получит информацию о новом подключении
            client_connection, address = self.server.accept()
            client = Client(client_connection)
            print(f"{str(address)} connected to the Server!")
            thread = threading.Thread(target=self.handle_connection,args=(client,))
            thread.start()



    def read_packet(self, message, client):
        type = message.get("type")
        data = message.get("data")
        print(f"Server: received packet from {client}:  {type}:{data}")

    def handle_connection(self, client):
        self.connect_client(client)
        while self.is_running:
            try:
                type, data = self.get_client_respose(client)
                if not type:
                    print(f"Connection with {client.name} lost. Disconnecting")
                    break

            except:
                print(f"Exception in client {client.name}. Disconnecting")
                break

        if client.opponent:
            self.sent_packet(Response.OPPONENT_LEFT, None, client.opponent)
            client.opponent.opponent = None

        self.disconnect(client)

    def connect_client(self, client):
        while self.is_running:
            self.sent_packet(Response.REQUEST_NICKNAME, None, client)
            response_type, data = self.get_client_respose(client)
            if not response_type:
                self.disconnect(client)
                break
            if response_type == Request.PROVIDE_NICKNAME:
                self.clients.append(client)
                print(f"Client {client.name} choose name {data}. Such a stupid decision...")
                client.name = data  # Клиент выбрал себе имя: обновляем.

            else:
                continue

            self.waiting_for_connection = len(self.clients) < 2
            if not self.waiting_for_connection:
                for i in range(2):
                    client1 = self.clients[1-i]
                    client2 = self.clients[i]
                    client1.opponent = client2
                    self.sent_packet(Response.OPPONENT_FOUND, client1.name, client2)
            break


if __name__ == "__main__":
    server = Server()
    server.open_server()