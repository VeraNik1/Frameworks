"""Задание №9
Создать страницу, на которой будет форма для ввода имени
и электронной почты
При отправке которой будет создан cookie файл с данными
пользователя
Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка "Выйти"
При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты."""

from flask import Flask, render_template, request, redirect, make_response
import os

app = Flask(__name__)

# главная страница
@app.route('/')



def index():
    return render_template('start.html')

# обработчик формы ввода имени и email
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    # Создание cookie-файла и перенаправление на страницу приветствия
    resp = make_response(redirect('/greeting'))
    resp.set_cookie('name', name)
    resp.set_cookie('email', email)
    return resp


# страница приветствия
@app.route('/greeting')
def greeting():
    name = request.cookies.get('name')
    return render_template('greeting.html', name=name)


# обработчик выхода
@app.route('/logout')
def logout():

    # удаление cookie-файла и перенаправление на страницу ввода
    resp = make_response(redirect('/'))
    resp.delete_cookie('name')
    resp.delete_cookie('email')
    return resp


if __name__ == '__main__':
    app.run()