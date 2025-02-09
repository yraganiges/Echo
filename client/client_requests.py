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
        
        
    # def receive_message(self):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server:
    #         self.server.connect((self.IP, self.port))
    #         try:
    #             data = self.server.recv(1024 ** 3) # Получаем данные от сервера
                
    #             if not data:
    #                 return None
                
    #             message = data.decode('utf-8') # Декодируем и выводим сообщение
    #             return message
    #         except Exception as e:
    #             print(f"Ошибка: {e}")
    #             break
        
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
        
    def get_user_avatar(self, user_id: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        self.server.send(data_handler([user_id, "GET-USER-AVATAR"]).encode())
        
        avatar_from_user_id = self.server.recv((1024 ** 3) // 3 ) #~2мб
                
        if avatar_from_user_id != "user id not found":
            #принимаем файл с сервера
            with open(f"client\\user_avatars\\{user_id}.png", "wb") as file:
                file.write(avatar_from_user_id)
        else:
            return "<er>:not load avatar"
            
        self.server.close()
        
    def get_chat(self, self_user_id: str, interlocutor_id: str) -> List[Any] | None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error"
        
        self.server.send(
            data_handler(data = [self_user_id, interlocutor_id, "GET-CHAT"]).encode()
        )

        try: server_data = self.server.recv(2097152).decode() #2мб #data from server
        except: server_data = "None"
        
        if server_data != "None":
            return literal_eval(server_data)
        return None 
        
    def get_data_contacts(self, self_id: str) -> Tuple[Any]:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except Exception as e:
            return f"connect_error: {str(e)}"
        
        self.server.send(data_handler([self_id, "GET-CONTACTS"]).encode())
        
        #получаем данные о контактах от сервера
        contacts_data = literal_eval(self.server.recv(1024).decode())
        return contacts_data
        
    def get_data_user(self, user_id: str) -> Tuple[Any]:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except Exception as e:
            return f"connect_error: {str(e)}"
        
        self.server.send(data_handler(data=[user_id, "GET-USER-DATA"]).encode())
    
        # Получение данных от сервера
        # try: data_from_user_id = (self.server.recv(1024 * 2)).decode()
        # except: data_from_user_id = None
        data_from_user_id = (self.server.recv(1024 * 2)).decode()
        
        self.server.close()
        # if data_from_user_id == None: #debug
        #     return "None"
        if data_from_user_id[0:4] == "<er>":
            return data_from_user_id #return error
        return data_from_user_id.split("$$")
    
    def get_user_id_by_nickname(self, user_nickname: str) -> str:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except Exception as e:
            return f"connect_error: {str(e)}"
        
        self.server.send(data_handler([user_nickname, "GET-USER-ID"]).encode())
        
        user_id = self.server.recv(1024).decode()
        
        if user_id == "None":
            return None
        return user_id


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
            
    def add_contact(self, self_id: str, contact_id: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "connect_error" 
        
        self.server.send(data_handler([self_id, contact_id, "ADD-CONTACT"]).encode())
    
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
    
    client.add_contact("dzyg0n546z58854o", "79k261w10r0ui03i")
    
    
    
    
    
