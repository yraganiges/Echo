# with open("server\\ai\\datasets\\danger_messages.txt", "r") as file:
#     for index in file.read().split("$"):
#         try:
#             print(index[-1])
#         except IndexError:
#             pass
        
# import tkinter as tk

# def create_scrollable_buttons(root, num_buttons):
#     # Создаем фрейм для размещения кнопок
#     frame = tk.Frame(root)
    
#     # Создаем полосу прокрутки
#     scrollbar = tk.Scrollbar(root, orient="vertical")
#     scrollbar.pack(side="right", fill="y")

#     # Создаем холст
#     canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
#     canvas.pack(side="left", fill="both", expand=True)

#     # Привязываем полосу прокрутки к холсту
#     scrollbar.config(command=canvas.yview)

#     # Создаем внутренний фрейм для кнопок
#     button_frame = tk.Frame(canvas)

#     # Добавляем кнопки в фрейм
#     for i in range(num_buttons):
#         button = tk.Button(button_frame, text=f"Button {i + 1}", padx=10, pady=5)
#         button.pack(pady=2)  # Добавляем немного отступа между кнопками

#     # Добавляем внутренний фрейм на холст
#     canvas.create_window((0, 0), window=button_frame, anchor="nw")

#     # Обновляем размер холста при изменении размера внутреннего фрейма
#     def on_frame_configure(event):
#         canvas.configure(scrollregion=canvas.bbox("all"))

#     button_frame.bind("<Configure>", on_frame_configure)

#     # Обработчик прокрутки с помощью колеса мыши
#     def on_mouse_wheel(event):
#         canvas.yview_scroll(int(-1*(event.delta/120)), "units")

#     # Привязываем событие прокрутки к обработчику
#     root.bind_all("<MouseWheel>", on_mouse_wheel)

#     frame.pack(fill="both", expand=True)

# # Создаем главное окно
# root = tk.Tk()
# root.title("Scrollable Buttons")

# # Создаем прокручиваемые кнопки
# create_scrollable_buttons(root, 50)

# # Запускаем основной цикл приложения
# root.mainloop()

# import random
# import keyboard
# import time

# codes = []
# corrected_code = "452543"


# while True:
#     code = ""
    
#     for _ in range(6):
#         code += str(random.randint(0, 9))
        
#     if code not in codes:
#         keyboard.write(code + "\n", delay = 0.1)
#         print(code)
#         codes.append(code)
        
#         if code == corrected_code:
#             break
        
#     time.sleep(0.1)

# import random
# import time

# corrected_code = "141453"
# start_time = time.time()

# while True:
#     code = ""
#     for _ in range(6):
#         code += str(random.randint(0, 9))
        
#     if code == corrected_code:
#         break
    
# print(f"code is unlocked!\ncode is {code}")

# end_time = time.time()
# print("время расшифровки кода: " + str(start_time - end_time) + "с")

import tkinter as tk

def on_button_click():
    print("Выполняется действие")
    # Ваш код здесь

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Выполнить", command=on_button_click)
button.pack()

# Устанавливаем кнопку по умолчанию (срабатывает при нажатии Enter)
root.bind('<Return>', lambda event: button.invoke())

root.mainloop()
