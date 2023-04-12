from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired


class RegisterForm(FlaskForm):
    email = EmailField('*Почта', validators=[DataRequired()])
    password = PasswordField('*Пароль', validators=[DataRequired()])
    password_again = PasswordField('*Повторите пароль', validators=[DataRequired()])
    name = StringField('*Имя пользователя', validators=[DataRequired()])
    surname = StringField('*Фамилия пользователя', validators=[DataRequired()])
    city = StringField('Город')
    country = StringField('Страна')
    telephon_number = StringField('Телефон')
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Продолжить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditPassword(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    total_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    submit = SubmitField('Продолжить')


class EditProfile(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    city = StringField('Город')
    country = StringField('Страна')
    telephon_number = StringField('Телефон')
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Продолжить')


class AddAvatar(FlaskForm):
    avatar = FileField('Аватарка', validators=[FileRequired()])
    submit = SubmitField('Обновить')