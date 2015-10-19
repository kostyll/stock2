from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from sdk.p24 import p24
from decimal import Decimal
from crypton import settings
import sys


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'

    def handle(self, *args, **options):
        # reload(sys)
        #	sys.setdefaultencoding('utf-8')
        D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)

# D.pay2p(200,"6762462680255004" , Decimal("10394.01"))
<< << << < HEAD
D.pay2p(224, "5167982300501472", Decimal("360"))
#	D.pay2p(214,"4149497816294591" , Decimal("226.75"))
#	D.pay2p(218,"5168755617294299" , Decimal("69.30"))

#rint D.balance()
== == == =
#	D.pay2p(224,"5167982300501472" , Decimal("360"))
#	D.pay2p(214,"4149497816294591" , Decimal("226.75"))
#	D.pay2p(218,"5168755617294299" , Decimal("69.30"))

print D.balance()
>> >> >> > 137e852
afcc19395c1c41f4212fde52f31cbc0a7
                                

       
