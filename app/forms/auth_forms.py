from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.models import User


class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Тык')


class AdminLoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Тык')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired(),
                                                              EqualTo('password')])
    submit = SubmitField('Сбросить пароль')

# class RegistrationForm(FlaskForm):
#     username = StringField('Никнейм', validators=[DataRequired()])
#     email = StringField('Почта', validators=[DataRequired(), Email()])
#     password = PasswordField('Пароль', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Повторить пароль', validators=[DataRequired(),
#                                         EqualTo('password')])
#     submit = SubmitField('Зарегистрироваться')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Пожалуйста, придумай другое имя.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Пожалуйста, используйте другую почту.')
