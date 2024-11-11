from tkinter import (
    Tk, #main
    CENTER,  #positions
    Label, Button, Entry #ui
)
from ui_components.tk_editor import (
    clear_entry_field,
    show_entry_text
)
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
        self.top_field = Label(
            self.root,
            text = ui_config["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        ).place(relx = 0.06, rely = 0.01, anchor = CENTER)
        
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
        self.welcome_text = Label(
            self.root,
            text = f"Добро пожаловать в {ui_config['title']}!",
            bg = "gray9",
            fg = ui_config["fg_color"],
            font = (
                ui_config["fonts"][0],
                16
            )
        ).place(relx = 0.5, rely = 0.17, anchor = CENTER)
        
        #mail
        self.entry_mail = Entry(
            self.root,
            justify = CENTER,
            bg = ui_config["window_color"], fg = ui_config["fg_color"],
            bd = 0,
            width = 28,
            font = (ui_config["fonts"][2], 15)
        )
        self.entry_mail.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        self.entry_mail.insert(0, "Почта")
        self.entry_mail.bind("<Enter>", lambda event: clear_entry_field(
            body = self.entry_mail, text = "Почта"
        ))
        self.entry_mail.bind("<Leave>", lambda event: (
            show_entry_text(body = self.entry_mail, text = "Почта")
        ))

        self.lbl = Label(self.root, bg = ui_config["main_color"], width = 332, font = ("", 1))
        self.lbl.place(relx = 0.5, rely = 0.33, anchor = CENTER)
        
        #password
        self.entry_password = Entry(
            self.root,
            justify = CENTER,
            bg = ui_config["window_color"], fg = ui_config["fg_color"],
            bd = 0,
            width = 28,
            font = (ui_config["fonts"][2], 15)
        )
        self.entry_password.place(relx = 0.5, rely = 0.45, anchor = CENTER)
        self.entry_password.insert(0, "Пароль")
        self.entry_password.bind("<Enter>", lambda event: clear_entry_field(
            body = self.entry_password, text = "Пароль"
        ))
        self.entry_password.bind("<Leave>", lambda event: (
            show_entry_text(body = self.entry_password, text = "Пароль")
        ))

        self.lbl = Label(self.root, bg = ui_config["main_color"], width = 332, font = ("", 1))
        self.lbl.place(relx = 0.5, rely = 0.48, anchor = CENTER)
        
        #button registation
        self.btn_enter_account = Button(
            self.root,
            text = "Войти в аккаунт",
            width = 18, height = 2, bd = 0,
            bg = ui_config["main_color"], fg = ui_config["fg_color"],
            font = (
                ui_config["fonts"][0],
                12
            ),
            command = ...
        )
        self.btn_enter_account.place(relx = 0.5, rely = 0.7, anchor = CENTER)
        self.btn_enter_account.bind(
            "<Enter>", lambda event: self.btn_enter_account.configure(bg = "#360c96")
        )
        self.btn_enter_account.bind(
            "<Leave>", lambda event: self.btn_enter_account.configure(
                bg = ui_config["main_color"]
            )
        )
        
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
