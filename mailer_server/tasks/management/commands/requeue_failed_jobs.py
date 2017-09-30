from django.core.management.base import BaseCommand, CommandError
from django_rq.queues import get_failed_queue
import datetime

class Command(BaseCommand):
    help = 'Requeue all failed jobs'

    def add_arguments(self, parser):
        parser.add_argument('dry', help='Dry run')

    def handle(self, *args, **options):
        print options['dry']
        
        fq = get_failed_queue()
