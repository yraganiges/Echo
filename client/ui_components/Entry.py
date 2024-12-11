from typing import Any
from tkinter import Entry, Label, CENTER

if __name__ == "__main__":
    from tk_editor import show_entry_text, clear_entry_field
else:
    from ui_components.tk_editor import show_entry_text, clear_entry_field
#from ui_components.tk_editor import show_entry_text, clear_entry_field

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
        
class GameDes_Entry:
    def __init__(
        self,
        window: Any,
        width: int = 40,
        height: int = 5,
        size_line: int = 1,
        bg_1: str = "gray12",
        bg_2: str = "gray9",
        fg: str = "#a79eb5",
        color_line: str = "#2c0661",
        border: int = 0,
        text: str = "entry text...",
        font: str = "Cascadia Mono SemiBold",
        size: int = 15,
    ) -> Entry:
        
        self.foreground_field = Label(
            window,
            width = width,
            height = height,
            bg = bg_2,
        )
        
        self.background_field = Label(
            window,
            width = width,
            height = height,
            bg = bg_1    
        )
        
        self.lbl = Label(window, bg = color_line, width = width * 6, font = ("", size_line))
        
        self.gamedes_entry = Entry(
            window,
            width = width // 2, bd = border,
            bg = bg_1, fg = fg,
            font = (
                font,
                size
            )
        )
        self.gamedes_entry.insert(0, text)
        self.gamedes_entry.bind("<Enter>", lambda event: clear_entry_field(
            body = self.gamedes_entry, text = text
        ))
        self.gamedes_entry.bind("<Leave>", lambda event: (
            show_entry_text(body = self.gamedes_entry, text = text)
        ))
        
        self.entry_text = text
        
    def get(self) -> Entry:
        return self.gamedes_entry
    
    def get_entry_text(self) -> str:
        return self.entry_text
        
    def show(
        self,
        relx: float = 0.0,
        rely: float = 0.0,
        pos_x_line: float = 0.1, 
        anchor: Any = CENTER
    ) -> None:
        self.gamedes_entry.place(relx = relx - 0.01, rely = rely - 0.04, anchor = anchor)
        self.background_field.place(relx = relx, rely = rely, anchor = anchor)
        self.foreground_field.place(relx = relx + 0.05, rely = rely + 0.05, anchor = anchor)
        self.lbl.place(relx = pos_x_line, rely = rely - 0.01)
        
if __name__ == "__main__":
    from tkinter import Tk
    
    root = Tk()
    root.geometry("400x500")
    root.config(bg = "gray7")
    
    # entry_1 = Default_Entry(window = root)
    # entry_1.show(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    # entry_2 = Left_Entry(window = root)
    # entry_2.show(relx = 0.5, rely = 0.7, anchor = CENTER)
    
    entry_3 = GameDes_Entry(window = root, text = "Email:")
    entry_3.show(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    root.mainloop()
        

        