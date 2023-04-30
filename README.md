# suap-bot


Um Bot de Telegram feito em python que consome a api do SUAP.


## Como executar o projeto

```
flask run
```

Celery beat:

```
celery -A wsgi.celery beat
```

Celery worker:

```
celery -A wsgi.celery worker
```

Run Flower:

```
celery -A wsgi.celery flower
```
