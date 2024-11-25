from tkinter import Tk, CENTER
from ui_components.Entry import Default_Entry, Left_Entry

root = Tk()
root.geometry("400x500")
root.config(bg = "gray7")

entry_1 = Default_Entry(window = root)
entry_1.show(relx = 0.5, rely = 0.5, anchor = CENTER)

entry_2 = Left_Entry(window = root)
entry_2.show(relx = 0.5, rely = 0.7, anchor = CENTER)

root.mainloop()
