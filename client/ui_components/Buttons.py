from typing import Any
from tkinter import Button, Label
from PIL import Image, ImageTk

class Default_Button:
    def __init__(
        self,
        window: Any,
        width: int = 18,
        height: int = 2,
        bg: str = "#2c0661",
        enter_cursor_color: str = "#360c96",
        fg: str = "white",
        border: int = 0,
        text: str = "Button",
        font: str = "Cascadia Mono SemiBold",
        size: int = 12,
        command_func: Any = None
    ) -> Button:
        
        self.default_button = Button(
            window,
            text = text,
            width = width, height = height, bd = border,
            bg = bg, fg = fg,
            font = (
                font,
                size
            ),
            command = command_func if command_func != None else ...
        )
        
        self.default_button.bind(
            "<Enter>", lambda event: self.default_button.configure(bg = enter_cursor_color)
        )
        self.default_button.bind(
            "<Leave>", lambda event: self.default_button.configure(
                bg = bg
            )
        )
        
    def get(self) -> Button:
        return self.default_button
        
class Rounded_Button:
    def __init__(
        self,
        window: Any,
        width: int = 200,
        height: int = 200,
        fg: str = "gray7",
        text: str = "Button",
        font: str = "Cascadia Mono SemiBold",
        command_func: Any = None
    ) -> None:
        
        self.image = Image.open("client\\ui_components\\RoundedButton_2.png")
        self.image = self.image.resize((width, height))
        self.photo = ImageTk.PhotoImage(self.image) 
        
        self.rounded_button = Label(
            window,
            image = self.photo,
            text = text,
            fg = fg
        )
        if command_func != None:
            self.rounded_button.bind("<Button - 1>", command_func)
            
    def get(self) -> Button:
        return self.rounded_button
        
if __name__ == "__main__":
    from tkinter import Tk, CENTER
    
    root = Tk()
    root.geometry("400x500")
    root.config(bg = "gray7")
    
    btn_1 = Default_Button(window = root, size = 9).get()
    btn_1.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    btn_2 = Rounded_Button(window = root).get()
    btn_2.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    root.mainloop()
    

        