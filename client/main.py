from tkinter import Tk, CENTER, Label, Button
from config import j

class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(j["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg = j["window_color"])
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
    def build(self) -> None:
        Label(
            self.root,
            text = j["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        ).place(relx = 0.018, rely = 0.01, anchor = CENTER)
        
    def main(self) -> None:
        self.build()
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()
