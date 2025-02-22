from typing import Any, Tuple, List
from databaser import User_ID, Database, Encryption
from threading import Thread
from cryptography.fernet import Fernet
from string_handlers import data_handler, text_for_generate_avatar_handler
from avatar_generator import generate_avatar
import socket
import asyncio
import time

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

class Server(object):
    def __init__(self, IP: str, port: int) -> None:
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind((IP, port))
        
        self.users: List[Any] = []
        self.server_run_status: bool = False
        
        #databases
        self.accounts_db = Database("server\\data\\accounts.db", "users")
        self.friend_requests_db = Database("server\\data\\accounts.db", "friend_requests")
        self.messages_db = Database("server\\data\\messages.db", "all_messages")
        # self.messages_db = Database("server\\data\\messages.db", "all_messages")
        # self.account_keys_db = Database("server\\data\\accounts.db", "keys")
        
        
    def status_run_server(self) -> bool:
        return self.server_run_status
            
    def connect_user_to_server(
        self,
        user_id: User_ID | str
    ) -> bool:
        ...
        
    async def stop(self) -> None:
        self.server_run_status = False
        self.serv.close() #stop server
        
    def listen(self, delay: float = 0.05) -> None:
        print("start")
        if self.status_run_server():
            while self.status_run_server():
                try:
                    connect, add = self.serv.accept() #Ждём запросы от клиента
                    client_user = (connect.recv(2097152)).decode() #декодируем запрос от клиента, если запрос поступил на сервер
                    self.users.append(tuple(client_user.split("$$"))) #Добавляем данные пользователя, подключившегося к серверу в список данных пользователей 
                    
                    print(client_user)
                    list_user_data = client_user.split("$$")
                    
                    if list_user_data[-1] == "":
                        user_data = tuple(list_user_data[0:-1])
                    else:
                        user_data = tuple(list_user_data)
                        
                    print(user_data)
                    
                    #Создаём аккаунт, если id пользователя нету в БД
                    # if self.accounts_db.get_data_user(user_data[1]) is None or user_data[-1] == "CR-ACCOUNT":
                    if user_data[-1] == "CR-ACCOUNT":
                        key = Fernet.generate_key()
                        
                        if user_data[1] == "None":
                            user_id = user_data[1]
                            while (user_id == "None") or (self.accounts_db.get_data_user(user_id) is not None):
                                user_id = User_ID.generate_user_id()
                        
                        path_avatar = f"server\\avatars\\{user_id}.png"
                        
                        self.accounts_db.create_account(
                            nickname = user_data[0],
                            user_id = user_id,
                            password = user_data[2],
                            mail = user_data[3],
                            date_created_account = user_data[4],
                            path_avatar = path_avatar
                        )
                        
                        generate_avatar(
                            text = text_for_generate_avatar_handler(user_data[0]),
                            path_save = path_avatar,
                            size = (100, 100)
                        )
                        
                    if user_data[-1] == "ADD-CONTACT":
                        self.contacts_db = Database("server\\data\\contacts.db", user_data[0])
                        
                        self.contacts_db.add_contact(
                            self_id = user_data[0],
                            contact_id = user_data[1]
                        )
                        
                    if user_data[-1] == "SEND-TEXT-MESSAGE":
                        #add message
                        self.messages_db.add_message(
                            sender_id = user_data[0], #sender_id
                            data_message = user_data[1], #message
                            type_message = "text",
                            time_send_message = user_data[2], #time_send_message
                            to_whom_message = user_data[3] #to_whom_message(user_id)
                        )
                        
                    print(user_data[-1])
                    print(user_data[-1] == "GET-USER-DATA")                        
                        
                    if user_data[-1] == "GET-USER-ID":
                        status = False
                        for index in self.accounts_db.get_all_data():
                            if user_data[0] == index[0]:
                                connect.send(index[1].encode()) #send user id
                                status = True
                        if status == False:
                            connect.send("None".encode())
                        
                        
                    if user_data[-1] == "GET-USER-DATA":
                        #Передаём данные пользователя обратно клиенту
                        if self.accounts_db.get_data_user(user_data[0]) is None:
                            connect.sendall("<er>:user is not found".encode())
                        else:
                            connect.sendall(
                                (data_handler(self.accounts_db.get_data_user(user_data[0]))).encode()
                            )
                        
                    if user_data[-1] == "GET-CHAT":
                        
                        self.chat_db = Database(
                            database = "server\\data\\messages.db",
                            table = f"{user_data[0]}$$${user_data[1]}"
                        )
                        
                        if self.chat_db.check_table_exists() == False:
                            self.chat_db = Database(
                                database = "server\\data\\messages.db",
                                table = f"{user_data[1]}$$${user_data[0]}"
                            )
                            
                        if self.chat_db.check_table_exists() == False:
                            connect.sendall("None".encode())
                        else:
                            #Передаём клиенту данные о переписке
                            connect.sendall(
                                str(self.chat_db.get_all_data()).encode()
                            )
                        
                    if user_data[-1] == "GET-CONTACTS":
                        self.contacts_db = Database(
                            "server\\data\\contacts.db",
                            user_data[0]
                        )
                        
                        if self.contacts_db.check_table_exists() is True:
                            #Передаём данные чата
                            connect.sendall(
                                str(self.contacts_db.get_all_data()).encode()
                            )
                        else:
                            connect.send("None".encode())
                                            
                        
                    if user_data[-1] == "SEND-FRIEND-REQUEST":
                        if self.accounts_db.get_data_user(user_id = user_data[1]) is not None:
                            self.friend_requests_db.insert_data(
                                (user_data[0], user_data[1], user_data[2])
                            )

                            connect.sendall("friend request sent".encode()) #response
                        else:
                            connect.sendall("user not found".encode())
                            
                    if user_data[-1] == "GET-USER-AVATAR":
                        if self.accounts_db.get_data_user(user_data[0]) is not None:
                            with open(f"server\\avatars\\{user_data[0]}.png", "rb") as file:
                                connect.sendall(file.read()) #передаём png файл клиенту
                        else:
                            connect.sendall("user id not found!")
                except:
                    pass
                
                time.sleep(delay)
                
        print("end")
        
    async def run(self, time_working: int | bool = False) -> None:
        """
        Если установлено время, для работы сервера, то рекомендуется
        запускать сервер, с помощью ассинхронности (module async).
        
        time_working(секунды) > 0
        """
        
        self.serv.listen() #start server
        self.server_run_status = True
        print("server is run!")
        
        asyncio.run(self.listen())
        
        if type(time_working) is int and time_working > 0:
            while time_working > 0 and self.server_run_status:
                time_working -= 1
                await asyncio.sleep(1)

            self.serv.close() #stop server
            self.server_run_status = False
        else:
            while self.server_run_status:
                await asyncio.sleep(0.1)
            
if __name__ == "__main__":
    # srv = Server("26.61.8.55", 50) 
    # asyncio.run(srv.run(300))
    # Thread(daemon = True, target = srv.listen).start()
    
    srv = CallServer("26.61.8.55", 52)
    srv.start_server()
    
        
