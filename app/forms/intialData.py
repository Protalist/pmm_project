from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class InitialData(FlaskForm):
    insuranceId = StringField('Insurance Id', validators=[DataRequired()])
    submit = SubmitField('Insert')