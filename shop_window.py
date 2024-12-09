import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
from ui import RoundedButton  # Убедитесь, что RoundedButton определен
from database import Database  # Убедитесь, что модуль Database подключен
import json
import sqlite3


class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление магазинами")
        self.center_window(self.root, 0.8, 0.6)
        self.db = Database()  # Инициализация базы данных
        self.create_widgets()
        self.load_shop_data()

    def load_shop_data(self):
        """Загрузка данных магазинов из базы в таблицу."""
        shops = self.db.get_all_shops()

        # Очистка текущих данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Добавление новых данных
        for shop in shops:
            self.tree.insert('', 'end', values=(shop[0], shop[1], shop[2], shop[3], shop[4]))

    def add_shop_via_dialog(self):
        """Добавление магазина через диалоговые окна."""
        shop_number = simpledialog.askstring("Добавить магазин", "Введите номер магазина:")
        if not shop_number:
            messagebox.showerror("Ошибка", "Номер магазина не может быть пустым.")
            return

        shop_name = simpledialog.askstring("Добавить магазин", "Введите название магазина:")
        if not shop_name:
            messagebox.showerror("Ошибка", "Название магазина не может быть пустым.")
            return

        address = simpledialog.askstring("Добавить магазин", "Введите адрес:")
        if not address:
            messagebox.showerror("Ошибка", "Адрес магазина не может быть пустым.")
            return

        phone_number = simpledialog.askstring("Добавить магазин", "Введите телефон (12 символов):")
        if not phone_number or len(phone_number) != 12:
            messagebox.showerror("Ошибка", "Номер телефона должен быть длиной 12 символов.")
            return

        specialization = simpledialog.askstring("Добавить магазин", "Введите специализацию магазина:")
        if not specialization:
            messagebox.showerror("Ошибка", "Специализация магазина не может быть пустой.")
            return

        # Добавляем в базу данных
        success, message = self.db.add_shop(shop_number, shop_name, address, phone_number, specialization)
        if success:
            messagebox.showinfo("Успех", message)
            self.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def delete_shop(self):
        """Удаление выбранного магазина."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите магазин для удаления.")
            return

        shop_name = self.tree.item(selected_item)['values'][1]
        success, message = self.db.delete_shop(shop_name)
        if success:
            messagebox.showinfo("Успех", message)
            self.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def update_phone(self):
        """Обновление номера телефона по номеру и имени магазина."""
        shop_number = simpledialog.askstring("Обновление телефона", "Введите номер магазина:")
        shop_name = simpledialog.askstring("Обновление телефона", "Введите название магазина:")

        if not shop_number or not shop_name:
            messagebox.showerror("Ошибка", "Номер и название магазина обязательны.")
            return

        new_phone_number = simpledialog.askstring("Обновление телефона", "Введите новый номер телефона (12 символов):")
        if not new_phone_number or len(new_phone_number) != 12:
            messagebox.showerror("Ошибка", "Номер телефона должен быть длиной 12 символов.")
            return

        success, message = self.db.update_phone(shop_number, shop_name, new_phone_number)
        if success:
            messagebox.showinfo("Успех", message)
            self.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def export_to_json(self):
        """Экспорт данных в JSON файл."""
        shops = self.db.get_all_shops()
        shops_list = [
            {"shop_number": shop[0], "shop_name": shop[1], "address": shop[2], "phone_number": shop[3], "specialization": shop[4]}
            for shop in shops
        ]
        file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_name:
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(shops_list, json_file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные успешно экспортированы в {file_name}.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {e}")

    def import_from_json(self):
        """Импорт данных из JSON файла."""
        file_name = filedialog.askopenfilename(title="Выберите файл JSON", filetypes=[("JSON Files", "*.json")])
        if not file_name:
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as json_file:
                shops_list = json.load(json_file)
            for shop in shops_list:
                self.db.add_shop(shop['shop_number'], shop['shop_name'], shop['address'], shop['phone_number'], shop['specialization'])
            self.load_shop_data()
            messagebox.showinfo("Успех", f"Данные успешно импортированы из {file_name}.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {e}")

    def create_widgets(self):
        """Создание интерфейса."""
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        # Buttons
        RoundedButton(button_frame, text="Добавить магазин через диалог", command=self.add_shop_via_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Удалить магазин", command=self.delete_shop).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Удалить магазин по имени", command=self.delete_shop_by_name).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Обновить телефон", command=self.update_phone).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Экспорт в JSON", command=self.export_to_json).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Импорт из JSON", command=self.import_from_json).pack(side=tk.LEFT, padx=10)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('Номер магазина', 'Название магазина', 'Адрес', 'Телефон', 'Специализация')
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
    def delete_shop_by_name(self):
        """Удаляет магазин по его наименованию (ввод через диалог)."""
        shop_name = simpledialog.askstring("Удаление магазина", "Введите название магазина для удаления:")
        
        if not shop_name:
            return  # Если имя не введено, выходим из функции
        
        # Удаление магазина по имени
        success, message = self.db.delete_shop(shop_name)
        if success:
            messagebox.showinfo("Успех", message)
            self.load_shop_data()  # Перезагрузка данных
        else:
            messagebox.showerror("Ошибка", message)


    def center_window(self, root, width_ratio, height_ratio):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width * width_ratio
        window_height = screen_height * height_ratio

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        root.geometry(f'{int(window_width)}x{int(window_height)}+{position_right}+{position_top}')
