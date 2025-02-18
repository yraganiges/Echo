from tkinter import (
    Tk, Toplevel, #main
    CENTER, LEFT,  #positions
    Label #ui
)
from typing import List
from PIL import Image, ImageTk

from config import ui_config, app_config, paths_config
from client_requests import Client

from ui_components.Buttons import Rounded_Button


class PairCall(Tk):
    def __init__(self, users_id: List[str]) -> None:
        super().__init__()

        self.title(ui_config["title"])
        self.geometry("450x600")
        self.configure(bg = ui_config["window_color"])
        self.resizable(0, 0)
        
        self.users_in_call = users_id
        self.client = Client(IP = app_config["IP"], port = app_config["Port"])
        
        self.x, self.y = 0.5, 0.4
        
        try: self.iconbitmap(paths_config["icon"])
        except: pass
        
    def show_users_handler(self) -> None:
        for index in self.users_in_call[0:2]:
            user_data = self.client.get_data_user(user_id = index)
            
            self.rounded_label = Rounded_Button(
                self,
                text = "",
                radius = 10,
                width = 300, height = 60,
                bg = "gray12",
                back_color = ui_config["window_color"]
            )
            self.rounded_label.place(relx = self.x, rely = self.y, anchor = CENTER)
            
            self.txt_nickname = Label(
                self,
                text = user_data[0],
                bg = "gray12", fg = "white",
                font = (
                    ui_config["fonts"][0],
                    12
                )
            )
            self.txt_nickname.place(relx = self.x - 0.05, rely = self.y, anchor = "se")
            
            self.y += 0.12
        
    def main(self) -> None:
        self.show_users_handler()
        self.mainloop()
        
if __name__ == "__main__":
    PairCall(["dzyg0n546z58854o", "f72b2z06j94x0xm8"]).main()    