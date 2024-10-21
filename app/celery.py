# app/celery.py

from celery import Celery

# Broker URL (Using Redis)
CELERY_BROKER_URL = "redis://localhost:6379/0"

app = Celery('app', broker=CELERY_BROKER_URL)

# Example Celery configuration
app.conf.update(
    result_expires=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
