# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail as django_send_mail
from django.core.mail import send_mass_mail as django_send_mass_mail
from django.db import connections
from django_rq import job
from django.utils import timezone
from rq import get_current_job, Queue, Worker
from rq.connections import NoRedisConnectionException
import django_rq

from mailer_server.tasks.models import Task
from mailer_server.mail.models import Mail


@job
def send_email_async(subject, body, email_from, email_to, task):
    "A job to send email"

    job = get_current_job()
    job_id = job.get_id()

    django_send_mail(subject, body, email_from, email_to)

    task.finished_on = timezone.now()
    task.result = "OK"
    task.save()


def can_do_async():
    redis_conn = django_rq.get_connection('default')
    queue = Queue(connection=redis_conn)
    workers = Worker.all(connection=redis_conn)
    return len(workers)>0


email_from = 'noreply@hcg.gr'

def send_test_mail(user):
    email_to = settings.ADMINS
    body = "TEST email from {0}".format(user)
    subject = "TEST EMAIL"
    if can_do_async():
        task = Task.objects.create(
            name='send_test_mail',
            started_by=user,
            result='NOT STARTED',
        )
        send_email_async.delay(subject, body, email_from, email_to, task)

    else:
        django_send_mail(subject, body, email_from, email_to)



def send_mail(mail):
    mail_to = mail.mail_to.split(',')
    if can_do_async():
        task = Task.objects.create(
            name='send_mail',
            started_by=mail.created_by
        )
        send_email_async.delay(mail.subject, mail.body, mail.mail_from, mail_to, task)
    else:
        django_send_mail(mail.subject, mail.body, mail.mail_from, mail_to)


@job
def send_mass_mail_async(mm_serializer, user):
    task = Task.objects.create(
        name='send_mass_mail',
        started_by=user
    )

    mass_mail = mm_serializer.save(created_by=user)
    email_list = mass_mail.get_mails()
    email_tuple_list = []
    for mail in email_list:
        email_tuple_list.append(mail.get_tuple())

    Mail.objects.bulk_create(email_list)
    django_send_mass_mail(tuple(email_tuple_list))



def send_mass_mail(mass_mail, user):
    if can_do_async():
        send_mass_mail_async.delay(mass_mail, user)

        return True
    else:
        return False

