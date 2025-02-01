from tkinter import Tk, CENTER, LEFT, END, Label, Button, Entry, scrolledtext
from ui_components.Labels import Top_Field
from ui_components.Entry import Default_Entry
from ui_components.Buttons import Rounded_Button

from PIL import Image, ImageTk
from datetime import datetime
from random import choice
from typing import List

from config import ui_config, app_config
from client_requests import Client
from databaser import Database
from handlers import make_indents

import os


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
        self.labels = []
        self.x, self.y = 0.13, 0.1
        
    def hidden_contacts(self) -> None:
        for label in self.labels:
            label.destroy() 
        self.labels.clear()

        self.added_users.clear()
        
    def contacts_handler(self) -> None:
        for index in self.client.get_data_contacts(self_id = self.self_user_id):
            user_data = self.client.get_data_user(index[0])
            print(user_data)

            avatar_path = f"client\\user_avatars\\{user_data[1]}.png"
            
            #проверка существования аватара в директории
            # if not os.path.exists(avatar_path):
            try: os.remove(avatar_path)
            except: pass
            self.client.get_user_avatar(user_id = user_data[1])
            
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
                        "<Button - 1>", lambda event: (
                            self.open_chat_user(event.widget["text"]),
                            self.load_right_part(event.widget["text"])
                        )
                    )
                    
                    image = None
                    
                    #Открываем директорию с аватарами
                    try:
                        image = Image.open(avatar_path)
                        image = image.resize((40, 40), Image.ANTIALIAS)  # Увеличение размера для теста
                        self.avatar = ImageTk.PhotoImage(image)
                        self.images.append(self.avatar)
                    except:
                        pass

                    self.avatar_label = Label(
                        self.root,
                        image=self.avatar if image is not None else "",
                        bg = "gray8"
                    )
                    self.avatar_label.place(relx=self.x - 0.05, rely=self.y, anchor=CENTER)
                    
                    self.y += 0.08
                    self.added_users.append(user_data[1])
                    self.labels.append(self.lbl)
                    self.labels.append(self.txt_last_message)
                    self.labels.append(self.txt_data_contact)
                    self.labels.append(self.avatar_label)

                except Exception as e:
                    print(f"Error loading image {avatar_path}: {e}")
    
    #правая часть
    def load_right_part(self, user_id: str) -> None:
        user_data = self.client.get_data_user(user_id)
        colors = ["#120909", "#0e0b14", "#211a24", "#241f1f"]
        
        #аватар пользователя
        try:
            img_logo = Image.open(f"client\\user_avatars\\{user_data[1]}.png")
            img_logo = img_logo.resize((120, 120), Image.ANTIALIAS) 
            self.img_logo = ImageTk.PhotoImage(img_logo)
        except:
            pass
        
        self.lbl_right_path = Label(
            self.root,
            width = 80,
            height = 100,
            bg = "gray9"
        )
        self.lbl_right_path.place(relx = 0.955, rely = 0.5, anchor = CENTER)
        
        self.lbl_backgroud_avatar = Label(
            self.root,
            width = 80,
            height = 12,
            bg = "#262425" #choice(colors)    
        )
        self.lbl_backgroud_avatar.place(relx = 0.955, rely = 0.1, anchor = CENTER)
        
        self.title_label.lift()
        
        #аватар
        self.avatar_label = Label(
            self.root,
            image = self.img_logo, 
        )
        self.avatar_label.place(relx = 0.89, rely = 0.18, anchor = CENTER)
        
        #никнейм
        self.txt_nickname_rp = Label(
            self.root,
            text = user_data[0], #nickname
            bg = "gray9", fg = "white",
            font = (
                ui_config["fonts"][0],
                20
            )
        )
        self.txt_nickname_rp.place(relx = 0.89, rely = 0.28, anchor = CENTER)
        
        #buttons control user
        self.btn_call = Rounded_Button(
            self.root,
            width = 70, height = 60,
            radius = 10,
            bg = "#14a859", fg = "gray9",
            image_path = "client\\ui_components\\call.png",
            image_size = (60, 50)
        )
        self.btn_call.place(relx = 0.83, rely = 0.35, anchor = CENTER)
        
        self.btn_blocked = Rounded_Button(
            self.root,
            width = 70, height = 60,
            radius = 10,
            bg = "red", fg = "gray9",
            image_path = "client\\ui_components\\blocked.png",
            image_size = (55, 45)
        )
        self.btn_blocked.place(relx = 0.89, rely = 0.35, anchor = CENTER)
        
        self.btn_complain = Rounded_Button(
            self.root,
            width = 70, height = 60,
            radius = 10,
            bg = "#8c3e01", fg = "gray9",
            image_path = "client\\ui_components\\complain.png",
            image_size = (55, 45)
        )
        self.btn_complain.place(relx = 0.95, rely = 0.35, anchor = CENTER)
        
        #описание
        self.txt_description = Label(
            self.root,
            text = "Описание:",
            bg = "gray9", fg = "white",
            font = (
            ui_config["fonts"][0],
                16
            )
        )
        self.txt_description.place(relx = 0.828, rely = 0.44, anchor = CENTER)
        
        self.user_description = Label(
            self.root,
            text = make_indents(user_data[8]) if user_data[8] != "None" else "Описание отсуствует...",
            bg = "gray9", fg = "#a3a3a3",
            font = (
            ui_config["fonts"][0],
                10
            )
        )
        self.user_description.place(relx = 0.85, rely = 0.47, anchor = CENTER)
            
            
    def open_chat_user(self, user_id: str) -> None:
        chat_data = self.client.get_chat(self.self_user_id, user_id)
        
        try:
            self.entry_message.destroy()
            self.btn_send_message.destroy()
            self.chat_display.destroy()
            self.txt_not_chat.destroy()
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
                
                self.chat_display.insert(
                    END, info,
                    "you" if index[3] == self.self_user_id else "interlocutor"
                )
                
            self.chat_display.tag_config("you", foreground = "#b5ace8")
            self.chat_display.tag_config("interlocutor", foreground = "#c1ace8")
        else:
            self.txt_not_chat = Label(
                self.root,
                text = "У вас нету переписки с данным контактом, но\nвы можете её начать первым😀",
                bg = "gray7", fg = "#4a4061",
                font = (
                    ui_config["fonts"][0],
                    20
                )
            )
            self.txt_not_chat.place(relx = 0.48, rely = 0.5, anchor = CENTER)
    
        self.entry_message = Default_Entry(
            self.root,
            text = "Введите сообщение...",
            justify = LEFT,
            bg = "gray18",
            fg = "#c0bcf7", # > gray32
            width = 80,
            font = ui_config["fonts"][0],
            size = 13
        ).get()
        self.entry_message.place(relx = 0.48, rely = 0.95, anchor = CENTER)
        
        img_send_message = Image.open("client\\ui_components\\send_message.png")
        img_send_message = img_send_message.resize((30, 30), Image.ANTIALIAS)
        self.img_send_message = ImageTk.PhotoImage(img_send_message)
        # self.images.append(self.avatar)
        
        #кнопка отправить сообщение
        self.btn_send_message = Button(
            self.root,
            image = self.img_send_message,
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
        self.chat_display.insert(
            END, 
            f"<{now_time}>\nВы: {message}\n\n",
            "you",
        ) #добавляем сообщение в чат дисплей
        
        #удаляем текст о начале переписки, если оно имелось
        try: self.txt_not_chat.destroy() 
        except: pass
    
    def build(self) -> None:
        self.title_label = Label(
            self.root,
            text = ui_config["title"],
            bg = "gray12", fg = "#a3a0a0",
            width = 500, height = 1,
            font = ("Arial Black", 8)
        )
        self.title_label.place(relx = 0.018, rely = 0.01, anchor = CENTER)
        
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
        
        #кнопка управления
        img_control = Image.open("client\\ui_components\\setting.png")
        img_control = img_control.resize((60, 60), Image.ANTIALIAS)  # Увеличение размера для теста
        self.control_ui = ImageTk.PhotoImage(img_control)
        
        self.btn_control = Button(
            self.root,
            image = self.control_ui,
            bg = "gray5", bd = 0,
            command = self.hidden_contacts
        )
        self.btn_control.place(relx = 0.027, rely = 0.075, anchor = CENTER)
        
        self.btn_control.bind("<Enter>", lambda event: event.widget.configure(bg = "gray9"))
        self.btn_control.bind("<Leave>", lambda event: event.widget.configure(bg = "gray5"))
        
    def main(self) -> None:
        self.build()
        self.contacts_handler()
        self.root.mainloop()
        
if __name__ == "__main__": 
    App("dzyg0n546z58854o").main()
