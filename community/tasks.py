from __future__ import absolute_import, unicode_literals
import celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community.settings')

# config celery settings
app = celery.Celery('community')

app.config_from_object('django.conf:settings', namespace='CELERY')

# autodiscover tasks in installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))