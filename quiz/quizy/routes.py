from flask import render_template, url_for, flash, redirect, request
from quizy import app, db, bcrypt
from quizy.form import *
from quizy.modele import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql.expression import func


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
            user = Uzytkownik.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                nast = request.args.get('next')
                return redirect(nast) if nast else redirect(url_for('index'))
            else:
                flash('Login niepoprawny. Sprawdź email i hasło', 'danger')
    return render_template('login.html', title='Zaloguj się', form=form)

@app.route('/rejestruj', methods=['GET', 'POST'])
def rejestruj():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Rejestracja()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Uzytkownik(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto {form.username.data} zostało utworzone', 'success')
        return redirect(url_for('index'))
    return render_template('rejestruj.html', title='Zarejestruj się', form=form)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    pytania = Pytanie.query.join(Odpowiedz).order_by(func.random()).limit(12).offset(0)
    if not pytania:
        flash('Brak pytań w bazie.', 'danger')
        return redirect(url_for('index'))


    if request.method == 'POST':
        punkty = 0
        poprawne = 0
        zle = 0
        total = 0
        for pid, odp in request.form.items():
            total += 1
            odpopr = db.session.query(Pytanie.odpopr).filter(
                Pytanie.id == int(pid)).scalar()
            if odp == odpopr:
                punkty += 10

                poprawne += 1
            else:
                zle += 1
            percent = poprawne/(total) *100
           
            
        return redirect(url_for('rezult', punkty=punkty, poprawne=poprawne, zle=zle, percent=percent))

    return render_template('quiz.html', title='Quiz', pytania=pytania)


@app.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    form = Dodaj()
    if form.validate_on_submit():
        odp = form.odpowiedzi.data
        p = Pytanie(pytanie=form.pytanie.data, odpopr=odp[int(form.odpopr.data)], userid=current_user.id)
        db.session.add(p)
        db.session.commit()
        for o in odp:
            inst = Odpowiedz(pnr=p.id, odpowiedz=o)
            db.session.add(inst)
        db.session.commit()
        flash("Dodano pytanie: {}".format(form.pytanie.data), 'info')
        return redirect(url_for("twoje"))

    return render_template('dodaj.html', title='Dodaj pytanie', form=form, radio=list(form.odpopr))

@app.route('/twoje')
@login_required
def twoje():
    pytania = Pytanie.query.join(Uzytkownik).all()
    if not pytania:
        flash('Brak pytań w bazie.', 'danger')
        return redirect(url_for('index'))

    return render_template('twoje.html', title='Twoje pytania', pytania=pytania)


@app.route('/wyloguj')
def wyloguj():
    logout_user()
    return redirect(url_for('index'))


@app.route('/usun/<int:pid>', methods=['GET', 'POST'])
def usun(pid):
    p = Pytanie.query.get(pid)
    if request.method == 'POST':
        flash('Usunięto pytanie {0}'.format(p.pytanie), 'info')
        db.session.delete(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("usun.html", pytanie=p)

@app.route('/rezult', methods = ["POST", "GET"])
def rezult():
    punkty = request.args.get('punkty')
    poprawne = request.args.get('poprawne')
    zle = request.args.get('zle')
    percent = request.args.get('percent')
    
    if request.method == 'POST':
        r = Ranking(pkt=punkty, usr=current_user.id)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('ranking'))
    return render_template("rezult.html", punkty=punkty, poprawne=poprawne, zle=zle, percent=percent)

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():

    ranking = Ranking.query.join(Uzytkownik).order_by(Ranking.pkt.desc()).all()
    if not ranking:
        flash('Brak obecnie pozycji w rankingu.', 'danger')
        return redirect(url_for('index'))
    return render_template("ranking.html", ranking=ranking)