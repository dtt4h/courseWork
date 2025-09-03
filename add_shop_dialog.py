import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database


class AddShopDialog:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.create_dialog()

    def create_dialog(self):
        """Создание диалогового окна для добавления магазина."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Добавить магазин")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        # Центрирование окна
        self.center_window(self.dialog, 400, 300)

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

        tk.Label(input_frame, text="Адрес:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.address_entry = tk.Entry(input_frame)
        self.address_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        tk.Label(input_frame, text="Телефон (12 символов):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone_entry = tk.Entry(input_frame)
        self.phone_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        tk.Label(input_frame, text="Специализация:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.specialization_entry = tk.Entry(input_frame)
        self.specialization_entry.grid(row=4, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

        # Кнопки
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20, fill=tk.X, padx=20)

        tk.Button(button_frame, text="Добавить", command=self.add_shop).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT)

        # Настройка растяжения колонок
        input_frame.columnconfigure(1, weight=1)

    def add_shop(self):
        """Добавление магазина в базу данных."""
        shop_number = self.shop_number_entry.get().strip()
        shop_name = self.shop_name_entry.get().strip()
        address = self.address_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        specialization = self.specialization_entry.get().strip()

        # Валидация
        if not shop_number:
            messagebox.showerror("Ошибка", "Номер магазина не может быть пустым.")
            return

        if not shop_name:
            messagebox.showerror("Ошибка", "Название магазина не может быть пустым.")
            return

        if not address:
            messagebox.showerror("Ошибка", "Адрес магазина не может быть пустым.")
            return

        if not phone_number or len(phone_number) != 12:
            messagebox.showerror("Ошибка", "Номер телефона должен быть длиной 12 символов.")
            return

        if not specialization:
            messagebox.showerror("Ошибка", "Специализация магазина не может быть пустой.")
            return

        # Добавляем в базу данных
        success, message = self.db.add_shop(shop_number, shop_name, address, phone_number, specialization)
        if success:
            messagebox.showinfo("Успех", message)
            self.dialog.destroy()
            # Обновляем данные в главном окне
            if hasattr(self.parent, 'load_shop_data'):
                self.parent.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def center_window(self, window, width, height):
        """Центрирование окна на экране."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        window.geometry(f'{width}x{height}+{position_right}+{position_top}')
