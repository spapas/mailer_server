# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail as django_send_mail
from django.core.mail import send_mass_mail as django_send_mass_mail
from django.db import connections, transaction
from django_rq import job
from django.utils import timezone
from rq import get_current_job, Queue, Worker
from rq.connections import NoRedisConnectionException
import django_rq

from mailer_server.tasks.models import Task
from mailer_server.mail.models import Mail

import logging
logger = logging.getLogger(__name__)



@job
def send_email_async(email_object, task_id, ):
    "A job to send email"

    logger.info('Sending a new mail async!')

    job = get_current_job()
    job_id = job.get_id()

    email_object.send()

    task = Task.objects.get(id=task_id)
    task.job_id = job_id
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
    logger.error('Something went wrong!')
    logger.info('Something went right!')
    email_to = settings.ADMINS
    body = "TEST email from {0}".format(user)
    subject = "TEST EMAIL"
    if can_do_async():
        logger.info('Async test mail send!')
        task = Task.objects.create(
            name='send_test_mail',
            started_by=user,
            result='NOT STARTED',
        )
        email_object = EmailMessage(
            subject=subject,
            body=body,
            from_email=email_from,
            to=email_to,
        )
        #send_email_async.delay(email_object, task.id)
        transaction.on_commit(lambda: send_email_async.delay(email_object, task.id, ))

    else:
        logger.info('Will send the mail synchronously!')
        django_send_mail(subject, body, email_from, email_to)


def send_mail(mail):
    if can_do_async():
        logger.info('Async mail send!')
        task = Task.objects.create(
            name='send_mail',
            started_by=mail.created_by,
            result='NOT STARTED',
        )
        transaction.on_commit(lambda: send_email_async.delay(mail.get_email_object(), task.id, ))
    else:
        logger.info('Will send the mail synchronously!')
        mail_to = mail.mail_to.split(',')
        django_send_mail(mail.subject, mail.body, mail.mail_from, mail_to)


@job
def send_mass_mail_async(mm_serializer, user):
    task = Task.objects.create(
        name='send_mass_mail',
        started_by=user,
        result='NOT STARTED',
    )

    logger.info('Sending mass mails!')
    mass_mail = mm_serializer.save(created_by=user)
    mail_list = mass_mail.get_mails()
    email_list = mass_mail.get_emails()

    Mail.objects.bulk_create(mail_list)
    connection = get_connection()
    connection.send_messages(email_list)
    #django_send_mass_mail(tuple(email_tuple_list))


def send_mass_mail(mass_mail, user):
    if can_do_async():
        logger.info('Will send the mass mails!')
        transaction.on_commit(lambda: send_mass_mail_async.delay(mass_mail, user))

        return True
    else:
        logger.error('Cannot do async, will not send mails!')
        return False
