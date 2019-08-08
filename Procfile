migrate: python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
web: gunicorn django_api.wsgi:application -b 0.0.0.0:5000