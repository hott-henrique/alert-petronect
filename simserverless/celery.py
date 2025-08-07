from celery import Celery

app = Celery("simserverless", broker="redis://redis-db:6379/0")

app.config_from_object("simserverless")

app.autodiscover_tasks([ "simserverless" ])
