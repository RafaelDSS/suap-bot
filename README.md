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


### Screenshots
[![image-2023-06-07-18-55-53.png](https://i.postimg.cc/wTxB4qnR/image-2023-06-07-18-55-53.png)](https://postimg.cc/V5T1d8fz)
