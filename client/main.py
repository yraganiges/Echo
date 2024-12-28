from tkinter import Tk, CENTER, Label, Button, RIGHT
from ui_components.Labels import Top_Field

from PIL import Image, ImageTk

from config import ui_config, app_config
from client_requests import Client
from databaser import Database


class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg = ui_config["window_color"])
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
        self.client = Client(IP = app_config["IP"], port = app_config["Port"])
        self.users_db = Database("client\\data\\contacts.db", "users")
        
    def contacts_handler(self) -> None:
        x, y = 0.13, 0.1
        for index in self.users_db.get_data():
            user_data = self.client.get_data_user(index[0])
            print(user_data)
            
            #TODO add avatar
            image = Image.open(f"client\\avatars\\{user_data[1]}.png")
            image = image.resize((380, 500))
            self.photo = ImageTk.PhotoImage(image)
            
            self.avatar = Label(
                self.root,
                image = self.photo
            ).place(relx = x - 0.03, rely = y, anchor = CENTER)
            
            self.lbl = Label(
                self.root,
                text = "        " + user_data[0], anchor = "w",
                width = 29, height = 2,
                bg = "gray8", fg = "white",
                font = (ui_config["fonts"][0], 10)
            )
            self.lbl.place(relx = x, rely = y, anchor = CENTER)
            self.lbl.bind("<Enter>", lambda event: event.widget.configure(bg = "gray10"))
            self.lbl.bind("<Leave>", lambda event: event.widget.configure(bg = "gray8"))
            
            y += 0.047
        
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
            width = 40,
            height = 200,
            bg = "#1e1f1e"
        ).place(relx = 0.12, rely = 0.5, anchor = CENTER)
        
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
        self.contacts_handler()
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()
