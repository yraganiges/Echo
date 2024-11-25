from typing import Any
from tkinter import Entry, Label, CENTER
from ui_components.tk_editor import show_entry_text, clear_entry_field

class Default_Entry:
    def __init__(
        self,
        window: Any,
        width: int = 28,
        justify: Any = CENTER,
        width_line: int = 332,
        size_line: int = 1,
        bg: str = "gray7",
        fg: str = "white",
        color_line: str = "#2c0661",
        border: int = 0,
        text: str = "entry text...",
        font: str = "Cascadia Mono Light",
        size: int = 15,
    ) -> Entry:
        
        self.default_entry = Entry(
            window,
            justify = justify,
            width = width, bd = border,
            bg = bg, fg = fg,
            font = (
                font,
                size
            )
        )
        self.default_entry.insert(0, text)
        self.default_entry.bind("<Enter>", lambda event: clear_entry_field(
            body = self.default_entry, text = text
        ))
        self.default_entry.bind("<Leave>", lambda event: (
            show_entry_text(body = self.default_entry, text = text)
        ))

        self.lbl = Label(window, bg = color_line, width = width_line, font = ("", size_line))
        
    def get(self) -> Entry:
        return self.default_entry        
        
    def show(self, relx: float = 0.0, rely: float = 0.0, anchor: Any = CENTER) -> None:
        self.default_entry.place(relx = relx, rely = rely, anchor = anchor)
        self.lbl.place(relx = relx, rely = rely + 0.03, anchor = anchor)
        
class Left_Entry:
    def __init__(
        self,
        window: Any,
        width: int = 28,
        width_line: int = 303,
        size_line: int = 1,
        bg: str = "gray7",
        fg: str = "white",
        color_line: str = "#2c0661",
        border: int = 0,
        text: str = "entry text...",
        font: str = "Candara Light",
        size: int = 15,
    ) -> Entry:
        
        #lbl
        self.lbl = Label(window, bg = color_line, width = width_line, font = ("", size_line))
        
        #entry
        self.left_entry = Entry(
            window,
            width = width, bd = border,
            bg = bg, fg = fg,
            font = (
                font,
                size
            )
        )
        self.left_entry.insert(0, text)
        self.left_entry.bind("<Enter>", lambda event: clear_entry_field(
            body = self.left_entry, text = text
        ))
        self.left_entry.bind("<Leave>", lambda event: (
            show_entry_text(body = self.left_entry, text = text)
        ))
        
    def get(self) -> Entry:
        return self.left_entry
                
    def show(self, relx: float = 0.0, rely: float = 0.0, anchor: Any = CENTER) -> None:
        self.left_entry.place(relx = relx, rely = rely, anchor = anchor)
        self.lbl.place(relx = relx, rely = rely + 0.03, anchor = anchor)
        
if __name__ == "__main__":
    from tkinter import Tk
    
    root = Tk()
    root.geometry("400x500")
    root.config(bg = "gray7")
    
    entry_1 = Default_Entry(window = root)
    entry_1.show(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    entry_2 = Left_Entry(window = root)
    entry_2.show(relx = 0.5, rely = 0.7, anchor = CENTER)
    
    root.mainloop()
        

        