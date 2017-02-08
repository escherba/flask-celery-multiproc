import time
import argparse
from flask import Flask, jsonify
from celery import Celery, group

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://',
)


def parse_args(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', action='store_true',
                    help='run app in debug mode (allows breakpoints)')
    ap.add_argument('--host', type=str, default='localhost')
    ap.add_argument('--port', type=int, default=5000)
    namespace = ap.parse_args(args)
    return namespace


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


@celery.task(name="tasks.do_work", bind=True, soft_time_limit=20)
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


@app.route("/")
def index():
    return 'simple celery+flask example'


@app.route("/add_numbers")
def add_numbers():

    job = group([
        do_work.s(2, 2),
        do_work.s(4, 4),
        do_work.s(8, 8),
        do_work.s(16, 16),
        do_work.s(32, 32),
        do_work.s(64, 64),
        do_work.s(128, 128),
        do_work.s(256, 256)
    ])
    result = job.apply_async()
    j = result.join()
    return jsonify(j)


def serve(args):
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    args = parse_args()
    serve(args)