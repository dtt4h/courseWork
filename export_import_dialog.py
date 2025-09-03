import tkinter as tk
from tkinter import messagebox, filedialog
import json
from database import Database


class ExportImportDialog:
    def __init__(self, app):
        self.app = app
        self.db = Database()
        self.create_dialog()

    def create_dialog(self):
        """Создание диалогового окна для экспорта/импорта данных."""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title("Экспорт/Импорт данных")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)

        # Центрирование окна
        self.center_window(self.dialog, 300, 150)

        # Создание фрейма для кнопок
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=30, padx=20, fill=tk.X)

        # Кнопки для экспорта и импорта
        tk.Button(button_frame, text="Экспорт в JSON", command=self.export_to_json, width=15).pack(pady=5)
        tk.Button(button_frame, text="Импорт из JSON", command=self.import_from_json, width=15).pack(pady=5)
        tk.Button(button_frame, text="Закрыть", command=self.dialog.destroy, width=15).pack(pady=10)

    def export_to_json(self):
        """Экспорт данных в JSON файл."""
        shops = self.db.get_all_shops()
        shops_list = [
            {"shop_number": shop[0], "shop_name": shop[1], "address": shop[2], "phone_number": shop[3], "specialization": shop[4]}
            for shop in shops
        ]

        file_name = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Сохранить файл JSON"
        )

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
        file_name = filedialog.askopenfilename(
            title="Выберите файл JSON",
            filetypes=[("JSON Files", "*.json")]
        )

        if not file_name:
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as json_file:
                shops_list = json.load(json_file)

            for shop in shops_list:
                self.db.add_shop(
                    shop['shop_number'],
                    shop['shop_name'],
                    shop['address'],
                    shop['phone_number'],
                    shop['specialization']
                )

            messagebox.showinfo("Успех", f"Данные успешно импортированы из {file_name}.")
            # Обновляем данные в главном окне
            if hasattr(self.app, 'load_shop_data'):
                self.app.load_shop_data()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {e}")

    def center_window(self, window, width, height):
        """Центрирование окна на экране."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        window.geometry(f'{width}x{height}+{position_right}+{position_top}')
