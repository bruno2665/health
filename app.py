import os

from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from forms import HealthDataForm


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def _database_uri():
    uri = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("POSTGRES_URL")
        or "sqlite:///health_data.db"
    )
    # SQLAlchemy 2.x akzeptiert "postgres://" nicht mehr, viele Hoster liefern es aber noch.
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri


def _secret_key():
    key = os.environ.get("SECRET_KEY")
    if key:
        return key
    if os.environ.get("FLASK_DEBUG") == "1":
        return "dev-only-insecure-key"
    raise RuntimeError(
        "SECRET_KEY ist nicht gesetzt. Setze die Umgebungsvariable SECRET_KEY "
        "(oder FLASK_DEBUG=1 nur für die lokale Entwicklung)."
    )


app = Flask(__name__)
app.config["SECRET_KEY"] = _secret_key()
app.config["SQLALCHEMY_DATABASE_URI"] = _database_uri()

db.init_app(app)


class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    meditation = db.Column(db.Integer, nullable=False)
    sleep = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<HealthData {self.id}>"


# Ersetzt das entfernte @app.before_first_request. Läuft einmal beim Import
# (bei gunicorn mit --preload nur im Master-Prozess, also ohne Race Condition).
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return "ok"


@app.route("/form", methods=["GET", "POST"])
def form():
    form = HealthDataForm()
    if form.validate_on_submit():
        new_data = HealthData(
            date=form.date.data,
            exercise=form.exercise.data,
            meditation=form.meditation.data,
            sleep=form.sleep.data,
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("form.html", form=form)


@app.route("/dashboard")
def dashboard():
    all_data = db.session.scalars(db.select(HealthData).order_by(HealthData.date)).all()

    return render_template(
        "dashboard.html",
        dates=[d.date.strftime("%Y-%m-%d") for d in all_data],
        exercise_data=[d.exercise for d in all_data],
        meditation_data=[d.meditation for d in all_data],
        sleep_data=[d.sleep for d in all_data],
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
