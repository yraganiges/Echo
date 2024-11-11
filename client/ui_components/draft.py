import tkinter as tk
from PIL import Image, ImageTk

def main():
    root = tk.Tk()
    root.title("Загрузка изображения")

    # Загрузка изображения
    image = Image.open("client\\ui_components\\RoundedLabel.png")
    photo = ImageTk.PhotoImage(image)

    # Отображение изображения в Label
    label = tk.Label(root, image=photo)
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
