import os
from celery import Celery

if not os.environ.get("IS_PROD"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.production")
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
