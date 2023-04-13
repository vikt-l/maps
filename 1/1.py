from flask import Flask, render_template, request, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm, LoginForm, EditPassword, EditProfile, AddAvatar
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/maps.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    login_user(user)
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    news = db_sess.query(News).filter(News.user == current_user)
    form = AddAvatar()
    return render_template('profile_user.html', user=user, news=news, form=form)


if __name__ == "__main__":
    main()