from tkinter import Tk, CENTER, Label, Button, Entry 
from ui_components.Labels import Top_Field

from PIL import Image, ImageTk

from config import ui_config, app_config
from client_requests import Client
from databaser import Database

from threading import Thread


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
        
        self.images = []
        self.added_users = []
        self.x, self.y = 0.13, 0.1
        
    def contacts_handler(self) -> None:
        for index in self.users_db.get_data():
            user_data = self.client.get_data_user(index[0])
            print(user_data)

            avatar_path = f"client\\user_avatars\\{user_data[1]}.png"
            print(f"Loading avatar from: {avatar_path}")  # Отладочная информация

            if user_data[1] not in self.added_users:        
                try:
                    image_ui = Image.open("client\\ui_components\\RoundedLabel_2.png")
                    image_ui = image_ui.resize((245, 70), Image.ANTIALIAS)  # Увеличение размера для теста
                    self.rounded_label = ImageTk.PhotoImage(image_ui)
                    self.images.append(self.rounded_label)
                    
                    #поле с данными контакта
                    self.lbl = Label(
                        self.root,
                        text = user_data[1],
                        bg="#1e1f1e", fg="white",
                        image=self.rounded_label,
                        font=(ui_config["fonts"][0], 10)
                    )
                    self.lbl.place(relx=self.x, rely=self.y, anchor=CENTER)
                    
                    self.txt_data_contact = Label(
                        self.root,
                        bg="#171717", fg="white",
                        anchor="w",
                        font=(ui_config["fonts"][0], 10),
                        text=user_data[0]  # Убрали лишние пробелы
                    )
                    self.txt_data_contact.place(relx=self.x - 0.03, rely=self.y - 0.01, anchor="w")  # Убедитесь, что anchor также установлен на "w"

                    #TODO добавить последнее сообщение из чата
                    self.txt_last_message = Label(
                        self.root,
                        text = "    last message...", 
                        bg = "#171717", fg = "gray30",
                        font=(ui_config["fonts"][0], 8, "italic")
                    )
                    self.txt_last_message.place(relx = self.x - 0.01, rely = self.y + 0.017, anchor = CENTER)

                    self.lbl.bind("<Enter>", lambda event: event.widget.configure(bg="gray10"))
                    self.lbl.bind("<Leave>", lambda event: event.widget.configure(bg="#1e1f1e"))
                    self.lbl.bind(
                        "<Button - 1>", lambda event: self.open_chat_user(event.widget["text"])
                    )
                    
                    image = Image.open(avatar_path)
                    image = image.resize((40, 40), Image.ANTIALIAS)  # Увеличение размера для теста
                    self.avatar = ImageTk.PhotoImage(image)
                    self.images.append(self.avatar)

                    avatar_label = Label(
                        self.root,
                        image=self.avatar,
                        bg = "gray8"
                    )
                    avatar_label.place(relx=self.x - 0.05, rely=self.y, anchor=CENTER)
                    
                    self.y += 0.08
                    self.added_users.append(user_data[1])

                except Exception as e:
                    print(f"Error loading image {avatar_path}: {e}")
                
    def open_chat_user(self, user_id: str) -> None:
        print(self.users_db.get_data_chat(user_id))
        try: self.entry_message.destroy()
        except: pass
        
        self.entry_message = Entry
   
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
