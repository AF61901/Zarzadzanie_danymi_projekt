import os
import csv
from quizy.modele import Pytanie, Odpowiedz
from quizy import db


def pobierz(plikcsv):
    dane = []
    if os.path.isfile(plikcsv):
        with open(plikcsv, newline='', encoding='utf-8') as plikcsv:
            tresc = csv.reader(plikcsv, delimiter='#')
            for rekord in tresc:
                dane.append(tuple(rekord))
    else:
        print("Plik z danymi", plikcsv, "nie istnieje!")

    return tuple(dane)


def dodaj(dane):
    for pytanie, odpowiedzi, odpopr in dane:
        p = Pytanie(pytanie=pytanie, odpopr=odpopr)
        db.session.add(p)
        db.session.commit()
        for o in odpowiedzi.split(","):
            odp = Odpowiedz(pnr=p.id, odpowiedz=o.strip())
            db.session.add(odp)
        db.session.commit()
    print("Dodano przykładowe dane")