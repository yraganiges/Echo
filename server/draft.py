# from cryptography.fernet import Fernet
 
# # Генерация ключа
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
 
# # Шифрование данных
# data = b"Hello, world!"
# encrypted_data = cipher_suite.encrypt(data)
 
# # Дешифрование данных
# decrypted_data = cipher_suite.decrypt(encrypted_data)
 
# print("Исходные данные:", data)
# print("Зашифрованные данные:", encrypted_data)
# print("Расшифрованные данные:", decrypted_data)

# import tkinter as tk
# from tkinter import scrolledtext

# def main():
#     root = tk.Tk()
#     root.title("Пример ScrolledText с цветным текстом")

#     # Создаем виджет ScrolledText
#     text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
#     text_area.pack(padx=10, pady=10)

#     # Вставляем текст
#     text_area.insert(tk.END, "Это обычный текст.\n")
    
#     # Добавляем тег для изменения цвета
#     text_area.insert(tk.END, "Это цветной текст.\n", "color")
    
#     text_area.insert(tk.END, "Это снова обычный текст.")

#     # Настраиваем тег
#     text_area.tag_config("color", foreground="red")  # Устанавливаем цвет текста

#     # Делаем текстовое поле не редактируемым (по желанию)
#     text_area.configure(state='disabled')

#     root.mainloop()

# if __name__ == "__main__":
#     main()

# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk

# def insert_image(text_widget: scrolledtext, image_path: str) -> None:
#     # Открываем изображение
#     img = Image.open(image_path)
#     img = img.resize((100, 100), Image.ANTIALIAS)  # Измените размер по необходимости
#     photo = ImageTk.PhotoImage(img)

#     # Вставляем изображение в текстовый виджет
    
#     text_widget.image_create(tk.END, image=photo)
    
#     # Сохраняем ссылку на изображение, чтобы оно не удалилось из памяти
#     text_widget.image = photo

# # Создаем главное окно
# root = tk.Tk()
# root.title("ScrolledText with Image")

# # Создаем ScrolledText
# text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
# text_area.pack(padx=10, pady=10)

# # Вставляем текст
# text_area.insert(tk.END, "Вот изображение ниже:\n\n")

# # Вставляем изображение
# insert_image(text_area, "server\\avatars\\test_image.png")  # Укажите путь к вашему изображению

# # Запускаем главный цикл
# root.mainloop()


import tkinter as tk
from tkinter import scrolledtext

def on_mouse_wheel(event):
    # Прокрутка вверх или вниз в зависимости от направления колеса
    if event.delta > 0:
        print("Прокрутка вверх")
        text.yview_scroll(-1, "units")  # Прокрутка вверх
    else:
        print("Прокрутка вниз")
        text.yview_scroll(1, "units")   # Прокрутка вниз

# Создаем главное окно
root = tk.Tk()
root.title("Прокрутка с помощью колеса мыши")

# Создаем текстовое поле с прокруткой
text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text.pack(pady=10)

# Добавляем текст для демонстрации прокрутки
for i in range(1, 101):
    text.insert(tk.END, f"Строка {i}\n")

# Привязываем событие колеса мыши к функции прокрутки
root.bind("<MouseWheel>", on_mouse_wheel)  # Для Windows и Mac

# Для Linux используем другое событие
root.bind("<Button-4>", lambda event: text.yview_scroll(-1, "units"))  # Прокрутка вверх
root.bind("<Button-5>", lambda event: text.yview_scroll(1, "units"))   # Прокрутка вниз

# Запускаем главный цикл
root.mainloop()









