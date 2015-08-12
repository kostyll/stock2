from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from main.models import Msg
import time
from datetime import timedelta
from django.contrib.auth.models import User
import os
import sys


class Command(BaseCommand):
    args = ''
    help = 'delete users msgs '
    def handle(self, *args, **options):
    	  	process_command()

        


def process_command():
        Now = datetime.now()
	 
	l1 = Msg.objects.raw("SELECT * FROM main_msg WHERE user_from_id in (4,698,4722,3824,4350,4716) AND pub_date>=NOW()-interval 1 hour")
        for item in l1:
		print "delete message %s " % item
		item.user_hide_to = 'true'
		item.user_hide_from = 'true'
		item.save() 
