from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restful.settings')

app = Celery('restful')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    # 'add-every-one-minute': {
    #     'task': 'tempsensor.tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16),
    # },
    #
    'multi-every-30s': {
        'task': 'tempsensor.tasks.simulate_gastemp',
        'schedule': 30.0,
        'args': (),
    }
}


@app.task(bind=True)
def debug_task(self):
    print ('Request: {0!r}'.format(self.request))
