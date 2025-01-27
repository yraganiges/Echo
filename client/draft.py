# from tkinter import Tk, Label, PhotoImage
# from PIL import Image, ImageTk  # Импортируем необходимые модули из Pillow

# class App(object):
#     def __init__(self) -> None:
#         self.root = Tk()
#         self.root.title(ui_config ["title"])
#         self.root.geometry("1640x920")
#         self.root.configure(bg=ui_config["window_color"])
        
#         try: 
#             self.root.iconbitmap("icons\main_icon.ico")
#         except: 
#             pass
        
#         self.client = Client(IP=app_config["IP"], port=app_config["Port"])
#         self.users_db = Database("client\data\contacts.db", "users")
        
#         self.images = []  # Список для хранения всех изображений
#         self.contacts_handler()

#     def contacts_handler(self) -> None:
#         x, y = 0.13, 0.1
#         for index in self.users_db.get_data():
#             user_data = self.client.get_data_user(index[0])
#             print(user_data)

#             # Загрузка аватара пользователя
#             avatar_path = f"client\user_avatars\{user_data[1]}.png"
#             try:
#                 # Открываем изображение с помощью Pillow
#                 image = Image.open(avatar_path)
#                 image = image.resize((20, 20), Image.ANTIALIAS)  # Изменяем размер изображения
#                 photo_image = ImageTk.PhotoImage(image)  # Преобразуем в PhotoImage

#                 # Сохраняем ссылку на изображение
#                 self.images.append(photo_image)

#                 # Создаем метку для отображения изображения
#                 avatar_label = Label(
#                     self.root,
#                     image=photo_image
#                 )
#                 avatar_label.place(relx=x - 0.03, rely=y, anchor='center')
                
#                 # Обновляем координаты для следующего аватара
#                 y += 0.05  # Увеличиваем y для размещения следующего аватара

#             except Exception as e:
#                 print(f"Ошибка загрузки аватара для пользователя {user_data[1]}: {e}")

# # Пример создания экземпляра приложения
# if __name__ == "__main__":
#     app = App()
#     app.root.mainloop()

# import tkinter as tk
# from tkinter import scrolledtext

# class ChatApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Чат")

#         # Создаем текстовое поле для отображения сообщений
#         self.chat_display = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
#         self.chat_display.pack(padx=10, pady=10)

#         # Создаем текстовое поле для ввода сообщений
#         self.message_input = tk.Entry(root, width=48)
#         self.message_input.pack(padx=10, pady=(0, 10))

#         # Создаем кнопку для отправки сообщения
#         self.send_button = tk.Button(root, text="Отправить", command=self.send_message)
#         self.send_button.pack(pady=(0, 10))

#     def send_message(self):
#         message = self.message_input.get()
#         if message:
#             # Включаем режим редактирования и добавляем сообщение в чат
#             self.chat_display.config(state='normal')
#             self.chat_display.insert(tk.END, "Вы: " + message + "\n")
#             self.chat_display.config(state='disabled')

#             # Очищаем поле ввода
#             self.message_input.delete(0, tk.END)

#             # Пример автоматического ответа (можно заменить на логику обработки сообщений)
#             self.auto_reply(message)

#     def auto_reply(self, message):
#         # Простой ответ на сообщение (можно добавить свою логику)
#         reply = "Сообщение получено: " + message
#         self.chat_display.config(state='normal')
#         self.chat_display.insert(tk.END, "Бот: " + reply + "\n")
#         self.chat_display.config(state='disabled')

# if __name__ == "__main__":
#     root = tk.Tk()
#     chat_app = ChatApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Чат")

        # Создаем ScrolledText для отображения сообщений
        self.text_area = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.bind("<Button-3>", self.delete_message)  # ПКМ для удаления сообщения
        self.text_area.bind("<Motion>", self.on_mouse_move)  # Наведение мыши
        self.text_area.bind("<Leave>", self.on_mouse_leave)  # Уход мыши

        # Создаем поле ввода для новых сообщений
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)  # Отправка сообщения по нажатию Enter

    def send_message(self, event):
        message = self.entry.get()
        if message:
            self.text_area.insert(tk.END, message + "\n")
            self.entry.delete(0, tk.END)

    def delete_message(self, event):
        try:
            index = self.text_area.index("@%s,%s" % (event.x, event.y))
            line = int(index.split('.')[0])  # Получаем номер строки
            self.text_area.delete(f"{line}.0", f"{line}.end")
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось удалить сообщение.")

    def on_mouse_move(self, event):
        index = self.text_area.index("@%s,%s" % (event.x, event.y))
        line = int(index.split('.')[0])  # Получаем номер строки
        # Меняем цвет текста на красный при наведении
        self.text_area.tag_add("hover", f"{line}.0", f"{line}.end")
        self.text_area.tag_config("hover", foreground="red")

    def on_mouse_leave(self, event):
        # Убираем цвет при уходе мыши
        self.text_area.tag_remove("hover", "1.0", "end")

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()


