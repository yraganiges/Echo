import socket
from threading import Thread

class CallServer:
    def __init__(self, IP: str, port: int) -> None:
        self.clients = []
        self.ip = IP
        self.port = port
    
    def handle_client(self, conn, addr):
        print(f"Подключен клиент: {addr}")
        self.clients.append(conn)
        if len(self.clients) == 2:
            print("Два клиента подключены, начинаем передачу данных между ними.")
            Thread(target=self.forward_audio, args=(self.clients[0], self.clients[1])).start()
            Thread(target=self.forward_audio, args=(self.clients[1], self.clients[0])).start()

    def forward_audio(self, source, target):
        while True:
            try:
                data = source.recv(1024)
                if not data:
                    break
                target.sendall(data)
            except ConnectionResetError:
                print("Клиент отключился.")
                break
            except ConnectionAbortedError:
                print("Клиент отключился.")
                break
            except:
                break
            
        # Удаляем клиентов из списка после завершения передачи данных
        self.remove_client(source)
        self.remove_client(target)
    
    def remove_client(self, conn):
        if conn in self.clients:
            self.clients.remove(conn)
            print(f"Клиент удален из списка. Осталось клиентов: {len(self.clients)}")
    
    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()
            print(f"Сервер запущен на {self.ip}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(True)
                Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    srv = CallServer("26.61.8.55", 52)
    srv.start_server()
