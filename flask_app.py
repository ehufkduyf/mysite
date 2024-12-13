from flask import Flask, render_template, request, redirect, url_for, flash
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Задайте URI для вашей БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())  # Временная метка
# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')



# Маршрут для обработки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    email = request.form['textInput']
    email = email.strip().lower()
    # Создаем новую запись
    new_user = User(email=email,)
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None: 
        valid = False
    # Добавляем запись в базу данных
    if valid:
        db.session.add(new_user)
        db.session.commit()
    
    # Перенаправляем на главную страницу или другую страницу
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
