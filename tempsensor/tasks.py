from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x+y


@shared_task
def mul(x, y):
    return x*y


@shared_task
def interval_task():
    print 'interval task execute'


@shared_task
def crontab_task():
    print 'crontab task execute'