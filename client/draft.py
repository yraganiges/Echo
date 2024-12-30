from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk  # Импортируем необходимые модули из Pillow

class App(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(ui_config ["title"])
        self.root.geometry("1640x920")
        self.root.configure(bg=ui_config["window_color"])
        
        try: 
            self.root.iconbitmap("icons\main_icon.ico")
        except: 
            pass
        
        self.client = Client(IP=app_config["IP"], port=app_config["Port"])
        self.users_db = Database("client\data\contacts.db", "users")
        
        self.images = []  # Список для хранения всех изображений
        self.contacts_handler()

    def contacts_handler(self) -> None:
        x, y = 0.13, 0.1
        for index in self.users_db.get_data():
            user_data = self.client.get_data_user(index[0])
            print(user_data)

            # Загрузка аватара пользователя
            avatar_path = f"client\user_avatars\{user_data[1]}.png"
            try:
                # Открываем изображение с помощью Pillow
                image = Image.open(avatar_path)
                image = image.resize((20, 20), Image.ANTIALIAS)  # Изменяем размер изображения
                photo_image = ImageTk.PhotoImage(image)  # Преобразуем в PhotoImage

                # Сохраняем ссылку на изображение
                self.images.append(photo_image)

                # Создаем метку для отображения изображения
                avatar_label = Label(
                    self.root,
                    image=photo_image
                )
                avatar_label.place(relx=x - 0.03, rely=y, anchor='center')
                
                # Обновляем координаты для следующего аватара
                y += 0.05  # Увеличиваем y для размещения следующего аватара

            except Exception as e:
                print(f"Ошибка загрузки аватара для пользователя {user_data[1]}: {e}")

# Пример создания экземпляра приложения
if __name__ == "__main__":
    app = App()
    app.root.mainloop()
