from celery import Celery
import logging.config
from django.conf import settings
from celery.signals import setup_logging
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learnit.settings")

app = Celery("learnit")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.config.dictConfig(settings.LOGGING)
