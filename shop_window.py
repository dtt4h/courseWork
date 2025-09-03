import tkinter as tk
from tkinter import messagebox, ttk
from ui import RoundedButton  # Убедитесь, что RoundedButton определен
from database import Database  # Убедитесь, что модуль Database подключен
from add_shop_dialog import AddShopDialog
from delete_shop_dialog import DeleteShopDialog
from update_phone_dialog import UpdatePhoneDialog
from export_import_dialog import ExportImportDialog


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

    def open_add_shop_dialog(self):
        """Открытие диалогового окна для добавления магазина."""
        AddShopDialog(self.root)

    def open_delete_shop_dialog(self):
        """Открытие диалогового окна для удаления магазина."""
        selected_item = self.tree.selection()
        if selected_item:
            selected_shop = self.tree.item(selected_item)['values']
            DeleteShopDialog(self.root, selected_shop)
        else:
            DeleteShopDialog(self.root)

    def open_update_phone_dialog(self):
        """Открытие диалогового окна для обновления телефона."""
        UpdatePhoneDialog(self.root)

    def open_export_import_dialog(self):
        """Открытие диалогового окна для экспорта/импорта."""
        ExportImportDialog(self.root)



    def create_widgets(self):
        """Создание интерфейса."""
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        # Buttons
        RoundedButton(button_frame, text="Добавить магазин через диалог", command=self.open_add_shop_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Удалить магазин", command=self.open_delete_shop_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Удалить магазин по имени", command=self.open_delete_shop_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Обновить телефон", command=self.open_update_phone_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Экспорт в JSON", command=self.open_export_import_dialog).pack(side=tk.LEFT, padx=10)
        RoundedButton(button_frame, text="Импорт из JSON", command=self.open_export_import_dialog).pack(side=tk.LEFT, padx=10)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('Номер магазина', 'Название магазина', 'Адрес', 'Телефон', 'Специализация')
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)



    def center_window(self, root, width_ratio, height_ratio):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width * width_ratio
        window_height = screen_height * height_ratio

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        root.geometry(f'{int(window_width)}x{int(window_height)}+{position_right}+{position_top}')
