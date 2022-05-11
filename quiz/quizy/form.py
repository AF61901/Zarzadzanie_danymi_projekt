from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FieldList, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from quizy.modele import Uzytkownik

class Rejestracja(FlaskForm):
    username = StringField('Nazwa',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email(message='Nieprawidłowy email')])
    password = PasswordField('Hasło',
        validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = Uzytkownik.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nazwa jest już zajęta.')

    def validate_email(self, email):
        user = Uzytkownik.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email jest już zajety.')




class Login(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
        validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')




class Dodaj(FlaskForm):
    pytanie = StringField('Treść pytania:',
                          validators=[DataRequired()])
    odpowiedzi = FieldList(StringField(
                           'Odpowiedź',
                           validators=[DataRequired()]),
                           min_entries=3,
                           max_entries=3)
    odpopr = RadioField(
        'Poprawna odpowiedź',
        validators=[DataRequired()],
        choices=[('0', 'o0'), ('1', 'o1'), ('2', 'o2')]
    )

    pid = HiddenField("Pytanie id")
  