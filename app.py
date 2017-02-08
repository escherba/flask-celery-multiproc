from flask import Flask, jsonify
from celery import group
app = Flask(__name__)


@app.route("/")
def index():
    return 'simple celery+flask example'


@app.route("/add_numbers")
def add_numbers():

    from tasks import do_work

    job = group([
        do_work.s(2, 2),
        do_work.s(4, 4),
        do_work.s(8, 8),
        do_work.s(16, 16),
        do_work.s(32, 32),
        do_work.s(64, 64),
        do_work.s(128, 128)
    ])
    result = job.apply_async()
    j = result.join()
    return jsonify(j)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
