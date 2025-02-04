from tkinter import (
    Toplevel,
    CENTER,
    Label
)

from config import ui_config, paths_config

class App(Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.title(ui_config["title"] + " - Настройки")
        self.geometry("1200x800")
        self.configure(bg = ui_config["window_color"])
        self.resizable(1, 1)
    
        try: self.iconbitmap(paths_config["icon"])
        except: pass
        
    def build(self) -> None:
        self.title_label = Label(
            self,
            text = ui_config["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        )
        self.title_label.place(relx = 0.018, rely = 0.01, anchor = CENTER)
    
    def main(self) -> None:
        self.build()
        self.mainloop()
        
if __name__ == "__main__":
    App().main()