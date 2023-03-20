from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class JobsForm(FlaskForm):
    team_leader = StringField('ID of captain', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField("Collaborators' id", validators=[DataRequired()])
    is_finished = BooleanField('Is finished?', validators=[DataRequired()])
    department = StringField('Hazard category', validators=[DataRequired()])
    submit = SubmitField('Add work')


class JobsRedactionForm(FlaskForm):
    team_leader = StringField('ID of captain', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField("Collaborators' id", validators=[DataRequired()])
    is_finished = BooleanField('Is finished?', validators=[DataRequired()])
    department = StringField('Hazard category', validators=[DataRequired()])
    submit = SubmitField('Redact job')


class DepartmentsForm(FlaskForm):
    title = StringField('Title of Department', validators=[DataRequired()])
    members = StringField("Members' id", validators=[DataRequired()])
    email = EmailField('Department email', validators=[DataRequired()])
    submit = SubmitField('Add a Department')


class DepartmentsRedactionForm(FlaskForm):
    title = StringField('Title of Department', validators=[DataRequired()])
    chief = StringField('Chief', validators=[DataRequired()])
    members = StringField("Members' id", validators=[DataRequired()])
    email = EmailField('Department email', validators=[DataRequired()])
    submit = SubmitField('Redact a Department')


