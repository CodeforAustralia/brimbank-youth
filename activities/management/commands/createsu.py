from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="youshareadmin").exists():
            User.objects.create_superuser("youshareadmin", "BT@brimbank.vic.gov.au", "youshareadmin")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))