release: python manage.py migrate --noinput
web: gunicorn IN16_Study_Manager.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120
