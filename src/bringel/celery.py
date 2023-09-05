from os import environ

from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'bringel.settings')
app = Celery('bringel')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
