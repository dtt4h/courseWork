import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database


class DeleteShopDialog:
    def __init__(self, app, selected_shop=None):
        self.app = app
        self.selected_shop = selected_shop
        self.db = Database()
        self.create_dialog()

    def create_dialog(self):
        """Создание диалогового окна для удаления магазина."""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title("Удалить магазин")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)

        # Центрирование окна
        self.center_window(self.dialog, 400, 200)

        # Создание фрейма для контента
        content_frame = tk.Frame(self.dialog)
        content_frame.pack(pady=20, padx=20, fill=tk.X)

        # Если магазин выбран в главном окне
        if self.selected_shop:
            shop_name = self.selected_shop[1]  # Предполагаем, что имя магазина во второй колонке
            tk.Label(content_frame, text=f"Удалить магазин: {shop_name}?", font=("Arial", 12)).pack(pady=10)

            # Кнопки для подтверждения
            button_frame = tk.Frame(self.dialog)
            button_frame.pack(pady=20, fill=tk.X, padx=20)

            tk.Button(button_frame, text="Удалить", command=self.delete_selected_shop).pack(side=tk.LEFT, padx=(0, 10))
            tk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT)
        else:
            # Ввод имени магазина для удаления
            tk.Label(content_frame, text="Введите название магазина для удаления:", font=("Arial", 10)).pack(pady=10)

            self.shop_name_entry = tk.Entry(content_frame, width=30)
            self.shop_name_entry.pack(pady=5)

            # Кнопки
            button_frame = tk.Frame(self.dialog)
            button_frame.pack(pady=20, fill=tk.X, padx=20)

            tk.Button(button_frame, text="Удалить", command=self.delete_by_name).pack(side=tk.LEFT, padx=(0, 10))
            tk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT)

    def delete_selected_shop(self):
        """Удаление выбранного магазина."""
        if not self.selected_shop:
            messagebox.showerror("Ошибка", "Магазин не выбран.")
            return

        shop_name = self.selected_shop[1]
        success, message = self.db.delete_shop(shop_name)
        if success:
            messagebox.showinfo("Успех", message)
            self.dialog.destroy()
            # Обновляем данные в главном окне
            if hasattr(self.app, 'load_shop_data'):
                self.app.load_shop_data()
        else:
            messagebox.showerror("Ошибка", message)

    def delete_by_name(self):
        """Удаление магазина по введенному имени."""
        shop_name = self.shop_name_entry.get().strip()

        if not shop_name:
            messagebox.showerror("Ошибка", "Название магазина не может быть пустым.")
            return

        success, message = self.db.delete_shop(shop_name)
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
