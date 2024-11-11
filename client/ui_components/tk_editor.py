from tkinter import Entry, END
from typing import Any

def clear_entry_field(body: Entry, text: str) -> None:
    if body.get().lower().strip() == text.lower():
        body.delete(0, END) #clear text
        
def show_entry_text(body: Entry, text: str) -> None:
    if body.get().lower().strip() == "":
        body.delete(0, END)
        body.insert(0, text)
        
    