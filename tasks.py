import time
from celery import Celery
from app import app


app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)


def make_celery(app):
    """after http://flask.pocoo.org/docs/0.12/patterns/celery/
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task(bind=True)
def add(self, x, y):
    # do something CPU-intensive
    time.sleep(5)
    return x + y
