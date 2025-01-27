from typing import List, Any, Dict, Tuple
import socket
from config import app_config

from databaser import Database
from ast import literal_eval

def data_handler(data: List[Any]) -> str:
    output = ""
    
    for index in data:
        output += str(index)
        output += "$$"
        
    return output 

class Client:
    def __init__(self, IP: str, port: int) -> None:
        self.IP = IP
        self.port = port
        
        self.contacts_users_db = Database("client\\data\\contacts.db", table = "users")
        
    def get_user_avatar(self, user_id: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        self.server.send(data_handler([user_id, "GET-USER-AVATAR"]))
        
        avatar_from_user_id = (self.server.recv(1024)).decode()
        
        if avatar_from_user_id != "user id not found":
            #принимаем файл с сервера
            with open(f"client\\avatars\\{user_id}.png", "w") as file:
                file.write(avatar_from_user_id)
            
        self.server.close()
        
    def accept_friend_request(self, sender_id: str) -> None:
        self.contacts_users_db.add_contact(sender_id)
        
    def send_friend_request(self, sender_id: str, to_whom_id: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        self.server.send(
            data_handler(data = [sender_id, to_whom_id, "wait", "SEND-FRIEND-REQUEST"]).encode()
        )
        
        data_from_server = (self.server.recv(1024)).decode()
        self.server.close()
        print(data_from_server)
        
    def get_chat(self, self_user_id: str, interlocutor_id: str) -> List[Any] | None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        self.server.send(
            data_handler(data = [self_user_id, interlocutor_id, "GET-CHAT"]).encode()
        )

        server_data = self.server.recv(1024).decode() #data from server
        
        if server_data != "None":
            return literal_eval(server_data)
        return None 
        
    def get_data_user(self, user_id: str) -> Tuple[Any]:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except Exception as e:
            return f"connect_error: {str(e)}"
        
        self.server.send(data_handler(data=[user_id, "GET-USER-DATA"]).encode())
    
        # Получение данных от сервера
        data_from_user_id = (self.server.recv(1024)).decode()
        
        self.server.close()
        return data_from_user_id.split("$$")

    def send_message(self, message_data: dict[Any], type_message: str) -> None | str:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        list_data = []
        
        for index in message_data:
            list_data.append(message_data[index])
            print(list_data)
            
        if type_message == "text":
            self.server.send((data_handler(data = list_data) + "SEND-TEXT-MESSAGE").encode())
    
    def connect_to_server(self, user_data: List[Any] = None) -> None | str:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        user_data.append(None) #avatar
        self.server.send((data_handler(data = user_data) + "CR-ACCOUNT").encode()) #nick_id
    
if __name__ == "__main__":
    client = Client(app_config["IP"], app_config["Port"])
    # client.connect_to_server(["user", "f14d1rf2152fqw", "q2wr2424wwrwrw", "mail@gmail.com"])
    # print(client.get_data_user(user_id = "f14d1rf2152fqw"))
    
    message_data = {
        "sender_id": "dzyg0n546z58854o",
        "message": "Здаров, как дела?",
        "time_send_message": "21:36 05.01.2025",
        "to_whom_message": "k3w7jxthk3ufihus"
    }
    
    client.send_message(message_data, "text")
    
    # client.send_message(message_data, "text")
    print(client.get_chat(
        self_user_id = "dzyg0n546z58854o",
        interlocutor_id = "k3w7jxthk3ufihus"
    ))
    
    
    
