"""Füllt die Datenbank mit 90 Tagen Testdaten.

Nutzung:
    python seed.py            # nur wenn die Tabelle leer ist
    python seed.py --reset    # löscht alle Daten (nur mit SQLite erlaubt)
"""
import argparse
import random
import sys
from datetime import date, timedelta

from app import HealthData, app, db


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reset", action="store_true", help="vorhandene Daten löschen (nur SQLite)")
    args = parser.parse_args()

    with app.app_context():
        if args.reset:
            if db.engine.dialect.name != "sqlite":
                sys.exit("--reset ist nur mit SQLite erlaubt, um versehentliches Löschen echter Daten zu verhindern.")
            db.drop_all()
            db.create_all()

        if db.session.scalar(db.select(db.func.count(HealthData.id))):
            sys.exit("Die Datenbank enthält bereits Daten. Nutze --reset (nur SQLite), um neu zu befüllen.")

        start = date.today() - timedelta(days=89)
        for i in range(90):
            db.session.add(
                HealthData(
                    date=start + timedelta(days=i),
                    exercise=random.randint(0, 120),    # Minuten
                    meditation=random.randint(0, 60),   # Minuten
                    sleep=random.randint(4, 10),        # Stunden
                )
            )
        db.session.commit()
        print("Datenbank mit 90 Testeinträgen befüllt.")


if __name__ == "__main__":
    main()
