from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from hashlib import sha256

from reg_db import db, User
from reg_form import RegForm

app = Flask(__name__)
"""
Генерация секретного ключа
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SECRET_KEY'] = 'qwerty123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        user_exist = User.query.filter(User.username == username).first()
        email_exist = User.query.filter(User.email == email).first()
        if user_exist:
            flash('Пользователь с таким именем уже зарегистрирован!', 'danger')
        elif email_exist:
            flash('Пользователь с таким email уже зарегистрирован!', 'danger')
        else:
            new_user = User(username=username, email=email,
                            password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest())
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно зарегистрирован!', 'success')
        return redirect(url_for('registration'))
    else:
        for obj in form:
            for error in obj.errors:
                flash(error)
    return render_template('registration.html', form=form)


@app.cli.command('init-db')
def init_db():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
