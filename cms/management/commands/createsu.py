from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="tsubuanko").exists():
            User.objects.create_superuser(username="tsubuanko", email="eitaro.612@icloud.com", password="e19980612")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))