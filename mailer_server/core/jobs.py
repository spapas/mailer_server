# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.mail import send_mail as django_send_mail
from django.db import connections
from django_rq import job
from rq import get_current_job, Queue, Worker
from rq.connections import NoRedisConnectionException
import django_rq

from mailer_server.tasks.models import Task


@job
def send_email(user, subject, body, email_from, email_to, task):
    "A job to send email"
    try:
        job = get_current_job()
        job_id = job.get_id()
    except NoRedisConnectionException:
        job_id = '000'

    django_send_mail(subject, body, email_from, email_to)

    task.finished_on = datetime.datetime.now()
    task.result = "OK"
    task.save()


def can_do_async():
    redis_conn = django_rq.get_connection('default')
    queue = Queue(connection=redis_conn)
    workers = Worker.all(connection=redis_conn)
    return len(workers)>0

   

subject = u'Εκκρεμότητα απογραφής γενικού υλικού'
email_from = 'noreply@hcg.gr'

def send_test_email(user):
    email_to=['spapas@hcg.gr', 'spapas@gmail.com', ]
    body="TEST email from {0}".format(user)
    subject="TEST"
    if can_do_async():
        task = Task.objects.create(
            name='send_email_apografh_test',
            started_by=user
        )
        send_email.delay(user, subject, body, email_from, email_to, task)

    else:
        django_send_mail(subject, body, email_from, email_to)




def send_email(diakinhsh, user):
    
    if can_do_async():
        task = Task.objects.create(
            name='send_email_check',
            started_by=user
        )
        send_email.delay(user, subject, body, email_from, email_to, task)
    else:
        django_send_mail(subject, body, email_from, email_to)

