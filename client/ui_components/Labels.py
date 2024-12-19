from typing import Any
from tkinter import Label

class Text:
    def __init__(
        self,
        window: Any,
        text: str = "text",
        bg: str = "gray7",
        fg: str = "white",
        font: str = "Cascadia Mono SemiBold",
        size: int = 20,
    ):
        self.text = Label(
            window,
            text = text,
            bg = bg, fg = fg,
            font = (
                font,
                size
            )
        )
        
    def get(self) -> Label:
        return self.text
    
class Top_Field:
    def __init__(
        self,
        window: Any,
        text: str = "top_field",
        bg: str = "gray12",
        fg: str = "#a3a0a0",
        font: str = "Arial Black",
        width: int = 500,
        height: int = 1,
        size: int = 8
    ):
        self.top_field = Label(
            window,
            text = text,
            bg = bg, fg = fg,
            width = width, height = height,
            font = (font, size)
        )
    
    def get(self) -> Label:
        return self.top_field
    
if __name__ == "__main__":
    from tkinter import Tk, CENTER
    
    root = Tk()
    root.geometry("400x500")
    root.config(bg = "gray7")
    
    txt_1 = Text(window = root).get()
    txt_1.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    root.mainloop()