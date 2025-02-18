import os

from celery import Celery

# Укажите путь к настройкам Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("habit_tracker", broker="redis://localhost:6379/0")

# Настройки Celery берутся из настроек Django, начиная с префикса CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживать задачи в установленных приложениях
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
