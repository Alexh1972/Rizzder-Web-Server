web: python3 manage.py makemigrations --noinput && python3 manage.py migrate --noinput && python3 manage.py collectstatic --noinput && gunicorn rizzder.wsgi:application && daphne -b 0.0.0.0 -p $PORT yourproject.asgi:application
