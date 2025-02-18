from tkinter import Tk, CENTER, LEFT, END, Label, Button, Entry, scrolledtext
from ui_components.Labels import Top_Field
from ui_components.Entry import Default_Entry
from ui_components.Buttons import Rounded_Button

from threading import Thread, Event
from PIL import Image, ImageTk
from datetime import datetime
from typing import List, Any
from time import sleep

from config import ui_config, app_config, paths_config
from client_requests import Client
from databaser import Database
from handlers import make_indents

import add_user
import settings

import os


class App(object):
    def __init__(self, user_id: str) -> None:
        self.root = Tk()
        self.root.title(ui_config["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg = ui_config["window_color"])
        
        try: self.root.iconbitmap(paths_config["icon"])
        except: pass
        
        self.client = Client(IP = app_config["IP"], port = app_config["Port"])
        self.users_db = Database(paths_config["contacts_db"], "users")
        
        self.stop_event = Event()
        self.self_user_id = user_id
        
        self.images = []
        self.added_users = []
        self.contact_labels = []
        self.buttons_control = []
        self.btn_control_status = False
        
        self.x, self.y = 0.13, 0.1
        
        
    def hidden_objects(self, objects: List[Any]) -> None:
        for index in objects:
            index.destroy() 
        objects.clear()
        
    def show_control_buttons(
        self,
        buttons: List[List[str | Any]],
    ) -> None:
        y = 0.08
        
        for button in buttons:
            self.btn_control_part = Rounded_Button(
                self.root,
                text = button[0],
                width = 200, height = 50,
                back_color = "gray12",
                bg = "gray9" if button[2] is None else button[2], fg = "white",
                size = 9,
                command_func = button[1]
            )
            self.btn_control_part.place(relx = 0.13, rely = y, anchor = CENTER)
            
            self.buttons_control.append(self.btn_control_part)
            y += 0.06
            
            self.btn_control.destroy()
            del self.btn_control #на всякий
            
            self.btn_control = Button(
                self.root,
                image = self.control_ui,
                bg = "gray5", bd = 0,
                command = lambda: (
                    self.hidden_objects(self.buttons_control),
                    self.contacts_handler(),
                )
            )
            self.btn_control.place(relx = 0.027, rely = 0.075, anchor = CENTER)
            
            self.y = 0.1
        
    def contacts_handler(self) -> None:
        #Проверяем, были ли вскрыты контакты
        if self.contact_labels == []:
            self.added_users.clear()
            
        contacts_data = self.client.get_data_contacts(self_id = self.self_user_id)    
            
        #останавливаем процесс, если у пользователя нету контактов и предлагаем добавить контакт
        if contacts_data is None:
            #1-й текст
            self.txt = Label(
                self.root,
                text = "У вас нету ещё ни одного контакта",
                bg = "gray7", fg = "gray16",
                font = (
                    ui_config["fonts"][0],
                    25
                )
            )
            self.txt.place(relx = 0.55, rely = 0.385, anchor = CENTER)
            
            #2-й текст
            self.txt = Label(
                self.root,
                text = f"Ваш id: {self.self_user_id} \nс помощью него вас смогут добавить в друзья",
                bg = "gray7", fg = "gray16",
                font = (
                    ui_config["fonts"][0],
                    15
                )
            )
            self.txt.place(relx = 0.55, rely = 0.45, anchor = CENTER)
            
            #кнопка добавить контакт
            self.btn_add_contact = Rounded_Button(
                self.root,
                text = "Добавить контакт",
                width = 200, height = 50,
                back_color = "gray7",
                bg = ui_config["main_color"], fg = "white",
                size = 11,
                command_func = self.window_add_user
            )
            self.btn_add_contact.place(relx = 0.55, rely = 0.55, anchor = CENTER)
            
            return 
             
        for index in contacts_data:
            user_data = self.client.get_data_user(index[0])
            print(user_data)

            avatar_path = f'{paths_config["user_avatars_folder"]}\\{user_data[1]}.png'
            
            #проверка существования аватара в директории
            # if not os.path.exists(avatar_path):
            try: os.remove(avatar_path)
            except: pass
            self.client.get_user_avatar(user_id = user_data[1])
            
            print(f"Loading avatar from: {avatar_path}")  # Отладочная информация

            if user_data[1] not in self.added_users:        
                try:
                    image_ui = Image.open(f'{paths_config["ui_components_folder"]}\\RoundedLabel_2.png')
                    image_ui = image_ui.resize((245, 70))  # Увеличение размера для теста
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
                            self.load_contact_info(event.widget["text"]),
                            
                            self.stop_receiving_messages(),
                            Thread(
                                daemon = None,
                                target = self.receiving_messages,
                                args=(event.widget["text"],)
                            ).start(),
                            # self.stop_receiving_messages(),
                            # Thread(target = self.stop_receiving_messages).start(),
                        )
                    )
                    
                    image = None
                    
                    #Открываем директорию с аватарами
                    try:
                        image = Image.open(avatar_path)
                        image = image.resize((40, 40))  # Увеличение размера для теста
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
                    
                    #кнопка управления
                    img_control = Image.open(f'{paths_config["ui_components_folder"]}\\setting.png')
                    img_control = img_control.resize((60, 60))  # Увеличение размера для теста
                    self.control_ui = ImageTk.PhotoImage(img_control)
                    
                    self.btn_control = Button(
                        self.root,
                        image = self.control_ui,
                        bg = "gray5", bd = 0,
                        command = lambda: (
                            self.hidden_objects(self.contact_labels),
                            self.show_control_buttons(
                                buttons = [
                                    ("Настройки", lambda event: settings.App(
                                        (self.root.winfo_x(), self.root.winfo_y())     
                                    ).main(), None),
                                    ("Редактировать профиль", ..., None),
                                    ("Добавить контакт", self.window_add_user, "#1d2b1c"),
                                    ("Создать группу", ..., "#10151a"),
                                    ("Создать сообщество", ..., "#10151a")
                                ]
                            )
                        )
                    )
                    self.btn_control.place(relx = 0.027, rely = 0.075, anchor = CENTER)
                    self.btn_control.bind("<Enter>", lambda event: event.widget.configure(bg = "gray9"))
                    self.btn_control.bind("<Leave>", lambda event: event.widget.configure(bg = "gray5"))
                    
                    self.y += 0.08
                    self.added_users.append(user_data[1])
                    self.contact_labels.append(self.lbl)
                    self.contact_labels.append(self.txt_last_message)
                    self.contact_labels.append(self.txt_data_contact)
                    self.contact_labels.append(self.avatar_label)

                except Exception as e:
                    print(f"Error loading image {avatar_path}: {e}")
    
    #информация о контакте
    def load_contact_info(self, user_id: str) -> None:
        user_data = self.client.get_data_user(user_id)
        colors = ["#120909", "#0e0b14", "#211a24", "#241f1f"]
        
        """ -- Верхняя часть --"""
        self.top_lbl = Label(
            self.root,
            width = 134, height = 4,
            bg = "gray9"
        )
        self.top_lbl.place(relx = 0.495, rely = 0.05, anchor = CENTER)
        
        #никнейм
        self.txt_nickname_up = Label(
            self.root,
            text = user_data[0], #nickname
            bg = "gray9", fg = "white",
            font = (
                ui_config["fonts"][0],
                13
            ),
            anchor = "w"
        )
        self.txt_nickname_up.place(relx = 0.28 - len(user_data[0]) // 20 - 0.03, rely = 0.04, anchor = CENTER)
        
        #статус сети
        self.txt_online_status = Label(
            self.root,
            text = "не в сети" if user_data[5] == "None" or user_data[5] is False else "в сети",
            bg = "gray9", fg = "#5b5266",
            font = (
                ui_config["fonts"][1],
                9
            ),
            anchor = "w"
        )
        self.txt_online_status.place(relx = 0.235 - len(user_data[0]) // 20, rely = 0.065, anchor = CENTER)
        
        """ -- Правая часть -- """
        #аватар пользователя
        try:
            img_logo = Image.open(f'{paths_config["user_avatars_folder"]}\\{user_data[1]}.png')
            img_logo = img_logo.resize((120, 120)) 
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
            image_path = f'{paths_config["ui_components_folder"]}\\call.png',
            image_size = (60, 50)
        )
        self.btn_call.place(relx = 0.83, rely = 0.35, anchor = CENTER)
        
        self.btn_blocked = Rounded_Button(
            self.root,
            width = 70, height = 60,
            radius = 10,
            bg = "red", fg = "gray9",
            image_path = f'{paths_config["ui_components_folder"]}\\blocked.png',
            image_size = (55, 45)
        )
        self.btn_blocked.place(relx = 0.89, rely = 0.35, anchor = CENTER)
        
        self.btn_complain = Rounded_Button(
            self.root,
            width = 70, height = 60,
            radius = 10,
            bg = "#8c3e01", fg = "gray9",
            image_path = f'{paths_config["ui_components_folder"]}\\complain.png',
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
       
    def stop_receiving_messages(self) -> None:
        self.stop_event.clear() # Устанавливаем флаг остановки
        # self.stop_event.set()
        self.is_checking_messages = False       
       
    def receiving_messages(self, user_id: str) -> None:
        print(1111111111)
        self.is_checking_messages = True
        
        self.stop_event.set()
        self.stop_event.clear() #Сбрасываем флаг остановки
        self.stop_event.clear()
        
        print(self.is_checking_messages, not self.stop_event.is_set())
        print((self.is_checking_messages) and (not(self.stop_event.is_set())))
    
        
        while self.is_checking_messages and not self.stop_event.is_set():
            # print(self.client.get_data_user(user_id = self.self_user_id)[0])
            print("Loop is started!")
            try:
                print("rm")
                self.server_chat = self.client.get_chat(self.self_user_id, user_id)
                self.chat = self.chat_display.get("1.0", END).rstrip().split("\n")
                
                user_nickname = self.client.get_data_user(user_id = self.server_chat[-1][3])[0]
                self_nickname = self.client.get_data_user(user_id = self.self_user_id)[0]
                
                print(self.chat[-2][1:-1])
                print(self_nickname)
                print(user_nickname)
                
                #проверяем время и никнейм
                if self.server_chat[-1][2] != self.chat[-2][1:-1] and self_nickname != user_nickname: 
                    info = f"\n\n<{self.server_chat[-1][2]}>\n{user_nickname}: {self.server_chat[-1][0]}"
                
                    self.chat_display.insert(
                        END, info,
                        "you" if self.server_chat[-1][3] == self.self_user_id else "interlocutor"
                    )
                    
                    self.chat_display.tag_config("you", foreground = ui_config["self_messages_color"])
                    self.chat_display.tag_config("interlocutor", foreground = ui_config["interlocutor_messages_color"])
                    self.chat_display.see(END) #Прокручиваем к концу
                       
            except:
                print("PASS PASS PASS")
                self.stop_event.set()
                break
            
            sleep(0.3)
        else:
            print("Loop is not started!")
            Thread(
                daemon = None,
                target = self.receiving_messages,
                args=(user_id,)
            ).start(),
            
        print("TRUE is closed")   
        self.is_checking_messages = False 
        self.stop_event.clear()
                
    def window_add_user(self, event) -> None:
        # self.root.destroy()
        add_user.App(self.self_user_id).main() #run file
            
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
            width = 100, height = 38,
            bg = "gray7", fg = "white",
            bd = 0,
            font = (
                ui_config["fonts"][0],
                12
            )
        )        
        self.chat_display.place(relx = 0.5, rely = 0.48, anchor = CENTER)
        
        if chat_data != None:
            sender_nickname = self.client.get_data_user(chat_data[0][3])[0]
            for index in chat_data:
                
                info = f"\n\n<{str(index[2])}>\n"
                if index[3] == self.self_user_id:
                    info += "Вы: "
                else:
                    info += sender_nickname + ": "
                
                info += str(index[0]).strip() #добавляем сообщение пользователя
                
                self.chat_display.insert(
                    END, info,
                    "you" if index[3] == self.self_user_id else "interlocutor"
                )
                
            self.chat_display.tag_config("you", foreground = ui_config["self_messages_color"])
            self.chat_display.tag_config("interlocutor", foreground = ui_config["interlocutor_messages_color"])
            self.chat_display.see(END) #Прокручиваем к концу
        

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

        self.entry_field = Rounded_Button(
            self.root,
            bg = "gray18", back_color = "gray7",
            width = 830, height = 30,
            text = "",
            size = 30
        )
        self.entry_field.place(relx = 0.48, rely = 0.95, anchor = CENTER)
        
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
        self.entry_message.place(relx = 0.475, rely = 0.95, anchor = CENTER)
        
        img_send_message = Image.open(f'{paths_config["ui_components_folder"]}\\send_message.png')
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
        now_time = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        
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
            f"\n\n<{now_time}>\nВы: {message}",
            "you",
        ) #добавляем сообщение в чат дисплей
        self.chat_display.see(END)
        
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
        
    def close_main_window(self) -> None:
        self.root.destroy()
        
    def main(self) -> None:
        self.build()
        self.contacts_handler()
        self.root.mainloop()
        
if __name__ == "__main__": 
    # App("dzyg0n546z58854o").main()
    
    Thread(target = App("dzyg0n546z58854o").main()) #test11
    # Thread(target = App("f72b2z06j94x0xm8").main()) #Коклеш
    # Thread(target = App("ego07n52hx2u7q5m").main()) #пiпiдастр
    # Thread(target = App("ei3284i0wuyw24o2").main()) #Волтер Уайт
    # Thread(target = App("bbx90n9it00b0vgs").main()) 
    
    
