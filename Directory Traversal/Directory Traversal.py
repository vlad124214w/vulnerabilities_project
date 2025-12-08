#Сущность атаки
from flask import Flask, request, send_file, abort
import os

app = Flask(__name__)

BASE_DIR = "/home/user/files"  # Каталог с файлами

@app.route('/download')
def download():
    filename = request.args.get('file')
    if not filename:
        abort(400)

    # Уязвимость
    file_path = os.path.join(BASE_DIR, filename)

    # Нет проверки
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run()

# Проблема: Пользователь может передать `file=../../../../../etc/passwd`, 
# и программа попытается открыть системный файл, что дает доступ к любым файлам на сервере

### Исправленный, защищенный код


from flask import Flask, request, send_file, abort
import os

app = Flask(__name__)

BASE_DIR = "/home/user/files"  # Каталог

@app.route('/download')
def download():
    filename = request.args.get('file')
    if not filename:
        abort(400)

    # Используем безопасную обработку входных данных:
    # Испольхуем только basename (чтобы убрать пути)
    safe_filename = os.path.basename(filename)

    # Формируем путь внутри BASE_DIR
    file_path = os.path.join(BASE_DIR, safe_filename)

    # Проверяем, что путь внутри BASE_DIR
    if os.path.commonprefix([os.path.realpath(file_path), BASE_DIR]) != BASE_DIR:
        abort(403)  # Запрещаем доступ к файлам за пределами каталога

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run()