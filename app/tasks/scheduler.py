from app.tasks.celery_config import celery_app


@celery_app.task(name='periodic_task')
def periodic_task():
    print('Hello, World!')
