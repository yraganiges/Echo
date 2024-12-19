from tkinter import Tk, CENTER, Label, Button
from ui_components.Labels import Top_Field
from config import ui_config

class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg = ui_config["window_color"])
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
    def build(self) -> None:
        Label(
            self.root,
            text = ui_config["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        ).place(relx = 0.018, rely = 0.01, anchor = CENTER)
        
        #users field
        Label(
            self.root,
            width = 50,
            height = 200,
            bg = "#1e1f1e"
        ).place(relx = 0.16, rely = 0.5, anchor = CENTER)
        
        #channels field
        Label(
            self.root,
            width = 12,
            height = 200,
            bg = "gray5"
        ).place(relx = 0.025, rely = 0.5, anchor = CENTER)
        
        top_field = Top_Field(
            self.root,
            text = ui_config["title"]
        ).get().place(relx = 0.02, rely = 0.01, anchor = CENTER)
        
    def main(self) -> None:
        self.build()
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()
