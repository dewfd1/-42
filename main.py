import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class MenuItem:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

class RestaurantSystem:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                description TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                user_id INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS order_items
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                order_id INTEGER NOT NULL,
                                item_id INTEGER NOT NULL,
                                quantity INTEGER NOT NULL,
                                FOREIGN KEY (order_id) REFERENCES orders(id),
                                FOREIGN KEY (item_id) REFERENCES menu_items(id))''')

    def register_user(self, name, email, password):
        try:
            self.cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            self.conn.commit()
            print("Пользователь успешно зарегестрирован!")
        except sqlite3.Error as error:
            print("Ошибка регистрации пользователя:", error)

    def login_user(self, email, password):
        try:
            self.cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
            user = self.cursor.fetchone()
            if user:
                print("Вход успешно завершен!")
            else:
                print("Неверный email или пароль.")
        except sqlite3.Error as error:
            print("Ошибка входа:", error)

    def add_menu_item(self, name, price, description):
        try:
            self.cursor.execute('INSERT INTO menu_items (name, price, description) VALUES (?, ?, ?)', (name, price, description))
            self.conn.commit()
            print("Блюдо успешно добавлено!")
        except sqlite3.Error as error:
            print("Ошибка добавления блюда:", error)

    def update_menu_item(self, menu_item_id, name, price, description):
        try:
            self.cursor.execute('UPDATE menu_items SET name=?, price=?, description=? WHERE id=?', (name, price, description, menu_item_id))
            self.conn.commit()
            print("Блюдо успешно обновлено!")
        except sqlite3.Error as error:
            print("Ошибка обновления блюда:", error)

    def delete_menu_item(self, menu_item_id):
        try:
            self.cursor.execute('DELETE FROM menu_items WHERE id=?', (menu_item_id,))
            self.conn.commit()
            print("Блюдо успешно удалено!")
        except sqlite3.Error as error:
            print("Ошибка удаления блюда:", error)

    def filter_menu_items_by_price(self, max_price):
        try:
            self.cursor.execute('SELECT * FROM menu_items WHERE price <= ?', (max_price,))
            menu_items = self.cursor.fetchall()
            print("Блюда сортированы по цене:")
            for item in menu_items:
                print(item)
        except sqlite3.Error as error:
            print("Ошибка фильтрации блюд по цене:", error)

system = RestaurantSystem("database.db")

name = input("Введите ваше имя: ")
email = input("Введите ваш email: ")
password = input("Введите ваш пароль: ")

system.register_user(name, email, password)
