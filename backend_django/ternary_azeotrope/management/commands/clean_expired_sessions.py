from datetime import datetime

from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes expired sessions from the database"

    def handle(self, *args, **options):
        now = datetime.now()
        expired_sessions = Session.objects.filter(expire_date__lt=now)
        nb = len(expired_sessions)
        expired_sessions.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {nb} expired sessions"))
