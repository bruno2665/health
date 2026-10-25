# Health Tracker

Kleine Flask-App zum Erfassen von Bewegung, Meditation und Schlaf, mit Dashboard (Chart.js).

Basiert auf den Übungsdateien des LinkedIn-Learning-Kurses *Flask Essential Training*
(Natasha Ferguson), modernisiert auf aktuelle Versionen und für Docker aufbereitet.
Es gilt die Lizenz der ursprünglichen Übungsdateien (LinkedIn Learning Exercise Files License).

## Stack

Python 3.13, Flask 3.1, Flask-SQLAlchemy 3.1, SQLAlchemy 2.0, Flask-WTF 1.3, gunicorn.
Bootstrap 5.3.3 und Chart.js 4.4.7 liegen lokal in `static/vendor/`.

## Mit Docker starten

```bash
docker build -t health-tracker .
docker run -p 8000:8000 \
  -e SECRET_KEY=$(openssl rand -hex 32) \
  -v health-data:/data \
  health-tracker
```

Dann `http://localhost:8000` öffnen. Testdaten:

```bash
docker exec <container> python seed.py
```

## Ohne Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY=dev FLASK_DEBUG=1
python app.py
```

## Konfiguration

| Variable | Bedeutung |
|---|---|
| `SECRET_KEY` | Pflicht. Ohne sie startet die App nicht (außer mit `FLASK_DEBUG=1`). |
| `DATABASE_URL` / `POSTGRES_URL` | Datenbank-URL. Standard: SQLite (im Container unter `/data`). `postgres://` wird zu `postgresql://` umgeschrieben. |
| `FLASK_DEBUG` | `1` nur für lokale Entwicklung. |

`seed.py --reset` löscht Daten und ist nur mit SQLite erlaubt.
