from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=[
        'app.tasks.tasks',
        'app.tasks.scheduler'
    ]
)

celery_app.conf.beat_schedule = {
    'periodic_task': {
        'task': 'periodic_task',
        'schedule': crontab(minute='30')
    }
}
