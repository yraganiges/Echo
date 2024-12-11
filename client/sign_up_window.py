from tkinter import (
    Tk, #main
    CENTER,  #positions
    Label #ui
)

from ui_components.Buttons import Default_Button, Rounded_Button
from ui_components.Entry import GameDes_Entry
from ui_components.Labels import Top_Field, Text

from config import ui_config, app_config
from PIL import Image, ImageTk

from client_requests import Client

class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("900x600")
        self.root.configure(bg = ui_config["window_color"])
        self.root.resizable(1, 1)
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
    def push_button_create_account(self) -> None:
        if (
            (self.entry_mail.get().get().strip() != self.entry_mail.get_entry_text()) or
            (len(self.entry_mail.get().get()) > 3) 
            and
            (self.entry_password.get().get().strip() != self.entry_password.get_entry_text()) or
            (len(self.entry_password.get().get()) > 3)
            and
            (self.entry_nickname.get().get().strip() != self.entry_nickname.get_entry_text()) or
            (len(self.entry_nickname.get().get()) > 3)
        ):
            client = Client(IP = app_config["IP"], port = app_config["Port"])
            client.connect_to_server() #Сделать подключение пользователя(передать его данные)
            
    def build(self) -> None:
        self.top_field = Top_Field(
            window = self.root,
            text = ui_config["title"]
        ).get()
        self.top_field.place(relx = 0.03, rely = 0.01, anchor = CENTER)
        
        image = Image.open("client\\ui_components\\RoundedLabel.png")
        image = image.resize((760, 500))
        self.photo = ImageTk.PhotoImage(image)
        
        #field
        self.field = Label(
            self.root,
            image = self.photo,
            bg = ui_config["window_color"]
        ).place(relx = 0.5, rely = 0.5, anchor = CENTER)
        
        #welcome text
        self.welcome_text = Text(
            self.root,
            text = f"Создайте аккаунт в {ui_config['title']}!",
            bg = "gray9",
            size = 16
        ).get()
        self.welcome_text.place(relx = 0.5, rely = 0.17, anchor = CENTER)
        
        #mail
        self.entry_mail = GameDes_Entry(
            self.root,
            text = "Почта:",
            bg_2 = "gray7"
        )
        self.entry_mail.show(relx = 0.3, rely = 0.33, anchor = CENTER)
        
        #password
        self.entry_password = GameDes_Entry(
            self.root,
            text = "Пароль:",
            bg_2 = "gray7"
        )
        self.entry_password.show(relx = 0.3, rely = 0.57, anchor = CENTER)
        
        #nickname
        self.entry_nickname = GameDes_Entry(
            self.root,
            text = "Никнейм:",
            bg_2 = "gray7"
        )
        self.entry_nickname.show(relx = 0.7, rely = 0.45, pos_x_line = 0.5,anchor = CENTER)
        
        #button registation
        self.btn_enter_account = Default_Button(
            self.root,
            text = "Создать аккаунт"
        ).get()
        self.btn_enter_account.place(relx = 0.5, rely = 0.8, anchor = CENTER)
        
        #text_sign_up
        self.txt_sign_up = Label(
            self.root,
            text = "Назад, к окну авторизации",
            bg = "gray9", fg = "#b6b6b8",
            font = (
                ui_config["fonts"][2],
                10,
                "underline"
            )
        )
        self.txt_sign_up.place(relx = 0.5, rely = 0.87, anchor = CENTER)
        self.txt_sign_up.bind(
            "<Enter>", lambda event: self.txt_sign_up.configure(fg = "#f03043")
        )
        self.txt_sign_up.bind(
            "<Leave>", lambda event: self.txt_sign_up.configure(fg = "#b6b6b8")
        )
        
    def main(self) -> None:
        self.build()
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()
