from quizy import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Uzytkownik.query.get(int(user_id))


class Uzytkownik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    twpyt = db.relationship('Pytanie', backref='autor', lazy=True)
    rnkd = db.relationship('Ranking', backref=db.backref('pozycja'), lazy=True)
    def __str__(self):
        return self.username


class Pytanie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pytanie = db.Column(db.Unicode(255), unique=True)
    odpopr = db.Column(db.Unicode(100))
    odpowiedzi = db.relationship(
        'Odpowiedz', backref=db.backref('pytanie'),
        cascade="all, delete, delete-orphan")
    userid = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'))

    def __str__(self):
        return self.pytanie


class Odpowiedz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.Integer, db.ForeignKey('pytanie.id'))
    odpowiedz = db.Column(db.Unicode(100))

    def __str__(self):
        return self.odpowiedz


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pkt = db.Column(db.Integer)
    usr = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'))

    def __str__(self):
        return self.pkt


