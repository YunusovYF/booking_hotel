#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.tasks.celery_config:celery_app worker -l INFO
fi
if [[ "${1}" == "celery_beat" ]]; then
    celery --app=app.tasks.celery_config:celery_app worker -l INFO -B
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.celery_config:celery_app flower
fi