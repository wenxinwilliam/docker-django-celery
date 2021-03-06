from functools import wraps
from time import sleep

from mydjangoapp.celeryconf import app
from .models import Job
from .messagequeue import send_msg
from .redisconf import redis_conn


def update_job(fn):
    @wraps(fn)
    def wrapper(job_id, *args, **kwargs):
        job = Job.objects.get(id=job_id)
        job.status = 'started'
        job.save()
        try:
            result = fn(*args, **kwargs)
            job.result = result
            job.status = 'finished'
            job.save()
        except:
            job.result = None
            job.status = 'failed'
            job.save()

        token = redis_conn.get(job.user_id)
        if token:
            send_msg({'user_id': job.user_id, 'job_id': job.id, 'status': job.status})

    return wrapper


@app.task
@update_job
def power(n):
    """Return 2 to the n'th power"""
    return 2 ** n


@app.task
@update_job
def fib(n):
    """Return the n'th Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci numbers are only defined for n >= 0.")
    return _fib(n)


def _fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return _fib(n - 1) + _fib(n - 2)


@app.task
@update_job
def sleepwake(n):
    """sleeping for a number of seconds"""
    sleep(n)
    return n


@update_job
def syncsleepwake(n=1):
    """sleeping for a number of seconds"""
    sleep(n)
    return n


TASK_MAPPING = {
    'power': power,
    'fibonacci': fib,
    'sleepwake': sleepwake,
}