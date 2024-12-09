#auth_window.py
import tkinter as tk
from tkinter import messagebox, ttk
from ui import RoundedButton  # Убедитесь, что RoundedButton определен в utils.py
from auth import login, register  # Функции для авторизации и регистрации пользователей

class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Аутентификация")
        self.center_window(self.root, 0.3, 0.2)

        # Поля для ввода
        input_frame = tk.Frame(root)
        input_frame.pack(pady=20, padx=20)

        tk.Label(input_frame, text="Имя пользователя:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = ttk.Entry(input_frame)  # Используем ttk для лучшего вида
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(input_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Кнопки
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        RoundedButton(button_frame, text="Войти", command=self.handle_login, width=130, height=32).grid(row=0, column=0, padx=10, pady=10)
        RoundedButton(button_frame, text="Регистрация", command=self.handle_register, width=130, height=32).grid(row=0, column=1, padx=10, pady=10)

    def handle_login(self):
        """Обработка входа пользователя"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = login(username, password)
        if success:
            self.root.destroy()  # Закрываем окно аутентификации
            self.open_main_app()
        else:
            messagebox.showerror("Ошибка", message)

    def handle_register(self):
        """Обработка регистрации нового пользователя"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Проверка на пустые поля
        if not username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, введите логин и пароль.")
            return

        # Проверка на минимальную длину пароля
        if len(password) < 6:
            messagebox.showerror("Ошибка", "Пароль должен содержать минимум 6 символов.")
            return

        success, message = register(username, password)
        if success:
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)

    def open_main_app(self):
        """Открытие главного окна приложения"""
        root = tk.Tk()
        from shop_app import ShopApp  # Импортируем главный интерфейс с магазинами
        app = ShopApp(root)
        root.mainloop()

    def center_window(self, root, width_ratio, height_ratio):
        """Функция для центрирования окна на экране"""
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width * width_ratio
        window_height = screen_height * height_ratio

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        root.geometry(f'{int(window_width)}x{int(window_height)}+{position_right}+{position_top}')
