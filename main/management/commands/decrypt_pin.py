from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import PinsImages
from django.db import connection
import time
import crypton.settings
from main.http_common import common_decrypt, get_crypto_object


class Command(BaseCommand):
    args = ''
    help = 'reset pins for all users'

    def handle(self, *args, **options):
        Id = 4394
        item = PinsImages.objects.using("security").get(user_id=Id)
        print item.iv_key
        (Obj, Iv) = get_crypto_object(crypton.settings.CRYPTO_KEY, item.iv_key)
        print common_decrypt(Obj, item.raw_value)

