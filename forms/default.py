from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FileField, FloatField
# from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired
from markupsafe import Markup


class DefaultForm(FlaskForm):
    longitude = FloatField('longitude')
    lattitude = FloatField('lattitude')
    delta = FloatField('delta')
    object = StringField('object')
    address = StringField('address')