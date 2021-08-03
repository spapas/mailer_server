from django.core.management.base import BaseCommand, CommandError
from mailer_server.mail.models import Mail
import datetime

class Command(BaseCommand):
    help = 'Removes old mails from database'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help='Remove mails older than N days')

    def handle(self, *args, **options):
        
        date = datetime.date.today() - datetime.timedelta(days=options['days'])
        mails = Mail.objects.filter(created_on__lte=date)
        
        print("Will delete mails older than", date, "i.e", len(mails), "mails.")
        mails.delete()