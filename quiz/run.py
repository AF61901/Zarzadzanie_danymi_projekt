from quizy import app, db
from quizy.pytiodp import *
import os


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        db.create_all() 
        dodaj(pobierz('quizy/pytania.csv'))
    app.run(debug=True)