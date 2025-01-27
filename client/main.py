from tkinter import Tk, CENTER, LEFT, END, Label, Button, Entry, scrolledtext
from ui_components.Labels import Top_Field
from ui_components.Entry import Default_Entry

from PIL import Image, ImageTk
from datetime import datetime

from config import ui_config, app_config
from client_requests import Client
from databaser import Database

from threading import Thread


class App(object):
    def __init__(self, user_id: str) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg = ui_config["window_color"])
        
        try: self.root.iconbitmap("icons\\main_icon.ico")
        except: pass
        
        self.client = Client(IP = app_config["IP"], port = app_config["Port"])
        self.users_db = Database("client\\data\\contacts.db", "users")
        
        self.self_user_id = user_id
        
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

                    #последнее сообщение из чата
                    chat_data = self.client.get_chat(self.self_user_id, user_data[1])
                    
                    self.txt_last_message = Label(
                        self.root,
                        text = f"       {chat_data[-1][0][0:15]}..." if chat_data != None else "    last message...", 
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
        chat_data = self.client.get_chat(self.self_user_id, user_id)
        print(chat_data)
        
        try:
            self.entry_message.destroy()
            self.btn_send_message.destroy()
            self.chat_display.destroy()
        except: 
            pass
        
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            state = "normal", #disabled
            width = 100, height = 40,
            bg = "gray7", fg = "white",
            bd = 0,
            font = (
                ui_config["fonts"][0],
                12
            )
        )        
        self.chat_display.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        
        if chat_data != None:
            for index in chat_data:
                info = f"<{str(index[2])}>\n"
                if index[3] == self.self_user_id:
                    info += "Вы: "
                else:
                    info += self.client.get_data_user(index[3])[0]
                
                info += str(index[0]).strip() + "\n\n" #добавляем сообщение пользователя
                
                self.chat_display.insert(END, info)
                
                
        self.entry_message = Default_Entry(
            self.root,
            text = "Введите сообщение...",
            justify = LEFT,
            bg = "gray18",
            fg = "#8c8c8c", # > gray32
            width = 80,
            font = ui_config["fonts"][0],
            size = 13
        ).get()
        self.entry_message.place(relx = 0.48, rely = 0.95, anchor = CENTER)
        
        image = Image.open("client\\ui_components\\send_message.png")
        image = image.resize((30, 30), Image.ANTIALIAS)  # Увеличение размера для теста
        self.image = ImageTk.PhotoImage(image)
        # self.images.append(self.avatar)
        
        #кнопка отправить сообщение
        self.btn_send_message = Button(
            self.root,
            image = self.image,
            bg = "gray32", bd = 0,
            command = lambda: self.send_text_message(
                message = self.entry_message.get(),
                sender_id = self.self_user_id,
                receiver_id = user_id
            )
        )
        self.btn_send_message.place(relx = 0.75, rely = 0.95, anchor = CENTER)
        self.btn_send_message.bind(
            "<Enter>", lambda event: self.btn_send_message.configure(bg = "#595958")
        )
        self.btn_send_message.bind(
            "<Leave>", lambda event: self.btn_send_message.configure(bg = "gray32")
        )
    
    def send_text_message(self, message: str, sender_id: str, receiver_id: str) -> None:
        now_time = datetime.now().strftime("%H:%M %Y-%m-%d")
        
        if message.lower().strip() == "введите сообщение..." or message.strip() == "":
            return
        
        message_data = {
            "sender_id": sender_id,
            "message": message.strip(),
            "time_send_message": now_time,
            "to_whom_message": receiver_id
        }   

        self.client.send_message(message_data, "text")
        self.chat_display.insert(END, f"<{now_time}>\nВы: {message}\n\n") #добавляем сообщение в чат дисплей
    
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
    App("dzyg0n546z58854o").main()
