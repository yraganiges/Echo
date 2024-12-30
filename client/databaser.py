from typing import Any, Tuple
import sqlite3

class Database(object):
    def __init__(self, database: str, table: str) -> None:
        self.table = table
        
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        
    def add_contact(self, user_id: str) -> None:
        self.cursor.execute(
            f"INSERT INTO {self.table} VALUES (?, ?)",
            (user_id, None)
        )
        self.db.commit()
        
    def delete_contact(self, user_id: str) -> None:
        self.cursor.execute(
            f"DELETE FROM {self.table} WHERE user_id = ?",
            (user_id, )
        )
        self.db.commit()
        
    def get_data_chat(self, user_id: str) -> Tuple[Any]:
        for index in self.get_data():
            if index[0] == user_id:
                return index[1]
        
    def get_data(self) -> Tuple[Any]:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()
    
if __name__ == "__main__":
    db = Database("client\\data\\contacts.db", "users")
    print(db.get_data())
    
    db.add_contact("0s27298594w99s24")
    db.add_contact("2slkkb842smf39m0")
    db.add_contact("7r6mv3z7773ogzio")
    db.add_contact("k3w7jxthk3ufihus")
