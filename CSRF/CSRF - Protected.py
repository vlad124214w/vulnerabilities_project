#Защита
from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import os
import secrets

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Инициализация БД
def init_db():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            balance INTEGER DEFAULT 1000
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount INTEGER,
            recipient TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    try:
        cursor.execute("INSERT INTO users (username, password, balance) VALUES ('alex', 'password123', 1000)")
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

init_db()

# Генерация CSRF-токена
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

# Валидация CSRF-токена
def validate_csrf_token():
    token = request.form.get('csrf_token')
    return token and token == session.get('csrf_token')

# Защищенная форма перевода денег
@app.route('/transfer', methods=['GET', 'POST'])
def transfer_money():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # ЗАЩИТА: Проверка CSRF-токена
        if not validate_csrf_token():
            return "Ошибка безопасности: Неверный CSRF-токен", 403
        
        amount = int(request.form['amount'])
        recipient = request.form['recipient']
        
        # Дополнительная валидация
        if amount <= 0:
            return "Неверная сумма", 400
        
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT balance FROM users WHERE username = ?", (session['username'],))
        current_balance = cursor.fetchone()[0]
        
        if current_balance >= amount:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE username = ?", 
                         (amount, session['username']))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", 
                         (amount, recipient))
            
            cursor.execute("INSERT INTO transactions (user_id, amount, recipient) VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)",
                         (session['username'], amount, recipient))
            
            conn.commit()
            message = f"Успешно переведено {amount} пользователю {recipient}"
        else:
            message = "Недостаточно средств"
        
        conn.close()
        return render_template_string('''
            <h2>Результат перевода</h2>
            <p>{{ message }}</p>
            <a href="/transfer">Вернуться к переводу</a>
        ''', message=message)
    
    # Генерация нового токена для формы
    csrf_token = generate_csrf_token()
    
    return render_template_string('''
        <h2>Перевод денег</h2>
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <p>Сумма: <input type="number" name="amount" min="1" required></p>
            <p>Получатель: <input type="text" name="recipient" required></p>
            <p><button type="submit">Перевести</button></p>
        </form>
        <p><a href="/">На главную</a></p>
    ''', csrf_token=csrf_token)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            generate_csrf_token()  # Генерируем токен при входе
            return redirect(url_for('transfer_money'))
        else:
            return "Неверные учетные данные"
    
    return render_template_string('''
        <h2>Вход в систему</h2>
        <form method="POST">
            <p>Логин: <input type="text" name="username" required></p>
            <p>Пароль: <input type="password" name="password" required></p>
            <p><button type="submit">Войти</button></p>
        </form>
        <p>Тестовые данные: alex / password123</p>
    ''')

@app.route('/')
def index():
    if 'username' in session:
        return f'<h1>Добро пожаловать, {session["username"]}!</h1><a href="/transfer">Перевод денег</a>'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)