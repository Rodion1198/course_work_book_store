import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "client_store.settings")

app = Celery("client_store")

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    # "periodical": {
    #     "task": "store.tasks.sync_book",
    #     "schedule": timedelta(seconds=15),
    # },
    # "send_order": {
    #     "task": "store.tasks.send_order",
    #     "schedule": timedelta(seconds=15),
    # },
}
