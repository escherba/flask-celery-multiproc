import time
import celery


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
