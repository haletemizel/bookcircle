from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from sqlalchemy import select
from app import db
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Lütfen farklı bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = db.session.scalar(select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Lütfen farklı bir e-posta adresi kullanın.')

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-posta Adresi', validators=[DataRequired(), Email()])
    submit = SubmitField('Şifre Sıfırlama Bağlantısı Gönder')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Yeni Şifre', validators=[DataRequired()])
    password_confirm = PasswordField('Yeni Şifre (Tekrar)', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Şifreyi Sıfırla')
