import celery


@celery.task(name="tasks.do_work", bind=True, soft_time_limit=20)
def do_work(self, x, y):
    # do something CPU-intensive
    c = 0
    for i in range(10000000):
        c += i * i
    return x + y
