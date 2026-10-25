FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATABASE_URL=sqlite:////data/health_data.db

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Nicht als root laufen; /data hält die SQLite-Datei (als Volume mountbar).
RUN useradd --system --uid 10001 app \
    && mkdir /data \
    && chown app /data
USER app

VOLUME /data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')" || exit 1

# --preload: Tabellen werden einmal im Master angelegt, nicht von jedem Worker.
# --no-control-socket: gunicorn >= 25.1 legt sonst einen Socket in $HOME/.gunicorn an;
# der System-User hat kein beschreibbares Home (Errno 13) und der Socket wird im Container nicht gebraucht.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--preload", "--no-control-socket", "app:app"]
