from tkinter import Tk, Button, Label, CENTER
from config import server_conf
from server_controller import Server
from threading import Thread
import asyncio

class App(object):
    def __init__(self, time_working_server: int = False) -> None:
        self.root = Tk()
        self.root.title("Server controller")
        self.root.geometry("400x500")
        self.root.config(bg="gray12")
        self.root.resizable(0, 0)
        try: self.root.iconbitmap("__path__")
        except: pass
        
        self.time_working_server: int = time_working_server
        self.srv = Server(server_conf["IP"], server_conf["Port"])
        
        # Метка для отображения статуса сервера
        self.txt = Label(self.root, bg="gray12", fg="white", font=("Cascadia Mono SemiBold", 12))
        self.txt.place(relx=0.5, rely=0.6, anchor=CENTER)
        
        self.btn_run_server = Button(
            self.root,
            text = "Stop server" if self.srv.status_run_server() else "Run server",
            bg="red", fg="white",
            width=15, height=2, bd=0, border=0,
            font=("Cascadia Mono SemiBold", 12),
            command = Thread(target = self.run_server_wrapper).start()
        )
        self.btn_run_server.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Запускаем периодическое обновление статуса
        self.update_status()

    def update_status(self) -> None:
        """Обновляем статус сервера каждые 500 мс."""
        self.txt.config(text=self.srv.status_run_server())
        self.btn_run_server.config(text = "Stop server" if self.srv.status_run_server() else "Run server",)
        self.root.after(500, self.update_status)

    async def run_server(self):
        """Асинхронный метод для запуска сервера."""
        await self.srv.run(self.time_working_server)

    def run_server_wrapper(self):
        """Обертка для запуска асинхронного метода."""
        asyncio.run(self.run_server())

    def ui_components(self) -> None:
        self.txt_address = Label(
            self.root,
            text=f"Address for server: {server_conf['IP']} {server_conf['Port']}",
            bg="gray12", fg="white",
            font=("Cascadia Mono SemiBold", 12)
        ).place(relx=0.5, rely=0.3, anchor=CENTER)
        
    def main(self) -> None:
        self.ui_components()
        self.root.mainloop()
        
if __name__ == "__main__":
    App(server_conf["time_working_server"]).main()
