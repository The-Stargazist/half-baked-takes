FROM python:3.12-slim

# System deps for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files at build time (no DB needed)
RUN SECRET_KEY=buildtime-placeholder python manage.py collectstatic --noinput

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
