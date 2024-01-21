"""Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал),
и дочерние шаблоны для страниц категорий товаров и отдельных товаров. Например, создать страницы «Одежда»,
 «Обувь» и «Куртка», используя базовый шаблон"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    context = {'title': 'Главная страница'}
    return render_template('index.html', **context)


@app.route('/clothes/')
def dress():
    context = {'title': 'Одежда'}
    return render_template('clothes.html', **context)


@app.route('/footwear/')
def shoes():
    context = {'title': 'Обувь'}
    return render_template('footwear.html', **context)


@app.route('/jacket/')
def jacket_page():
    context = {'title': 'Куртка'}
    return render_template('jacket.html', **context)


if __name__ == '__main__':
    app.run(debug=True)