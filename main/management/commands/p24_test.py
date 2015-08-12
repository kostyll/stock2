from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from sdk.p24 import p24


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
        D = p24()
        D.balance()
                                

       