import sqlite3

# Создаем или подключаемся к базе данных SQLite
connection_sqlite = sqlite3.connect('db3.db', check_same_thread=False)
cursor_sqlite = connection_sqlite.cursor()

# Создаем таблицу Users
cursor_sqlite.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password TEXT)
''')

try:
    cursor_sqlite.execute('''INSERT INTO Users (username, password) VALUES ('Alex', 'Alex')''')
    cursor_sqlite.execute('''INSERT INTO Users (username, password) VALUES ('Pavel', 'Pavel')''')
    cursor_sqlite.execute('''INSERT INTO Users (username, password) VALUES ('Sergey', 'Sergey')''')
    connection_sqlite.commit()
except sqlite3.IntegrityError:
    # Пользователи уже есть, игнорируем ошибку
    pass

# Получаем логин и пароль от пользователя
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

cursor_mysql = connection_sqlite.cursor()

entrance = "SELECT username FROM Users WHERE username = ? AND password = ?"
cursor_mysql.execute(entrance, (username, password))
result = cursor_mysql.fetchall()

# Проверяем результат
if len(result) > 0:
    print("Успешный вход")
else:
    print("Неверные учетные данные")

# Закрываем соединения
cursor_mysql.close()

cursor_sqlite.close()
connection_sqlite.close()