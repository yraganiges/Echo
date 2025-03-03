from tkinter import Label, Tk
from webbrowser import open

from config import ui_config, paths_config
from ui_components.Buttons import Rounded_Button

from threading import Thread
import main

text_description_error = "Возможно на данный момент сервер выключен\nили у вас отсуствует подключение к интернету.\nРекомендуем проверить ваше состояние сети.\nВся информация о работе Echo есть по ссылке:"

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x400")
        self.root.title(ui_config["title"])
        self.root.resizable(0, 0)
        self.root.config(bg = ui_config["window_color"])
        try: self.root.iconbitmap(paths_config["icon"])
        except: pass
        
    def restart_main_win(self, event) -> None:
        self.root.destroy()
        Thread(target = lambda: main.App("dzyg0n546z58854o").main()).start()
        
    def main(self) -> None:
        
        #название ошибки
        self.txt_title = Label(
            self.root,
            text = "Нет соединения с сервервом!",
            bg = "gray7", fg = "#6c5d85",
            font = (
                ui_config["fonts"][0],
                22
            )
        ).place(relx = 0.5, rely = 0.2, anchor = "center")
        
        #описание ошибки
        self.txt_description = Label(
            self.root,
            text = text_description_error,
            bg = "gray7", fg = "gray32",
            font = (
                ui_config["fonts"][0],
                12
            )
        ).place(relx = 0.5, rely = 0.45, anchor = "center")
        
        #ссылка
        self.txt_link = Label(
            self.root,
            text = "https://github.com/yraganiges/Echo",
            bg = "gray7", fg = "white",
            font = (
                ui_config["fonts"][0],
                12,
                "underline"
            )
        )
        self.txt_link.place(relx = 0.5, rely = 0.65, anchor = "center")
        self.txt_link.bind("<Enter>", lambda event: self.txt_link.configure(fg = "#6d8ae3"))
        self.txt_link.bind("<Leave>", lambda event: self.txt_link.configure(fg = "#b6b6b8"))
        self.txt_link.bind("<Button - 1>", lambda event: open(event.widget["text"]))
        
        #Кнопка рестарта
        self.btn_restart = Rounded_Button(
            self.root,
            text = "Попробовать снова",
            width = 200, height = 50,
            back_color = "gray7",
            command_func = self.restart_main_win
        )
        self.btn_restart.place(relx = 0.5, rely = 0.85, anchor = "center")
        
        self.root.mainloop()
        
if __name__ == "__main__":
    App().main()