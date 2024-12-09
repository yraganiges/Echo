from tkinter import (
    Tk, #main
    CENTER,  #positions
    Label #ui
)

from ui_components.Buttons import Default_Button, Rounded_Button
from ui_components.Entry import GameDes_Entry
from ui_components.Labels import Top_Field, Text

from config import ui_config
from PIL import Image, ImageTk

class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("450x600")
        self.root.configure(bg = ui_config["window_color"])
        self.root.resizable(0, 0)
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
    def build(self) -> None:
        self.top_field = Top_Field(
            window = self.root,
            text = ui_config["title"]
        ).get()
        self.top_field.place(relx = 0.06, rely = 0.01, anchor = CENTER)
        
        image = Image.open("client\\ui_components\\RoundedLabel.png")
        image = image.resize((380, 500))
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
            text = f"Добро пожаловать в {ui_config['title']}!",
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
        self.entry_mail.show(relx = 0.5, rely = 0.3, anchor = CENTER)
        
        #password
        self.entry_password = GameDes_Entry(
            self.root,
            text = "Пароль:",
            bg_2 = "gray7"
        )
        self.entry_password.show(relx = 0.5, rely = 0.55, anchor = CENTER)
        
        #button registation
        self.btn_enter_account = Default_Button(
            self.root,
            text = "Войти в аккаунт"
        ).get()
        self.btn_enter_account.place(relx = 0.5, rely = 0.75, anchor = CENTER)
        
        #text_sign_up
        self.txt_sign_up = Label(
            self.root,
            text = "Нет аккаунта? Тогда зарегистрируйтесь",
            bg = "gray9", fg = "#b6b6b8",
            font = (
                ui_config["fonts"][2],
                10,
                "underline"
            )
        )
        self.txt_sign_up.place(relx = 0.5, rely = 0.85, anchor = CENTER)
        self.txt_sign_up.bind(
            "<Enter>", lambda event: self.txt_sign_up.configure(fg = "#6d8ae3")
        )
        self.txt_sign_up.bind(
            "<Leave>", lambda event: self.txt_sign_up.configure(fg = "#b6b6b8")
        )
        
    def main(self) -> None:
        self.build()
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()
