migrate: python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
web: newrelic-admin run-program gunicorn --reload --config gunicorn_config.py config.wsgi --log-level DEBUG --chdir /app -b 0.0.0.0:$GUNICORN_PORT