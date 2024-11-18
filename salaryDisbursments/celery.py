# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from django.conf import settings
#
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salaryDisbursments.settings')
#
# app = Celery('salaryDisbursments')  # Replace 'salaryDisbursments' with your project name.
#
# # Configure Celery using settings from Django settings.py.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load tasks from all registered Django app configs.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# # Celery configuration settings
# app.conf.update(
#     broker_url='redis://localhost:6379/0',  # This is the Redis broker URL
#     result_backend='redis://localhost:6379/0',  # For storing task results
#     accept_content=['json'],  # Accept only JSON data
#     task_serializer='json',  # Serialize task data in JSON format
#     result_serializer='json',  # Serialize results in JSON format
# )


import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salaryDisbursments.settings')
app = Celery('salaryDisbursments')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()