from celery import shared_task
from time import sleep
@shared_task()
def first_task(message):
    # print('hello')
    sleep(25)
    print(message)

