from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class compileForm(FlaskForm):
    insuranceId = StringField('Insurance Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    mail = StringField('Mail', validators=[DataRequired()])
    submit = SubmitField('Sign In')