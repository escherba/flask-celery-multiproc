import time
from celery import Celery
from app import app


app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://',
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


@celery.task(bind=True, soft_time_limit=20)
def do_work(self, x, y):
    # do something CPU-intensive
    start = time.clock()
    while True:
        c = 0
        for i in range(1000000):
            c += i * i
        cur = time.clock()
        if cur - start >= 5.0:
            break
    return x + y
