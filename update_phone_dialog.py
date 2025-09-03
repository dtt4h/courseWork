import tkinter as tk
from tkinter import messagebox
from database import Database


class UpdatePhoneDialog:
    def __init__(self, app):
        self.app = app
        self.db = Database()
        self.create_dialog()

    def create_dialog(self):
        """Создание диалогового окна для обновления номера телефона."""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title("Обновить телефон")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)

        # Центрирование окна
        self.center_window(self.dialog, 400, 250)

        # Создание фрейма для полей ввода
        input_frame = tk.Frame(self.dialog)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        # Поля ввода
        tk.Label(input_frame, text="Номер магазина:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.shop_number_entry = tk.Entry(input_frame)
        self.shop_number_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        tk.Label(input_frame, text="Название магазина:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.shop_name_entry = tk.Entry(input_frame)
        self.shop_name_entry.grid(row=1, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        tk.Label(input_frame, text="Новый телефон (12 символов):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.new_phone_entry = tk.Entry(input_frame)
        self.new_phone_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        # Кнопки
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20, fill=tk.X, padx=20)

        tk.Button(button_frame, text="Обновить", command=self.update_phone).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT)

        # Настройка растяжения колонок
        input_frame.columnconfigure(1, weight=1)

    def update_phone(self):
        """Обновление номера телефона в базе данных."""
        shop_number = self.shop_number_entry.get().strip()
        shop_name = self.shop_name_entry.get().strip()
        new_phone_number = self.new_phone_entry.get().strip()

        # Валидация
        if not shop_number:
            messagebox.showerror("Ошибка", "Номер магазина обязателен.")
            return

        if not shop_name:
            messagebox.showerror("Ошибка", "Название магазина обязательно.")
            return

        if not new_phone_number or len(new_phone_number) != 12:
            messagebox.showerror("Ошибка", "Номер телефона должен быть длиной 12 символов.")
            return

        # Обновляем в базе данных
        success, message = self.db.update_phone(shop_number, shop_name, new_phone_number)
        if success:
            messagebox.showinfo("Успех", message)
            self.dialog.destroy()
            # Обновляем данные в главном окне
            if hasattr(self.app, 'load_shop_data'):
                self.app.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def center_window(self, window, width, height):
        """Центрирование окна на экране."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        window.geometry(f'{width}x{height}+{position_right}+{position_top}')
