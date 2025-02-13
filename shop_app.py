#Главная программа
import tkinter as tk
from auth_window import AuthWindow
from shop_window import ShopApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthWindow(root)
    root.mainloop()
