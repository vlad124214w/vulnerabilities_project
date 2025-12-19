

import secrets
from flask import Flask, render_template, request, session, abort

app = Flask(__name__)
app.secret_key = 'my-secret-key'  # мой ключик
current_user = None  # Эээ.. переменная для пользователя?

# Здеся генерируемс CSRF-токен
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token_from_form = request.form.get('_csrf_token')
        token_in_session = session.get('_csrf_token', None)
        if not token_from_form or token_from_form != token_in_session:
            abort(403)  # Как я понял, это нужно, ну просто для понимания, если вдруг не совпали токены

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_user
    if request.method == 'POST':
        username = request.form.get('username', '')
        current_user = username
    csrf_token = generate_csrf_token()
    return render_template('sayt.html', csrf_token=csrf_token, current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)