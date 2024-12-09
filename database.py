import sqlite3

class Database:
    def __init__(self, db_name="shops.db"):
        """Инициализация базы данных."""
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        """Устанавливает соединение с базой данных и возвращает объект соединения."""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Создает таблицы, если их еще нет."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shops (
                    shop_number TEXT PRIMARY KEY,
                    shop_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    specialization TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_shop(self, shop_number, shop_name, address, phone_number, specialization):
        """Добавляет новый магазин в базу данных."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO shops (shop_number, shop_name, address, phone_number, specialization)
                    VALUES (?, ?, ?, ?, ?)
                """, (shop_number, shop_name, address, phone_number, specialization))
                conn.commit()
            return True, "Магазин добавлен успешно."
        except sqlite3.IntegrityError:
            return False, "Магазин с таким номером уже существует."
        except Exception as e:
            return False, f"Произошла ошибка: {str(e)}"

    def delete_shop(self, shop_name):
        """Удаляет магазин по его названию."""
        try:
            with sqlite3.connect("shops.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM shops WHERE shop_name = ?", (shop_name,))
                if cursor.rowcount > 0:
                    return True, f"Магазин '{shop_name}' успешно удалён."
                else:
                    return False, f"Магазин '{shop_name}' не найден."
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def update_phone(self, shop_number, shop_name, new_phone_number):
        """Обновляет номер телефона магазина по № и наименованию."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE shops 
                    SET phone_number = ? 
                    WHERE shop_number = ? AND shop_name = ?
                """, (new_phone_number, shop_number, shop_name))
                if cursor.rowcount == 0:
                    return False, "Магазин с указанным номером и наименованием не найден."
                conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e):
                return False, "Номер телефона уже существует."
            return False, "Ошибка при обновлении номера телефона."
        return True, "Номер телефона успешно обновлен."


    def find_shops_by_specialization(self, specialization):
        """Ищет магазины по специализации."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM shops WHERE LOWER(specialization) = ?", (specialization.lower(),))
            shops = cursor.fetchall()
        return shops

    def get_shop(self, shop_number):
        """Возвращает магазин по номеру."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM shops WHERE shop_number = ?", (shop_number,))
            shop = cursor.fetchone()
        return shop

    def get_all_shops(self):
        """Возвращает все магазины из базы данных."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM shops")
            shops = cursor.fetchall()
        return shops
