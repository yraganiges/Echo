from tkinter import END, Toplevel, scrolledtext
from typing import List

from handlers import make_indents
from config import ui_config, paths_config

class App:
    def __init__(self, remind_messages: List[str]) -> None:
        self.root = Toplevel()
        self.root.geometry("470x400")
        self.root.title("Важные упоминания")
        self.root.config(bg = ui_config["window_color"])
        try: self.root.iconbitmap(paths_config["icon"])
        except: pass
        
        self.remind_messages = remind_messages
        
    def show_remind_messages(self) -> None:
        print(self.remind_messages)
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            state = "normal", #disabled
            width = 50, height = 19,
            bg = "gray7", fg = "white",
            bd = 0,
            font = (
                ui_config["fonts"][0],
                12
            )
        )        
        self.chat_display.place(relx = 0.5, rely = 0.5, anchor = "center")
        
        for index in self.remind_messages:
            self.chat_display.insert(
                END,
                make_indents(index) + "\n\n",
                "you" if index[:3].lower().strip() == "вы:" else "interlocutor"
            )
            
            self.chat_display.tag_config("you", foreground = ui_config["self_messages_color"])
            self.chat_display.tag_config("interlocutor", foreground = ui_config["interlocutor_messages_color"])
            
        
    def main(self) -> None:
        self.show_remind_messages() 
        self.root.mainloop()
        
if __name__ == "__main__":
    App(["Вы: завтра возьми доки", "собеседник: сегодня встреча", "не забудь приготовить подарок"]).main()