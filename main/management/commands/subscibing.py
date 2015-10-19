from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import UserCustomSettings, CustomMailMulti
from django.core.mail import EmailMultiAlternatives
import time
from django.utils.html import strip_tags
from main.subscribing import subscribe_connection

from django.db import connection


class Command(BaseCommand):
    args = ''
    help = 'reset pins for all users'

    def handle(self, *args, **options):
        Connection = subscribe_connection()
        for email in CustomMailMulti.objects.filter(status="created"):
            text_content = strip_tags(email.Text)
            for item in UserCustomSettings.objects.filter(setting__title="news_notify"):
                if item.value == "yes" and item.user.email != '':
                    print "send message to %s email %s" % (item.user.username, item.user.email)
                    msg = EmailMultiAlternatives(email.Subject, text_content, email.From, [item.user.email],
                                                 connection=Connection)
                    msg.attach_alternative(email.Text, "text/html")
                    msg.send()
                    time.sleep(1)
            email.status = "processed"
            email.save()
