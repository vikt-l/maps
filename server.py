from flask import Flask, render_template, request, redirect
from getMap import get_info, get_address, get_obj
from forms.default import DefaultForm
from forms.user import RegisterForm, LoginForm, EditPassword, EditProfile, AddAvatar
from data import db_session
from data.users import User
from data.news import News
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/maps.db")
    app.run()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map_edit', methods=['GET', 'POST'])
def map_edit():
    form = DefaultForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if request.method == 'POST':
        if form.delta.data:
            delta = form.delta.data
        else:
            delta = 0.2
            form.delta.data = 0.2
        img = 'static/img/default_img.png'
        if form.address.data:
            address = form.address.data
            img, form.longitude.data, form.lattitude.data = get_address(address, delta)
        if form.longitude.data and form.lattitude.data:
            toponym_longitude = form.longitude.data
            toponym_lattitude = form.lattitude.data
            if form.object.data:
                object = form.object.data
                img, form.longitude.data, form.lattitude.data = get_obj(toponym_longitude, toponym_lattitude, object, delta)
            elif not form.address.data:
                img = get_info(toponym_longitude, toponym_lattitude, delta)
        return render_template('map_edit.html', form=form, img=img, user=user)
    return render_template('map_edit.html', form=form, img='static/img/default_img.png', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            city=form.city.data,
            country=form.country.data,
            telephon_number=form.telephon_number.data,
            email=form.email.data,
            about='',
            avatar='test.jpg'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/map_edit")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile_user/<int:id_user>', methods=['GET', 'POST'])
def profile_user(id_user):
    if current_user.id == id_user:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        news = db_sess.query(News).filter(News.user == current_user)
        form = AddAvatar()
        if form.validate_on_submit():

            f = form.avatar.data
            form.avatar.file.save(os.path.join(app.config['static/avatars'], f'{id_user}.png'))
            user.avatar = f'{id_user}.png'
            db_sess.commit()
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            news = db_sess.query(News).filter(News.user == current_user)
            return render_template('profile_user.html', title='Профиль', user=user, news=news, form=form)
        return render_template('profile_user.html', title='Профиль', user=user, news=news, form=form)


@app.route('/profile_edit/<int:id_user>', methods=['GET', 'POST'])
def profile_edit(id_user):
    if current_user.id == id_user:
        form = EditProfile()
        if request.method == "GET":
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == id_user).first()
            if user:
                form.name.data = user.name
                form.surname.data = user.surname
                form.about.data = user.about

                form.email.data = user.email
                form.telephon_number.data = user.telephon_number

                form.city.data = user.city
                form.country.data = user.country

        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == id_user).first()
            if user:
                user.name = form.name.data
                user.surname = form.surname.data
                user.about = form.about.data
                user.email = form.email.data
                user.telephon_number = form.telephon_number.data
                user.city = form.city.data
                user.country = form.country.data
                db_sess.commit()
                return redirect(f'/profile_user/{id_user}')
        return render_template('profile_edit.html', title='Изменение профиля', form=form)


@app.route('/password_edit/<int:id_user>', methods=['GET', 'POST'])
def password_edit(id_user):
    if current_user.id == id_user:
        form = EditPassword()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == id_user).first()
            if not user.check_password(form.total_password.data):
                return render_template('password_edit.html', title='Изменение пароля', form=form,
                                       message='Неверный страрый пароль')
            if not form.password.data == form.password_again.data:
                return render_template('password_edit.html', title='Изменение пароля', form=form,
                                       message='Не совпадают новые пароли')
            if user and user.check_password(form.total_password.data) and form.password.data == form.password_again.data:
                user.set_password(form.password.data)
                db_sess.commit()
                return redirect(f'/profile_user/{id_user}')
        return render_template('password_edit.html', title='Изменение пароля', form=form, message='')
if __name__ == "__main__":
    main()