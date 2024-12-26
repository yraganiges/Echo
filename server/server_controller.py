from typing import Any, Tuple, List
from databaser import User_ID, Database, Encryption
from threading import Thread
from cryptography.fernet import Fernet
from string_handlers import data_handler
import socket
import asyncio
import time

class Server(object):
    def __init__(self, IP: str, port: int) -> None:
        self.serv = socket.socket()
        self.serv.bind((IP, port))
        
        self.users: List[Any] = []
        self.server_run_status: bool = False
        
        #databases
        self.accounts_db = Database("server\\data\\accounts.db", "users")
        self.messages_db = Database("server\\data\\messages.db", "all_messages")
        self.account_keys_db = Database("server\\data\\accounts.db", "keys")
        
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
        
    def listen(self) -> None:
        print("start")
        if self.status_run_server():
            while self.status_run_server():
                try:
                    connect, add = self.serv.accept() #Ждём запросы от клиента
                    client_user = (connect.recv(1024)).decode() #декодируем запрос от клиента, если запрос поступил на сервер
                    self.users.append(tuple(client_user.split("$$"))) #Добавляем данные пользователя, подключившегося к серверу в список данных пользователей 
                    
                    list_user_data = client_user.split("$$")
                    
                    if list_user_data[-1] == "":
                        user_data = tuple(list_user_data[0:-1])
                    else:
                        user_data = tuple(list_user_data)
                        
                    print(user_data)
                    
                    #Создаём аккаунт, если id пользователя нету в БД
                    if self.accounts_db.get_data_user(user_data[1]) is None and user_data[-1] == "CR-ACCOUNT":
                        key = Fernet.generate_key()
                        
                        self.accounts_db.create_account(
                            nickname = user_data[0],
                            user_id = user_data[1],
                            password = user_data[2],
                            mail = user_data[3],
                            date_created_account = user_data[4]
                        )
                        
                    if user_data[-1] == "SEND-MESSAGE":
                        #add message
                        self.messages_db.add_message(
                            user_data[0], #sender_id
                            user_data[1], #message
                            user_data[2], #time_send_message
                            user_data[3] #to_whom_message(user_id)
                        )
                        
                    if user_data[-1] == "GET-USER-DATA":
                        print(True)
                        #Передаём данные пользователя обратно клиенту
                        connect.sendall(
                            (data_handler(self.accounts_db.get_data_user(user_data[0]))).encode()
                        )
                        print(True)
                        
                except:
                    pass
                
                print(self.users)
                time.sleep(0.5)
                
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
                await asyncio.sleep(0.5)
            
if __name__ == "__main__":
    srv = Server("127.0.0.1", 50) 
    asyncio.run(srv.run(300))
    Thread(daemon = True, target = srv.listen).start()
    
        
