from celery.schedules import crontab

beat_schedule = {
    'check-for-biddings': {
        'task': 'check_for_biddings',
        'schedule': crontab(minute=0, hour='9,15,19'),
        'args': (dict(), dict())
    },
}

timezone = 'America/Sao_Paulo'
