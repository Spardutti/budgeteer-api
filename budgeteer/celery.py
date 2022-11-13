import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budgeteer.settings')

task_routes = [
    {'app.task.create_monthly_income_login': {'queue': 'income'}},
    {'app.task.create_weekly_category_login': {'queue': 'category'}}
]
app = Celery('budgeteer')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.conf.task_default_queue = "Main queue"
app.conf.task = task_routes
app.autodiscover_tasks()