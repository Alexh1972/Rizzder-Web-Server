web: python3 manage.py makemigrations --noinput && python3 manage.py migrate --noinput && python3 manage.py collectstatic --noinput && gunicorn rizzder.wsgi:application --bind 0.0.0.0:$PORT
websocket: daphne -b 0.0.0.0 -p 8001 rizzder.asgi:application
