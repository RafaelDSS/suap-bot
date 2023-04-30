web: flask run
celery: celery -A wsgi.celery worker --concurrency=1
celery-beat: celery -A wsgi.celery beat -l
celery-flower: 'celery -A wsgi.celery flower'
