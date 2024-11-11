from typing import Any, Tuple
import sqlite3

class Database(object):
    def __init__(self, database: str, table: str) -> None:
        self.table = table
        
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        
    # def add
        
    def get_data(self) -> Tuple[Any]:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()
    
