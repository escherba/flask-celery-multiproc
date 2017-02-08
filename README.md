Celery+Flask multiprocessing demo
=================================

Demonstrates use of Celery workers to speed up long-running web requests

Setup
-----

Let's say a web request needs to run a long-running task on some data but the task
is easily parallelizable on the data. We define the task in a module away from the main app
(let's call it `tasks.py`):

```python
@celery.task(bind=True, soft_time_limit=20)
def do_work(self, x, y):
    """
    Performs a CPU-intensive task for exactly 5 seconds,
    with 20-second timeout
    """
    start = time.clock()
    while True:
        c = 0
        for i in range(1000000):
            c += i * i
        cur = time.clock()
        if cur - start >= 5.0:
            break
    return x + y
```

In the app module we then split the data and spawn the needed number of tasks (this should typically be no larger than 
the number of CPU cores):

```python
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
        do_work.s(128, 128),
        do_work.s(256, 256)
    ])
    result = job.apply_async()
    j = result.join()
    return jsonify(j)
```

Usage
-----

Create virtualenv

    $ virtualenv env --system-site-packages
    $ . env/bin/activate
    $ pip install -r requirements.txt

Make sure you have RabbitMQ running (on Mac you may have to first run `brew install rabbitmq` and `brew services start rabbitmq`) and start Celery:

    $ celery -A demo.tasks.celery worker -l info

In a separate terminal, start Flask app:

    $ python -m demo.app

Finally, make some requests:

    $ time curl http://localhost:5000/add_numbers
    [ 4, 8, 16, 32, 64, 128, 256, 512 ]

    real	0m5.573s
    user	0m0.007s
    sys	0m0.009s
    
As you can see from these numbers (on a i7 4-core laptop), the parallelism overhead here is quite low.
