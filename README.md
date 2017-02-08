Celery+Flask multiprocessing demo
=================================

Demonstrates use of Celery workers to speed up long-running web requests

Usage
-----

Create virtualenv

    $ virtualenv env --system-site-packages
    $ . env/bin/activate
    $ pip install -r requirements.txt

Make sure you have RabbitMQ running (on Mac it's `brew services start rabbitmq`) and start Celery:

    $ celery -A tasks.celery worker -l info

In a separate terminal, start Flask app:

    $ python app.py

Finally, make some requests:

    $ time curl http://localhost:5000/add_numbers
    [ 4, 8, 16, 32, 64 ]

    real	0m5.054s
    user	0m0.006s
    sys	0m0.010s
