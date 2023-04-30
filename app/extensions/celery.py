from celery import Celery


celery_app = Celery()

def init_app(app):
    celery_app.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery_app.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    app.celery_app = celery_app
    return celery_app
