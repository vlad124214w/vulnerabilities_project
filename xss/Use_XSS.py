import psycopg2
from flask import request, render_template_string,Flask,render_template
import time
from flask import Flask, request, render_template_string
from markupsafe import escape


app = Flask(__name__)

# http://127.0.0.1:5000/xss?code=%3Cscript%3Ealert(%22%D0%92%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BB%D1%8E%D0%B1%D0%BE%D0%B3%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%B0%22)%3C/script%3E
@app.route("/xss")
def index():
	code = request.args.get('code')
	return render_template_string(f"<h1>Ваш ввод: </h1> <h2>  {code} </h2>")
#   <script> var code=123; alert(); eval(code) <script>; 



if __name__ == '__main__':
    app.run()


