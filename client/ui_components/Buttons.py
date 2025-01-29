from typing import Any
from tkinter import Button, Canvas
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
        
class Rounded_Button(Canvas):
    def __init__(
        self,
        master = None,
        text: str = "button",
        command: Any = None,
        radius: int = 10,
        width: int = 150,
        height: int = 80,
        bg: str = "#2c0661",
        fg: str = "white",
        font: str = "Cascadia Mono SemiBold",
        size: int = 12,
        back_color: str = None,
        command_func: Any = None,
        **kwargs
    ) -> None:
        super().__init__(master, **kwargs)
        self.command = command
        self.text = text
        self.radius = radius 
        self.bg = bg
        
        # Убираем рамки и устанавливаем фон
        self.config(
            bg=self.master.cget('bg') if back_color == None else back_color,
            highlightthickness=0,
            width = width,
            height = height
        )  
        
        self.create_rounded_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(), self.radius)
        self.create_text(self.winfo_reqwidth()/2, self.winfo_reqheight()/2, text=text, fill=fg, font = (font, size))
        
        if command_func != None:
            self.bind("<Button - 1>", command_func)
        
    def create_rounded_rectangle(self, x1, y1, x2, y2, r) -> None:
        """Создание закругленного прямоугольника."""
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=self.bg, outline="")
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=self.bg, outline="")
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=self.bg, outline="")
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=self.bg, outline="")
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=self.bg, outline="")
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=self.bg, outline="")
        
if __name__ == "__main__":
    from tkinter import Tk, CENTER
    
    root = Tk()
    root.geometry("400x500")
    root.config(bg = "gray7")
    
    btn_1 = Default_Button(window = root, size = 9).get()
    btn_1.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    btn_2 = Rounded_Button(root)
    btn_2.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    
    root.mainloop()
    

        