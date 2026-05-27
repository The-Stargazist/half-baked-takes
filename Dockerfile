FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN SECRET_KEY=buildtime-placeholder python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py loaddata data.json || true && gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 2 --timeout 60"]
