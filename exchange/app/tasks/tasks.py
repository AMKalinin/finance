from app.tasks.celery import celery
from app.utils.utils import create_currency_pair, get_exchange_rate, write_rate


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s("hello"), name="add every 10")


@celery.task
def test(arg):
    print(arg)


@celery.task
def get_new_rate():
    create_currency_pair()
    get_exchange_rate()
    write_rate()
