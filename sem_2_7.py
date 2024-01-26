"""Задание №7
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат."""

from flask import Flask, render_template, request, redirect, make_response
import os

app = Flask(__name__)
# главная страница
@app.route('/')

def number():
    return render_template('number.html')

# обработчик формы ввода числа
@app.route('/input_num', methods=['POST'])
def input_num():
    number = request.form['number']
    result = str(int(number) ** 2)
    resp = make_response(redirect('/result'))
    resp.set_cookie('number', number)
    resp.set_cookie('result', result)
    return resp



@app.route('/result')
def result():
    result = request.cookies.get('result')
    number = request.cookies.get('number')
    return render_template('result.html', result=result, number=number)


# обработчик возврата назад
@app.route('/back')
def back():
    # удаление cookie-файла и перенаправление на страницу ввода
    resp = make_response(redirect('/'))
    resp.delete_cookie('number')
    resp.delete_cookie('result')
    return resp


if __name__ == '__main__':
    app.run()