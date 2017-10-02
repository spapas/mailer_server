from django.core.management.base import BaseCommand, CommandError
from django_rq.queues import get_failed_queue
import datetime

class Command(BaseCommand):
    help = 'Requeue all failed jobs'

    def add_arguments(self, parser):
        parser.add_argument('dry', nargs='?', help='Dry run')

    def handle(self, *args, **options):
        dry = options['dry']

        print "Starting requeue failed jobs at {0} with {1}".format(
            datetime.datetime.now(),
            "dry" if dry else "no dry"
        )

        fq = get_failed_queue()

        tot = 0
        for ji in fq.job_ids:
            tot += 1
            if not dry:
                print "Requeing {0}".format(ji)
                fq.requeue(ji)

        print "Finished requeue failed jobs at {0} - requeued {1} jobs (if not dry)".format(
            datetime.datetime.now(),
            tot
        )