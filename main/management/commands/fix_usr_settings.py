from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection

from main.models import CustomSettings, UserCustomSettings
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = ''
    help = 'fix user settings'

    def handle(self, *args, **options):

        List = list(User.objects.all())
        bulk_add = []
        for setting in CustomSettings.objects.all():

            for user in List:
                try:
                    Setting = UserCustomSettings.objects.get(
                        user=user,
                        setting=setting
                    )
                except UserCustomSettings.DoesNotExist:
                    bulk_add.append(
                        UserCustomSettings(user=user,
                                           value=setting.def_value,
                                           setting=setting
                        )
                    )

        UserCustomSettings.objects.bulk_create(bulk_add)