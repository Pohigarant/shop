import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop1.settings")

app = Celery("shop1")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
