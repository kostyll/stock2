from django.core.management.base import BaseCommand, CommandError
from main.models import OnlineUsers
from datetime import datetime
from django.db import connection


class Command(BaseCommand):
    args = ''
    help = 'check online users'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM main_onlineusers WHERE pub_date<NOW() - interval 20 minute")
