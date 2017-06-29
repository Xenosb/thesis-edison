from app import celery
from time import sleep

@celery.task
def t_add(x, y):
    print("Celery")
    return x + y