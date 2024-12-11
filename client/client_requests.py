from typing import List, Any
import socket
from config import app_config

class Client:
    def __init__(self, IP: str, port: int) -> None:
        self.server = socket.socket()
        self.IP = IP
        self.port = port
    
    def connect_to_server(self, user_data: List[Any] = None) -> Any:
        try:
            self.server.connect((self.IP, self.port))
        except:
            return "error_connect"
        
        self.user_nickname: str = user_data[0]
        self.user_id: str = user_data[1]
        
        self.server.send((self.user_nickname + "_" + self.user_id).encode()) #nick_id
    
if __name__ == "__main__":
    client = Client(app_config["IP"], app_config["Port"])
    client.connect_to_server(["user", "f14d1rf2152fqw"])
        
    
    
