from tkinter import Toplevel, Tk, CENTER, Label
from typing import List
from PIL import Image, ImageTk
import socket
import pyaudio
import threading

from config import ui_config, app_config, paths_config
from client_requests import Client
from ui_components.Buttons import Rounded_Button

class VoiceCall:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.conn = None

    def start_call(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((app_config["IP"], 52))
        self.stream = self.p.open(format=pyaudio.paInt16,
                                 channels=2,
                                 rate=44100,
                                 input=True,
                                 output=True)
        threading.Thread(target=self.play_audio).start()
        threading.Thread(target=self.record_audio).start()

    def play_audio(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
                self.stream.write(data)
            except ConnectionResetError:
                print("Соединение с сервером разорвано.")
                self.conn.close()
                break

    def record_audio(self):
        while True:
            try:
                data = self.stream.read(1024)
                self.conn.sendall(data)
            except ConnectionResetError:
                print("Соединение с сервером разорвано.")
                self.conn.close()
                break
            except:
                pass

    def end_call(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.conn:
            self.conn.close()
        self.p.terminate()


class PairCall(Toplevel):
    def __init__(self, users_id: List[str]) -> None:
        super().__init__()
        self.title(ui_config["title"])
        self.geometry("450x600")
        self.configure(bg=ui_config["window_color"])
        self.resizable(0, 0)
        
        self.users_in_call = users_id
        self.client = Client(IP=app_config["IP"], port=app_config["Port"])
        self.voice_call = VoiceCall()
        
        self.x, self.y = 0.5, 0.4
        self.images = []
        
        try: self.iconbitmap(paths_config["icon"])
        except: pass
        
        # Добавление кнопок для управления звонком
        self.start_button = Rounded_Button(self, text="Start Call", command_func=self.start_call)
        self.start_button.place(relx=0.3, rely=0.9, anchor=CENTER)
        
        self.end_button = Rounded_Button(self, text="End Call", command_func=self.end_call)
        self.end_button.place(relx=0.7, rely=0.9, anchor=CENTER)
        
    def start_call(self, event):
        self.voice_call.start_call()
        
    def end_call(self, event):
        self.voice_call.end_call()
        
    def show_users_handler(self) -> None:
        for index in self.users_in_call[0:2]:
            user_data = self.client.get_data_user(user_id=index)
            print(user_data)
            
            self.rounded_label = Rounded_Button(
                self,
                text="",
                radius=10,
                width=300, height=60,
                bg="gray12",
                back_color=ui_config["window_color"]
            )
            self.rounded_label.place(relx=self.x, rely=self.y, anchor=CENTER)
            
            #avatar
            try:
                image = Image.open(f"{paths_config['user_avatars_folder']}\\{user_data[1]}.png")
                image = image.resize((45, 45))  # Увеличение размера для теста
                avatar = ImageTk.PhotoImage(image)
                self.images.append(avatar)
            

                self.avatar_label = Label(
                    self,
                    image=avatar if image is not None else "",
                    bg="gray8"
                )
                self.avatar_label.place(relx=self.x - 0.25, rely=self.y, anchor=CENTER)
            except:
                pass
            #nickname
            self.txt_nickname = Label(
                self,
                text=user_data[0],
                bg="gray12", fg="white",
                font=(ui_config["fonts"][0], 12)
            )
            self.txt_nickname.place(relx=self.x - 0.05, rely=self.y + 0.01, anchor="se")
            
            self.y += 0.12
        
    def main(self) -> None:
        self.show_users_handler()
        self.mainloop()
        
if __name__ == "__main__":
    PairCall(["dzyg0n546z58854o", "f72b2z06j94x0xm8"]).main()