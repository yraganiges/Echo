from tkinter import Toplevel, CENTER, Label, Tk
from time import sleep

from ui_components.Entry import GameDes_Entry
from ui_components.Buttons import Rounded_Button
from config import ui_config, app_config, paths_config
from client_requests import Client

import main

class App(Tk):
    def __init__(self, self_id: str) -> None:
        super().__init__()
        self.title("Добавить пользователя")
        self.geometry("550x300")
        self.configure(bg = ui_config["window_color"])
        self.protocol("WM_DELETE_WINDOW", self.on_closing_window) 
        self.resizable(1, 1)
        
        self.client = Client(app_config["IP"], app_config["Port"])
        
        self.self_id = self_id
        
        self.main_app = main.App(self.self_id)
        self.main_app.close_main_window()
    
        try: self.iconbitmap(paths_config["icon"])
        except: pass
        
    def on_closing_window(self) -> None:
        self.destroy()
        self.main_app.main()
        
    def add_contact(self) -> bool:
        try: self.txt_add_status.destroy()
        except: pass
        
        user_id = self.entr_user_id.get().get().strip()
        
        if self.client.get_data_user(user_id)[0:4] == "<er>":
            self.txt_add_contact_status = f"Пользователь c id <{user_id}> не найден!",
            self.txt_add_contact_status = self.txt_add_contact_status[0]
        else:
            self.txt_add_contact_status = "Пользователь добавлен в контакты"
            
        self.txt_add_status = Label(
            self,
            text = self.txt_add_contact_status,
            bg = ui_config["window_color"], fg = "red" if self.txt_add_contact_status[-1] == "!" else "green",
            font = (
                ui_config["fonts"][0],
                12
            )
        )
        self.txt_add_status.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        
        sleep(1)
        
        if self.txt_add_contact_status[-1] != "!":
            self.client.add_contact(self.self_id, user_id) #добавляем контакт у себя
            self.client.add_contact(user_id, self.self_id) #добавляем наш контанк у собеседника
            self.destroy()
            
            self.main_app = main.App(self.self_id)
            try: self.main_app.close_main_window()
            except: pass
            self.main_app.main()
            
        
    def build(self) -> None:
        #поле с названием
        self.title_label = Label(
            self,
            text = ui_config["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        )
        self.title_label.place(relx = 0.05, rely = 0.02, anchor = CENTER)
        
        #ввод никнейма
        self.entr_user_id = GameDes_Entry(
            window = self,
            text = "Введите ID пользователя",
            width = 60,
        )
        
        self.entr_user_id.show(relx = 0.5, rely = 0.4)
        self.entr_user_id.get().place(relx = 0.47, rely = 0.34, anchor = CENTER)
        
        #кнопк добавить контакт
        self.btn_add_contact = Rounded_Button(
            self,
            text = "Добавить контакт",
            bg = ui_config["main_color"], fg = "white", back_color = ui_config["window_color"],
            command_func = lambda event: self.add_contact(),
            radius = 10,
            size = 10, height = 40, width = 180
        )
        self.btn_add_contact.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    
    def main(self) -> None:
        self.build()
        self.mainloop()
        
if __name__ == "__main__":
    App().main()