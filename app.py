from flask import Flask, jsonify
from celery import group
app = Flask(__name__)


@app.route("/")
def index():
    return 'simple celery+flask example'


@app.route("/add_numbers")
def print_numbers_action():

    from tasks import add

    job = group([
        add.s(2, 2),
        add.s(4, 4),
        add.s(8, 8),
        add.s(16, 16),
        add.s(32, 32),
    ])
    result = job.apply_async()
    j = result.join()
    return jsonify(j)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
