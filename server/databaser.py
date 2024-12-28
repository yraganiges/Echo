from typing import Any, Tuple, List
from config import app_conf

from datetime import date
from cryptography.fernet import Fernet

import random
import sqlite3

class User_ID:
    def generate_user_id(length: int = 16) -> str:
        output: str = ""
        
        for _ in range(length):
            if random.choice(("num", "lett")) == "num":
                output += str(random.choice(list(range(0, 10))))
            else:
                output += random.choice("qwertyuiopasdfghjklzxcvbnm")
                
        return output

class Encryption:
    def encryption_password(password: str, key: bytes = Fernet.generate_key()) -> bytes:
        cipher_suite = Fernet(key)
        
        return cipher_suite.encrypt(password.encode())
    
    def decryption_password(encrypt_password: bytes, key: bytes) -> bytes:
        if key is None:
            raise ValueError()
        else:
            return Fernet(key).decrypt(encrypt_password)
        
    def encryption_message(**args) -> bytes:
        ...
        #TODO Сделать шифрование сообщений по немножку другому алгоритму
        
class Database(object):
    def __init__(self, database: str, table: str) -> None:
        self.table = table
        
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        
    def insert_data(
        self,
        values: Tuple[str] | List[str],
    ) -> None:
        values_string = ("(" + ("?," * len(values)))[0:-1] + ")" #example: (?,?,?) 
        
        self.cursor.execute(f"INSERT INTO {self.table} VALUES {values_string}", values)
        self.db.commit()
        
    def get_data_user(self, user_id: User_ID | str) -> Tuple[Any] | None:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        
        for index in self.cursor.fetchall():
            if user_id == index[1]:
                return index
            
    def edit_online_status(self, status: bool, user_id: User_ID | str) -> None:
        self.cursor.execute(f"UPDATE {self.table} SET online_status = ?, where id = ?", (status, user_id))
        self.db.commit()
        
    def table_data_count(self) -> int:
        count = 0
        
        for _ in range(len(self.get_all_data())):
            count += 1
            
        return count
        
    def get_all_data(self) -> Tuple[Any]:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()
    
    def delete_account(
        self,
        user_id: User_ID | str,
    ) -> bool:
        if self.get_data_user(user_id) is not None:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (user_id, ))
            self.db.commit()
            
            return True
        return False
    
    def add_message(
        self,
        sender_id: User_ID | str,
        message: str,
        time_send_message: date | str,
        to_whom_message: User_ID | str
    ) -> None | str:
        if self.get_data_user(user_id = sender_id) is False: 
            return "sender id not found!"
        if self.get_data_user(user_id = to_whom_message) is False:
            return "receiver id is not found!"
        
        if len(message) <= app_conf["max_length_message"]:
            self.cursor.execute(
                f"INSERT INTO {self.table} VALUES (?, ?, ?, ?)",
                (
                    sender_id,
                    message,
                    time_send_message,
                    to_whom_message
                )
            )
            self.db.commit()
    
    def create_account(
        self,
        nickname: str,
        user_id: User_ID | str,
        password: str,
        mail: str,
        date_created_account: date,
        path_avatar: str
    ) -> None | str:
        #Проверяем, есть ли уже такой аккаунт в базе данных
        for index in self.get_all_data():
            if nickname in index[0]: return "никнейм занят"
            if user_id in index[1]: return "id занят"
            if mail in index[3]: return "аккаунт с такой почтой уже существует"
            if len(nickname) > 32: return "длина никнейма должна быть короче 32-ух символов"
            
        self.cursor.execute(
            f"INSERT INTO {self.table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                nickname, 
                user_id,
                Encryption.encryption_password(password),
                mail,
                date_created_account,
                None, #online_status
                None, #time_last_online
                path_avatar, #avatar
                None #description
            )
        )
        self.db.commit()
    
if __name__ == "__main__":
    db = Database("server\\data\\accounts.db", "users")
    # db.create_account(
    #     nickname = "test11",
    #     user_id = User_ID.generate_user_id(),
    #     password = "qef24fweg1",
    #     mail = "test2@gmail.com",
    #     date_created_account = str(date.day)
    # )
    # print(db.get_all_data()) 
    # print(db.table_data_count())
    # print(db.get_data_user(user_id = "dzyg0n546z58854o"))