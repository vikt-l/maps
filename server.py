from flask import Flask, render_template, request, redirect
from getMap import get_info, get_address, get_obj
from forms.default import DefaultForm
from forms.user import RegisterForm, LoginForm
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

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
    if request.method == 'POST':
        if form.delta.data:
            delta = form.delta.data
        else:
            delta = 0.2
            form.delta.data = 0.2
        img = 'static/img/default_img.png'
        if form.address.data:
            address = form.address.data
            img = get_address(address, delta)
        elif form.longitude.data and form.lattitude.data:
            toponym_longitude = form.longitude.data
            toponym_lattitude = form.lattitude.data
            if form.object.data:
                object = form.object.data
                img = get_obj(toponym_longitude, toponym_lattitude, object, delta)
            else:
                img = get_info(toponym_longitude, toponym_lattitude, delta)
        return render_template('map_edit.html', form=form, img=img)
    return render_template('map_edit.html', form=form, img='static/img/default_img.png')


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
            about=form.about.data
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
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == "__main__":
    main()