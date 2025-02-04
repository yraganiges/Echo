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
            if random.choice(("num", "lett")) == "num" and len(output) >= 1:
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
        values: Tuple[str],
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
    
    def check_table_exists(self, table: str = None) -> bool:
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (
                self.table if table is None else table,
            )
        )
        self.db.commit()

        return self.cursor.fetchone() is not None
    
    def add_message(
        self,
        sender_id: User_ID | str,
        data_message: str,
        type_message: str, 
        time_send_message: date | str,
        to_whom_message: User_ID | str
    ) -> None | str:
        
        # Проверяем существование пользователя
        if self.get_data_user(user_id=sender_id) is False: 
            return "<er>:Sender ID not found!"
        
        if self.get_data_user(user_id=to_whom_message) is False:
            return "<er>:Receiver ID not found!"
        
        table_name = f"{sender_id}$$${to_whom_message}"
        
        # Проверяем существование таблицы
        if not self.check_table_exists(table_name):
            table_name = f"{to_whom_message}$$${sender_id}"
            if not self.check_table_exists(table_name): #снова пробуем, если нету, то создаём табл
                try:
                    self.cursor.execute( # Создаем таблицу
                        f"""CREATE TABLE {table_name} (
                            data_message TEXT,
                            type_message TEXT,
                            time_send_message TEXT,
                            sender_id TEXT,
                            receiver_id TEXT
                        )"""
                    )
                    self.db.commit()  # Сохраняем изменения
                except Exception as e:
                    return f"<er>:Error creating table: {str(e)}"
        
        # Проверяем длину сообщения и тип сообщения
        if ((len(data_message) <= app_conf["max_length_message"]) and (type_message == "text")) or (type_message != "text"):
            try:
                self.cursor.execute(
                    f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)",
                    (
                        data_message,
                        type_message,
                        time_send_message,
                        sender_id,
                        to_whom_message
                    )
                )
                self.db.commit()  # Сохраняем изменения
            except Exception as e:
                return f"<er>:Error inserting message: {str(e)}"
        else:
            return "<er>:Message length exceeds the maximum limit."

    def add_contact(self, self_id: str, contact_id: str) -> None:
        # if (self.get_data_user(self_id) is None) or (self.get_data_user(contact_id)) is None:
        #     return "<er>:user id is not found!"
        
        #создаём таблицу, если такой нету
        if self.check_table_exists(self_id) is False:
            self.cursor.execute(
                f"""CREATE TABLE {self_id} (
                    contact_id text
                )"""
            )
            self.db.commit()
            
        self.cursor.execute(f"INSERT INTO {self_id} VALUES (?)", (contact_id,))
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
            if nickname in index[0]: return "<er>:никнейм занят"
            if user_id in index[1]: return "<er>:id занят"
            if mail in index[3]: return "<er>:аккаунт с такой почтой уже существует"
            if len(nickname) > 32: return "<er>:длина никнейма должна быть короче 32-ух символов"
            if len(nickname) < 3: return "<er>:длина никнейма должна быть длинее 3-х символов"
            if nickname.strip() == "": return "<er>:никнейм не может быть пустым"
            
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
    
    # db = Database("server\\data\\accounts.db", "users")
    # print(db.get_all_data())