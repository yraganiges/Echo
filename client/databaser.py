from typing import Any, Tuple
import sqlite3

class Database(object):
    def __init__(self, database: str, table: str) -> None:
        self.table = table
        
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        
    def add_contact(self, user_id: str) -> None:
        self.cursor.execute(
            f"INSERT INTO {self.table} VALUES ?",
            (user_id, )
        )
        self.db.commit()
        
    def get_data(self) -> Tuple[Any]:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()
    
